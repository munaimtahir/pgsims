from django.core.management import call_command
from django.test import Client, TestCase

from sims.academics.models import Department
from sims.notifications.models import Notification
from sims.rotations.models import Hospital, HospitalDepartment
from sims.training.models import (
    ProgramMilestone,
    ProgramRotationTemplate,
    ResidentResearchProject,
    ResidentTrainingRecord,
    ResidentWorkshopCompletion,
    RotationAssignment,
    TrainingProgram,
    Workshop,
)
from sims.users.models import (
    DepartmentMembership,
    HODAssignment,
    HospitalAssignment,
    ResidentProfile,
    StaffProfile,
    SupervisorResidentLink,
    User,
)


class SeedDemoDataCommandTests(TestCase):
    def test_seed_demo_data_creates_demo_graph_and_admin_login(self):
        call_command("seed_demo_data", reset=True)

        admin = User.objects.get(username="admin")
        self.assertEqual(admin.role, "admin")
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.check_password("admin123"))
        self.assertTrue(Client().login(username="admin", password="admin123"))

        self.assertEqual(User.objects.filter(username__startswith="demo_").count(), 14)
        self.assertEqual(
            User.objects.filter(username__startswith="demo_", role__in=["resident", "pg"]).count(),
            8,
        )
        self.assertEqual(Hospital.objects.filter(code__startswith="DEMO-").count(), 2)
        self.assertEqual(Department.objects.filter(code__startswith="DEMO-").count(), 2)
        self.assertEqual(
            HospitalDepartment.objects.filter(
                hospital__code__startswith="DEMO-",
                department__code__startswith="DEMO-",
            ).count(),
            4,
        )
        self.assertEqual(StaffProfile.objects.count(), 4)
        self.assertEqual(ResidentProfile.objects.count(), 8)
        self.assertEqual(
            DepartmentMembership.objects.filter(department__code__startswith="DEMO-").count(),
            12,
        )
        self.assertEqual(
            HospitalAssignment.objects.filter(
                hospital_department__hospital__code__startswith="DEMO-"
            ).count(),
            12,
        )
        self.assertEqual(HODAssignment.objects.filter(department__code__startswith="DEMO-").count(), 2)
        self.assertEqual(
            SupervisorResidentLink.objects.filter(department__code__startswith="DEMO-").count(),
            8,
        )
        self.assertEqual(TrainingProgram.objects.filter(code__startswith="DEMO-").count(), 2)
        self.assertEqual(
            ProgramMilestone.objects.filter(program__code__startswith="DEMO-").count(),
            4,
        )
        self.assertEqual(
            ProgramRotationTemplate.objects.filter(program__code__startswith="DEMO-").count(),
            6,
        )
        self.assertEqual(Workshop.objects.filter(code__startswith="DEMO-").count(), 3)
        self.assertEqual(
            ResidentTrainingRecord.objects.filter(program__code__startswith="DEMO-").count(),
            8,
        )
        self.assertEqual(
            RotationAssignment.objects.filter(resident_training__program__code__startswith="DEMO-").count(),
            24,
        )
        self.assertEqual(
            ResidentResearchProject.objects.filter(
                resident_training_record__program__code__startswith="DEMO-"
            ).count(),
            8,
        )
        self.assertEqual(
            ResidentWorkshopCompletion.objects.filter(
                resident_training_record__program__code__startswith="DEMO-"
            ).count(),
            8,
        )
        self.assertEqual(
            Notification.objects.filter(metadata__seed_source="seed_demo_data").count(),
            15,
        )

    def test_seed_demo_data_is_idempotent(self):
        call_command("seed_demo_data", reset=True)
        snapshot = self._snapshot_counts()

        call_command("seed_demo_data")
        self.assertEqual(self._snapshot_counts(), snapshot)
        self.assertTrue(User.objects.get(username="admin").check_password("admin123"))

    def _snapshot_counts(self):
        return {
            "demo_users": User.objects.filter(username__startswith="demo_").count(),
            "demo_hospitals": Hospital.objects.filter(code__startswith="DEMO-").count(),
            "demo_departments": Department.objects.filter(code__startswith="DEMO-").count(),
            "demo_matrix": HospitalDepartment.objects.filter(
                hospital__code__startswith="DEMO-",
                department__code__startswith="DEMO-",
            ).count(),
            "training_records": ResidentTrainingRecord.objects.filter(
                program__code__startswith="DEMO-"
            ).count(),
            "rotations": RotationAssignment.objects.filter(
                resident_training__program__code__startswith="DEMO-"
            ).count(),
            "research": ResidentResearchProject.objects.filter(
                resident_training_record__program__code__startswith="DEMO-"
            ).count(),
            "workshop_completions": ResidentWorkshopCompletion.objects.filter(
                resident_training_record__program__code__startswith="DEMO-"
            ).count(),
            "notifications": Notification.objects.filter(
                metadata__seed_source="seed_demo_data"
            ).count(),
        }
