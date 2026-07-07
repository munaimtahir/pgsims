"""
Models for Academic management in SIMS.

This module defines:
- Department: Academic departments / Specialties
"""

from django.conf import settings
from django.db import models


class Department(models.Model):
    """Academic department model."""

    name = models.CharField(max_length=200, unique=True, help_text="Department name")
    code = models.CharField(max_length=20, unique=True, help_text="Department code")
    description = models.TextField(blank=True, help_text="Department description")
    head = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="headed_departments",
        limit_choices_to={"role__in": ["ADMIN", "SUPERVISOR"]},
        help_text="Department head",
    )
    active = models.BooleanField(default=True, help_text="Is department active?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Department / Specialty"
        verbose_name_plural = "Departments / Specialties"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["active"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"
