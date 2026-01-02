from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from sims.tests.factories.user_factories import AdminFactory, PGFactory, SupervisorFactory

from .forms import (
    BulkCertificateApprovalForm,
    CertificateCreateForm,
    CertificateReviewForm,
    QuickCertificateUploadForm,
)
from .models import Certificate, CertificateReview, CertificateStatistics, CertificateType

User = get_user_model()


class CertificateTypeModelTests(TestCase):
    """
    Test cases for the CertificateType model.

    Created: 2025-05-29 17:03:46 UTC
    Author: SMIB2012
    """

    def test_certificate_type_creation(self):
        """Test basic certificate type creation"""
        cert_type = CertificateType.objects.create(
            name="Basic Life Support",
            category="safety",
            description="Basic life support certification",
            is_required=True,
            validity_period_months=24,
            cme_points=10,
        )

        self.assertEqual(cert_type.name, "Basic Life Support")
        self.assertEqual(cert_type.category, "safety")
        self.assertTrue(cert_type.is_required)
        self.assertEqual(cert_type.validity_period_months, 24)
        self.assertTrue(cert_type.is_active)

    def test_certificate_type_string_representation(self):
        """Test the __str__ method"""
        cert_type = CertificateType.objects.create(
            name="Advanced Cardiac Life Support", category="safety"
        )
        expected = "Advanced Cardiac Life Support (Safety & Compliance)"
        self.assertEqual(str(cert_type), expected)

    def test_certificate_type_counts(self):
        """Test certificate count methods"""
        cert_type = CertificateType.objects.create(name="Test Certificate", category="cme")

        # Initially no certificates
        self.assertEqual(cert_type.get_active_certificates_count(), 0)
        self.assertEqual(cert_type.get_pending_certificates_count(), 0)


