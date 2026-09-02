from django.urls import path
from . import views

urlpatterns = [
    # Backup Jobs
    path('backups/', views.BackupJobListView.as_view(), name='backup-list'),
    path('backups/<int:pk>/', views.BackupJobDetailView.as_view(), name='backup-detail'),
    path('backups/create-routine/', views.CreateRoutineBackupView.as_view(), name='backup-create-routine'),
    path('backups/create-disaster/', views.CreateDisasterBackupView.as_view(), name='backup-create-disaster'),
    path('backups/<int:pk>/download/', views.DownloadBackupView.as_view(), name='backup-download'),
    path('backups/<int:pk>/delete/', views.DeleteBackupView.as_view(), name='backup-delete'),
    path('backups/<int:pk>/validate/', views.ValidateBackupJobView.as_view(), name='backup-validate'),
    
    # Restores
    path('restores/', views.RestoreJobListView.as_view(), name='restore-list'),
    path('restores/upload/', views.UploadRestoreFileView.as_view(), name='restore-upload'),
    path('restores/<int:pk>/validate/', views.ValidateRestoreJobView.as_view(), name='restore-validate'),
    path('restores/<int:pk>/dry-run/', views.DryRunRestoreView.as_view(), name='restore-dry-run'),
    path('restores/<int:pk>/confirm/', views.ConfirmRestoreView.as_view(), name='restore-confirm'),
    
    # Audit
    path('audit-logs/', views.BackupAuditLogListView.as_view(), name='backup-audit-logs'),

    # Google Drive Backup Connector
    path('google-drive/status/', views.GoogleDriveStatusView.as_view(), name='google-drive-status'),
    path('google-drive/connect/', views.GoogleDriveConnectView.as_view(), name='google-drive-connect'),
    path('google-drive/oauth/callback/', views.GoogleDriveOAuthCallbackView.as_view(), name='google-drive-oauth-callback'),
    path('google-drive/disconnect/', views.GoogleDriveDisconnectView.as_view(), name='google-drive-disconnect'),
    path('google-drive/health-check/', views.GoogleDriveHealthCheckView.as_view(), name='google-drive-health-check'),
    path('google-drive/create-folder/', views.GoogleDriveCreateFolderView.as_view(), name='google-drive-create-folder'),
    path('backups/<int:pk>/google-drive/upload/', views.GoogleDriveUploadBackupView.as_view(), name='google-drive-upload'),
    path('backups/<int:pk>/google-drive/verify/', views.GoogleDriveVerifyBackupView.as_view(), name='google-drive-verify'),
    path('backups/<int:pk>/google-drive/download/', views.GoogleDriveDownloadBackupView.as_view(), name='google-drive-download'),
    path('google-drive/list/', views.GoogleDriveListView.as_view(), name='google-drive-list'),
]
