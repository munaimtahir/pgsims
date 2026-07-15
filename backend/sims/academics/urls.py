from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"institutions", views.InstitutionViewSet, basename="master-institutions")
router.register(r"training-sites", views.HospitalViewSet, basename="master-training-sites")
router.register(r"departments", views.DepartmentViewSet, basename="master-departments")
router.register(r"programs", views.TrainingProgramViewSet, basename="master-programs")
router.register(r"specialties", views.SpecialtyViewSet, basename="master-specialties")
router.register(r"designations", views.DesignationViewSet, basename="master-designations")
router.register(r"academic-sessions", views.AcademicSessionViewSet, basename="master-academic-sessions")

urlpatterns = [
    path("", include(router.urls)),
]
