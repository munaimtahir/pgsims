from django.urls import path
from . import views

app_name = 'backup_center'

urlpatterns = [
    path('jobs/', views.BackupJobListView.as_view(), name='backup-list'),
    path('jobs/create/', views.CreateBackupView.as_view(), name='backup-create'),
    path('jobs/<int:pk>/download/', views.DownloadBackupView.as_view(), name='backup-download'),
    
    path('restore/validate/', views.ValidateBackupView.as_view(), name='restore-validate'),
    path('restore/upload/', views.UploadBackupView.as_view(), name='restore-upload'),
    path('restore/execute/', views.ExecuteRestoreView.as_view(), name='restore-execute'),
    path('restore/history/', views.RestoreHistoryView.as_view(), name='restore-history'),
]
