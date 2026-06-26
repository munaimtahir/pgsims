from __future__ import annotations

import csv
import io
import re
from datetime import date, datetime
from typing import Any, Iterable

import pandas as pd
from dateutil import parser as date_parser
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from openpyxl import Workbook
from openpyxl.styles import Font
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from rest_framework import permissions, serializers, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from sims.academics.models import Department
from sims.rotations.models import HospitalDepartment
from sims.training.models import ResidentTrainingRecord, TrainingProgram
from sims.users.data_quality import recompute_flags_for_user
from sims.users.models import DepartmentMembership, OnboardingImportBatch, ResidentProfile, SupervisorResidentLink, User

TEMP_PASSWORD = "pgfmu123"
LOGIN_URL = "https://pg.fmu.edu.pk"
RESIDENT_FIELDS = [
    ("resident_name", "Resident Name"),
    ("father_name", "Father Name"),
    ("department", "Department"),
    ("program_name", "Program"),
    ("training_year", "Training Year"),
    ("supervisor_name", "Supervisor Name"),
    ("mobile_number", "Mobile Number"),
    ("email", "Email"),
    ("cnic", "CNIC"),
    ("registration_number", "PMDC / PMC Number"),
    ("joining_date", "Joining Date"),
]
MAPPING_ALIASES = {
    "resident_name": ["name", "residentname", "traineename", "full name", "fullname"],
    "father_name": ["father", "fathername", "s/o", "son of", "guardian"],
    "department": ["department", "dept", "unit"],
    "program_name": ["program", "degree", "course", "training program"],
    "training_year": ["year", "training year", "year of training"],
    "supervisor_name": ["supervisor", "supervisor name"],
    "mobile_number": ["mobile", "phone", "contact", "cell"],
    "email": ["email", "email address"],
    "cnic": ["cnic", "nic"],
    "registration_number": ["pmdc", "pmc", "registration no", "registration number"],
    "joining_date": ["joining", "joining date", "date of joining"],
}
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
CNIC_RE = re.compile(r"^\d{5}-?\d{7}-?\d$")
USERNAME_RE = re.compile(r"^pgr(\d{3,})$")


class ResidentOnboardingUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class ResidentOnboardingMappingSerializer(serializers.Serializer):
    batch_id = serializers.IntegerField(min_value=1)
    mapping = serializers.DictField(child=serializers.CharField(allow_blank=True), required=True)


class ResidentOnboardingBatchSerializer(serializers.Serializer):
    batch_id = serializers.IntegerField(min_value=1)


class ResidentOnboardingIssueSerializer(serializers.Serializer):
    resident_ids = serializers.ListField(child=serializers.IntegerField(min_value=1), required=False)
    mark_all = serializers.BooleanField(default=False)


class ResidentEmptySerializer(serializers.Serializer):
    pass


class ResidentProfileCompleteSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=8)
    confirm_new_password = serializers.CharField(min_length=8)
    mobile_number = serializers.CharField()
    email = serializers.EmailField()
    cnic = serializers.CharField()
    program = serializers.CharField()
    training_year = serializers.CharField()
    joining_date = serializers.DateField(required=False, allow_null=True)


class ResidentEditSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False)
    mobile_number = serializers.CharField(required=False, allow_blank=True)
    cnic = serializers.CharField(required=False, allow_blank=True)
    program = serializers.CharField(required=False, allow_blank=True)
    training_year = serializers.CharField(required=False, allow_blank=True)
    joining_date = serializers.DateField(required=False, allow_null=True)
    department_id = serializers.IntegerField(required=False, allow_null=True)
    profile_completed = serializers.BooleanField(required=False)


def _manager_only(user) -> None:
    if not user or not user.is_authenticated or getattr(user, "role", None) not in {"admin", "utrmc_admin"}:
        raise PermissionDenied("Admin access required.")


def _resident_only(user) -> None:
    if not user or not user.is_authenticated or getattr(user, "role", None) not in {"resident", "pg"}:
        raise PermissionDenied("Resident access required.")


def _normalize(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value or "").strip().lower())


def _clean_text(value: Any) -> str:
    return str(value or "").strip()


def _parse_date(value: Any):
    if value in {None, "", "nan"}:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date_parser.parse(str(value), dayfirst=False).date()
    except Exception:
        return None


def _split_name(name: str) -> tuple[str, str]:
    parts = [part for part in _clean_text(name).split() if part]
    if not parts:
        return "", ""
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], " ".join(parts[1:])