class CertificateModelTests(TestCase):
    """Test cases for the Certificate model"""

    def setUp(self):
        """Set up test data"""
        # Create certificate type
        self.cert_type = CertificateType.objects.create(
            name="Basic Life Support", category="safety", validity_period_months=24, cme_points=10
        )

        # Create test users
        self.admin_user = User.objects.create_user(
            username="admin_test",
            email="admin@test.com",
            password="testpass123",
            role="admin",
            first_name="Admin",
            last_name="User",
        )

        self.supervisor = SupervisorFactory(username="supervisor_test", specialty="medicine")
        self.pg = PGFactory(supervisor=self.supervisor, specialty="medicine", year="1")

        self.pg_user = User.objects.create_user(
            username="pg_test",
            email="pg@test.com",
            password="testpass123",
            role="pg",
            specialty="medicine",
            year="1",
            supervisor=self.supervisor,
        )

        # Create test file
        self.test_file = SimpleUploadedFile(
            "test_certificate.pdf", b"fake pdf content", content_type="application/pdf"
        )

    def test_certificate_creation(self):
        """Test basic certificate creation"""
        certificate = Certificate.objects.create(
            pg=self.pg_user,
            certificate_type=self.cert_type,
            title="Basic Life Support Certification",
            issuing_organization="American Heart Association",
            issue_date=date.today(),
            certificate_file=self.test_file,
            created_by=self.admin_user,
        )

        self.assertEqual(certificate.pg, self.pg_user)
        self.assertEqual(certificate.certificate_type, self.cert_type)
        self.assertEqual(certificate.status, "pending")
        self.assertFalse(certificate.is_verified)

    def test_certificate_string_representation(self):
        """Test the __str__ method"""
        certificate = Certificate.objects.create(
            pg=self.pg_user,
            certificate_type=self.cert_type,
            title="Test Certificate",
            issuing_organization="Test Org",
            issue_date=date.today(),
            certificate_file=self.test_file,
        )

        expected = f"Test Certificate - {self.pg_user.get_full_name()}"
        self.assertEqual(str(certificate), expected)

    def test_certificate_expiry_validation(self):
        """Test certificate expiry date validation"""
        # Test invalid expiry date (before issue date)
        certificate = Certificate(
            pg=self.pg_user,
            certificate_type=self.cert_type,
            title="Test Certificate",
            issuing_organization="Test Org",
            issue_date=date.today(),
            expiry_date=date.today() - timedelta(days=1),  # Before issue date
            certificate_file=self.test_file,
        )

        with self.assertRaises(ValidationError):
            certificate.full_clean()

    def test_certificate_automatic_expiry_setting(self):
        """Test automatic expiry date setting from certificate type"""
        certificate = Certificate.objects.create(
            pg=self.pg_user,
            certificate_type=self.cert_type,
            title="Test Certificate",
            issuing_organization="Test Org",
            issue_date=date.today(),
            certificate_file=self.test_file,
        )

        # Should automatically set expiry date based on certificate type
        expected_expiry = date.today() + timedelta(days=24 * 30)  # 24 months
        self.assertEqual(certificate.expiry_date, expected_expiry)

    def test_certificate_expiry_methods(self):
        """Test expiry checking methods"""
        # Create expired certificate
        expired_cert = Certificate.objects.create(
            pg=self.pg_user,
            certificate_type=self.cert_type,
            title="Expired Certificate",
            issuing_organization="Test Org",
            issue_date=date.today() - timedelta(days=100),
            expiry_date=date.today() - timedelta(days=1),
            certificate_file=self.test_file,
        )

        self.assertTrue(expired_cert.is_expired())
        self.assertEqual(expired_cert.get_days_until_expiry(), 0)
        self.assertEqual(expired_cert.get_validity_status(), "Expired")

        # Create certificate expiring soon
        expiring_cert = Certificate.objects.create(
            pg=self.pg_user,
            certificate_type=self.cert_type,
            title="Expiring Certificate",
            issuing_organization="Test Org",
            issue_date=date.today() - timedelta(days=50),
            expiry_date=date.today() + timedelta(days=15),
            certificate_file=self.test_file,
        )

        self.assertFalse(expiring_cert.is_expired())
        self.assertTrue(expiring_cert.is_expiring_soon())
        self.assertEqual(expiring_cert.get_days_until_expiry(), 15)

    def test_certificate_permissions(self):
        """Test certificate permission methods"""
        # Pending certificate can be edited
        pending_cert = Certificate.objects.create(
            pg=self.pg_user,
            certificate_type=self.cert_type,
            title="Pending Certificate",
            issuing_organization="Test Org",
            issue_date=date.today(),
            certificate_file=self.test_file,
            status="pending",
        )

        self.assertTrue(pending_cert.can_be_edited())
        self.assertTrue(pending_cert.can_be_deleted())

        # Approved certificate cannot be edited/deleted
        approved_cert = Certificate.objects.create(
            pg=self.pg_user,
            certificate_type=self.cert_type,
            title="Approved Certificate",
            issuing_organization="Test Org",
            issue_date=date.today(),
            certificate_file=self.test_file,
            status="approved",
        )

        self.assertFalse(approved_cert.can_be_edited())
        self.assertFalse(approved_cert.can_be_deleted())

    def test_certificate_cme_cpd_auto_setting(self):
        """Test automatic CME/CPD points setting from certificate type"""
        certificate = Certificate.objects.create(
            pg=self.pg_user,
            certificate_type=self.cert_type,
            title="Test Certificate",
            issuing_organization="Test Org",
            issue_date=date.today(),
            certificate_file=self.test_file,
        )

        # Should automatically set CME points from certificate type
        self.assertEqual(certificate.cme_points_earned, self.cert_type.cme_points)


