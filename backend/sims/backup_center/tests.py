import os
import pytest
import zipfile
import json
from unittest.mock import patch, MagicMock
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from sims.backup_center.models import BackupJob, RestoreJob, BackupAuditLog
from sims.backup_center.services import (
    create_routine_application_data_backup,
    validate_backup_file,
    create_disaster_recovery_backup,
    detect_database_engine
)

User = get_user_model()

@pytest.fixture
def super_admin(db):
    return User.objects.create_superuser(
        username="superadmin",
        email="superadmin@example.com",
        password="password123",
        role="admin"
    )

@pytest.fixture
def api_client(super_admin):
    client = APIClient()
    client.force_authenticate(user=super_admin)
    return client

@pytest.mark.django_db
class TestBackupCenterServices:
    
    @patch('sims.backup_center.services.subprocess.check_output')
    @patch('sims.backup_center.services.subprocess.run')
    def test_create_routine_backup(self, mock_run, mock_check, super_admin, tmp_path):
        # Setup mocks
        mock_run.return_value = MagicMock(returncode=0)
        mock_check.side_effect = ["test-branch", "test-commit"]

        
        # Override settings for test
        with patch('sims.backup_center.services.settings.BASE_DIR', tmp_path):
            with patch('sims.backup_center.services.settings.MEDIA_ROOT', tmp_path / 'media'):
                (tmp_path / 'media').mkdir()
                (tmp_path / 'media' / 'test.txt').write_text('test')
                
                job = create_routine_application_data_backup(user=super_admin, notes="Test backup")
                
                assert job.backup_kind == 'routine_application_data'
                assert job.status == 'completed'
                assert job.file_name.endswith('.pgsimsbak')
                assert os.path.exists(job.file_path)
                
                # Check ZIP content
                with zipfile.ZipFile(job.file_path, 'r') as zipf:
                    namelist = zipf.namelist()
                    assert 'manifest.json' in namelist
                    assert 'database_dump.sql' in namelist
                    assert 'checksum.sha256' in namelist
                    assert 'media/test.txt' in namelist
                    
                    manifest = json.loads(zipf.read('manifest.json'))
                    assert manifest['app_name'] == 'PGSIMS'
                    assert manifest['media_included'] is True
                    assert 'academics.department' in manifest['table_counts']

    def test_validate_backup_invalid(self, tmp_path):
        fake_backup = tmp_path / "fake.pgsimsbak"
        fake_backup.write_text("not a zip")
        
        result = validate_backup_file(str(fake_backup))
        assert result['valid'] is False
        assert "is not a valid ZIP archive" in result['errors'][0]

    @patch('sims.backup_center.services.create_routine_application_data_backup')
    def test_create_disaster_backup(self, mock_routine, super_admin, tmp_path):
        # Setup mock routine backup
        routine_path = tmp_path / "routine.pgsimsbak"
        with zipfile.ZipFile(routine_path, 'w') as zipf:
            zipf.writestr('dummy.txt', 'dummy')
        
        mock_routine.return_value = MagicMock(
            file_path=str(routine_path),
            file_name="routine.pgsimsbak"
        )
        
        with patch('sims.backup_center.services.settings.BASE_DIR', tmp_path):
            job = create_disaster_recovery_backup(user=super_admin, notes="Disaster test")
            
            assert job.backup_kind == 'disaster_recovery'
            assert job.status == 'completed'
            assert job.file_name.endswith('.pgsimsdr')
            
            with zipfile.ZipFile(job.file_path, 'r') as zipf:
                namelist = zipf.namelist()
                assert 'deployment_metadata.json' in namelist
                assert 'env.template' in namelist
                assert 'restore_instructions.md' in namelist
                assert 'routine.pgsimsbak' in namelist

@pytest.mark.django_db
class TestBackupCenterViews:
    
    def test_list_backups(self, api_client, super_admin):
        BackupJob.objects.create(created_by=super_admin, status='completed', file_name='test.pgsimsbak')
        url = reverse('backup-list')
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data['results']) == 1

    @patch('sims.backup_center.views.create_routine_application_data_backup')
    def test_create_routine_backup_api(self, mock_create, api_client, super_admin):
        mock_create.return_value = BackupJob.objects.create(created_by=super_admin, status='completed')
        url = reverse('backup-create-routine')
        response = api_client.post(url, {'notes': 'API test'})
        assert response.status_code == 201
        assert mock_create.called

    def test_delete_backup_api(self, api_client, super_admin, tmp_path):
        fake_file = tmp_path / "delete_me.pgsimsbak"
        fake_file.write_text("content")
        job = BackupJob.objects.create(created_by=super_admin, status='completed', file_path=str(fake_file))
        
        url = reverse('backup-delete', kwargs={'pk': job.id})
        response = api_client.delete(url)
        assert response.status_code == 204
        
        job.refresh_from_db()
        assert job.status == 'deleted'
        assert not fake_file.exists()

    @patch('sims.backup_center.views.validate_backup_file')
    def test_validate_restore_api(self, mock_val, api_client, super_admin, tmp_path):
        # Create a dummy restore job
        fake_file = tmp_path / "restore.pgsimsbak"
        fake_file.write_text("zip content")
        
        # We need a real file for the model to work if it uses FileField.path
        # but here we can mock it or use a simple file.
        from django.core.files.uploadedfile import SimpleUploadedFile
        restore_job = RestoreJob.objects.create(
            uploaded_file=SimpleUploadedFile("restore.pgsimsbak", b"content"),
            restored_by=super_admin
        )
        
        mock_val.return_value = {'valid': True, 'backup_kind': 'routine_application_data'}
        
        url = reverse('restore-validate', kwargs={'pk': restore_job.id})
        response = api_client.post(url)
        assert response.status_code == 200
        assert response.data['valid'] is True
        
        restore_job.refresh_from_db()
        assert restore_job.status == 'validation_passed'
