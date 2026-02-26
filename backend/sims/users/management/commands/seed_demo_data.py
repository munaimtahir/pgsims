"""Seed presentation-grade demo data for screenshots and walkthroughs."""

from __future__ import annotations

import re
from datetime import timedelta

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from sims.academics.models import Department
from sims.logbook.models import Diagnosis, LogbookEntry, Procedure
from sims.rotations.models import Hospital, HospitalDepartment, Rotation
from sims.users.models import User

DEMO_EMAIL_DOMAIN = "@demo.local"
DEMO_PASSWORD = "DemoPass123!"
DEMO_HOSPITAL_CODE = "DEMO-UTRMC-URO"

FACULTY_NAMES = [
    "Prof. Dr. Muhammad Tahir Bashir Malik",
    "Dr. Muhammad Irfan Munir",
    "Dr. Muhammad Sheraz Javed",
    "Dr. Aamir Imtiaz Khan",
    "Dr. Moin Anwar",
]

RESIDENT_NAMES = [
    "Dr. Muhammad Usman Ali",
    "Dr. Ahmed Raza Siddiqui",
    "Dr. Bilal Ahmad Cheema",
    "Dr. Hassan Rauf",
    "Dr. Ali Hamza Qureshi",
    "Dr. Umair Tariq",
    "Dr. Zain Ul Abideen",
    "Dr. Saad Masood",
    "Dr. Hamza Khalid",
    "Dr. Talha Mahmood",
]

DEPARTMENT_SPECS = [
    ("DEMO-URO", "Department of Urology & Renal Transplant"),
    ("DEMO-URO-GEN", "General Urology"),
    ("DEMO-URO-ENDO", "Endourology"),
    ("DEMO-URO-ONCO", "Uro-Oncology"),
    ("DEMO-URO-TRAN", "Renal Transplant Unit"),
]

PROCEDURE_SPECS = [
    ("URS (Ureterorenoscopy)", "surgical"),
    ("PCNL", "surgical"),
    ("TURP", "surgical"),
    ("Radical Nephrectomy", "surgical"),
    ("Cystoscopy", "diagnostic"),
    ("Pyeloplasty", "surgical"),
    ("Bladder Tumor Resection", "surgical"),
    ("Urethroplasty", "surgical"),
]

