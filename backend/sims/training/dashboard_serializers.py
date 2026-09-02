from rest_framework import serializers

class LogbookSummarySerializer(serializers.Serializer):
    total = serializers.IntegerField()
    draft = serializers.IntegerField()
    submitted = serializers.IntegerField()
    returned = serializers.IntegerField()
    approved = serializers.IntegerField()
    threshold = serializers.JSONField()

class DashboardReadinessSerializer(serializers.Serializer):
    logbook_threshold_met = serializers.BooleanField()
    synopsis_certificate_issued = serializers.BooleanField()
    thesis_certificate_issued = serializers.BooleanField()
    required_rotations_verified = serializers.BooleanField()
    required_rotation_count = serializers.IntegerField()
    verified_rotation_count = serializers.IntegerField()

class ResidentOperationalDashboardSerializer(serializers.Serializer):
    training_record_id = serializers.IntegerField(allow_null=True)
    logbook = LogbookSummarySerializer()
    submissions = serializers.JSONField()
    certificates = serializers.ListField(child=serializers.JSONField())
    readiness = DashboardReadinessSerializer()
    pending_actions = serializers.ListField(child=serializers.CharField())
