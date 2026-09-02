from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment


def _hosted_departments_qs():
    return Department.objects.filter(active=True).order_by("name")


def _hospitals_qs():
    return Hospital.objects.filter(is_active=True).order_by("name")
