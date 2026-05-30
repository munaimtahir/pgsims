import os
import logging
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission

from .models import BackupJob, RestoreJob, BackupAuditLog
from .serializers import BackupJobSerializer, RestoreJobSerializer, BackupAuditLogSerializer
from .services import (
    create_routine_application_data_backup,
    create_disaster_recovery_backup,
    validate_backup_file,
    restore_routine_application_data_backup
)

logger = logging.getLogger('sims.backup_center')

class IsSuperAdmin(BasePermission):
    """Allows access only to superadmin users."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class BackupJobListView(generics.ListAPIView):
    queryset = BackupJob.objects.exclude(status='deleted')
    serializer_class = BackupJobSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

class BackupJobDetailView(generics.RetrieveAPIView):
    queryset = BackupJob.objects.all()
    serializer_class = BackupJobSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

class CreateRoutineBackupView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request):
        notes = request.data.get('notes', '')
        try:
            job = create_routine_application_data_backup(user=request.user, notes=notes)
            serializer = BackupJobSerializer(job)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateDisasterBackupView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request):
        notes = request.data.get('notes', '')
        try:
            job = create_disaster_recovery_backup(user=request.user, notes=notes)
            serializer = BackupJobSerializer(job)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadBackupView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get(self, request, pk):
        try:
            job = BackupJob.objects.get(pk=pk)
            if job.status == 'deleted':
                return Response({'error': 'Backup has been deleted'}, status=status.HTTP_410_GONE)
                
            if not job.file_path or not os.path.exists(job.file_path):
                raise Http404("Backup file not found on disk")
            
            BackupAuditLog.objects.create(
                action='backup_downloaded',
                actor=request.user,
                backup_job=job,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT')
            )
            
            return FileResponse(open(job.file_path, 'rb'), as_attachment=True, filename=job.file_name)
        except BackupJob.DoesNotExist:
            raise Http404("Job not found")

class DeleteBackupView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def delete(self, request, pk):
        try:
            job = BackupJob.objects.get(pk=pk)
            if job.file_path and os.path.exists(job.file_path):
                os.remove(job.file_path)
            
            job.status = 'deleted'
            job.save()
            
            BackupAuditLog.objects.create(
                action='backup_deleted',
                actor=request.user,
                backup_job=job,
                details_json={'file_name': job.file_name}
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BackupJob.DoesNotExist:
            raise Http404("Job not found")

class UploadRestoreFileView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
            
        uploaded_file = request.FILES['file']
        if not (uploaded_file.name.endswith('.pgsimsbak') or uploaded_file.name.endswith('.pgsimsdr')):
            return Response({'error': 'Invalid file extension. Expected .pgsimsbak or .pgsimsdr'}, status=status.HTTP_400_BAD_REQUEST)
            
        backup_dir = Path(settings.SIMS_SETTINGS.get('BACKUP_LOCATION', settings.BASE_DIR / 'backups'))
        restore_tmp_dir = backup_dir / 'restore_tmp'
        restore_tmp_dir.mkdir(parents=True, exist_ok=True)
        
        fs = FileSystemStorage(location=str(restore_tmp_dir))
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        
        restore_job = RestoreJob.objects.create(
            uploaded_file=filename,
            uploaded_file_name=uploaded_file.name,
            status='pending',
            restored_by=request.user
        )
        
        # We store the absolute path in notes or a custom field if we had one, 
        # but for now we'll just return the job info.
        # Actually, RestoreJob.uploaded_file already handles the path relative to storage root.
        
        BackupAuditLog.objects.create(
            action='restore_uploaded',
            actor=request.user,
            restore_job=restore_job,
            details_json={'file_name': uploaded_file.name}
        )
        
        serializer = RestoreJobSerializer(restore_job)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ValidateRestoreJobView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request, pk):
        try:
            restore_job = RestoreJob.objects.get(pk=pk)
            file_path = restore_job.uploaded_file.path
            
            result = validate_backup_file(file_path)
            restore_job.validation_result_json = result
            if result['valid']:
                restore_job.status = 'validation_passed'
            else:
                restore_job.status = 'validation_failed'
                restore_job.error_message = str(result['errors'])
            
            restore_job.save()
            
            BackupAuditLog.objects.create(
                action='backup_validated',
                actor=request.user,
                restore_job=restore_job,
                details_json=result
            )
            
            return Response(result)
        except RestoreJob.DoesNotExist:
            raise Http404("Restore job not found")

class DryRunRestoreView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request, pk):
        try:
            restore_job = RestoreJob.objects.get(pk=pk)
            file_path = restore_job.uploaded_file.path
            
            job = restore_routine_application_data_backup(
                file_path=file_path,
                restored_by=request.user,
                dry_run=True
            )
            
            serializer = RestoreJobSerializer(job)
            return Response(serializer.data)
        except RestoreJob.DoesNotExist:
            raise Http404("Restore job not found")
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ConfirmRestoreView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request, pk):
        password = request.data.get('password')
        typed_confirmation = request.data.get('typed_confirmation')
        
        if not password or not typed_confirmation:
            return Response({'error': 'Password and typed confirmation required'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Verify password
        user = authenticate(username=request.user.username, password=password)
        if not user:
            return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
            
        try:
            restore_job = RestoreJob.objects.get(pk=pk)
            file_path = restore_job.uploaded_file.path
            
            restore_routine_application_data_backup(
                file_path=file_path,
                restored_by=request.user,
                password_confirmed=True,
                typed_confirmation=typed_confirmation,
                dry_run=False
            )
            
            serializer = RestoreJobSerializer(restore_job)
            return Response(serializer.data)
        except RestoreJob.DoesNotExist:
            raise Http404("Restore job not found")
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RestoreJobListView(generics.ListAPIView):
    queryset = RestoreJob.objects.all()
    serializer_class = RestoreJobSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

class BackupAuditLogListView(generics.ListAPIView):
    queryset = BackupAuditLog.objects.all()
    serializer_class = BackupAuditLogSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
