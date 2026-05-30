from django.db import models
from django.conf import settings

class BackupJob(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )

    backup_type = models.CharField(max_length=50, default='full')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    file_path = models.CharField(max_length=1024, blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_size = models.BigIntegerField(blank=True, null=True)
    checksum = models.CharField(max_length=255, blank=True, null=True)
    manifest_json = models.JSONField(blank=True, null=True)
    database_engine = models.CharField(max_length=255, blank=True, null=True)
    media_included = models.BooleanField(default=False)
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_backups')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Backup Job'
        verbose_name_plural = 'Backup Jobs'
        app_label = 'backup_center'

    def __str__(self):
        return f"BackupJob {self.id} - {self.status}"


class RestoreJob(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('validation_failed', 'Validation Failed'),
        ('validation_passed', 'Validation Passed'),
        ('restoring', 'Restoring'),
        ('restored', 'Restored'),
        ('failed', 'Failed'),
    )

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

    class Meta:
        ordering = ['-started_at']
        verbose_name = 'Restore Job'
        verbose_name_plural = 'Restore Jobs'
        app_label = 'backup_center'

    def __str__(self):
        return f"RestoreJob {self.id} - {self.status}"


class BackupAuditLog(models.Model):
    ACTION_CHOICES = (
        ('backup_created', 'Backup Created'),
        ('backup_failed', 'Backup Failed'),
        ('backup_downloaded', 'Backup Downloaded'),
        ('backup_deleted', 'Backup Deleted'),
        ('backup_validated', 'Backup Validated'),
        ('restore_uploaded', 'Restore Uploaded'),
        ('restore_validation_failed', 'Restore Validation Failed'),
        ('restore_started', 'Restore Started'),
        ('safety_backup_created', 'Safety Backup Created'),
        ('restore_completed', 'Restore Completed'),
        ('restore_failed', 'Restore Failed'),
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
