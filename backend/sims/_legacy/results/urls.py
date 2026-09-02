from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"exams", views.ExamViewSet, basename="exam")
router.register(r"scores", views.ScoreViewSet, basename="score")

urlpatterns = [
    path("api/", include(router.urls)),
]
