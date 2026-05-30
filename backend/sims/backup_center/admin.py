from django.contrib import admin
from .models import BackupJob, RestoreJob, BackupAuditLog

@admin.register(BackupJob)
class BackupJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'backup_type', 'created_by', 'created_at', 'completed_at', 'file_size', 'database_engine')
    list_filter = ('status', 'backup_type', 'database_engine')
    search_fields = ('file_name', 'created_by__username', 'created_by__email')
    readonly_fields = ('created_at', 'completed_at')

@admin.register(RestoreJob)
class RestoreJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'backup_job', 'safety_backup', 'restored_by', 'started_at', 'completed_at')
    list_filter = ('status',)
    search_fields = ('uploaded_file_name', 'restored_by__username', 'restored_by__email')
    readonly_fields = ('started_at', 'completed_at')

@admin.register(BackupAuditLog)
class BackupAuditLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'action', 'actor', 'backup_job', 'restore_job', 'created_at')
    list_filter = ('action',)
    search_fields = ('actor__username', 'actor__email')
    readonly_fields = ('created_at',)