def _read_rows(uploaded_file) -> tuple[list[str], list[dict[str, Any]]]:
    name = (uploaded_file.name or "").lower()
    if name.endswith(".csv"):
        uploaded_file.seek(0)
        content = uploaded_file.read().decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(content))
        headers = list(reader.fieldnames or [])
        rows = [dict(row) for row in reader]
        return headers, rows

    if name.endswith(".xlsx") or name.endswith(".xls"):
        uploaded_file.seek(0)
        engine = "openpyxl" if name.endswith(".xlsx") else "xlrd"
        frame = pd.read_excel(uploaded_file, dtype=str, engine=engine)
        frame = frame.fillna("")
        headers = [str(col).strip() for col in frame.columns.tolist()]
        rows = frame.to_dict(orient="records")
        return headers, rows

    raise ValidationError({"file": "Invalid file type. Use .xlsx, .xls, or .csv."})


def _auto_map(headers: Iterable[str]) -> dict[str, str]:
    normalized_headers = {_normalize(header): header for header in headers}
    mapping: dict[str, str] = {}
    for field, aliases in MAPPING_ALIASES.items():
        found = ""
        for alias in aliases:
            found = normalized_headers.get(_normalize(alias), "")
            if found:
                break
        if found:
            mapping[field] = found
    return mapping


def _resolve_department(value: Any) -> Department | None:
    text = _clean_text(value)
    if not text:
        return None
    return (
        Department.objects.filter(Q(name__iexact=text) | Q(code__iexact=text), active=True)
        .order_by("name")
        .first()
    )


def _resolve_home_hospital(department: Department | None):
    if not department:
        return None
    mapping = (
        HospitalDepartment.objects.select_related("hospital")
        .filter(department=department, is_active=True, hospital__is_active=True)
        .order_by("hospital__name")
        .first()
    )
    return mapping.hospital if mapping else None


def _resolve_program(value: Any) -> TrainingProgram | None:
    text = _clean_text(value)
    if not text:
        return None
    return (
        TrainingProgram.objects.filter(Q(name__iexact=text) | Q(code__iexact=text), active=True)
        .order_by("name")
        .first()
    )


def _resolve_supervisor(value: Any) -> User | None:
    text = _clean_text(value)
    if not text:
        return None
    normalized = _normalize(text)
    for user in User.objects.filter(role__in=["supervisor", "faculty"], is_active=True, is_archived=False):
        if normalized in {_normalize(user.username), _normalize(user.get_full_name()), _normalize(user.email)}:
            return user
    return None


def _row_payload(row: dict[str, Any], mapping: dict[str, str]) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    reverse_mapping = {field: source for field, source in mapping.items() if source}
    for field, source in reverse_mapping.items():
        payload[field] = _clean_text(row.get(source))
    return payload


def _existing_duplicate_reason(payload: dict[str, Any], department: Department | None) -> str | None:
    cnic = _clean_text(payload.get("cnic"))
    reg_no = _clean_text(payload.get("registration_number"))
    mobile = _clean_text(payload.get("mobile_number"))
    resident_name = _clean_text(payload.get("resident_name"))
    if cnic and User.objects.filter(cnic__iexact=cnic, role__in=["resident", "pg"], is_archived=False).exists():
        return "Same CNIC already exists"
    if reg_no and User.objects.filter(registration_number__iexact=reg_no, role__in=["resident", "pg"], is_archived=False).exists():
        return "Same PMDC / PMC number already exists"
    if mobile and User.objects.filter(phone_number__iexact=mobile, role__in=["resident", "pg"], is_archived=False).exists():
        return "Same mobile number already exists"
    if resident_name and department:
        normalized = _normalize(resident_name)
        for user in User.objects.filter(role__in=["resident", "pg"], is_archived=False).select_related("home_department"):
            if not user.home_department_id:
                continue
            if user.home_department_id != department.id:
                continue
            if _normalize(user.get_full_name() or user.username) == normalized:
                return "Same resident name and department already exists"
    return None