CASE_TEMPLATES = [
    {
        "title": "Proximal Ureteric Stone Managed with URS",
        "procedure": "URS (Ureterorenoscopy)",
        "diagnosis": "Ureteric Calculus",
        "summary": (
            "45-year-old male presented with right flank pain. CT scan showed 1.5 cm "
            "proximal ureteric calculus. URS performed successfully."
        ),
        "management": (
            "Endoscopic stone fragmentation completed with DJ stent placement. Analgesia, "
            "hydration advice, and follow-up imaging planned."
        ),
        "topic": "Endourology - Ureteric Calculus",
    },
    {
        "title": "Staghorn Calculus Managed with PCNL",
        "procedure": "PCNL",
        "diagnosis": "Renal Calculus",
        "summary": (
            "52-year-old female with recurrent urinary tract infection and left flank pain. "
            "Imaging showed partial staghorn calculus in left kidney."
        ),
        "management": (
            "PCNL performed under fluoroscopic guidance with near-complete stone clearance. "
            "Nephrostomy care and metabolic evaluation advised."
        ),
        "topic": "Endourology - Renal Stone Disease",
    },
    {
        "title": "LUTS Secondary to BPH Managed with TURP",
        "procedure": "TURP",
        "diagnosis": "Benign Prostatic Hyperplasia",
        "summary": (
            "66-year-old male reported severe lower urinary tract symptoms with recurrent "
            "retention episodes despite medical therapy."
        ),
        "management": (
            "TURP completed with good hemostasis. Catheter removed after trial without "
            "catheter; patient counseled regarding postoperative recovery."
        ),
        "topic": "General Urology - BPH",
    },
    {
        "title": "Localized Renal Mass Managed with Radical Nephrectomy",
        "procedure": "Radical Nephrectomy",
        "diagnosis": "Renal Cell Carcinoma",
        "summary": (
            "58-year-old male evaluated for incidentally detected right renal mass "
            "suspicious for malignancy on contrast CT."
        ),
        "management": (
            "Radical nephrectomy performed via transperitoneal approach. Histopathology "
            "discussion and oncology follow-up arranged."
        ),
        "topic": "Uro-Oncology - Renal Tumor",
    },
    {
        "title": "Gross Hematuria Workup with Cystoscopy",
        "procedure": "Cystoscopy",
        "diagnosis": "Hematuria Evaluation",
        "summary": (
            "49-year-old male presented with painless gross hematuria. Initial ultrasound "
            "was inconclusive."
        ),
        "management": (
            "Diagnostic cystoscopy performed with bladder mapping. Biopsy from suspicious "
            "area sent for histopathology."
        ),
        "topic": "General Urology - Hematuria",
    },
    {
        "title": "PUJ Obstruction Corrected with Pyeloplasty",
        "procedure": "Pyeloplasty",
        "diagnosis": "PUJ Obstruction",
        "summary": (
            "33-year-old male had intermittent flank pain and worsening hydronephrosis on "
            "serial imaging suggestive of PUJ obstruction."
        ),
        "management": (
            "Dismembered pyeloplasty performed with internal stenting. Renal scan follow-up "
            "planned to assess drainage improvement."
        ),
        "topic": "Reconstructive Urology - PUJ Obstruction",
    },
    {
        "title": "Non-Muscle Invasive Bladder Tumor Resection",
        "procedure": "Bladder Tumor Resection",
        "diagnosis": "Bladder Tumor",
        "summary": (
            "61-year-old smoker presented with intermittent painless hematuria. Cystoscopy "
            "revealed papillary bladder lesion."
        ),
        "management": (
            "Complete transurethral bladder tumor resection performed with detrusor sampling. "
            "Plan for intravesical therapy discussed."
        ),
        "topic": "Uro-Oncology - Bladder Tumor",
    },
    {
        "title": "Bulbar Stricture Managed with Urethroplasty",
        "procedure": "Urethroplasty",
        "diagnosis": "Urethral Stricture",
        "summary": (
            "38-year-old male with weak stream and recurrent retention had retrograde "
            "urethrogram showing short-segment bulbar stricture."
        ),
        "management": (
            "Anastomotic urethroplasty completed. Suprapubic diversion maintained with "
            "planned postoperative pericatheter urethrogram."
        ),
        "topic": "Reconstructive Urology - Urethral Stricture",
    },
]

DIAGNOSIS_SPECS = [
    ("Ureteric Calculus", "genitourinary"),
    ("Renal Calculus", "genitourinary"),
    ("Benign Prostatic Hyperplasia", "genitourinary"),
    ("Renal Cell Carcinoma", "oncology"),
    ("Hematuria Evaluation", "genitourinary"),
    ("PUJ Obstruction", "genitourinary"),
    ("Bladder Tumor", "oncology"),
    ("Urethral Stricture", "genitourinary"),
]


