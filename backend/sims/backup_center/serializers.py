from rest_framework import serializers
from .models import BackupJob, RestoreJob, BackupAuditLog

class BackupJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupJob
        fields = '__all__'

class RestoreJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestoreJob
        fields = '__all__'

class BackupAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupAuditLog
        fields = '__all__'
