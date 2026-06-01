from django.db import models
from django.conf import settings

class BackupJob(models.Model):
    KIND_CHOICES = (
        ('routine_application_data', 'Routine Application Data'),
        ('disaster_recovery', 'Disaster Recovery'),
    )
    TYPE_CHOICES = (
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
        ('safety_pre_restore', 'Safety Pre-Restore'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('deleted', 'Deleted'),
    )

    backup_kind = models.CharField(max_length=50, choices=KIND_CHOICES, default='routine_application_data')
    backup_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='manual')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    
    file_path = models.CharField(max_length=1024, blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_size = models.BigIntegerField(blank=True, null=True)
    checksum = models.CharField(max_length=255, blank=True, null=True)
    manifest_json = models.JSONField(blank=True, null=True)
    
    database_engine = models.CharField(max_length=255, blank=True, null=True)
    media_included = models.BooleanField(default=False)
    table_counts_json = models.JSONField(blank=True, null=True)
    media_summary_json = models.JSONField(blank=True, null=True)
    
    app_version = models.CharField(max_length=50, blank=True, null=True)
    branch = models.CharField(max_length=255, blank=True, null=True)
    commit_hash = models.CharField(max_length=255, blank=True, null=True)
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_backups')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    # Cloud Storage Fields
    cloud_enabled = models.BooleanField(default=False)
    cloud_provider = models.CharField(max_length=50, blank=True, null=True)
    cloud_bucket = models.CharField(max_length=255, blank=True, null=True)
    cloud_prefix = models.CharField(max_length=255, blank=True, null=True)
    cloud_object_key = models.CharField(max_length=1024, blank=True, null=True)
    cloud_manifest_key = models.CharField(max_length=1024, blank=True, null=True)
    cloud_checksum_key = models.CharField(max_length=1024, blank=True, null=True)
    cloud_upload_status = models.CharField(max_length=50, default='not_uploaded')
    cloud_upload_started_at = models.DateTimeField(blank=True, null=True)
    cloud_upload_completed_at = models.DateTimeField(blank=True, null=True)
    cloud_download_status = models.CharField(max_length=50, default='not_uploaded')
    cloud_last_verified_at = models.DateTimeField(blank=True, null=True)
    cloud_file_size = models.BigIntegerField(blank=True, null=True)
    cloud_checksum = models.CharField(max_length=255, blank=True, null=True)
    cloud_encryption_status = models.CharField(max_length=50, default='unencrypted')
    cloud_error_message = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Backup Job'
        verbose_name_plural = 'Backup Jobs'
        app_label = 'backup_center'

    def __str__(self):
        return f"BackupJob {self.id} ({self.backup_kind}) - {self.status}"


class RestoreJob(models.Model):
    KIND_CHOICES = (
        ('routine_application_data_restore', 'Routine Application Data Restore'),
        ('disaster_recovery_restore', 'Disaster Recovery Restore'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('validation_failed', 'Validation Failed'),
        ('validation_passed', 'Validation Passed'),
        ('restoring', 'Restoring'),
        ('restored', 'Restored'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )

    restore_kind = models.CharField(max_length=50, choices=KIND_CHOICES, default='routine_application_data_restore')
    backup_job = models.ForeignKey(BackupJob, on_delete=models.SET_NULL, null=True, blank=True, related_name='restores')
    uploaded_file = models.FileField(upload_to='restore_uploads/', blank=True, null=True)
    uploaded_file_name = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    validation_result_json = models.JSONField(blank=True, null=True)
    
    safety_backup = models.ForeignKey(BackupJob, on_delete=models.SET_NULL, null=True, blank=True, related_name='safety_for_restore')
    
    restored_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='performed_restores')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    post_restore_check_json = models.JSONField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-started_at']
        verbose_name = 'Restore Job'
        verbose_name_plural = 'Restore Jobs'
        app_label = 'backup_center'

    def __str__(self):
        return f"RestoreJob {self.id} ({self.restore_kind}) - {self.status}"


class BackupAuditLog(models.Model):
    ACTION_CHOICES = (
        ('routine_backup_started', 'Routine Backup Started'),
        ('routine_backup_completed', 'Routine Backup Completed'),
        ('routine_backup_failed', 'Routine Backup Failed'),
        ('disaster_backup_started', 'Disaster Backup Started'),
        ('disaster_backup_completed', 'Disaster Backup Completed'),
        ('disaster_backup_failed', 'Disaster Backup Failed'),
        ('backup_downloaded', 'Backup Downloaded'),
        ('backup_deleted', 'Backup Deleted'),
        ('backup_validated', 'Backup Validated'),
        ('restore_uploaded', 'Restore Uploaded'),
        ('restore_validation_passed', 'Restore Validation Passed'),
        ('restore_validation_failed', 'Restore Validation Failed'),
        ('restore_started', 'Restore Started'),
        ('safety_backup_created', 'Safety Backup Created'),
        ('restore_completed', 'Restore Completed'),
        ('restore_failed', 'Restore Failed'),
        ('restore_dry_run_completed', 'Restore Dry Run Completed'),
        ('cloud_upload_started', 'Cloud Upload Started'),
        ('cloud_upload_completed', 'Cloud Upload Completed'),
        ('cloud_upload_failed', 'Cloud Upload Failed'),
        ('cloud_download_started', 'Cloud Download Started'),
        ('cloud_download_completed', 'Cloud Download Completed'),
        ('cloud_download_failed', 'Cloud Download Failed'),
        ('cloud_verified', 'Cloud Verified'),
        ('cloud_verification_failed', 'Cloud Verification Failed'),
    )

    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='backup_audit_logs')
    backup_job = models.ForeignKey(BackupJob, on_delete=models.SET_NULL, null=True, blank=True)
    restore_job = models.ForeignKey(RestoreJob, on_delete=models.SET_NULL, null=True, blank=True)
    
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=512, blank=True, null=True)
    details_json = models.JSONField(blank=True, null=True, default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Backup Audit Log'
        verbose_name_plural = 'Backup Audit Logs'
        app_label = 'backup_center'

    def __str__(self):
        return f"{self.action} by {self.actor} at {self.created_at}"