class Command(BaseCommand):
    help = "Seed realistic demo data for Urology presentations."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing @demo.local users and demo-coded departments/hospitals before seeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        diagnostics = self._validate_model_contracts()
        if diagnostics:
            self.stdout.write(self.style.ERROR("DIAGNOSTIC REPORT"))
            for line in diagnostics:
                self.stdout.write(self.style.ERROR(f"- {line}"))
            raise CommandError("Model structure mismatch detected. Seeding aborted.")

        if options["reset"]:
            self._reset_demo_entities()

        LogbookEntry.objects.filter(pg__email__iendswith=DEMO_EMAIL_DOMAIN).delete()
        Rotation.objects.filter(pg__email__iendswith=DEMO_EMAIL_DOMAIN).delete()

        hospital = self._upsert_hospital()
        departments = self._upsert_departments()
        self._upsert_hospital_departments(hospital=hospital, departments=departments)

        supervisors, supervisors_created = self._upsert_supervisors(
            home_hospital=hospital,
            home_department=departments["DEMO-URO"],
        )
        head = supervisors[0]
        root_department = departments["DEMO-URO"]
        if root_department.head_id != head.id:
            root_department.head = head
            root_department.save(update_fields=["head"])

        residents, residents_created = self._upsert_residents(
            supervisors=supervisors,
            home_hospital=hospital,
            home_department=root_department,
        )

        rotations_created = self._seed_rotations(residents=residents, departments=departments, hospital=hospital)
        status_counts = self._seed_logbook_entries(residents=residents, rotations_by_pg=self._rotations_by_pg())
        research_created, research_note = self._seed_research_progress_if_supported(residents=residents)

        self.stdout.write(self.style.SUCCESS("seed_demo_data completed successfully."))
        self.stdout.write(f"Department Created: {len(departments)}")
        self.stdout.write(f"Supervisors Created: {supervisors_created}")
        self.stdout.write(f"Residents Created: {residents_created}")
        self.stdout.write("Cases per status:")
        self.stdout.write(f"  Draft: {status_counts['draft']}")
        self.stdout.write(f"  Submitted: {status_counts['submitted']}")
        self.stdout.write(f"  Sent Back: {status_counts['sent_back']}")
        self.stdout.write(f"  Resubmitted: {status_counts['resubmitted']}")
        self.stdout.write(f"  Verified: {status_counts['verified']}")
        self.stdout.write(f"Research entries created: {research_created}")
        self.stdout.write(f"Rotations created: {rotations_created}")
        if research_note:
            self.stdout.write(self.style.WARNING(f"Research note: {research_note}"))

    def _validate_model_contracts(self):
        required_fields = {
            "users.User": {
                "email",
                "username",
                "role",
                "specialty",
                "year",
                "supervisor",
                "home_hospital",
                "home_department",
            },
            "academics.Department": {"name", "code", "head", "active"},
            "rotations.Hospital": {"name", "code", "is_active"},
            "rotations.HospitalDepartment": {"hospital", "department", "is_active"},
            "rotations.Rotation": {
                "pg",
                "department",
                "hospital",
                "supervisor",
                "start_date",
                "end_date",
                "status",
            },
            "logbook.LogbookEntry": {
                "pg",
                "case_title",
                "date",
                "location_of_activity",
                "patient_history_summary",
                "management_action",
                "topic_subtopic",
                "status",
                "supervisor_feedback",
                "verified_by",
                "verified_at",
            },
            "logbook.Procedure": {"name", "category"},
            "logbook.Diagnosis": {"name", "category"},
        }
        diagnostics = []
        for label, fields in required_fields.items():
            app_label, model_name = label.split(".")
            model = apps.get_model(app_label, model_name)
            if model is None:
                diagnostics.append(f"Missing model: {label}")
                continue
            model_fields = {field.name for field in model._meta.get_fields()}
            missing = sorted(fields - model_fields)
            if missing:
                diagnostics.append(f"{label} missing fields: {', '.join(missing)}")

        logbook_model = apps.get_model("logbook", "LogbookEntry")
        if logbook_model is not None:
            status_field = logbook_model._meta.get_field("status")
            available_statuses = {choice[0] for choice in status_field.choices}
            required_statuses = {"draft", "pending", "returned", "approved"}
            if not required_statuses.issubset(available_statuses):
                diagnostics.append(
                    "logbook.LogbookEntry status choices must include: draft, pending, returned, approved"
                )
        return diagnostics

    def _reset_demo_entities(self):
        User.objects.filter(email__iendswith=DEMO_EMAIL_DOMAIN).delete()
        Hospital.objects.filter(code__startswith="DEMO-").delete()
        Department.objects.filter(code__startswith="DEMO-").delete()

    def _upsert_hospital(self):
        hospital, _ = Hospital.objects.update_or_create(
            code=DEMO_HOSPITAL_CODE,
            defaults={
                "name": "UTRMC Teaching Hospital",
                "description": "Demo hospital environment for postgraduate urology training.",
                "is_active": True,
            },
        )
        return hospital

    def _upsert_departments(self):
        departments = {}
        for code, name in DEPARTMENT_SPECS:
            department, _ = Department.objects.update_or_create(
                code=code,
                defaults={
                    "name": name,
                    "description": "Demo department seeded for presentation snapshots.",
                    "active": True,
                },
            )
            departments[code] = department
        return departments

    def _upsert_hospital_departments(self, hospital, departments):
        for department in departments.values():
            HospitalDepartment.objects.update_or_create(
                hospital=hospital,
                department=department,
                defaults={"is_active": True},
            )

    def _upsert_supervisors(self, home_hospital, home_department):
        supervisors = []
        created_count = 0
        for raw_name in FACULTY_NAMES:
            first_name, last_name = self._split_name(raw_name)
            email_local = self._email_local_from_name(raw_name)
            email = f"{email_local}{DEMO_EMAIL_DOMAIN}"
            username = f"faculty.{email_local}"
            supervisor, created = self._upsert_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role="supervisor",
                specialty="urology",
                year=None,
                supervisor=None,
                home_hospital=home_hospital,
                home_department=home_department,
            )
            supervisors.append(supervisor)
            created_count += int(created)
        return supervisors, created_count

    def _upsert_residents(self, supervisors, home_hospital, home_department):
        residents = []
        created_count = 0
        year_cycle = ["1", "2", "3", "4", "2", "3", "1", "4", "2", "3"]
        for index, raw_name in enumerate(RESIDENT_NAMES):
            core_name = re.sub(r"^(Prof\.\s*)?(Dr\.\s*)+", "", raw_name).strip()
            first_name, last_name = self._split_name(core_name)
            email_local = self._email_local_from_name(core_name)
            resident, created = self._upsert_user(
                username=email_local,
                email=f"{email_local}{DEMO_EMAIL_DOMAIN}",
                first_name=first_name,
                last_name=last_name,
                role="pg",
                specialty="urology",
                year=year_cycle[index % len(year_cycle)],
                supervisor=supervisors[index % len(supervisors)],
                home_hospital=home_hospital,
                home_department=home_department,
            )
            residents.append(resident)
            created_count += int(created)
        return residents, created_count

    def _upsert_user(
        self,
        *,
        username,
        email,
        first_name,
        last_name,
        role,
        specialty,
        year,
        supervisor,
        home_hospital,
        home_department,
    ):
        user = User.objects.filter(email__iexact=email).first()
        created = user is None
        if created:
            user = User(
                username=username,
                email=email,
            )
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.role = role
        user.specialty = specialty
        user.year = year
        user.supervisor = supervisor
        user.home_hospital = home_hospital
        user.home_department = home_department
        user.is_active = True
        user.is_archived = False
        user.set_password(DEMO_PASSWORD)
        user.save()
        return user, created

    def _seed_rotations(self, residents, departments, hospital):
        unit_codes = ["DEMO-URO-GEN", "DEMO-URO-ENDO", "DEMO-URO-ONCO", "DEMO-URO-TRAN"]
        windows = [
            (170, 126, "completed"),
            (125, 81, "completed"),
            (80, 36, "completed"),
            (35, -15, "ongoing"),
        ]
        today = timezone.now().date()
        created_count = 0
        for resident in residents:
            for offset, unit_code in enumerate(unit_codes):
                start_days, end_days, status = windows[offset]
                start_date = today - timedelta(days=start_days)
                end_date = today - timedelta(days=end_days)
                rotation = Rotation(
                    pg=resident,
                    department=departments[unit_code],
                    hospital=hospital,
                    supervisor=resident.supervisor,
                    start_date=start_date,
                    end_date=end_date,
                    status=status,
                    objectives=f"Competency development in {departments[unit_code].name}.",
                    learning_outcomes="Demonstrate independent procedural planning and documentation.",
                    notes="Presentation demo rotation data seeded by management command.",
                )
                rotation.save()
                created_count += 1
        return created_count

    def _rotations_by_pg(self):
        mapping = {}
        for rotation in Rotation.objects.filter(pg__email__iendswith=DEMO_EMAIL_DOMAIN).select_related(
            "pg", "department"
        ):
            mapping.setdefault(rotation.pg_id, []).append(rotation)
        return mapping

    def _seed_logbook_entries(self, residents, rotations_by_pg):
        procedures = self._upsert_procedures()
        diagnoses = self._upsert_diagnoses()
        today = timezone.now().date()
        counters = {"draft": 0, "submitted": 0, "sent_back": 0, "resubmitted": 0, "verified": 0}

        for resident_index, resident in enumerate(residents):
            resident_rotations = rotations_by_pg.get(resident.id, [])
            if not resident_rotations:
                continue
            for entry_index in range(14):
                template = CASE_TEMPLATES[(resident_index + entry_index) % len(CASE_TEMPLATES)]
                day_offset = ((resident_index + 2) * 7 + entry_index * 11) % 175 + 3
                encounter_date = today - timedelta(days=day_offset)
                rotation = resident_rotations[entry_index % len(resident_rotations)]
                entry = LogbookEntry.objects.create(
                    pg=resident,
                    supervisor=resident.supervisor,
                    rotation=rotation,
                    case_title=f"{template['title']} (Case {entry_index + 1})",
                    date=encounter_date,
                    location_of_activity=rotation.department.name,
                    patient_history_summary=template["summary"],
                    management_action=template["management"],
                    topic_subtopic=template["topic"],
                    clinical_reasoning=(
                        "Clinical findings were correlated with imaging before selecting definitive "
                        "procedural management."
                    ),
                    learning_points=(
                        "Improved operative planning, peri-operative counseling, and documentation quality."
                    ),
                    status="draft",
                )
                entry.procedures.add(procedures[template["procedure"]])
                entry.primary_diagnosis = diagnoses[template["diagnosis"]]
                entry.save(update_fields=["primary_diagnosis", "updated_at"])

                if entry_index <= 2:
                    counters["draft"] += 1
                    continue

                entry.status = "pending"
                entry.save()

                if 3 <= entry_index <= 5:
                    counters["submitted"] += 1
                    continue

                entry.status = "returned"
                entry.supervisor_feedback = (
                    "Please expand peri-operative risk documentation and postoperative follow-up details."
                )
                entry.save()

                if 6 <= entry_index <= 7:
                    counters["sent_back"] += 1
                    continue

                if 8 <= entry_index <= 9:
                    entry.management_action = (
                        f"{template['management']} Revised after supervisor feedback with clearer "
                        "documentation."
                    )
                    entry.save(update_fields=["management_action", "updated_at"])
                    entry.status = "pending"
                    entry.save()
                    counters["resubmitted"] += 1
                    continue

                entry.status = "approved"
                entry.supervisor_feedback = (
                    "Comprehensive entry. Clinical reasoning and operative details are satisfactory."
                )
                entry.save()
                counters["verified"] += 1

        return counters

    def _upsert_procedures(self):
        procedures = {}
        for name, category in PROCEDURE_SPECS:
            procedure, _ = Procedure.objects.get_or_create(
                name=name,
                defaults={
                    "category": category,
                    "difficulty_level": 3,
                    "cme_points": 2,
                    "description": "Demo procedure entry for urology showcase data.",
                    "is_active": True,
                },
            )
            procedures[name] = procedure
        return procedures

    def _upsert_diagnoses(self):
        diagnoses = {}
        for name, category in DIAGNOSIS_SPECS:
            diagnosis, _ = Diagnosis.objects.get_or_create(
                name=name,
                category=category,
                defaults={
                    "description": "Demo diagnosis entry for presentation scenarios.",
                    "is_active": True,
                },
            )
            diagnoses[name] = diagnosis
        return diagnoses

    def _seed_research_progress_if_supported(self, residents):
        research_models = [m for m in apps.get_models() if "research" in m.__name__.lower()]
        if not research_models:
            return 0, "No dedicated research progress model detected; skipped."
        return 0, "Research model detected but seeding is intentionally skipped pending explicit schema."

    def _split_name(self, full_name):
        parts = full_name.split()
        if len(parts) == 1:
            return parts[0], ""
        return " ".join(parts[:-1]), parts[-1]

    def _email_local_from_name(self, full_name):
        stripped = re.sub(r"^(Prof\.\s*)?(Dr\.\s*)+", "", full_name).strip()
        parts = stripped.split()
        if len(parts) < 2:
            local = stripped.lower()
        else:
            local = f"{parts[0].lower()}.{parts[-1].lower()}"
        local = re.sub(r"[^a-z0-9.]+", "", local)
        return local
