import pytest
from rest_framework.test import APIClient
from sims.users.models import User
from sims.backup_center.models import BackupJob

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def super_admin():
    return User.objects.create_user(
        username="superadmin",
        email="superadmin@example.com",
        password="password",
        role="admin",
        is_staff=True
    )

@pytest.fixture
def normal_user():
    return User.objects.create_user(
        username="normal",
        email="normal@example.com",
        password="password",
        role="resident"
    )

@pytest.mark.django_db
class TestBackupCenterViews:
    def test_list_backups_requires_auth(self, api_client):
        response = api_client.get('/api/backup_center/jobs/')
        assert response.status_code == 401

    def test_list_backups_requires_admin(self, api_client, normal_user):
        api_client.force_authenticate(user=normal_user)
        response = api_client.get('/api/backup_center/jobs/')
        assert response.status_code == 403

    def test_list_backups_success(self, api_client, super_admin):
        api_client.force_authenticate(user=super_admin)
        BackupJob.objects.create(
            created_by=super_admin,
            status='completed',
            file_name='test_backup.zip'
        )
        response = api_client.get('/api/backup_center/jobs/')
        assert response.status_code == 200
        assert response.data['count'] == 1
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['file_name'] == 'test_backup.zip'

    from unittest.mock import patch

    @patch('sims.backup_center.views.create_full_backup')
    def test_create_backup_success(self, mock_create, api_client, super_admin):
        api_client.force_authenticate(user=super_admin)
        mock_create.return_value = BackupJob.objects.create(created_by=super_admin)
        response = api_client.post('/api/backup_center/jobs/create/', {'notes': 'Test'})
        assert response.status_code in [200, 201]
        assert 'job_id' in response.data or 'id' in response.data
