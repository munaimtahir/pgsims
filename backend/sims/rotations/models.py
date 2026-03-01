from django.db import models

from sims.academics.models import Department


class Hospital(models.Model):
    """
    Model representing hospitals where rotations take place.

    Created: 2025-05-29 16:28:44 UTC
    Author: SMIB2012
    """

    name = models.CharField(max_length=200, help_text="Official name of the hospital")

    code = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        help_text="Hospital code or abbreviation",
    )

    address = models.TextField(blank=True, help_text="Complete hospital address")

    phone = models.CharField(max_length=20, blank=True, help_text="Hospital contact phone number")

    email = models.EmailField(blank=True, help_text="Hospital contact email")

    website = models.URLField(blank=True, help_text="Hospital website URL")

    description = models.TextField(
        blank=True, help_text="Description of hospital and its specialties"
    )

    facilities = models.TextField(blank=True, help_text="Available facilities and equipment")

    is_active = models.BooleanField(
        default=True, help_text="Whether this hospital is currently accepting rotations"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hospital"
        verbose_name_plural = "Hospitals"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name

    def get_departments_count(self):
        """Get count of active canonical departments hosted by this hospital."""
        return self.hospital_departments.filter(is_active=True).count()


class HospitalDepartment(models.Model):
    """Matrix of canonical departments hosted in a hospital."""

    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="hospital_departments",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="hospital_departments",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hospital Department"
        verbose_name_plural = "Hospital Departments"
        ordering = ["hospital__name", "department__name"]
        constraints = [
            models.UniqueConstraint(
                fields=["hospital", "department"],
                name="uniq_hospital_department",
            )
        ]
        indexes = [
            models.Index(fields=["hospital", "department"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.hospital} / {self.department}"
