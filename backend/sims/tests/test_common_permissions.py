from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APITestCase
from sims.common_permissions import (
    IsPGUser, IsUTRMCAdminUser, CanViewPendingLogbookQueue,
    CanVerifyLogbookEntry, ReadAnyWriteAdminOrUTRMCAdmin,
    IsTechAdmin, IsUTRMCAdmin, IsUTRMCUser, IsSupervisor,
    IsResident, IsFaculty
)

User = get_user_model()

class MockView:
    pass

class CommonPermissionsTests(APITestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.pg = User.objects.create_user(username="pg", role="pg")
        self.resident = User.objects.create_user(username="res", role="resident")
        self.supervisor = User.objects.create_user(username="sup", role="supervisor")
        self.admin = User.objects.create_user(username="admin", role="admin")
        self.utrmc_admin = User.objects.create_user(username="uadmin", role="utrmc_admin")
        self.utrmc_user = User.objects.create_user(username="uuser", role="utrmc_user")
        self.faculty = User.objects.create_user(username="faculty", role="faculty")
        self.anon = AnonymousUser()

    def _check(self, perm_class, user, method="GET"):
        request = self.factory.get("/") if method == "GET" else self.factory.post("/")
        request.user = user
        return perm_class().has_permission(request, MockView())

    def test_is_pg_user(self):
        self.assertTrue(self._check(IsPGUser, self.pg))
        self.assertTrue(self._check(IsPGUser, self.resident))
        self.assertFalse(self._check(IsPGUser, self.supervisor))
        self.assertFalse(self._check(IsPGUser, self.anon))

    def test_is_utrmc_admin_user(self):
        self.assertTrue(self._check(IsUTRMCAdminUser, self.utrmc_admin))
        self.assertFalse(self._check(IsUTRMCAdminUser, self.admin))

    def test_can_view_pending_logbook_queue(self):
        self.assertTrue(self._check(CanViewPendingLogbookQueue, self.supervisor))
        self.assertTrue(self._check(CanViewPendingLogbookQueue, self.admin))
        self.assertTrue(self._check(CanViewPendingLogbookQueue, self.utrmc_user))
        self.assertFalse(self._check(CanViewPendingLogbookQueue, self.pg))

    def test_read_any_write_admin_or_utrmc_admin(self):
        self.assertTrue(self._check(ReadAnyWriteAdminOrUTRMCAdmin, self.resident, "GET"))
        self.assertTrue(self._check(ReadAnyWriteAdminOrUTRMCAdmin, self.admin, "POST"))
        self.assertTrue(self._check(ReadAnyWriteAdminOrUTRMCAdmin, self.utrmc_admin, "POST"))
        self.assertFalse(self._check(ReadAnyWriteAdminOrUTRMCAdmin, self.resident, "POST"))

    def test_is_tech_admin(self):
        self.assertTrue(self._check(IsTechAdmin, self.admin))
        self.assertFalse(self._check(IsTechAdmin, self.utrmc_admin))

    def test_is_utrmc_admin(self):
        self.assertTrue(self._check(IsUTRMCAdmin, self.utrmc_admin))
        self.assertFalse(self._check(IsUTRMCAdmin, self.admin))

    def test_is_utrmc_user(self):
        self.assertTrue(self._check(IsUTRMCUser, self.utrmc_user))
        self.assertFalse(self._check(IsUTRMCUser, self.utrmc_admin))

    def test_is_supervisor(self):
        self.assertTrue(self._check(IsSupervisor, self.supervisor))
        self.assertFalse(self._check(IsSupervisor, self.faculty))

    def test_is_resident(self):
        self.assertTrue(self._check(IsResident, self.resident))
        self.assertTrue(self._check(IsResident, self.pg))
        self.assertFalse(self._check(IsResident, self.supervisor))

    def test_is_faculty(self):
        self.assertTrue(self._check(IsFaculty, self.faculty))
        self.assertFalse(self._check(IsFaculty, self.supervisor))

    def test_can_verify_logbook_entry(self):
        from sims.training.models import LogbookEntry
        # Create a mock entry
        class MockEntry:
            def __init__(self, pg_id, supervisor_id):
                self.pg_id = pg_id
                self.pg = type('obj', (object,), {'supervisor_id': supervisor_id})

        entry = MockEntry(self.pg.id, self.supervisor.id)
        
        perm = CanVerifyLogbookEntry()
        request = self.factory.post("/")
        
        request.user = self.supervisor
        self.assertTrue(perm.has_object_permission(request, MockView(), entry))
        
        request.user = self.faculty
        self.assertFalse(perm.has_object_permission(request, MockView(), entry))
        
        request.user = self.admin
        self.assertTrue(perm.has_object_permission(request, MockView(), entry))
