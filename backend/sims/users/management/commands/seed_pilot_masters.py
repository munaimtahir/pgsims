from django.core.management.base import BaseCommand
from django.db.models import Q
from sims.academics.models import Institution, Department, Specialty, Designation, AcademicSession
from sims.rotations.models import Hospital
from sims.training.models import TrainingProgram


class Command(BaseCommand):
    help = "Seeds pilot master data idempotently for local development and pilot setup."

    def handle(self, *args, **options):
        self.stdout.write("Seeding pilot master data...")

        # 1. Institutions
        institutions_data = [
            {"code": "FMU", "name": "Faisalabad Medical University", "description": "Local parent university"},
            {"code": "CPSP", "name": "College of Physicians and Surgeons Pakistan", "description": "Accrediting body for FCPS/MCPS"},
            {"code": "UHS", "name": "University of Health Sciences", "description": "Awarding body for MS/MD"},
        ]
        inst_created = 0
        inst_updated = 0
        for data in institutions_data:
            obj = Institution.objects.filter(Q(code=data["code"]) | Q(name=data["name"])).first()
            if obj:
                obj.code = data["code"]
                obj.name = data["name"]
                obj.description = data["description"]
                obj.active = True
                obj.save()
                inst_updated += 1
            else:
                Institution.objects.create(
                    code=data["code"],
                    name=data["name"],
                    description=data["description"],
                    active=True,
                )
                inst_created += 1
        self.stdout.write(self.style.SUCCESS(f"Institutions: {inst_created} created, {inst_updated} updated."))

        # 2. Hospitals
        fmu_inst = Institution.objects.filter(code="FMU").first()
        hospitals_data = [
            {"code": "ALLIED", "name": "Allied Hospital", "description": "Primary teaching site"},
            {"code": "DHQ", "name": "DHQ Hospital", "description": "District headquarter training site"},
            {"code": "FIC", "name": "Faisalabad Institute of Cardiology", "description": "Specialized cardiology site"},
            {"code": "CHILD", "name": "Children Hospital", "description": "Pediatric specialized site"},
        ]
        hosp_created = 0
        hosp_updated = 0
        for data in hospitals_data:
            obj = Hospital.objects.filter(Q(code=data["code"]) | Q(name=data["name"])).first()
            if obj:
                obj.code = data["code"]
                obj.name = data["name"]
                obj.description = data["description"]
                obj.institution = fmu_inst
                obj.is_active = True
                obj.save()
                hosp_updated += 1
            else:
                Hospital.objects.create(
                    code=data["code"],
                    name=data["name"],
                    description=data["description"],
                    institution=fmu_inst,
                    is_active=True,
                )
                hosp_created += 1
        self.stdout.write(self.style.SUCCESS(f"Hospitals: {hosp_created} created, {hosp_updated} updated."))

        # 3. Departments
        depts_data = [
            {"code": "MED", "name": "Medicine"},
            {"code": "SURG", "name": "Surgery"},
            {"code": "HEM", "name": "Hematology"},
            {"code": "CARD", "name": "Cardiology"},
            {"code": "UROL", "name": "Urology"},
            {"code": "PATH", "name": "Pathology"},
            {"code": "PEDS", "name": "Pediatrics"},
            {"code": "GYNAE", "name": "Gynecology"},
        ]
        dept_created = 0
        dept_updated = 0
        for data in depts_data:
            obj = Department.objects.filter(Q(code=data["code"]) | Q(name=data["name"])).first()
            if obj:
                obj.code = data["code"]
                obj.name = data["name"]
                obj.active = True
                obj.save()
                dept_updated += 1
            else:
                Department.objects.create(
                    code=data["code"],
                    name=data["name"],
                    active=True,
                )
                dept_created += 1
        self.stdout.write(self.style.SUCCESS(f"Departments: {dept_created} created, {dept_updated} updated."))

        # 4. Programs
        programs_data = [
            {"code": "FCPS", "name": "Fellow of College of Physicians and Surgeons", "degree_type": "FCPS"},
            {"code": "MS", "name": "Master of Surgery", "degree_type": "MS"},
            {"code": "MD", "name": "Doctor of Medicine", "degree_type": "MD"},
            {"code": "MPhil", "name": "Master of Philosophy", "degree_type": "Other"},
            {"code": "MCPS", "name": "Member of College of Physicians and Surgeons", "degree_type": "Other"},
            {"code": "Diploma", "name": "Postgraduate Diploma", "degree_type": "Diploma"},
        ]
        prog_created = 0
        prog_updated = 0
        med_dept = Department.objects.filter(code="MED").first()
        for data in programs_data:
            obj = TrainingProgram.objects.filter(Q(code=data["code"]) | Q(name=data["name"])).first()
            if obj:
                obj.code = data["code"]
                obj.name = data["name"]
                obj.degree_type = data["degree_type"]
                obj.duration_months = 48 if data["code"] in ["FCPS", "MS", "MD"] else 24
                obj.department = med_dept
                obj.active = True
                obj.save()
                prog_updated += 1
            else:
                TrainingProgram.objects.create(
                    code=data["code"],
                    name=data["name"],
                    degree_type=data["degree_type"],
                    duration_months=48 if data["code"] in ["FCPS", "MS", "MD"] else 24,
                    department=med_dept,
                    active=True,
                )
                prog_created += 1
        self.stdout.write(self.style.SUCCESS(f"Programs: {prog_created} created, {prog_updated} updated."))

        # 5. Designations
        designations_data = [
            {"code": "HOD", "name": "Head of Department (HOD)"},
            {"code": "Professor", "name": "Professor"},
            {"code": "Associate Professor", "name": "Associate Professor"},
            {"code": "Assistant Professor", "name": "Assistant Professor"},
            {"code": "Consultant", "name": "Consultant"},
            {"code": "Senior Registrar", "name": "Senior Registrar"},
            {"code": "Registrar", "name": "Registrar"},
            {"code": "Demonstrator", "name": "Demonstrator"},
        ]
        desig_created = 0
        desig_updated = 0
        for data in designations_data:
            obj = Designation.objects.filter(Q(code=data["code"]) | Q(name=data["name"])).first()
            if obj:
                obj.code = data["code"]
                obj.name = data["name"]
                obj.active = True
                obj.save()
                desig_updated += 1
            else:
                Designation.objects.create(
                    code=data["code"],
                    name=data["name"],
                    active=True,
                )
                desig_created += 1
        self.stdout.write(self.style.SUCCESS(f"Designations: {desig_created} created, {desig_updated} updated."))

        # 6. Academic Sessions
        sessions_data = [
            {"code": "2026", "name": "Session 2026"},
            {"code": "JAN-2026", "name": "JAN-2026 Induction"},
            {"code": "JUL-2026", "name": "JUL-2026 Induction"},
        ]
        sess_created = 0
        sess_updated = 0
        for data in sessions_data:
            obj = AcademicSession.objects.filter(Q(code=data["code"]) | Q(name=data["name"])).first()
            if obj:
                obj.code = data["code"]
                obj.name = data["name"]
                obj.active = True
                obj.save()
                sess_updated += 1
            else:
                AcademicSession.objects.create(
                    code=data["code"],
                    name=data["name"],
                    active=True,
                )
                sess_created += 1
        self.stdout.write(self.style.SUCCESS(f"Academic Sessions: {sess_created} created, {sess_updated} updated."))

        # 7. Specialties (Optional/Examples)
        specialties_data = [
            {"code": "GI_SURG", "name": "GI Surgery"},
            {"code": "PED_HEM", "name": "Pediatric Hematology"},
            {"code": "INT_CARD", "name": "Interventional Cardiology"},
        ]
        spec_created = 0
        spec_updated = 0
        for data in specialties_data:
            obj = Specialty.objects.filter(Q(code=data["code"]) | Q(name=data["name"])).first()
            if obj:
                obj.code = data["code"]
                obj.name = data["name"]
                obj.active = True
                obj.save()
                spec_updated += 1
            else:
                Specialty.objects.create(
                    code=data["code"],
                    name=data["name"],
                    active=True,
                )
                spec_created += 1
        self.stdout.write(self.style.SUCCESS(f"Specialties: {spec_created} created, {spec_updated} updated."))

        self.stdout.write(self.style.SUCCESS("All pilot master data seeded successfully!"))
