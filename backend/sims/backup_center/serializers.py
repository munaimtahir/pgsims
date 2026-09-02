from rest_framework import serializers
from .models import BackupJob, RestoreJob, BackupAuditLog

class BackupJobSerializer(serializers.ModelSerializer):
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = BackupJob
        fields = '__all__'

class RestoreJobSerializer(serializers.ModelSerializer):
    restored_by_username = serializers.ReadOnlyField(source='restored_by.username')
    
    class Meta:
        model = RestoreJob
        fields = '__all__'

class BackupAuditLogSerializer(serializers.ModelSerializer):
    actor_username = serializers.ReadOnlyField(source='actor.username')
    
    class Meta:
        model = BackupAuditLog
        fields = '__all__'