def _build_preview_rows(batch: OnboardingImportBatch, mapping: dict[str, str]) -> list[dict[str, Any]]:
    preview_rows: list[dict[str, Any]] = []
    seen_signatures: set[str] = set()
    ready = error = duplicate = 0
    for idx, row in enumerate(batch.raw_rows_json, start=2):
        payload = _row_payload(row, mapping)
        resident_name = _clean_text(payload.get("resident_name"))
        department_value = _clean_text(payload.get("department"))
        department = _resolve_department(department_value)
        program = _resolve_program(payload.get("program_name"))
        email = _clean_text(payload.get("email"))
        cnic = _clean_text(payload.get("cnic"))
        reg_no = _clean_text(payload.get("registration_number"))
        mobile = _clean_text(payload.get("mobile_number"))
        signature = "|".join(
            [
                _normalize(cnic or reg_no or mobile or ""),
                _normalize(resident_name),
                department.code if department else _normalize(department_value),
            ]
        )
        reason = None
        status_value = "Ready"
        if not resident_name or not department:
            status_value = "Error"
            reason = "Resident Name missing" if not resident_name else "Department not found"
        elif email and not EMAIL_RE.match(email):
            status_value = "Error"
            reason = "Invalid email format"
        elif cnic and not CNIC_RE.match(cnic.replace(" ", "")):
            status_value = "Error"
            reason = "Invalid CNIC format"
        elif payload.get("joining_date") and not _parse_date(payload.get("joining_date")):
            status_value = "Error"
            reason = "Invalid joining date"
        elif signature in seen_signatures:
            status_value = "Possible Duplicate"
            reason = "Duplicate row in uploaded file"
        else:
            duplicate_reason = _existing_duplicate_reason(payload, department)
            if duplicate_reason:
                status_value = "Possible Duplicate"
                reason = duplicate_reason
            else:
                seen_signatures.add(signature)
                ready += 1
        if status_value == "Error":
            error += 1
        elif status_value == "Possible Duplicate":
            duplicate += 1
        preview_rows.append(
            {
                "row_number": idx,
                "resident_name": resident_name,
                "father_name": _clean_text(payload.get("father_name")),
                "department": department.name if department else department_value,
                "program_name": payload.get("program_name", ""),
                "training_year": payload.get("training_year", ""),
                "supervisor_name": payload.get("supervisor_name", ""),
                "mobile_number": mobile,
                "email": email,
                "cnic": cnic,
                "registration_number": reg_no,
                "joining_date": _clean_text(payload.get("joining_date")),
                "status": status_value,
                "remarks": reason or "",
                "_payload": payload,
            }
        )
    batch.total_rows = len(preview_rows)
    batch.ready_rows = ready
    batch.error_rows = error
    batch.duplicate_rows = duplicate
    batch.preview_rows_json = preview_rows
    batch.error_rows_json = [
        {key: value for key, value in row.items() if key != "_payload"}
        for row in preview_rows
        if row["status"] != "Ready"
    ]
    batch.mapping_json = mapping
    batch.status = OnboardingImportBatch.STATUS_READY
    batch.save(
        update_fields=[
            "total_rows",
            "ready_rows",
            "error_rows",
            "duplicate_rows",
            "preview_rows_json",
            "error_rows_json",
            "mapping_json",
            "status",
        ]
    )
    return preview_rows


def _current_primary_department(user: User) -> Department | None:
    membership = (
        DepartmentMembership.objects.filter(user=user, active=True, is_primary=True)
        .select_related("department")
        .first()
    )
    if membership:
        return membership.department
    return user.home_department


def _training_year_level(value: str) -> str:
    normalized = _normalize(value)
    if normalized in {"1", "y1", "year1"}:
        return "y1"
    if normalized in {"2", "y2", "year2"}:
        return "y2"
    if normalized in {"3", "y3", "year3"}:
        return "y3"
    if normalized in {"4", "y4", "year4"}:
        return "y4"
    if normalized in {"5", "y5", "year5"}:
        return "y5"
    return ""


def _serialise_profile(profile: ResidentProfile) -> dict[str, Any]:
    user = profile.user
    department = _current_primary_department(user)
    return {
        "resident_id": user.id,
        "resident_name": user.get_full_name() or user.username,
        "department": department.name if department else "",
        "program": profile.program_name or "",
        "training_year": profile.training_year or user.year or "",
        "mobile_number": user.phone_number or "",
        "email": user.email or "",
        "cnic": user.cnic or "",
        "registration_number": user.registration_number or "",
        "username": user.username,
        "temporary_password": TEMP_PASSWORD if profile.login_generated else "",
        "login_url": LOGIN_URL,
        "login_generated": profile.login_generated,
        "login_issued": profile.login_issued,
        "login_issued_at": profile.login_issued_at,
        "login_issued_by": profile.login_issued_by.get_full_name() if profile.login_issued_by else "",
        "profile_completed": profile.profile_completed,
        "force_password_change": user.force_password_change,
        "last_login": user.last_login,
        "row_status": "Profile Complete" if profile.profile_completed else "Profile Incomplete",
    }


def _login_queryset(batch_id: int | None = None):
    qs = ResidentProfile.objects.select_related("user", "login_issued_by").order_by("user__last_name", "user__first_name")
    if batch_id:
        qs = qs.filter(import_batch_id=batch_id)
    return qs


def _apply_login_generation(profiles: Iterable[ResidentProfile]):
    generated = []
    with transaction.atomic():
        existing = list(
            User.objects.select_for_update()
            .filter(username__startswith="pgr")
            .values_list("username", flat=True)
        )
        current_max = 0
        for username in existing:
            match = USERNAME_RE.match(username or "")
            if match:
                current_max = max(current_max, int(match.group(1)))
        next_number = current_max + 1
        for profile in profiles:
            user = profile.user
            if profile.login_generated and USERNAME_RE.match(user.username or ""):
                continue
            username = f"pgr{next_number:03d}"
            while User.objects.filter(username=username).exists():
                next_number += 1
                username = f"pgr{next_number:03d}"
            user.username = username
            user.set_password(TEMP_PASSWORD)
            user.force_password_change = True
            user.save(update_fields=["username", "password", "force_password_change"])
            profile.login_generated = True
            profile.save(update_fields=["login_generated"])
            generated.append(profile)
            next_number += 1
    return generated


