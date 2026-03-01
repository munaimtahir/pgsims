from django.urls import path
from . import views

app_name = "rotations"

urlpatterns = [
    path(
        "api/departments/<int:hospital_id>/",
        views.department_by_hospital_api,
        name="departments_by_hospital",
    ),
]
