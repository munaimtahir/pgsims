from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from sims.rotations.models import Hospital, HospitalDepartment
from sims.academics.models import Department


@login_required
def department_by_hospital_api(request, hospital_id):
    """Return active departments for a hospital as JSON."""
    try:
        hospital = Hospital.objects.get(pk=hospital_id, is_active=True)
    except Hospital.DoesNotExist:
        return JsonResponse({"departments": []})
    depts = HospitalDepartment.objects.filter(
        hospital=hospital, is_active=True
    ).select_related("department").order_by("department__name")
    return JsonResponse({
        "departments": [
            {"id": hd.department.id, "name": hd.department.name, "code": hd.department.code}
            for hd in depts
        ]
    })
