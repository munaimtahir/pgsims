"""Serializers for bulk operation APIs."""

from __future__ import annotations

from rest_framework import serializers



class BulkReviewSerializer(serializers.Serializer):
    entry_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1), allow_empty=False
    )
    status = serializers.ChoiceField(choices=["pending", "approved", "returned", "rejected"])


class BulkAssignmentSerializer(serializers.Serializer):
    entry_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1), allow_empty=False
    )
    supervisor_id = serializers.IntegerField(min_value=1)


class BulkImportSerializer(serializers.Serializer):
    file = serializers.FileField()
    dry_run = serializers.BooleanField(default=True)
    allow_partial = serializers.BooleanField(default=False)


class TraineeImportSerializer(serializers.Serializer):
    file = serializers.FileField()
    dry_run = serializers.BooleanField(default=True)
    allow_partial = serializers.BooleanField(default=False)


class SupervisorImportSerializer(serializers.Serializer):
    file = serializers.FileField()
    dry_run = serializers.BooleanField(default=True)
    allow_partial = serializers.BooleanField(default=False)
    generate_passwords = serializers.BooleanField(default=True)


class ResidentImportSerializer(serializers.Serializer):
    file = serializers.FileField()
    dry_run = serializers.BooleanField(default=True)
    allow_partial = serializers.BooleanField(default=False)
    generate_passwords = serializers.BooleanField(default=True)


class DepartmentImportSerializer(serializers.Serializer):
    file = serializers.FileField()
    dry_run = serializers.BooleanField(default=True)
    allow_partial = serializers.BooleanField(default=False)


__all__ = [
    "BulkReviewSerializer",
    "BulkAssignmentSerializer",
    "BulkImportSerializer",
    "TraineeImportSerializer",
    "SupervisorImportSerializer",
    "ResidentImportSerializer",
    "DepartmentImportSerializer",
]