def _sheet_response(rows: list[dict[str, Any]], filename: str, format_: str = "xlsx") -> HttpResponse:
    if format_ == "csv":
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=list(rows[0].keys()) if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(rows)
        response = HttpResponse(buffer.getvalue(), content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{filename}.csv"'
        return response
    wb = Workbook()
    ws = wb.active
    ws.title = "Login Sheet"
    headers = list(rows[0].keys()) if rows else []
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)
    for row in rows:
        ws.append([row.get(h, "") for h in headers])
    buffer = io.BytesIO()
    wb.save(buffer)
    response = HttpResponse(buffer.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="{filename}.xlsx"'
    return response


def _pdf_response(rows: list[dict[str, Any]], filename: str) -> HttpResponse:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=0.35 * inch,
        rightMargin=0.35 * inch,
        topMargin=0.35 * inch,
        bottomMargin=0.35 * inch,
        title="PGSIMS Resident Login Sheet",
    )
    headers = list(rows[0].keys()) if rows else [
        "Resident Name",
        "Department",
        "Program",
        "Username",
        "Temporary Password",
        "Login URL",
    ]
    data = [headers]
    data.extend([[str(row.get(header, "")) for header in headers] for row in rows])
    table = Table(
        data,
        repeatRows=1,
        colWidths=[2.0 * inch, 1.35 * inch, 1.15 * inch, 0.9 * inch, 1.25 * inch, 2.1 * inch],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#344e41")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#9ca3af")),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("LEADING", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f4f7f5")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "LoginSheetTitle",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontSize=16,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "LoginSheetSubtitle",
        parent=styles["BodyText"],
        alignment=TA_CENTER,
        fontSize=8,
        textColor=colors.HexColor("#4b5563"),
    )
    doc.build(
        [
            Paragraph("PGSIMS Resident Login Sheet", title_style),
            Paragraph(
                f"Login URL: {LOGIN_URL} | Temporary password must be changed on first login.",
                subtitle_style,
            ),
            Spacer(1, 0.18 * inch),
            table,
        ]
    )
    response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}.pdf"'
    return response


@extend_schema(responses={200: None})
class ResidentOnboardingUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResidentOnboardingUploadSerializer

    def post(self, request):
        _manager_only(request.user)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        uploaded_file = serializer.validated_data["file"]
        headers, rows = _read_rows(uploaded_file)
        if not headers:
            raise ValidationError({"file": "No headers found."})
        if not rows:
            raise ValidationError({"file": "Empty file."})
        batch = OnboardingImportBatch.objects.create(
            file_name=uploaded_file.name,
            uploaded_by=request.user,
            status=OnboardingImportBatch.STATUS_UPLOADED,
            headers_json=headers,
            sample_rows_json=rows[:5],
            raw_rows_json=rows,
        )
        return Response(
            {
                "batch_id": batch.id,
                "file_name": batch.file_name,
                "headers": headers,
                "sample_rows": rows[:5],
                "total_rows": len(rows),
                "suggested_mapping": _auto_map(headers),
            }
        )


@extend_schema(responses={200: None})
class ResidentOnboardingMapView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResidentOnboardingMappingSerializer

    def post(self, request):
        _manager_only(request.user)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        batch = get_object_or_404(OnboardingImportBatch, pk=serializer.validated_data["batch_id"])
        mapping = serializer.validated_data["mapping"]
        if not mapping.get("resident_name"):
            raise ValidationError({"resident_name": "Resident Name must be mapped."})
        if not mapping.get("department"):
            raise ValidationError({"department": "Department must be mapped."})
        invalid_headers = sorted(
            {source for source in mapping.values() if source and source not in batch.headers_json}
        )
        if invalid_headers:
            raise ValidationError(
                {"mapping": f"Unknown spreadsheet columns: {', '.join(invalid_headers)}"}
            )
        preview_rows = _build_preview_rows(batch, mapping)
        return Response(
            {
                "batch_id": batch.id,
                "total_rows": batch.total_rows,
                "ready_rows": batch.ready_rows,
                "error_rows": batch.error_rows,
                "duplicate_rows": batch.duplicate_rows,
                "preview_rows": [
                    {k: v for k, v in row.items() if k != "_payload"} for row in preview_rows
                ],
                "mapping": mapping,
            }
        )