class CertificateReviewModelTests(TestCase):
    """Test cases for the CertificateReview model"""

    def setUp(self):
        """Set up test data"""
        self.cert_type = CertificateType.objects.create(
            name="Test Certificate Type", category="cme"
        )

        self.supervisor = SupervisorFactory(username="supervisor_test", specialty="medicine")
        self.pg = PGFactory(supervisor=self.supervisor, specialty="medicine", year="1")

        self.pg_user = User.objects.create_user(
            username="pg_test",
            email="pg@test.com",
            password="testpass123",
            role="pg",
            specialty="medicine",
            year="1",
            supervisor=self.supervisor,
        )

        self.test_file = SimpleUploadedFile(
            "test.pdf", b"fake content", content_type="application/pdf"
        )

        self.certificate = Certificate.objects.create(
            pg=self.pg_user,
            certificate_type=self.cert_type,
            title="Test Certificate",
            issuing_organization="Test Org",
            issue_date=date.today(),
            certificate_file=self.test_file,
            status="pending",
        )

    def test_certificate_review_creation(self):
        """Test basic review creation"""
        review = CertificateReview.objects.create(
            certificate=self.certificate,
            reviewer=self.supervisor,
            status="approved",
            comments="Certificate looks good",
        )

        self.assertEqual(review.certificate, self.certificate)
        self.assertEqual(review.reviewer, self.supervisor)
        self.assertEqual(review.status, "approved")

    def test_review_updates_certificate_status(self):
        """Test that review status updates certificate status"""
        # Create approval review
        _review = CertificateReview.objects.create(
            certificate=self.certificate,
            reviewer=self.supervisor,
            status="approved",
            comments="Approved",
        )

        # Certificate should be updated to approved
        self.certificate.refresh_from_db()
        self.assertEqual(self.certificate.status, "approved")
        self.assertEqual(self.certificate.verified_by, self.supervisor)
        self.assertIsNotNone(self.certificate.verified_at)

    def test_review_validation(self):
        """Test review validation rules"""
        # Test that PG cannot review certificates
        invalid_review = CertificateReview(
            certificate=self.certificate,
            reviewer=self.pg_user,  # PG trying to review
            status="approved",
        )

        with self.assertRaises(ValidationError):
            invalid_review.full_clean()

    def test_review_status_colors(self):
        """Test review status color methods"""
        review = CertificateReview.objects.create(
            certificate=self.certificate,
            reviewer=self.supervisor,
            status="approved",
            comments="Good",
        )

        color = review.get_status_color()
        self.assertEqual(color, "#28a745")  # Green for approved

        review.status = "rejected"
        review.save()
        color = review.get_status_color()
        self.assertEqual(color, "#dc3545")  # Red for rejected


class CertificateStatisticsModelTests(TestCase):
    """Test cases for the CertificateStatistics model"""

    def setUp(self):
        self.supervisor = SupervisorFactory(specialty="medicine")
        self.pg = PGFactory(supervisor=self.supervisor, specialty="medicine", year="1")
        """Set up test data"""
        self.cert_type = CertificateType.objects.create(
            name="Required Certificate", category="safety", is_required=True
        )

        self.pg_user = User.objects.create_user(
            username="pg_test", email="pg@test.com", password="testpass123", role="pg"
        )

        self.test_file = SimpleUploadedFile("test.pdf", b"content", content_type="application/pdf")

    def test_statistics_creation_and_update(self):
        """Test statistics creation and update"""
        # Create statistics object
        stats = CertificateStatistics.objects.create(pg=self.pg_user)

        # Initially should be zero
        self.assertEqual(stats.total_certificates, 0)
        self.assertEqual(stats.approved_certificates, 0)

        # Create certificates
        Certificate.objects.create(
            pg=self.pg_user,
            certificate_type=self.cert_type,
            title="Test Cert 1",
            issuing_organization="Test Org",
            issue_date=date.today(),
            certificate_file=self.test_file,
            status="approved",
        )

        Certificate.objects.create(
            pg=self.pg_user,
            certificate_type=self.cert_type,
            title="Test Cert 2",
            issuing_organization="Test Org",
            issue_date=date.today(),
            certificate_file=self.test_file,
            status="pending",
        )

        # Update statistics
        stats.update_statistics()

        self.assertEqual(stats.total_certificates, 2)
        self.assertEqual(stats.approved_certificates, 1)
        self.assertEqual(stats.pending_certificates, 1)
        self.assertEqual(stats.compliance_rate, 100.0)  # Has required certificate


