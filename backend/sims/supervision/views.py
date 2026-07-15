import csv
import io
from datetime import datetime
from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from sims.users.models import ResidentProfile, SupervisorProfile
from sims.audit.models import ActivityLog
from .models import ResidentSupervisorAssignment
from .serializers import ResidentSupervisorAssignmentSerializer
from .permissions import IsSupervisionAdminOrReadOnly
from .services import (
    create_supervisor_assignment,
    change_primary_supervisor,
    end_supervisor_assignment,
    get_supervision_data_quality,
)


class ResidentSupervisorAssignmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Resident-Supervisor Assignments.
    Supports list filtering and detailed action execution.
    """

    serializer_class = ResidentSupervisorAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsSupervisionAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        qs = ResidentSupervisorAssignment.objects.select_related(
            "resident__user",
            "resident__hospital",
            "resident__department_ref",
            "supervisor__user",
            "supervisor__hospital",
            "supervisor__department_ref",
            "supervisor__designation_ref",
        )

        # Role-based access queries
        if user.role == "RESIDENT":
            qs = qs.filter(resident__user=user)
        elif user.role == "SUPERVISOR":
            qs = qs.filter(supervisor__user=user)

        # Filters
        qp = self.request.query_params
        is_active_val = qp.get("is_active")
        if is_active_val is not None:
            qs = qs.filter(is_active=(is_active_val.lower() in ["true", "1"]))

        assignment_type = qp.get("assignment_type")
        if assignment_type:
            qs = qs.filter(assignment_type=assignment_type)

        resident_id = qp.get("resident_id")
        if resident_id:
            qs = qs.filter(resident_id=resident_id)

        supervisor_id = qp.get("supervisor_id")
        if supervisor_id:
            qs = qs.filter(supervisor_id=supervisor_id)

        hospital_id = qp.get("hospital_id")
        if hospital_id:
            qs = qs.filter(resident__hospital_id=hospital_id)

        department_id = qp.get("department_id")
        if department_id:
            qs = qs.filter(resident__department_ref_id=department_id)

        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        resident = serializer.validated_data["resident"]
        supervisor = serializer.validated_data["supervisor"]
        assignment_type = serializer.validated_data["assignment_type"]
        start_date = serializer.validated_data["start_date"]
        notes = serializer.validated_data.get("notes", "")

        try:
            assignment = create_supervisor_assignment(
                resident=resident,
                supervisor=supervisor,
                assignment_type=assignment_type,
                start_date=start_date,
                notes=notes,
                actor=request.user,
            )
        except ValidationError as e:
            return Response(
                {"detail": e.messages[0] if hasattr(e, "messages") else str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response_serializer = self.get_serializer(assignment)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="end")
    def end_assignment(self, request, pk=None):
        """Ends an active supervision assignment with end date and change reason."""
        assignment = self.get_object()
        end_date_str = request.data.get("end_date")
        reason_for_change = request.data.get("reason_for_change", "")

        if not end_date_str:
            return Response(
                {"end_date": "End date is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            ended_assignment = end_supervisor_assignment(
                assignment=assignment,
                end_date=end_date,
                reason_for_change=reason_for_change,
                actor=request.user,
            )
        except ValidationError as e:
            return Response(
                {"detail": e.messages[0] if hasattr(e, "messages") else str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValueError:
            return Response(
                {"end_date": "Invalid date format. Expected YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(ended_assignment)
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def change_primary_view(request):
    """Atomic endpoint to rotate/replace a resident's primary supervisor."""
    if request.user.role != "ADMIN":
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

    resident_id = request.data.get("resident_id")
    new_supervisor_id = request.data.get("new_supervisor_id")
    start_date_str = request.data.get("start_date")
    reason_for_change = request.data.get("reason_for_change", "")

    if not resident_id or not new_supervisor_id or not start_date_str:
        return Response(
            {"detail": "resident_id, new_supervisor_id, and start_date are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        resident = ResidentProfile.objects.get(id=resident_id)
        new_supervisor = SupervisorProfile.objects.get(id=new_supervisor_id)

        new_assignment = change_primary_supervisor(
            resident=resident,
            new_supervisor=new_supervisor,
            start_date=start_date,
            reason_for_change=reason_for_change,
            actor=request.user,
        )
    except ResidentProfile.DoesNotExist:
        return Response({"detail": "Resident not found."}, status=status.HTTP_404_NOT_FOUND)
    except SupervisorProfile.DoesNotExist:
        return Response({"detail": "Supervisor not found."}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError as e:
        return Response(
            {"detail": e.messages[0] if hasattr(e, "messages") else str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except ValueError:
        return Response(
            {"start_date": "Invalid date format. Expected YYYY-MM-DD."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ResidentSupervisorAssignmentSerializer(new_assignment)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def supervision_options_view(request):
    """Lists eligible residents and supervisors filtered dynamically for assignment forms."""
    qp = request.query_params
    training_site_id = qp.get("training_site_id")
    department_id = qp.get("department_id")
    only_unassigned = qp.get("only_unassigned_residents") in ["true", "1"]

    # Filter residents
    residents = ResidentProfile.objects.select_related(
        "user", "hospital", "department_ref", "program_ref", "academic_session_ref"
    )
    if training_site_id:
        residents = residents.filter(hospital_id=training_site_id)
    if department_id:
        residents = residents.filter(department_ref_id=department_id)

    # Filter supervisors
    supervisors = SupervisorProfile.objects.select_related(
        "user", "hospital", "department_ref", "designation_ref"
    )
    if training_site_id:
        supervisors = supervisors.filter(hospital_id=training_site_id)
    if department_id:
        supervisors = supervisors.filter(department_ref_id=department_id)

    # Pre-fetch counts and states
    from collections import defaultdict

    active_assignments = ResidentSupervisorAssignment.objects.filter(is_active=True)

    resident_has_primary = set(
        active_assignments.filter(
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY
        ).values_list("resident_id", flat=True)
    )

    supervisor_primary_counts = defaultdict(int)
    for a in active_assignments.filter(
        assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY
    ):
        supervisor_primary_counts[a.supervisor_id] += 1

    supervisor_total_counts = defaultdict(int)
    for a in active_assignments:
        supervisor_total_counts[a.supervisor_id] += 1

    residents_data = []
    for r in residents:
        has_primary = r.id in resident_has_primary
        if only_unassigned and has_primary:
            continue
        residents_data.append(
            {
                "id": r.id,
                "name": r.user.get_full_name(),
                "username": r.user.username,
                "training_site": r.hospital.name if r.hospital else "",
                "department": r.department_ref.name if r.department_ref else "",
                "program": r.program_ref.name if r.program_ref else "",
                "academic_session": r.academic_session_ref.name
                if r.academic_session_ref
                else "",
                "has_active_primary": has_primary,
            }
        )

    supervisors_data = []
    for s in supervisors:
        supervisors_data.append(
            {
                "id": s.id,
                "name": s.user.get_full_name(),
                "training_site": s.hospital.name if s.hospital else "",
                "department": s.department_ref.name if s.department_ref else "",
                "designation": s.designation_ref.name if s.designation_ref else "",
                "active_primary_count": supervisor_primary_counts[s.id],
                "active_total_count": supervisor_total_counts[s.id],
            }
        )

    return Response(
        {
            "residents": residents_data,
            "supervisors": supervisors_data,
        }
    )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def supervision_data_quality_view(request):
    """Aggregates all supervision data anomalies for admin review."""
    if request.user.role != "ADMIN":
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

    metrics = get_supervision_data_quality()
    return Response(metrics)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def supervision_import_view(request):
    """controlled CSV importer for resident-supervisor mapping."""
    if request.user.role != "ADMIN":
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

    file = request.FILES.get("file")
    if not file:
        return Response({"detail": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

    dry_run = request.data.get("dry_run", "true").lower() in ["true", "1"]

    try:
        decoded_file = file.read().decode("utf-8")
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)
    except Exception as e:
        return Response(
            {"detail": f"Failed to parse CSV: {e}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    rows = list(reader)
    failures = []
    successes = []

    from django.contrib.auth import get_user_model
    User = get_user_model()

    with transaction.atomic():
        for index, row in enumerate(rows, start=1):
            res_username = (row.get("resident_username") or "").strip()
            res_reg = (row.get("resident_registration_no") or "").strip()
            res_email = (row.get("resident_email") or "").strip()

            sup_username = (row.get("supervisor_username") or "").strip()
            sup_pmdc = (row.get("supervisor_pmdc_no") or "").strip()
            sup_email = (row.get("supervisor_email") or "").strip()

            assignment_type = (row.get("assignment_type") or "PRIMARY").strip().upper()
            start_date_str = (row.get("start_date") or "").strip()
            notes = (row.get("notes") or "").strip()

            # Find Resident
            resident_profile = None
            res_user = None
            if res_username:
                res_user = User.objects.filter(username=res_username).first()
            if not res_user and res_reg:
                resident_profile = ResidentProfile.objects.filter(
                    registration_number=res_reg
                ).first()
                if resident_profile:
                    res_user = resident_profile.user
            if not res_user and res_email:
                res_user = User.objects.filter(email=res_email).first()

            if res_user and not resident_profile:
                resident_profile = getattr(res_user, "resident_profile", None)

            if not resident_profile:
                failures.append(
                    {
                        "row": index,
                        "error": f"Resident not found for username '{res_username}', registration '{res_reg}', email '{res_email}'.",
                    }
                )
                continue

            # Find Supervisor
            supervisor_profile = None
            sup_user = None
            if sup_username:
                sup_user = User.objects.filter(username=sup_username).first()
            if not sup_user and sup_pmdc:
                supervisor_profile = SupervisorProfile.objects.filter(
                    pmdc_number=sup_pmdc
                ).first()
                if supervisor_profile:
                    sup_user = supervisor_profile.user
            if not sup_user and sup_email:
                sup_user = User.objects.filter(email=sup_email).first()

            if sup_user and not supervisor_profile:
                supervisor_profile = getattr(sup_user, "supervisor_profile", None)

            if not supervisor_profile:
                failures.append(
                    {
                        "row": index,
                        "error": f"Supervisor not found for username '{sup_username}', PMDC '{sup_pmdc}', email '{sup_email}'.",
                    }
                )
                continue

            # Parse Start Date
            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            except ValueError:
                failures.append(
                    {
                        "row": index,
                        "error": f"Invalid start_date format '{start_date_str}'. Expected YYYY-MM-DD.",
                    }
                )
                continue

            # Validate profiles match (hospital and department)
            if resident_profile.hospital != supervisor_profile.hospital:
                failures.append(
                    {
                        "row": index,
                        "error": f"Hospital mismatch: resident is at '{resident_profile.hospital.name if resident_profile.hospital else 'None'}', supervisor is at '{supervisor_profile.hospital.name if supervisor_profile.hospital else 'None'}'.",
                    }
                )
                continue

            if resident_profile.department_ref != supervisor_profile.department_ref:
                failures.append(
                    {
                        "row": index,
                        "error": f"Department mismatch: resident is in '{resident_profile.department_ref.name if resident_profile.department_ref else 'None'}', supervisor is in '{supervisor_profile.department_ref.name if supervisor_profile.department_ref else 'None'}'.",
                    }
                )
                continue

            if assignment_type not in [
                ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
                ResidentSupervisorAssignment.ASSIGNMENT_CO_SUPERVISOR,
            ]:
                failures.append(
                    {
                        "row": index,
                        "error": f"Invalid assignment_type '{assignment_type}'. Allowed types: PRIMARY, CO_SUPERVISOR.",
                    }
                )
                continue

            # Primary supervisor constraint
            if assignment_type == ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY:
                existing_primary = ResidentSupervisorAssignment.objects.filter(
                    resident=resident_profile,
                    assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
                    is_active=True,
                ).first()
                if existing_primary:
                    failures.append(
                        {
                            "row": index,
                            "error": f"Resident '{resident_profile.user.get_full_name()}' already has an active primary supervisor '{existing_primary.supervisor.user.get_full_name()}'.",
                        }
                    )
                    continue

            # Check duplicate active assignment
            existing_dup = ResidentSupervisorAssignment.objects.filter(
                resident=resident_profile,
                supervisor=supervisor_profile,
                assignment_type=assignment_type,
                is_active=True,
            ).exists()
            if existing_dup:
                failures.append(
                    {
                        "row": index,
                        "error": f"Duplicate active assignment for resident '{resident_profile.user.get_full_name()}' and supervisor '{supervisor_profile.user.get_full_name()}'.",
                    }
                )
                continue

            successes.append(
                {
                    "row": index,
                    "resident": resident_profile.user.get_full_name(),
                    "supervisor": supervisor_profile.user.get_full_name(),
                    "assignment_type": assignment_type,
                    "start_date": str(start_date),
                }
            )

            if not dry_run:
                create_supervisor_assignment(
                    resident=resident_profile,
                    supervisor=supervisor_profile,
                    assignment_type=assignment_type,
                    start_date=start_date,
                    notes=notes,
                    actor=request.user,
                )

        if dry_run or len(failures) > 0:
            transaction.set_rollback(True)

    action_name = "create" if not dry_run else "view"
    verb_name = "SUPERVISION_IMPORT_COMMITTED" if not dry_run else "SUPERVISION_IMPORT_DRY_RUN"
    ActivityLog.log(
        actor=request.user,
        action=action_name,
        verb=verb_name,
        metadata={
            "description": f"Supervision mapping import processed. Successes: {len(successes)}, Failures: {len(failures)}",
            "dry_run": dry_run,
            "success_count": len(successes),
            "failure_count": len(failures),
        },
    )

    return Response(
        {
            "success": len(failures) == 0,
            "dry_run": dry_run,
            "successes": successes,
            "failures": failures,
            "warnings": [],
        }
    )
