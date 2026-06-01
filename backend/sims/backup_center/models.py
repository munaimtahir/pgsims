from django.db import models
from django.conf import settings
from django.utils import timezone

from .encryption import decrypt_string, encrypt_string

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


class BackupCloudConnection(models.Model):
    PROVIDER_CHOICES = (
        ("google_drive", "Google Drive"),
    )

    STATUS_CHOICES = (
        ("not_connected", "Not Connected"),
        ("connected", "Connected"),
        ("disconnected", "Disconnected"),
        ("failed", "Failed"),
    )

    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES, unique=True)
    connected_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="backup_cloud_connections",
    )
    account_email = models.EmailField(blank=True, null=True)

    access_token_encrypted = models.TextField(blank=True, null=True)
    refresh_token_encrypted = models.TextField(blank=True, null=True)
    token_expiry = models.DateTimeField(blank=True, null=True)
    scopes = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="not_connected")
    backup_folder_id = models.CharField(max_length=255, blank=True, null=True)
    backup_folder_name = models.CharField(max_length=255, blank=True, null=True)

    last_health_check_at = models.DateTimeField(blank=True, null=True)
    last_error = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Backup Cloud Connection"
        verbose_name_plural = "Backup Cloud Connections"
        app_label = "backup_center"

    def __str__(self):
        return f"{self.provider} ({self.status})"

    def set_tokens(self, *, access_token: str, refresh_token: str | None, token_expiry, scopes: str | None):
        self.access_token_encrypted = encrypt_string(access_token)
        if refresh_token:
            self.refresh_token_encrypted = encrypt_string(refresh_token)
        self.token_expiry = token_expiry
        self.scopes = scopes

    def get_access_token(self) -> str:
        if not self.access_token_encrypted:
            raise ValueError("Access token is not stored")
        return decrypt_string(self.access_token_encrypted)

    def get_refresh_token(self) -> str:
        if not self.refresh_token_encrypted:
            raise ValueError("Refresh token is not stored")
        return decrypt_string(self.refresh_token_encrypted)

    def is_token_expired(self) -> bool:
        if not self.token_expiry:
            return True
        return self.token_expiry <= timezone.now()


class BackupCloudCopy(models.Model):
    PROVIDER_CHOICES = (
        ("google_drive", "Google Drive"),
    )

    STATUS_CHOICES = (
        ("not_uploaded", "Not Uploaded"),
        ("uploading", "Uploading"),
        ("uploaded", "Uploaded"),
        ("upload_failed", "Upload Failed"),
        ("verifying", "Verifying"),
        ("verified", "Verified"),
        ("verification_failed", "Verification Failed"),
        ("downloading", "Downloading"),
        ("downloaded", "Downloaded"),
        ("download_failed", "Download Failed"),
        ("restore_ready", "Restore Ready"),
    )

    backup_record = models.ForeignKey(BackupJob, on_delete=models.CASCADE, related_name="cloud_copies")
    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES)
    connection = models.ForeignKey(BackupCloudConnection, on_delete=models.CASCADE, related_name="copies")

    remote_file_id = models.CharField(max_length=255, blank=True, null=True)
    remote_manifest_file_id = models.CharField(max_length=255, blank=True, null=True)
    remote_checksum_file_id = models.CharField(max_length=255, blank=True, null=True)
    remote_folder_id = models.CharField(max_length=255, blank=True, null=True)

    remote_file_name = models.CharField(max_length=255, blank=True, null=True)
    remote_size = models.BigIntegerField(blank=True, null=True)

    local_checksum = models.CharField(max_length=255, blank=True, null=True)
    remote_checksum = models.CharField(max_length=255, blank=True, null=True)

    upload_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="not_uploaded")
    verification_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="not_uploaded")
    download_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="not_uploaded")

    uploaded_at = models.DateTimeField(blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    downloaded_at = models.DateTimeField(blank=True, null=True)

    error_message = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Backup Cloud Copy"
        verbose_name_plural = "Backup Cloud Copies"
        app_label = "backup_center"

    def __str__(self):
        return f"CloudCopy {self.id} ({self.provider}) - {self.upload_status}"


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
        ('google_drive_connected', 'Google Drive Connected'),
        ('google_drive_disconnected', 'Google Drive Disconnected'),
        ('google_drive_health_check', 'Google Drive Health Check'),
        ('google_drive_folder_ready', 'Google Drive Folder Ready'),
        ('google_drive_upload_completed', 'Google Drive Upload Completed'),
        ('google_drive_upload_failed', 'Google Drive Upload Failed'),
        ('google_drive_verified', 'Google Drive Verified'),
        ('google_drive_verification_failed', 'Google Drive Verification Failed'),
        ('google_drive_download_completed', 'Google Drive Download Completed'),
        ('google_drive_download_failed', 'Google Drive Download Failed'),
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
