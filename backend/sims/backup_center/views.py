import os
from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import BackupJob, RestoreJob, BackupAuditLog
from .serializers import BackupJobSerializer, RestoreJobSerializer, BackupAuditLogSerializer
from .services import create_full_backup, validate_backup_file, restore_full_backup
from django.core.files.storage import FileSystemStorage
from django.utils import timezone

class BackupJobListView(generics.ListAPIView):
    queryset = BackupJob.objects.all()
    serializer_class = BackupJobSerializer
    permission_classes = [IsAdminUser]

class CreateBackupView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        notes = request.data.get('notes', '')
        try:
            job = create_full_backup(user=request.user, notes=notes)
            serializer = BackupJobSerializer(job)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadBackupView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        try:
            job = BackupJob.objects.get(pk=pk)
            if not job.file_path or not os.path.exists(job.file_path):
                raise Http404("Backup file not found")
            
            # Log the download action
            BackupAuditLog.objects.create(
                action='backup_downloaded',
                actor=request.user,
                backup_job=job,
                details_json={'ip_address': request.META.get('REMOTE_ADDR')}
            )
            
            response = FileResponse(open(job.file_path, 'rb'), as_attachment=True, filename=job.file_name)
            return response
        except BackupJob.DoesNotExist:
            raise Http404("Job not found")

class UploadBackupView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
            
        uploaded_file = request.FILES['file']
        if not uploaded_file.name.endswith('.zip'):
            return Response({'error': 'Only ZIP files are allowed'}, status=status.HTTP_400_BAD_REQUEST)
            
        backup_dir = settings.SIMS_SETTINGS.get('BACKUP_LOCATION', getattr(settings, 'BASE_DIR', '') / 'pilot_data' / 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        fs = FileSystemStorage(location=backup_dir)
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        
        return Response({'message': 'File uploaded successfully', 'file_path': file_path}, status=status.HTTP_201_CREATED)

class ValidateBackupView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        file_path = request.data.get('file_path')
        if not file_path:
            return Response({'error': 'file_path is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        result = validate_backup_file(file_path)
        return Response(result)

class ExecuteRestoreView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        file_path = request.data.get('file_path')
        password_confirmed = request.data.get('password_confirmed', False)
        typed_confirmation = request.data.get('typed_confirmation', '')
        
        if not file_path:
            return Response({'error': 'file_path is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        restore_job = RestoreJob.objects.create(
            status='running',
            file_path=file_path,
            started_by=request.user,
        )
        
        try:
            restore_full_backup(
                restore_job=restore_job,
                file_path=file_path,
                user=request.user,
                password_confirmed=password_confirmed,
                typed_confirmation=typed_confirmation
            )
            serializer = RestoreJobSerializer(restore_job)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RestoreHistoryView(generics.ListAPIView):
    queryset = RestoreJob.objects.all()
    serializer_class = RestoreJobSerializer
    permission_classes = [IsAdminUser]