@extend_schema(responses={200: None})
class ResidentOnboardingImportView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResidentOnboardingBatchSerializer

    def post(self, request):
        _manager_only(request.user)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        batch = get_object_or_404(OnboardingImportBatch, pk=serializer.validated_data["batch_id"])
        if batch.imported_rows or batch.status in {
            OnboardingImportBatch.STATUS_IMPORTED,
            OnboardingImportBatch.STATUS_LOGINS_GENERATED,
            OnboardingImportBatch.STATUS_ISSUED,
            OnboardingImportBatch.STATUS_COMPLETED,
        }:
            return Response(
                {"detail": "This batch has already been imported."},
                status=status.HTTP_409_CONFLICT,
            )
        preview_rows = batch.preview_rows_json or _build_preview_rows(batch, batch.mapping_json)
        imported_ids: list[int] = []
        imported = 0
        with transaction.atomic():
            for row in preview_rows:
                if row.get("status") != "Ready":
                    continue
                payload = row.get("_payload") or {}
                department = _resolve_department(payload.get("department"))
                if not department:
                    continue
                hospital = _resolve_home_hospital(department)
                user = User.objects.create_user(
                    username=f"pending-{batch.id}-{row['row_number']}",
                    password=None,
                    email=_clean_text(payload.get("email")),
                    first_name=_split_name(payload.get("resident_name"))[0],
                    last_name=_split_name(payload.get("resident_name"))[1],
                    role="resident",
                    phone_number=_clean_text(payload.get("mobile_number")),
                    cnic=_clean_text(payload.get("cnic")),
                    registration_number=_clean_text(payload.get("registration_number")),
                    force_password_change=True,
                    home_hospital=hospital,
                    year=_clean_text(payload.get("training_year")),
                )
                user.set_unusable_password()
                user.home_department = department
                user.save(update_fields=["password", "home_department", "home_hospital", "year"])
                DepartmentMembership.objects.update_or_create(
                    user=user,
                    department=department,
                    member_type=DepartmentMembership.MEMBER_RESIDENT,
                    defaults={
                        "is_primary": True,
                        "active": True,
                        "start_date": _parse_date(payload.get("joining_date")) or timezone.now().date(),
                        "end_date": None,
                        "created_by": request.user,
                        "updated_by": request.user,
                    },
                )
                supervisor = _resolve_supervisor(payload.get("supervisor_name"))
                if supervisor:
                    user.supervisor = supervisor
                    user.save(update_fields=["supervisor"])
                    SupervisorResidentLink.objects.update_or_create(
                        supervisor_user=supervisor,
                        resident_user=user,
                        department=department,
                        defaults={
                            "start_date": _parse_date(payload.get("joining_date")) or timezone.now().date(),
                            "end_date": None,
                            "active": True,
                            "created_by": request.user,
                            "updated_by": request.user,
                        },
                    )
                profile = ResidentProfile.objects.create(
                    user=user,
                    import_batch=batch,
                    pgr_id="",
                    program_name=_clean_text(payload.get("program_name")),
                    training_year=_clean_text(payload.get("training_year")),
                    joining_date=_parse_date(payload.get("joining_date")),
                    raw_import_data=payload,
                    profile_completed=False,
                    login_generated=False,
                    login_issued=False,
                    training_start=_parse_date(payload.get("joining_date")) or timezone.now().date(),
                    training_level=_training_year_level(payload.get("training_year")),
                )
                program = _resolve_program(payload.get("program_name"))
                if program:
                    ResidentTrainingRecord.objects.update_or_create(
                        resident_user=user,
                        program=program,
                        defaults={
                            "start_date": profile.joining_date or timezone.now().date(),
                            "expected_end_date": None,
                            "current_level": _training_year_level(payload.get("training_year")),
                            "status": ResidentTrainingRecord.STATUS_ACTIVE,
                            "locked_program": True,
                            "active": True,
                            "created_by": request.user,
                        },
                    )
                imported += 1
                imported_ids.append(user.id)
        batch.imported_rows = imported
        batch.imported_resident_ids_json = imported_ids
        batch.status = OnboardingImportBatch.STATUS_IMPORTED
        batch.save(update_fields=["imported_rows", "imported_resident_ids_json", "status"])
        return Response({"batch_id": batch.id, "imported_rows": imported, "imported_resident_ids": imported_ids})


@extend_schema(responses={200: None})
class ResidentOnboardingGenerateLoginsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResidentOnboardingBatchSerializer

    def post(self, request):
        _manager_only(request.user)
        batch_id = request.data.get("batch_id")
        profiles = list(_login_queryset(int(batch_id)) if batch_id else _login_queryset())
        generated = _apply_login_generation(profiles)
        if batch_id:
            batch = get_object_or_404(OnboardingImportBatch, pk=batch_id)
            batch.logins_generated = _login_queryset(int(batch_id)).filter(login_generated=True).count()
            batch.status = OnboardingImportBatch.STATUS_LOGINS_GENERATED
            batch.save(update_fields=["logins_generated", "status"])
        return Response({"generated": len(generated)})


@extend_schema(responses={200: None})
class ResidentLoginSheetView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        _manager_only(request.user)
        batch_id = request.query_params.get("batch_id")
        queryset = _login_queryset(int(batch_id)) if batch_id else _login_queryset()
        rows = [_serialise_profile(profile) for profile in queryset if profile.login_generated]
        return Response(rows)