class CertificateViewTests(TestCase):
    """Test cases for certificate views"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()

        # Create certificate type
        self.cert_type = CertificateType.objects.create(name="Test Certificate", category="cme")

        # Create test users
        self.admin_user = User.objects.create_user(
            username="admin_test", email="admin@test.com", password="testpass123", role="admin"
        )

        self.supervisor = SupervisorFactory(username="supervisor_test", specialty="medicine")
        self.pg = PGFactory(supervisor=self.supervisor, specialty="medicine", year="1")

        self.pg_user = User.objects.create_user(
            username="pg_test",
            email="pg@test.com",
            password="testpass123",
            role="pg",
            specialty="medicine",
            year="1",
            supervisor=self.supervisor,
        )

        # Create test file
        self.test_file = SimpleUploadedFile(
            "test_certificate.pdf", b"fake pdf content", content_type="application/pdf"
        )

        # Create test certificate
        self.certificate = Certificate.objects.create(
            pg=self.pg_user,
            certificate_type=self.cert_type,
            title="Test Certificate",
            issuing_organization="Test Organization",
            issue_date=date.today(),
            certificate_file=self.test_file,
            status="pending",
            created_by=self.admin_user,
        )

    def test_certificate_list_view_access(self):
        """Test access to certificate list view"""
        # Unauthenticated access should redirect
        response = self.client.get(reverse("certificates:list"))
        self.assertEqual(response.status_code, 302)

        # Authenticated access should work
        self.client.login(username="admin_test", password="testpass123")
        response = self.client.get(reverse("certificates:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Certificates")

    def test_certificate_detail_view(self):
        """Test certificate detail view"""
        self.client.login(username="admin_test", password="testpass123")
        response = self.client.get(
            reverse("certificates:detail", kwargs={"pk": self.certificate.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.certificate.title)

    def test_certificate_create_view_permissions(self):
        """Test certificate creation permissions"""
        # All authenticated users should be able to create certificates
        self.client.login(username="pg_test", password="testpass123")
        response = self.client.get(reverse("certificates:create"))
        self.assertEqual(response.status_code, 200)

        # Admin users should also be able to create certificates
        self.client.login(username="admin_test", password="testpass123")
        response = self.client.get(reverse("certificates:create"))
        self.assertEqual(response.status_code, 200)

    def test_certificate_dashboard_view(self):
        """Test certificate dashboard view"""
        self.client.login(username="admin_test", password="testpass123")
        response = self.client.get(reverse("certificates:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard")

    def test_certificate_review_permissions(self):
        """Test certificate review permissions"""
        # PG users should not be able to review certificates
        self.client.login(username="pg_test", password="testpass123")
        response = self.client.get(
            reverse("certificates:review", kwargs={"certificate_pk": self.certificate.pk})
        )
        self.assertEqual(response.status_code, 403)

        # Supervisors should be able to review their PGs' certificates
        self.client.login(username="supervisor_test", password="testpass123")
        response = self.client.get(
            reverse("certificates:review", kwargs={"certificate_pk": self.certificate.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_role_based_certificate_filtering(self):
        """Test that users only see certificates they have permission to view"""
        # Create another PG with different supervisor
        other_supervisor = User.objects.create_user(
            username="other_supervisor",
            email="other@test.com",
            password="testpass123",
            role="supervisor",
            specialty="medicine",
        )

        other_pg = User.objects.create_user(
            username="other_pg",
            email="otherpg@test.com",
            password="testpass123",
            role="pg",
            specialty="medicine",
            year="1",
            supervisor=other_supervisor,
        )

        other_certificate = Certificate.objects.create(
            pg=other_pg,
            certificate_type=self.cert_type,
            title="Other Certificate",
            issuing_organization="Other Org",
            issue_date=date.today(),
            certificate_file=self.test_file,
        )

        # Supervisor should only see their PG's certificates
        self.client.login(username="supervisor_test", password="testpass123")
        response = self.client.get(reverse("certificates:list"))
        self.assertContains(response, self.certificate.title)
        self.assertNotContains(response, other_certificate.title)

        # PG should only see their own certificates
        self.client.login(username="pg_test", password="testpass123")
        response = self.client.get(reverse("certificates:list"))
        self.assertContains(response, self.certificate.title)
        self.assertNotContains(response, other_certificate.title)


class CertificateFormTests(TestCase):
    """Test cases for certificate forms"""

    def setUp(self):
        """Set up test data"""
        self.cert_type = CertificateType.objects.create(
            name="Test Certificate", category="cme", cme_points=10
        )

        self.admin_user = User.objects.create_user(
            username="admin_test", email="admin@test.com", password="testpass123", role="admin"
        )

        self.supervisor = SupervisorFactory(username="supervisor_test", specialty="medicine")
        self.pg = PGFactory(supervisor=self.supervisor, specialty="medicine", year="1")

        self.pg_user = User.objects.create_user(
            username="pg_test",
            email="pg@test.com",
            password="testpass123",
            role="pg",
            specialty="medicine",
            year="1",
            supervisor=self.supervisor,
        )

        self.test_file = SimpleUploadedFile(
            "test_certificate.pdf", b"fake pdf content", content_type="application/pdf"
        )

    def test_certificate_create_form_valid_data(self):
        """Test certificate creation form with valid data"""
        form_data = {
            "pg": self.pg_user.id,
            "certificate_type": self.cert_type.id,
            "title": "Test Certificate Title",
            "issuing_organization": "Test Organization",
            "issue_date": date.today(),
            "description": "Test description",
            "cme_points_earned": 10,
        }

        form = CertificateCreateForm(
            data=form_data, files={"certificate_file": self.test_file}, user=self.admin_user
        )
        self.assertTrue(form.is_valid())

    def test_certificate_create_form_invalid_dates(self):
        """Test certificate creation form with invalid dates"""
        form_data = {
            "pg": self.pg_user.id,
            "certificate_type": self.cert_type.id,
            "title": "Test Certificate",
            "issuing_organization": "Test Org",
            "issue_date": date.today() + timedelta(days=1),  # Future date
            "expiry_date": date.today(),
        }

        form = CertificateCreateForm(
            data=form_data, files={"certificate_file": self.test_file}, user=self.admin_user
        )
        self.assertFalse(form.is_valid())
        self.assertIn("Issue date cannot be in the future", str(form.errors))

    def test_certificate_review_form_valid_data(self):
        """Test certificate review form with valid data"""
        certificate = Certificate.objects.create(
            pg=self.pg_user,
            certificate_type=self.cert_type,
            title="Test Certificate",
            issuing_organization="Test Org",
            issue_date=date.today(),
            certificate_file=self.test_file,
            status="pending",
        )

        form_data = {
            "status": "approved",
            "comments": "Certificate looks authentic and valid",
            "recommendations": "Continue professional development",
            "review_date": date.today(),
        }

        form = CertificateReviewForm(data=form_data, certificate=certificate, user=self.supervisor)
        self.assertTrue(form.is_valid())

    def test_certificate_review_form_rejection_validation(self):
        """Test that rejection requires detailed comments"""
        certificate = Certificate.objects.create(
            pg=self.pg_user,
            certificate_type=self.cert_type,
            title="Test Certificate",
            issuing_organization="Test Org",
            issue_date=date.today(),
            certificate_file=self.test_file,
            status="pending",
        )

        form_data = {
            "status": "rejected",
            "comments": "No",  # Too short
            "review_date": date.today(),
        }

        form = CertificateReviewForm(data=form_data, certificate=certificate, user=self.supervisor)
        self.assertFalse(form.is_valid())
        self.assertIn("Detailed comments are required", str(form.errors))

    def test_bulk_approval_form(self):
        """Test bulk certificate approval form"""
        certificate1 = Certificate.objects.create(
            pg=self.pg_user,
            certificate_type=self.cert_type,
            title="Certificate 1",
            issuing_organization="Test Org",
            issue_date=date.today(),
            certificate_file=self.test_file,
            status="pending",
        )

        certificate2 = Certificate.objects.create(
            pg=self.pg_user,
            certificate_type=self.cert_type,
            title="Certificate 2",
            issuing_organization="Test Org",
            issue_date=date.today(),
            certificate_file=self.test_file,
            status="pending",
        )

        form_data = {
            "certificates": [certificate1.id, certificate2.id],
            "action": "approve",
            "bulk_comments": "Bulk approval test",
        }

        form = BulkCertificateApprovalForm(data=form_data, user=self.admin_user)
        self.assertTrue(form.is_valid())

    def test_quick_upload_form(self):
        """Test quick certificate upload form"""
        form_data = {
            "title": "Quick Upload Test",
            "certificate_type": self.cert_type.id,
            "issuing_organization": "Quick Org",
            "issue_date": date.today(),
        }

        form = QuickCertificateUploadForm(
            data=form_data, files={"certificate_file": self.test_file}, user=self.pg_user
        )
        self.assertTrue(form.is_valid())

    def test_file_validation(self):
        """Test file upload validation"""
        # Test invalid file type
        invalid_file = SimpleUploadedFile("test.txt", b"text content", content_type="text/plain")

        form_data = {
            "title": "Test Certificate",
            "certificate_type": self.cert_type.id,
            "issuing_organization": "Test Org",
            "issue_date": date.today(),
        }

        form = QuickCertificateUploadForm(
            data=form_data, files={"certificate_file": invalid_file}, user=self.pg_user
        )
        self.assertFalse(form.is_valid())
        self.assertIn("File type .txt not allowed", str(form.errors))


class CertificateAPITests(TestCase):
    """Test cases for certificate API endpoints"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()

        self.cert_type = CertificateType.objects.create(name="API Test Certificate", category="cme")

        self.admin_user = AdminFactory()
        self.supervisor = SupervisorFactory(specialty="medicine")
        self.pg_user = PGFactory(supervisor=self.supervisor, specialty="medicine", year="1")

        self.test_file = SimpleUploadedFile("test.pdf", b"content", content_type="application/pdf")

        self.certificate = Certificate.objects.create(
            pg=self.pg_user,
            certificate_type=self.cert_type,
            title="API Test Certificate",
            issuing_organization="Test Org",
            issue_date=date.today(),
            certificate_file=self.test_file,
            status="pending",
        )

    def test_certificate_stats_api(self):
        """Test certificate statistics API"""
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse("certificates:stats_api"))
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("total", data)
        self.assertIn("by_status", data)
        self.assertIn("by_type", data)
        self.assertEqual(data["total"], 1)

    def test_quick_stats_api(self):
        """Test quick statistics API"""
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse("certificates:quick_stats_api"))
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("pending", data)
        self.assertIn("approved", data)
        self.assertEqual(data["pending"], 1)

    def test_certificate_verification_api(self):
        """Test certificate verification API"""
        self.client.force_login(self.admin_user)
        response = self.client.post(
            reverse("certificates:verify_api", kwargs={"pk": self.certificate.pk})
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertTrue(data["success"])

        # Check that certificate was actually verified
        self.certificate.refresh_from_db()
        self.assertTrue(self.certificate.is_verified)
        self.assertEqual(self.certificate.verified_by, self.admin_user)

    def test_unauthorized_api_access(self):
        """Test that unauthorized users cannot access APIs"""
        # Test without login
        response = self.client.get(reverse("certificates:stats_api"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

        # Test with PG user trying to verify certificate
        self.client.force_login(self.pg_user)
        response = self.client.post(
            reverse("certificates:verify_api", kwargs={"pk": self.certificate.pk})
        )
        self.assertEqual(response.status_code, 403)


class CertificateExportTests(TestCase):
    """Test cases for certificate export functionality"""

    def setUp(self):
        self.supervisor = SupervisorFactory(specialty="medicine")
        self.pg = PGFactory(supervisor=self.supervisor, specialty="medicine", year="1")
        """Set up test data"""
        self.client = Client()

        self.cert_type = CertificateType.objects.create(
            name="Export Test Certificate", category="cme"
        )

        self.admin_user = User.objects.create_user(
            username="admin_test", email="admin@test.com", password="testpass123", role="admin"
        )

        self.pg_user = User.objects.create_user(
            username="pg_test", email="pg@test.com", password="testpass123", role="pg"
        )

        self.test_file = SimpleUploadedFile("test.pdf", b"content", content_type="application/pdf")

        # Create test certificate
        self.certificate = Certificate.objects.create(
            pg=self.pg_user,
            certificate_type=self.cert_type,
            title="Export Test Certificate",
            issuing_organization="Test Organization",
            issue_date=date.today(),
            certificate_file=self.test_file,
            status="approved",
            created_by=self.admin_user,
        )

    def test_csv_export(self):
        """Test CSV export functionality"""
        self.client.login(username="admin_test", password="testpass123")
        response = self.client.get(reverse("certificates:export_csv"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn("attachment", response["Content-Disposition"])

        # Check if certificate data is in the CSV
        content = response.content.decode("utf-8")
        self.assertIn(self.certificate.title, content)
        self.assertIn(self.pg_user.get_full_name(), content)

    def test_file_download(self):
        """Test certificate file download"""
        self.client.login(username="admin_test", password="testpass123")
        response = self.client.get(
            reverse("certificates:download", kwargs={"pk": self.certificate.pk})
        )

        self.assertEqual(response.status_code, 200)
        # Should be a file response


class CertificateIntegrationTests(TestCase):
    """Integration tests for certificate workflows"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()

        self.cert_type = CertificateType.objects.create(
            name="Integration Test Certificate", category="cme", cme_points=15
        )

        self.admin_user = User.objects.create_user(
            username="admin_test", email="admin@test.com", password="testpass123", role="admin"
        )

        self.supervisor = SupervisorFactory(username="supervisor_test", specialty="medicine")
        self.pg = PGFactory(supervisor=self.supervisor, specialty="medicine", year="1")

        self.pg_user = User.objects.create_user(
            username="pg_test",
            email="pg@test.com",
            password="testpass123",
            role="pg",
            specialty="medicine",
            year="1",
            supervisor=self.supervisor,
        )

    def test_complete_certificate_workflow(self):
        """Test the complete certificate workflow from upload to approval"""
        # 1. PG uploads certificate
        self.client.login(username="pg_test", password="testpass123")

        test_file = SimpleUploadedFile(
            "workflow_test.pdf", b"fake pdf content", content_type="application/pdf"
        )

        certificate_data = {
            "certificate_type": self.cert_type.id,
            "title": "Integration Test Certificate",
            "issuing_organization": "Test Organization",
            "issue_date": date.today(),
            "description": "Test certificate for integration workflow",
            "cme_points_earned": 15,
            "certificate_file": test_file,
        }

        response = self.client.post(reverse("certificates:create"), data=certificate_data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation

        # Check that certificate was created
        certificate = Certificate.objects.get(pg=self.pg_user)
        self.assertEqual(certificate.title, "Integration Test Certificate")
        self.assertEqual(certificate.status, "pending")

        # 2. View certificate details
        response = self.client.get(reverse("certificates:detail", kwargs={"pk": certificate.pk}))
        self.assertEqual(response.status_code, 200)

        # 3. Login as supervisor and review certificate
        self.client.login(username="supervisor_test", password="testpass123")

        review_data = {
            "status": "approved",
            "comments": "Certificate looks authentic and meets requirements",
            "recommendations": "Continue pursuing professional development",
            "review_date": date.today(),
        }

        response = self.client.post(
            reverse("certificates:review", kwargs={"certificate_pk": certificate.pk}),
            data=review_data,
        )
        self.assertEqual(response.status_code, 302)  # Redirect after review

        # Check that certificate was approved
        certificate.refresh_from_db()
        self.assertEqual(certificate.status, "approved")
        self.assertEqual(certificate.verified_by, self.supervisor)
        self.assertIsNotNone(certificate.verified_at)

        # Check that review was created
        review = CertificateReview.objects.get(certificate=certificate)
        self.assertEqual(review.status, "approved")
        self.assertEqual(review.reviewer, self.supervisor)

        # 4. Verify statistics are updated
        stats, created = CertificateStatistics.objects.get_or_create(pg=self.pg_user)
        stats.update_statistics()

        self.assertEqual(stats.total_certificates, 1)
        self.assertEqual(stats.approved_certificates, 1)
        self.assertEqual(stats.total_cme_points, 15)

    def test_certificate_rejection_workflow(self):
        """Test certificate rejection and resubmission workflow"""
        # Create pending certificate
        test_file = SimpleUploadedFile(
            "rejection_test.pdf", b"content", content_type="application/pdf"
        )

        certificate = Certificate.objects.create(
            pg=self.pg_user,
            certificate_type=self.cert_type,
            title="Rejection Test Certificate",
            issuing_organization="Test Org",
            issue_date=date.today(),
            certificate_file=test_file,
            status="pending",
        )

        # 1. Supervisor rejects certificate
        self.client.login(username="supervisor_test", password="testpass123")

        review_data = {
            "status": "rejected",
            "comments": "Certificate image is unclear and organization name is missing",
            "required_changes": "Please upload a clearer image and verify organization details",
            "review_date": date.today(),
        }

        response = self.client.post(
            reverse("certificates:review", kwargs={"certificate_pk": certificate.pk}),
            data=review_data,
        )
        self.assertEqual(response.status_code, 302)

        # Check certificate status
        certificate.refresh_from_db()
        self.assertEqual(certificate.status, "rejected")

        # 2. PG edits certificate (should be allowed for rejected certificates)
        self.client.login(username="pg_test", password="testpass123")

        response = self.client.get(reverse("certificates:edit", kwargs={"pk": certificate.pk}))
        self.assertEqual(response.status_code, 200)

        # Update certificate
        updated_data = {
            "certificate_type": self.cert_type.id,
            "title": "Updated Rejection Test Certificate",
            "issuing_organization": "Verified Test Organization",
            "issue_date": date.today(),
            "description": "Updated description with more details",
            "cme_points_earned": 15,
        }

        response = self.client.post(
            reverse("certificates:edit", kwargs={"pk": certificate.pk}), data=updated_data
        )
        # Should redirect back to certificate detail
        self.assertEqual(response.status_code, 302)

        # Check that certificate status reset to pending
        certificate.refresh_from_db()
        self.assertEqual(certificate.status, "pending")
        self.assertEqual(certificate.title, "Updated Rejection Test Certificate")
