from django.contrib import admin
from .models import BackupJob, RestoreJob, BackupAuditLog, BackupCloudConnection, BackupCloudCopy

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


@admin.register(BackupCloudConnection)
class BackupCloudConnectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'provider', 'status', 'account_email', 'backup_folder_name', 'updated_at')
    list_filter = ('provider', 'status')
    search_fields = ('account_email',)
    readonly_fields = ('created_at', 'updated_at', 'token_expiry', 'last_health_check_at', 'last_error')


@admin.register(BackupCloudCopy)
class BackupCloudCopyAdmin(admin.ModelAdmin):
    list_display = ('id', 'provider', 'backup_record', 'upload_status', 'verification_status', 'download_status', 'created_at')
    list_filter = ('provider', 'upload_status', 'verification_status', 'download_status')
    search_fields = ('remote_file_id', 'remote_file_name')
    readonly_fields = ('created_at', 'updated_at', 'uploaded_at', 'verified_at', 'downloaded_at', 'error_message')
