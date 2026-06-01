import os
import logging
import tempfile
from pathlib import Path
from urllib.parse import quote

from django.conf import settings
from django.core.files import File
from django.http import FileResponse, Http404
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    BackupJob,
    RestoreJob,
    BackupAuditLog,
    BackupCloudConnection,
    BackupCloudCopy,
)
from .serializers import BackupJobSerializer, RestoreJobSerializer, BackupAuditLogSerializer
from .services import (
    create_routine_application_data_backup,
    create_disaster_recovery_backup,
    validate_backup_file,
    restore_routine_application_data_backup
)
from .google_drive import GoogleDriveBackupProvider

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

class ValidateBackupJobView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request, pk):
        try:
            job = BackupJob.objects.get(pk=pk)
            if job.status == 'deleted':
                return Response({'error': 'Backup has been deleted'}, status=status.HTTP_410_GONE)
            if not job.file_path or not os.path.exists(job.file_path):
                raise Http404("Backup file not found on disk")

            result = validate_backup_file(job.file_path)
            BackupAuditLog.objects.create(
                action='backup_validated',
                actor=request.user,
                backup_job=job,
                details_json=result,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT'),
            )
            return Response(result)
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

        restore_job = RestoreJob.objects.create(
            uploaded_file_name=uploaded_file.name,
            status='pending',
            restored_by=request.user,
        )
        # Use the model FileField to persist into MEDIA_ROOT/restore_uploads/
        restore_job.uploaded_file.save(uploaded_file.name, uploaded_file, save=True)
        
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
                dry_run=True,
                restore_job=restore_job,
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
            
            job = restore_routine_application_data_backup(
                file_path=file_path,
                restored_by=request.user,
                password_confirmed=True,
                typed_confirmation=typed_confirmation,
                dry_run=False,
                restore_job=restore_job,
            )
            
            serializer = RestoreJobSerializer(job)
            return Response(serializer.data)
        except RestoreJob.DoesNotExist:
            raise Http404("Restore job not found")
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GoogleDriveStatusView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get(self, request):
        connection = BackupCloudConnection.objects.filter(provider="google_drive").first()
        if not connection:
            return Response(
                {
                    "enabled": GoogleDriveBackupProvider().config.enabled,
                    "status": "not_connected",
                    "connected_account": None,
                    "backup_folder": None,
                    "last_health_check_at": None,
                    "last_error": None,
                }
            )
        return Response(
            {
                "enabled": GoogleDriveBackupProvider().config.enabled,
                "status": connection.status,
                "connected_account": connection.account_email,
                "backup_folder": {
                    "id": connection.backup_folder_id,
                    "name": connection.backup_folder_name,
                }
                if connection.backup_folder_id or connection.backup_folder_name
                else None,
                "token_expiry": connection.token_expiry,
                "last_health_check_at": connection.last_health_check_at,
                "last_error": connection.last_error,
                "updated_at": connection.updated_at,
            }
        )


class GoogleDriveConnectView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get(self, request):
        try:
            provider = GoogleDriveBackupProvider()
            authorization_url = provider.build_authorization_url(user_id=request.user.id)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # For browser-navigation flows, callers can ask for a redirect explicitly.
        if request.query_params.get("redirect") in ("1", "true", "yes"):
            return redirect(authorization_url)
        return Response({"authorization_url": authorization_url})


class GoogleDriveOAuthCallbackView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        error = request.query_params.get("error")
        if error:
            return redirect(f"/dashboard/utrmc/backup?googleDrive=error&reason={quote(str(error))}")

        code = request.query_params.get("code")
        state = request.query_params.get("state")
        if not code or not state:
            return redirect("/dashboard/utrmc/backup?googleDrive=error&reason=missing_code_or_state")

        provider = GoogleDriveBackupProvider()
        try:
            connection = provider.handle_oauth_callback(code=code, state=state)
            BackupAuditLog.objects.create(
                action="google_drive_connected",
                actor_id=connection.connected_by_user_id,
                details_json={"account_email": connection.account_email},
            )
            return redirect("/dashboard/utrmc/backup?googleDrive=connected")
        except Exception as e:
            logger.exception(f"Google Drive OAuth callback failed: {e}")
            connection = BackupCloudConnection.objects.filter(provider="google_drive").first()
            if connection:
                connection.status = "failed"
                connection.last_error = str(e)
                connection.save(update_fields=["status", "last_error", "updated_at"])
            return redirect("/dashboard/utrmc/backup?googleDrive=error&reason=oauth_failed")


