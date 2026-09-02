"""Additional coverage for sims/common_permissions.py — the not_authenticated / denied
branches and permission classes that sims/tests/test_common_permissions.py doesn't touch:
CanApproveRotationOverride, ReadAnyWriteAdminOnly, ReadAnyWriteUTRMCAdmin, and the
has_object_permission denial branches of CanVerifyLogbookEntry.
"""
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APITestCase

from sims.common_permissions import (
    IsPGUser,
    CanViewPendingLogbookQueue,
    CanVerifyLogbookEntry,
    CanApproveRotationOverride,
    ReadAnyWriteAdminOnly,
    ReadAnyWriteUTRMCAdmin,
    IsTechAdmin,
    IsUTRMCAdmin,
    IsUTRMCUser,
    IsSupervisor,
    IsResident,
    IsFaculty,
)

User = get_user_model()


class MockView:
    pass


class MockEntry:
    def __init__(self, pg_id, supervisor_id=None):
        self.pg_id = pg_id
        if pg_id is not None:
            self.pg = type("obj", (object,), {"supervisor_id": supervisor_id})


class CommonPermissionsCoveragePush2Tests(APITestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.resident = User.objects.create_user(username="cp2_res", role="RESIDENT")
        self.supervisor = User.objects.create_user(username="cp2_sup", role="SUPERVISOR")
        self.other_supervisor = User.objects.create_user(username="cp2_sup2", role="SUPERVISOR")
        self.admin = User.objects.create_user(username="cp2_admin", role="ADMIN")
        self.support_staff = User.objects.create_user(username="cp2_support", role="SUPPORT_STAFF")
        self.anon = AnonymousUser()

    def _request(self, method="GET"):
        req = self.factory.get("/") if method == "GET" else self.factory.post("/")
        return req

    def test_can_view_pending_logbook_queue_anonymous_denied(self):
        req = self._request()
        req.user = self.anon
        self.assertFalse(CanViewPendingLogbookQueue().has_permission(req, MockView()))

    def test_can_view_pending_logbook_queue_role_not_allowed(self):
        req = self._request()
        req.user = self.resident
        self.assertFalse(CanViewPendingLogbookQueue().has_permission(req, MockView()))

    def test_can_verify_logbook_entry_anonymous_denied(self):
        req = self._request("POST")
        req.user = self.anon
        self.assertFalse(CanVerifyLogbookEntry().has_permission(req, MockView()))

    def test_can_verify_logbook_entry_role_not_allowed(self):
        req = self._request("POST")
        req.user = self.resident
        self.assertFalse(CanVerifyLogbookEntry().has_permission(req, MockView()))

    def test_can_verify_logbook_entry_object_permission_wrong_supervisor(self):
        perm = CanVerifyLogbookEntry()
        req = self._request("POST")
        req.user = self.other_supervisor
        entry = MockEntry(pg_id=1, supervisor_id=self.supervisor.id)
        self.assertFalse(perm.has_object_permission(req, MockView(), entry))

    def test_can_verify_logbook_entry_object_permission_resident_denied(self):
        perm = CanVerifyLogbookEntry()
        req = self._request("POST")
        req.user = self.resident
        entry = MockEntry(pg_id=1, supervisor_id=self.supervisor.id)
        self.assertFalse(perm.has_object_permission(req, MockView(), entry))

    def test_can_verify_logbook_entry_object_permission_no_pg(self):
        perm = CanVerifyLogbookEntry()
        req = self._request("POST")
        req.user = self.supervisor
        entry = MockEntry(pg_id=None)
        self.assertFalse(perm.has_object_permission(req, MockView(), entry))

    def test_can_approve_rotation_override(self):
        req = self._request()
        req.user = self.admin
        self.assertTrue(CanApproveRotationOverride().has_permission(req, MockView()))
        req.user = self.resident
        self.assertFalse(CanApproveRotationOverride().has_permission(req, MockView()))
        req.user = self.anon
        self.assertFalse(CanApproveRotationOverride().has_permission(req, MockView()))

    def test_read_any_write_admin_only(self):
        perm = ReadAnyWriteAdminOnly()
        req = self._request("GET")
        req.user = self.anon
        self.assertFalse(perm.has_permission(req, MockView()))

        req = self._request("GET")
        req.user = self.resident
        self.assertTrue(perm.has_permission(req, MockView()))

        req = self._request("POST")
        req.user = self.resident
        self.assertFalse(perm.has_permission(req, MockView()))

        req = self._request("POST")
        req.user = self.admin
        self.assertTrue(perm.has_permission(req, MockView()))

    def test_read_any_write_utrmc_admin(self):
        perm = ReadAnyWriteUTRMCAdmin()
        req = self._request("GET")
        req.user = self.anon
        self.assertFalse(perm.has_permission(req, MockView()))

        req = self._request("GET")
        req.user = self.resident
        self.assertTrue(perm.has_permission(req, MockView()))

        req = self._request("POST")
        req.user = self.resident
        self.assertFalse(perm.has_permission(req, MockView()))

        req = self._request("POST")
        req.user = self.admin
        self.assertTrue(perm.has_permission(req, MockView()))

    def test_is_tech_admin_denied_paths(self):
        req = self._request()
        req.user = self.anon
        self.assertFalse(IsTechAdmin().has_permission(req, MockView()))
        req.user = self.resident
        self.assertFalse(IsTechAdmin().has_permission(req, MockView()))

    def test_is_utrmc_admin_denied_paths(self):
        req = self._request()
        req.user = self.anon
        self.assertFalse(IsUTRMCAdmin().has_permission(req, MockView()))
        req.user = self.resident
        self.assertFalse(IsUTRMCAdmin().has_permission(req, MockView()))

    def test_is_utrmc_user_denied_paths(self):
        req = self._request()
        req.user = self.anon
        self.assertFalse(IsUTRMCUser().has_permission(req, MockView()))
        req.user = self.resident
        self.assertFalse(IsUTRMCUser().has_permission(req, MockView()))

    def test_is_supervisor_denied_paths(self):
        req = self._request()
        req.user = self.anon
        self.assertFalse(IsSupervisor().has_permission(req, MockView()))
        req.user = self.resident
        self.assertFalse(IsSupervisor().has_permission(req, MockView()))

    def test_is_resident_denied_paths(self):
        req = self._request()
        req.user = self.anon
        self.assertFalse(IsResident().has_permission(req, MockView()))
        req.user = self.supervisor
        self.assertFalse(IsResident().has_permission(req, MockView()))

    def test_is_faculty_denied_paths(self):
        req = self._request()
        req.user = self.anon
        self.assertFalse(IsFaculty().has_permission(req, MockView()))
        req.user = self.resident
        self.assertFalse(IsFaculty().has_permission(req, MockView()))

    def test_is_pg_user_support_staff_denied(self):
        req = self._request()
        req.user = self.support_staff
        self.assertFalse(IsPGUser().has_permission(req, MockView()))
