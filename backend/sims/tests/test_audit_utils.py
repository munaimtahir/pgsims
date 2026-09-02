from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from sims.audit.utils import log_view, log_mutation
from sims.audit.models import ActivityLog

User = get_user_model()

class AuditUtilsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="audit_test_user")
        # Clear logs created by user creation signal
        ActivityLog.objects.all().delete()

    def test_log_view_authenticated(self):
        request = self.factory.get("/")
        request.user = self.user
        log_view(request, "viewed_home")
        
        log = ActivityLog.objects.filter(action="view").last()
        self.assertIsNotNone(log)
        self.assertEqual(log.actor, self.user)
        self.assertEqual(log.verb, "viewed_home")

    def test_log_view_anonymous(self):
        from django.contrib.auth.models import AnonymousUser
        request = self.factory.get("/")
        request.user = AnonymousUser()
        log_view(request, "viewed_public")
        
        log = ActivityLog.objects.filter(action="view").last()
        self.assertIsNotNone(log)
        self.assertIsNone(log.actor)
        self.assertEqual(log.verb, "viewed_public")

    def test_log_view_missing_request(self):
        log_view(None, "no_request")
        self.assertEqual(ActivityLog.objects.filter(action="view").count(), 0)

    def test_log_mutation_success(self):
        request = self.factory.post("/")
        request.user = self.user
        log_mutation(request, "updated_profile", metadata={"field": "email"})
        
        log = ActivityLog.objects.filter(verb="updated_profile").last()
        self.assertIsNotNone(log)
        self.assertEqual(log.actor, self.user)
        self.assertEqual(log.action, "update")
        self.assertEqual(log.metadata["field"], "email")

    def test_log_mutation_no_request(self):
        log_mutation(None, "background_job", action="create")
        
        log = ActivityLog.objects.filter(verb="background_job").last()
        self.assertIsNotNone(log)
        self.assertIsNone(log.actor)
        self.assertEqual(log.action, "create")

    def test_get_ip_handling(self):
        request = self.factory.get("/", REMOTE_ADDR="1.2.3.4")
        request.user = self.user
        log_view(request, "check_ip")
        
        log = ActivityLog.objects.filter(verb="check_ip").last()
        self.assertEqual(log.ip_address, "1.2.3.4")
        
        request.META["HTTP_X_FORWARDED_FOR"] = "5.6.7.8"
        log_view(request, "check_proxy_ip")
        log = ActivityLog.objects.filter(verb="check_proxy_ip").last()
        self.assertEqual(log.ip_address, "5.6.7.8")