class GoogleDriveDisconnectView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request):
        connection = BackupCloudConnection.objects.filter(provider="google_drive").first()
        if not connection:
            return Response({"status": "not_connected"})

        connection.status = "disconnected"
        connection.access_token_encrypted = None
        connection.refresh_token_encrypted = None
        connection.token_expiry = None
        connection.account_email = None
        connection.last_error = None
        connection.last_health_check_at = timezone.now()
        connection.save()

        BackupAuditLog.objects.create(
            action="google_drive_disconnected",
            actor=request.user,
            details_json={"provider": "google_drive"},
        )
        return Response({"status": "disconnected"})


class GoogleDriveHealthCheckView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request):
        connection = BackupCloudConnection.objects.filter(provider="google_drive").first()
        if not connection or connection.status != "connected":
            return Response({"error": "Google Drive is not connected"}, status=status.HTTP_400_BAD_REQUEST)
        provider = GoogleDriveBackupProvider()
        try:
            result = provider.health_check(connection)
            BackupAuditLog.objects.create(
                action="google_drive_health_check",
                actor=request.user,
                details_json=result,
            )
            return Response(result)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GoogleDriveCreateFolderView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request):
        connection = BackupCloudConnection.objects.filter(provider="google_drive").first()
        if not connection or connection.status != "connected":
            return Response({"error": "Google Drive is not connected"}, status=status.HTTP_400_BAD_REQUEST)
        provider = GoogleDriveBackupProvider()
        try:
            connection = provider.ensure_backup_folder(connection)
            BackupAuditLog.objects.create(
                action="google_drive_folder_ready",
                actor=request.user,
                details_json={"folder_id": connection.backup_folder_id, "folder_name": connection.backup_folder_name},
            )
            return Response(
                {
                    "status": "ready",
                    "backup_folder": {"id": connection.backup_folder_id, "name": connection.backup_folder_name},
                }
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GoogleDriveUploadBackupView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request, pk):
        try:
            backup_job = BackupJob.objects.get(pk=pk)
        except BackupJob.DoesNotExist:
            raise Http404("Backup job not found")

        provider = GoogleDriveBackupProvider()
        try:
            cloud_copy = provider.upload_backup(backup_record=backup_job)
            BackupAuditLog.objects.create(
                action="google_drive_upload_completed",
                actor=request.user,
                backup_job=backup_job,
                details_json={"cloud_copy_id": cloud_copy.id, "remote_file_id": cloud_copy.remote_file_id},
            )
            return Response({"status": "uploaded", "cloud_copy_id": cloud_copy.id})
        except Exception as e:
            BackupAuditLog.objects.create(
                action="google_drive_upload_failed",
                actor=request.user,
                backup_job=backup_job,
                details_json={"error": str(e)},
            )
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GoogleDriveVerifyBackupView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request, pk):
        try:
            backup_job = BackupJob.objects.get(pk=pk)
        except BackupJob.DoesNotExist:
            raise Http404("Backup job not found")

        cloud_copy = (
            BackupCloudCopy.objects.filter(backup_record=backup_job, provider="google_drive")
            .exclude(remote_file_id__isnull=True)
            .order_by("-created_at")
            .first()
        )
        if not cloud_copy:
            return Response({"error": "No Google Drive cloud copy found"}, status=status.HTTP_404_NOT_FOUND)

        provider = GoogleDriveBackupProvider()
        try:
            cloud_copy.verification_status = "verifying"
            cloud_copy.save(update_fields=["verification_status", "updated_at"])
            provider.verify_uploaded_file(
                connection=cloud_copy.connection,
                drive_file_id=cloud_copy.remote_file_id,
                expected_size=cloud_copy.remote_size,
                expected_md5=cloud_copy.remote_checksum,
            )
            cloud_copy.verification_status = "verified"
            cloud_copy.verified_at = timezone.now()
            cloud_copy.save(update_fields=["verification_status", "verified_at", "updated_at"])
            BackupAuditLog.objects.create(
                action="google_drive_verified",
                actor=request.user,
                backup_job=backup_job,
                details_json={"cloud_copy_id": cloud_copy.id},
            )
            return Response({"status": "verified", "cloud_copy_id": cloud_copy.id})
        except Exception as e:
            cloud_copy.verification_status = "verification_failed"
            cloud_copy.error_message = str(e)
            cloud_copy.save(update_fields=["verification_status", "error_message", "updated_at"])
            BackupAuditLog.objects.create(
                action="google_drive_verification_failed",
                actor=request.user,
                backup_job=backup_job,
                details_json={"error": str(e), "cloud_copy_id": cloud_copy.id},
            )
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GoogleDriveDownloadBackupView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request, pk):
        try:
            backup_job = BackupJob.objects.get(pk=pk)
        except BackupJob.DoesNotExist:
            raise Http404("Backup job not found")

        cloud_copy = (
            BackupCloudCopy.objects.filter(backup_record=backup_job, provider="google_drive", verification_status="verified")
            .exclude(remote_file_id__isnull=True)
            .order_by("-verified_at", "-created_at")
            .first()
        )
        if not cloud_copy:
            return Response({"error": "No verified Google Drive cloud copy found"}, status=status.HTTP_404_NOT_FOUND)

        provider = GoogleDriveBackupProvider()
        tmp_dir = tempfile.mkdtemp(prefix="pgsims-drive-restore-")
        local_restore_name = backup_job.file_name or f"backup-{backup_job.id}.pgsimsbak"
        tmp_out_path = os.path.join(tmp_dir, local_restore_name)
        try:
            provider.download_backup(cloud_copy=cloud_copy, destination_path=tmp_out_path)

            restore_job = RestoreJob.objects.create(
                uploaded_file_name=local_restore_name,
                status="pending",
                restored_by=request.user,
            )
            with open(tmp_out_path, "rb") as f:
                restore_job.uploaded_file.save(local_restore_name, File(f), save=True)

            cloud_copy.download_status = "restore_ready"
            cloud_copy.save(update_fields=["download_status", "updated_at"])

            BackupAuditLog.objects.create(
                action="google_drive_download_completed",
                actor=request.user,
                backup_job=backup_job,
                restore_job=restore_job,
                details_json={"cloud_copy_id": cloud_copy.id, "restore_job_id": restore_job.id},
            )
            return Response({"status": "restore_ready", "restore_job_id": restore_job.id, "cloud_copy_id": cloud_copy.id})
        except Exception as e:
            BackupAuditLog.objects.create(
                action="google_drive_download_failed",
                actor=request.user,
                backup_job=backup_job,
                details_json={"error": str(e), "cloud_copy_id": cloud_copy.id},
            )
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            try:
                if os.path.exists(tmp_out_path):
                    os.remove(tmp_out_path)
                if os.path.exists(tmp_dir):
                    os.rmdir(tmp_dir)
            except Exception:
                pass


class GoogleDriveListView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get(self, request):
        copies = BackupCloudCopy.objects.filter(provider="google_drive").order_by("-created_at")[:50]
        data = [
            {
                "id": c.id,
                "backup_record_id": c.backup_record_id,
                "remote_file_id": c.remote_file_id,
                "remote_file_name": c.remote_file_name,
                "remote_size": c.remote_size,
                "upload_status": c.upload_status,
                "verification_status": c.verification_status,
                "download_status": c.download_status,
                "uploaded_at": c.uploaded_at,
                "verified_at": c.verified_at,
                "downloaded_at": c.downloaded_at,
                "error_message": c.error_message,
            }
            for c in copies
        ]
        return Response({"results": data})

class RestoreJobListView(generics.ListAPIView):
    queryset = RestoreJob.objects.all()
    serializer_class = RestoreJobSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

class BackupAuditLogListView(generics.ListAPIView):
    queryset = BackupAuditLog.objects.all()
    serializer_class = BackupAuditLogSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