@extend_schema(responses={200: None})
class ResidentLoginSheetExportExcelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        _manager_only(request.user)
        batch_id = request.query_params.get("batch_id")
        queryset = _login_queryset(int(batch_id)) if batch_id else _login_queryset()
        rows = [_serialise_profile(profile) for profile in queryset if profile.login_generated]
        export_rows = [
            {
                "Resident Name": row["resident_name"],
                "Department": row["department"],
                "Program": row["program"],
                "Username": row["username"],
                "Temporary Password": row["temporary_password"] or TEMP_PASSWORD,
                "Login URL": row["login_url"],
            }
            for row in rows
        ]
        return _sheet_response(export_rows, "resident_login_sheet", "xlsx")


@extend_schema(responses={200: None})
class ResidentLoginSheetExportPdfView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        _manager_only(request.user)
        batch_id = request.query_params.get("batch_id")
        queryset = _login_queryset(int(batch_id)) if batch_id else _login_queryset()
        rows = [_serialise_profile(profile) for profile in queryset if profile.login_generated]
        export_rows = [
            {
                "Resident Name": row["resident_name"],
                "Department": row["department"],
                "Program": row["program"],
                "Username": row["username"],
                "Temporary Password": row["temporary_password"] or TEMP_PASSWORD,
                "Login URL": row["login_url"],
            }
            for row in rows
        ]
        return _pdf_response(export_rows, "resident_login_sheet")


@extend_schema(responses={200: None})
class ResidentLoginIssuedView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResidentOnboardingIssueSerializer

    def post(self, request):
        _manager_only(request.user)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        resident_ids = serializer.validated_data.get("resident_ids") or []
        mark_all = serializer.validated_data.get("mark_all", False)
        qs = ResidentProfile.objects.select_related("user", "import_batch").filter(login_generated=True)
        if not mark_all:
            qs = qs.filter(user_id__in=resident_ids)
        batch_ids = set(qs.exclude(import_batch_id=None).values_list("import_batch_id", flat=True))
        updated = 0
        for profile in qs:
            profile.login_issued = True
            profile.login_issued_at = timezone.now()
            profile.login_issued_by = request.user
            profile.save(update_fields=["login_issued", "login_issued_at", "login_issued_by"])
            updated += 1
        for batch in OnboardingImportBatch.objects.filter(id__in=batch_ids):
            if not batch.resident_profiles.filter(login_generated=True, login_issued=False).exists():
                batch.status = OnboardingImportBatch.STATUS_ISSUED
                batch.save(update_fields=["status"])
        return Response({"updated": updated})


@extend_schema(responses={200: None})
class ResidentBatchListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(operation_id="resident_onboarding_batch_list", responses={200: None})
    def get(self, request):
        _manager_only(request.user)
        batches = OnboardingImportBatch.objects.select_related("uploaded_by").all()
        return Response(
            [
                {
                    "id": batch.id,
                    "file_name": batch.file_name,
                    "uploaded_by": batch.uploaded_by.get_full_name() or batch.uploaded_by.username,
                    "uploaded_at": batch.uploaded_at,
                    "total_rows": batch.total_rows,
                    "ready_rows": batch.ready_rows,
                    "error_rows": batch.error_rows,
                    "duplicate_rows": batch.duplicate_rows,
                    "imported_rows": batch.imported_rows,
                    "logins_generated": batch.logins_generated,
                    "status": batch.status,
                }
                for batch in batches
            ]
        )


@extend_schema(responses={200: None})
class ResidentBatchDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(operation_id="resident_onboarding_batch_detail", responses={200: None})
    def get(self, request, batch_id: int):
        _manager_only(request.user)
        batch = get_object_or_404(OnboardingImportBatch.objects.select_related("uploaded_by"), pk=batch_id)
        return Response(
            {
                "id": batch.id,
                "file_name": batch.file_name,
                "uploaded_by": batch.uploaded_by.get_full_name() or batch.uploaded_by.username,
                "uploaded_at": batch.uploaded_at,
                "total_rows": batch.total_rows,
                "ready_rows": batch.ready_rows,
                "error_rows": batch.error_rows,
                "duplicate_rows": batch.duplicate_rows,
                "imported_rows": batch.imported_rows,
                "logins_generated": batch.logins_generated,
                "status": batch.status,
                "mapping": batch.mapping_json,
                "headers": batch.headers_json,
                "sample_rows": batch.sample_rows_json,
                "preview_rows": batch.preview_rows_json,
                "error_rows_data": batch.error_rows_json,
                "imported_resident_ids": batch.imported_resident_ids_json,
            }
        )


@extend_schema(responses={200: None})
class ResidentBatchResidentsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, batch_id: int):
        _manager_only(request.user)
        qs = ResidentProfile.objects.filter(import_batch_id=batch_id).select_related("user")
        return Response([_serialise_profile(profile) for profile in qs])


@extend_schema(responses={200: None})
class ResidentBatchGenerateLoginsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResidentEmptySerializer

    def post(self, request, batch_id: int):
        _manager_only(request.user)
        batch = get_object_or_404(OnboardingImportBatch, pk=batch_id)
        generated = _apply_login_generation(_login_queryset(batch_id))
        batch.logins_generated = _login_queryset(batch_id).filter(login_generated=True).count()
        batch.status = OnboardingImportBatch.STATUS_LOGINS_GENERATED
        batch.save(update_fields=["logins_generated", "status"])
        return Response({"generated": len(generated)})


@extend_schema(responses={200: None})
class ResidentBatchLoginSheetExportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, batch_id: int):
        _manager_only(request.user)
        rows = [_serialise_profile(profile) for profile in _login_queryset(batch_id) if profile.login_generated]
        export_rows = [
            {
                "Resident Name": row["resident_name"],
                "Department": row["department"],
                "Program": row["program"],
                "Username": row["username"],
                "Temporary Password": row["temporary_password"] or TEMP_PASSWORD,
                "Login URL": row["login_url"],
            }
            for row in rows
        ]
        return _sheet_response(export_rows, f"resident_login_sheet_batch_{batch_id}", "xlsx")


@extend_schema(responses={200: None})
class ResidentBatchErrorReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, batch_id: int):
        _manager_only(request.user)
        batch = get_object_or_404(OnboardingImportBatch, pk=batch_id)
        rows = []
        for row in batch.preview_rows_json:
            if row.get("status") == "Ready":
                continue
            rows.append(
                {
                    "Row Number": row.get("row_number"),
                    "Resident Name": row.get("resident_name", ""),
                    "Department": row.get("department", ""),
                    "Error Reason": row.get("remarks", ""),
                    "Original Mapped Data": row.get("_payload", {}),
                }
            )
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=["Row Number", "Resident Name", "Department", "Error Reason", "Original Mapped Data"])
        writer.writeheader()
        writer.writerows(rows)
        response = HttpResponse(buffer.getvalue(), content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="resident_batch_{batch_id}_errors.csv"'
        return response


@extend_schema(responses={200: None})
class ResidentIncompleteProfilesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        _manager_only(request.user)
        qs = ResidentProfile.objects.select_related("user").filter(
            Q(profile_completed=False) | Q(user__force_password_change=True)
        )
        rows = []
        for profile in qs:
            user = profile.user
            department = _current_primary_department(user)
            rows.append(
                {
                    "resident_id": user.id,
                    "resident_name": user.get_full_name() or user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "department_id": department.id if department else None,
                    "department": department.name if department else "",
                    "program": profile.program_name,
                    "training_year": profile.training_year or user.year or "",
                    "joining_date": profile.joining_date,
                    "mobile_number": user.phone_number or "",
                    "email": user.email or "",
                    "cnic": user.cnic or "",
                    "profile_completed": profile.profile_completed,
                    "force_password_change": user.force_password_change,
                    "last_login": user.last_login,
                    "login_issued": profile.login_issued,
                    "login_generated": profile.login_generated,
                }
            )
        return Response(rows)


@extend_schema(responses={200: None})
class ResidentIncompleteProfilesExportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        _manager_only(request.user)
        rows = ResidentIncompleteProfilesView().get(request).data
        export_rows = [
            {
                "Resident Name": row["resident_name"],
                "Username": row["username"],
                "Department": row["department"],
                "Program": row["program"],
                "Mobile": row["mobile_number"],
                "Email": row["email"],
                "CNIC": row["cnic"],
                "Profile Completed": row["profile_completed"],
                "Force Password Change": row["force_password_change"],
                "Last Login": row["last_login"],
                "Login Issued": row["login_issued"],
            }
            for row in rows
        ]
        return _sheet_response(export_rows, "incomplete_resident_profiles", "xlsx")


@extend_schema(responses={200: None})
class ResidentResetPasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResidentEmptySerializer

    def post(self, request, resident_id: int):
        _manager_only(request.user)
        profile = get_object_or_404(ResidentProfile.objects.select_related("user"), user_id=resident_id)
        profile.user.set_password(TEMP_PASSWORD)
        profile.user.force_password_change = True
        profile.user.save(update_fields=["password", "force_password_change"])
        profile.login_generated = True
        profile.save(update_fields=["login_generated"])
        return Response({"detail": "Password reset to temporary password."})


@extend_schema(responses={200: None})
class ResidentEditProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResidentEditSerializer

    def patch(self, request, resident_id: int):
        _manager_only(request.user)
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        profile = get_object_or_404(ResidentProfile.objects.select_related("user"), user_id=resident_id)
        user = profile.user
        data = serializer.validated_data
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]
        if "email" in data:
            user.email = data["email"]
        if "mobile_number" in data:
            user.phone_number = data["mobile_number"]
        if "cnic" in data:
            user.cnic = data["cnic"]
        if "joining_date" in data:
            profile.joining_date = data["joining_date"]
        if "program" in data:
            profile.program_name = data["program"]
        if "training_year" in data:
            profile.training_year = data["training_year"]
            user.year = data["training_year"]
        if "profile_completed" in data:
            profile.profile_completed = data["profile_completed"]
            if data["profile_completed"]:
                profile.profile_completed_at = timezone.now()
        department = None
        if "department_id" in data and data["department_id"]:
            department = get_object_or_404(Department, pk=data["department_id"])
            user.home_department = department
        user.save()
        profile.save()
        if department:
            DepartmentMembership.objects.update_or_create(
                user=user,
                department=department,
                member_type=DepartmentMembership.MEMBER_RESIDENT,
                defaults={
                    "is_primary": True,
                    "active": True,
                    "start_date": profile.joining_date or timezone.now().date(),
                    "created_by": request.user,
                    "updated_by": request.user,
                },
            )
        return Response({"detail": "Resident profile updated."})


@extend_schema(responses={200: None})
class ResidentMarkProfileCompleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResidentEmptySerializer

    def post(self, request, resident_id: int):
        _manager_only(request.user)
        profile = get_object_or_404(ResidentProfile.objects.select_related("user"), user_id=resident_id)
        profile.profile_completed = True
        profile.profile_completed_at = timezone.now()
        profile.first_login_completed_at = profile.first_login_completed_at or timezone.now()
        profile.save(update_fields=["profile_completed", "profile_completed_at", "first_login_completed_at"])
        return Response({"detail": "Profile marked complete."})


@extend_schema(responses={200: None})
class ResidentProfileCompletionStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        _resident_only(request.user)
        profile = ResidentProfile.objects.filter(user=request.user).first()
        profile_completed = (
            bool(profile.profile_completed) if profile else not request.user.force_password_change
        )
        return Response(
            {
                "profile_completed": profile_completed,
                "force_password_change": request.user.force_password_change,
                "needs_completion": (profile is not None and not profile.profile_completed)
                or request.user.force_password_change,
                "program": profile.program_name if profile else "",
                "training_year": (profile.training_year if profile else "")
                or request.user.year
                or "",
                "joining_date": profile.joining_date if profile else None,
            }
        )


@extend_schema(responses={200: None})
class ResidentCompleteProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResidentProfileCompleteSerializer

    def post(self, request):
        _resident_only(request.user)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if data["new_password"] == TEMP_PASSWORD:
            raise ValidationError({"new_password": "New password must not remain the temporary password."})
        if data["new_password"] != data["confirm_new_password"]:
            raise ValidationError({"confirm_new_password": "Passwords do not match."})
        with transaction.atomic():
            profile, _ = ResidentProfile.objects.get_or_create(
                user=request.user,
                defaults={
                    "pgr_id": "",
                    "training_start": timezone.now().date(),
                    "training_level": "",
                },
            )
            request.user.set_password(data["new_password"])
            request.user.email = data["email"]
            request.user.phone_number = data["mobile_number"]
            request.user.cnic = data["cnic"]
            request.user.year = data["training_year"]
            request.user.force_password_change = False
            request.user.save()
            profile.program_name = data["program"]
            profile.training_year = data["training_year"]
            profile.joining_date = data.get("joining_date") or profile.joining_date
            profile.profile_completed = True
            profile.profile_completed_at = timezone.now()
            profile.first_login_completed_at = profile.first_login_completed_at or timezone.now()
            profile.save()

            program = _resolve_program(data["program"])
            if program:
                ResidentTrainingRecord.objects.update_or_create(
                    resident_user=request.user,
                    program=program,
                    defaults={
                        "start_date": profile.joining_date or timezone.now().date(),
                        "expected_end_date": None,
                        "current_level": _training_year_level(data["training_year"]),
                        "status": ResidentTrainingRecord.STATUS_ACTIVE,
                        "locked_program": True,
                        "active": True,
                        "created_by": request.user,
                    },
                )
            department = _current_primary_department(request.user)
            if department is None and request.user.home_department:
                department = request.user.home_department
            if department:
                DepartmentMembership.objects.update_or_create(
                    user=request.user,
                    department=department,
                    member_type=DepartmentMembership.MEMBER_RESIDENT,
                    defaults={
                        "is_primary": True,
                        "active": True,
                        "start_date": profile.joining_date or timezone.now().date(),
                        "created_by": request.user,
                        "updated_by": request.user,
                    },
                )
            recompute_flags_for_user(request.user)
        return Response(
            {
                "detail": "Profile completed successfully.",
                "redirect_to": "/dashboard/resident",
            }
        )
