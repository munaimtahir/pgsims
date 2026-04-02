"""Phase 6 tests — Academic program engine, research workflow, workshop, eligibility."""
import json
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment
from sims.training.models import (
    TrainingProgram,
    ProgramPolicy,
    ProgramMilestone,
    ProgramMilestoneResearchRequirement,
    ProgramMilestoneWorkshopRequirement,
    ResidentTrainingRecord,
    ResidentResearchProject,
    ResidentThesis,
    Workshop,
    ResidentWorkshopCompletion,
    ResidentMilestoneEligibility,
)
from sims.training.eligibility import compute_milestone_eligibility, recompute_for_record

User = get_user_model()


# ---------------------------------------------------------------------------
# Fixtures helper
# ---------------------------------------------------------------------------

def _make_supervisor(username="supervisor_default"):
    """Create a supervisor user (needed as FK for pg users)."""
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return User.objects.create_user(
            username=username,
            password="Test1234!",
            role="supervisor",
            email=f"{username}@test.com",
            specialty="urology",
        )


def _make_user(username, role, **kwargs):
    if role == "pg":
        kwargs.setdefault("specialty", "urology")
        kwargs.setdefault("year", "1")
        if "supervisor" not in kwargs:
            kwargs["supervisor"] = _make_supervisor(f"sup_{username}")
    elif role == "supervisor":
        kwargs.setdefault("specialty", "urology")
    user = User.objects.create_user(
        username=username,
        password="Test1234!",
        role=role,
        email=f"{username}@test.com",
        **kwargs,
    )
    return user


def _make_program(code="FCPS-URO", department=None):
    if department is None:
        department, _ = Department.objects.get_or_create(
            code="URO", defaults={"name": "Urology"}
        )
    prog, _ = TrainingProgram.objects.get_or_create(
        code=code,
        defaults={
            "name": f"Program {code}",
            "duration_months": 60,
            "degree_type": TrainingProgram.DEGREE_FCPS,
            "department": department,
        },
    )
    return prog


def _make_rtr(pg_user, program=None):
    if program is None:
        program = _make_program()
    rtr, _ = ResidentTrainingRecord.objects.get_or_create(
        resident_user=pg_user,
        program=program,
        defaults={"start_date": date.today() - timedelta(days=365), "active": True},
    )
    return rtr


# ---------------------------------------------------------------------------
# Model constraint tests
# ---------------------------------------------------------------------------

class TrainingProgramModelTests(APITestCase):
    def setUp(self):
        self.dept, _ = Department.objects.get_or_create(
            code="MED", defaults={"name": "Medicine"}
        )

    def test_degree_type_field_exists(self):
        prog = TrainingProgram.objects.create(
            code="MD-MED-TEST",
            name="MD Medicine Test",
            duration_months=48,
            degree_type=TrainingProgram.DEGREE_MD,
            department=self.dept,
        )
        self.assertEqual(prog.degree_type, "MD")
        self.assertEqual(prog.is_active, True)

    def test_notes_field(self):
        prog = TrainingProgram.objects.create(
            code="MS-SURG-TEST",
            name="MS Surgery Test",
            duration_months=36,
            degree_type=TrainingProgram.DEGREE_MS,
            notes="Some notes here",
        )
        self.assertEqual(prog.notes, "Some notes here")


class ResidentTrainingRecordConstraintTests(APITestCase):
    def setUp(self):
        self.pg = _make_user("pg_constraint", "pg")
        self.program = _make_program("FCPS-CONST")

    def test_unique_active_program_per_resident(self):
        ResidentTrainingRecord.objects.create(
            resident_user=self.pg,
            program=self.program,
            start_date=date.today(),
            active=True,
        )
        from django.db import IntegrityError
        with self.assertRaises(Exception):
            ResidentTrainingRecord.objects.create(
                resident_user=self.pg,
                program=self.program,
                start_date=date.today(),
                active=True,
            )

    def test_lock_fields_exist(self):
        rtr = _make_rtr(self.pg, self.program)
        self.assertTrue(rtr.locked_program)
        self.assertTrue(rtr.restart_from_scratch_on_change)
        self.assertEqual(rtr.status, ResidentTrainingRecord.STATUS_ACTIVE)

    def test_current_month_index_computed(self):
        rtr = _make_rtr(self.pg, self.program)
        rtr.start_date = date.today() - timedelta(days=90)
        rtr.save()
        idx = rtr.current_month_index()
        self.assertGreaterEqual(idx, 2)


# ---------------------------------------------------------------------------
# Research workflow transition tests
# ---------------------------------------------------------------------------

class ResearchProjectTransitionTests(APITestCase):
    def setUp(self):
        self.pg = _make_user("pg_research", "pg")
        self.supervisor = _make_user("sup_research", "supervisor")
        self.admin = _make_user("admin_research", "admin")
        self.rtr = _make_rtr(self.pg)

    def test_create_draft(self):
        proj = ResidentResearchProject.objects.create(
            resident_training_record=self.rtr,
            title="Impact of X on Y",
            topic_area="Nephrology",
            supervisor=self.supervisor,
        )
        self.assertEqual(proj.status, ResidentResearchProject.STATUS_DRAFT)

    def test_valid_transition_draft_to_submitted(self):
        proj = ResidentResearchProject.objects.create(
            resident_training_record=self.rtr,
            title="Research Title",
            supervisor=self.supervisor,
        )
        proj.transition_to(ResidentResearchProject.STATUS_SUBMITTED_SUPERVISOR)
        self.assertEqual(proj.status, ResidentResearchProject.STATUS_SUBMITTED_SUPERVISOR)
        self.assertIsNotNone(proj.submitted_to_supervisor_at)

    def test_invalid_transition_raises(self):
        proj = ResidentResearchProject.objects.create(
            resident_training_record=self.rtr,
            title="Research Title",
            supervisor=self.supervisor,
        )
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            proj.transition_to(ResidentResearchProject.STATUS_ACCEPTED_UNIVERSITY)

    def test_full_flow(self):
        proj = ResidentResearchProject.objects.create(
            resident_training_record=self.rtr,
            title="Full Flow",
            supervisor=self.supervisor,
        )
        proj.transition_to(ResidentResearchProject.STATUS_SUBMITTED_SUPERVISOR)
        proj.transition_to(ResidentResearchProject.STATUS_APPROVED_SUPERVISOR)
        self.assertIsNotNone(proj.synopsis_approved_at)
        proj.transition_to(ResidentResearchProject.STATUS_SUBMITTED_UNIVERSITY)
        proj.transition_to(ResidentResearchProject.STATUS_ACCEPTED_UNIVERSITY)
        self.assertEqual(proj.status, ResidentResearchProject.STATUS_ACCEPTED_UNIVERSITY)
        self.assertIsNotNone(proj.accepted_at)


# ---------------------------------------------------------------------------
# Eligibility computation tests
# ---------------------------------------------------------------------------

class EligibilityComputationTests(APITestCase):
    def setUp(self):
        self.pg = _make_user("pg_elig", "pg")
        self.supervisor = _make_user("sup_elig", "supervisor")
        self.program = _make_program("FCPS-ELIG")
        self.rtr = _make_rtr(self.pg, self.program)

        # Milestone
        self.milestone = ProgramMilestone.objects.create(
            program=self.program,
            code=ProgramMilestone.CODE_IMM,
            name="Intermediate Membership",
            is_active=True,
        )
        # Research requirement: synopsis must be approved
        self.research_req = ProgramMilestoneResearchRequirement.objects.create(
            milestone=self.milestone,
            requires_synopsis_approved=True,
            requires_synopsis_submitted_to_university=False,
            requires_thesis_submitted=False,
        )

        # Workshop requirement
        self.workshop = Workshop.objects.create(
            name="Basic Life Support",
            code="BLS-TEST",
        )
        self.workshop_req = ProgramMilestoneWorkshopRequirement.objects.create(
            milestone=self.milestone,
            workshop=self.workshop,
            required_count=1,
        )

    def _compute(self):
        return compute_milestone_eligibility(self.rtr, self.milestone)

    def test_not_ready_when_no_research_or_workshops(self):
        result = self._compute()
        self.assertEqual(result["status"], ResidentMilestoneEligibility.STATUS_NOT_READY)
        self.assertGreater(len(result["reasons"]), 0)
        self.assertTrue(any("Synopsis" in r for r in result["reasons"]))
        self.assertTrue(any("BLS-TEST" in r or "Basic Life Support" in r for r in result["reasons"]))

    def test_partially_ready_when_workshop_done_but_not_research(self):
        ResidentWorkshopCompletion.objects.create(
            resident_training_record=self.rtr,
            workshop=self.workshop,
            completed_at=date.today(),
        )
        result = self._compute()
        self.assertEqual(result["status"], ResidentMilestoneEligibility.STATUS_PARTIALLY_READY)
        self.assertTrue(any("Synopsis" in r for r in result["reasons"]))

    def test_eligible_when_all_requirements_met(self):
        # Complete workshop
        ResidentWorkshopCompletion.objects.create(
            resident_training_record=self.rtr,
            workshop=self.workshop,
            completed_at=date.today(),
        )
        # Approved research
        proj = ResidentResearchProject.objects.create(
            resident_training_record=self.rtr,
            title="My Research",
            supervisor=self.supervisor,
        )
        proj.transition_to(ResidentResearchProject.STATUS_SUBMITTED_SUPERVISOR)
        proj.transition_to(ResidentResearchProject.STATUS_APPROVED_SUPERVISOR)

        result = self._compute()
        self.assertEqual(result["status"], ResidentMilestoneEligibility.STATUS_ELIGIBLE)
        self.assertEqual(len(result["reasons"]), 0)

    def test_recompute_for_record_creates_rows(self):
        results = recompute_for_record(self.rtr)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["milestone_code"], ProgramMilestone.CODE_IMM)
        # DB row created
        self.assertTrue(
            ResidentMilestoneEligibility.objects.filter(
                resident_training_record=self.rtr,
                milestone=self.milestone,
            ).exists()
        )


# ---------------------------------------------------------------------------
# API endpoint tests
# ---------------------------------------------------------------------------

class ProgramPolicyAPITests(APITestCase):
    def setUp(self):
        self.admin = _make_user("admin_api_pol", "admin")
        self.pg = _make_user("pg_api_pol", "pg")
        self.program = _make_program("FCPS-POLTEST")
        self.url = f"/api/programs/{self.program.pk}/policy/"

    def test_get_policy_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("allow_program_change", resp.data)

    def test_put_policy_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        resp = self.client.put(self.url, {
            "allow_program_change": True,
            "imm_allowed_from_month": 24,
        }, format="json")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data["allow_program_change"])

    def test_get_policy_denied_for_pg(self):
        self.client.force_authenticate(user=self.pg)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 403)


class ResearchProjectAPITests(APITestCase):
    def setUp(self):
        self.pg = _make_user("pg_api_res", "pg")
        self.supervisor = _make_user("sup_api_res", "supervisor")
        self.rtr = _make_rtr(self.pg)
        self.pg.supervisor = self.supervisor
        self.pg.save()

    def test_create_research_project(self):
        self.client.force_authenticate(user=self.pg)
        resp = self.client.post("/api/my/research/", {
            "title": "API Test Research",
            "topic_area": "Cardiology",
            "supervisor": self.supervisor.pk,
        }, format="json")
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data["status"], ResidentResearchProject.STATUS_DRAFT)

    def test_submit_to_supervisor(self):
        self.client.force_authenticate(user=self.pg)
        self.client.post("/api/my/research/", {
            "title": "Research X",
            "supervisor": self.supervisor.pk,
        }, format="json")
        resp = self.client.post(
            "/api/my/research/action/submit-to-supervisor/", {}, format="json"
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["status"], ResidentResearchProject.STATUS_SUBMITTED_SUPERVISOR)

    def test_supervisor_approve(self):
        # Create and submit
        self.client.force_authenticate(user=self.pg)
        cr = self.client.post("/api/my/research/", {
            "title": "Research Y",
            "supervisor": self.supervisor.pk,
        }, format="json")
        project_id = cr.data["id"]
        self.client.post("/api/my/research/action/submit-to-supervisor/", {}, format="json")

        # Supervisor approves
        self.client.force_authenticate(user=self.supervisor)
        resp = self.client.post("/api/my/research/action/supervisor-approve/", {
            "project_id": project_id,
            "feedback": "Good work!",
        }, format="json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["status"], ResidentResearchProject.STATUS_APPROVED_SUPERVISOR)

    def test_supervisor_return_transitions_project_to_draft(self):
        self.client.force_authenticate(user=self.pg)
        created = self.client.post("/api/my/research/", {
            "title": "Research needs revision",
            "supervisor": self.supervisor.pk,
        }, format="json")
        project_id = created.data["id"]
        self.client.post("/api/my/research/action/submit-to-supervisor/", {}, format="json")

        self.client.force_authenticate(user=self.supervisor)
        resp = self.client.post("/api/my/research/action/supervisor-return/", {
            "project_id": project_id,
            "feedback": "Please revise methodology.",
        }, format="json")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["status"], ResidentResearchProject.STATUS_DRAFT)
        self.assertEqual(resp.data["supervisor_feedback"], "Please revise methodology.")


class WorkshopCompletionAPITests(APITestCase):
    def setUp(self):
        self.pg = _make_user("pg_ws_test", "pg")
        self.rtr = _make_rtr(self.pg)
        self.workshop = Workshop.objects.create(name="ACLS Test", code="ACLS-TEST")

    def test_create_workshop_completion(self):
        self.client.force_authenticate(user=self.pg)
        resp = self.client.post("/api/my/workshops/", {
            "workshop": self.workshop.pk,
            "completed_at": str(date.today()),
        }, format="json")
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data["source"], ResidentWorkshopCompletion.SOURCE_MANUAL)

    def test_list_workshop_completions(self):
        ResidentWorkshopCompletion.objects.create(
            resident_training_record=self.rtr,
            workshop=self.workshop,
            completed_at=date.today(),
        )
        self.client.force_authenticate(user=self.pg)
        resp = self.client.get("/api/my/workshops/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["count"], 1)


class EligibilityAPITests(APITestCase):
    def setUp(self):
        self.pg = _make_user("pg_eli_api", "pg")
        self.admin = _make_user("admin_eli_api", "admin")
        self.program = _make_program("FCPS-ELI-API")
        self.rtr = _make_rtr(self.pg, self.program)

    def test_my_eligibility_empty_when_no_milestones(self):
        self.client.force_authenticate(user=self.pg)
        resp = self.client.get("/api/my/eligibility/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("eligibilities", resp.data)
        self.assertEqual(resp.data["eligibilities"], [])

    def test_my_eligibility_items_use_reasons_field(self):
        milestone = ProgramMilestone.objects.create(
            program=self.program,
            code=ProgramMilestone.CODE_IMM,
            name="IMM",
            is_active=True,
        )
        ProgramMilestoneResearchRequirement.objects.create(
            milestone=milestone,
            requires_thesis_submitted=True,
        )

        self.client.force_authenticate(user=self.pg)
        resp = self.client.get("/api/my/eligibility/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data["eligibilities"]), 1)
        item = resp.data["eligibilities"][0]
        self.assertIn("reasons", item)
        self.assertNotIn("reasons_json", item)
        self.assertIsInstance(item["reasons"], list)
        self.assertGreaterEqual(len(item["reasons"]), 1)

    def test_utrmc_eligibility_requires_admin(self):
        self.client.force_authenticate(user=self.pg)
        resp = self.client.get("/api/utrmc/eligibility/")
        self.assertEqual(resp.status_code, 403)

    def test_utrmc_eligibility_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        resp = self.client.get("/api/utrmc/eligibility/")
        self.assertEqual(resp.status_code, 200)

    def test_utrmc_eligibility_items_use_reasons_field(self):
        milestone = ProgramMilestone.objects.create(
            program=self.program,
            code=ProgramMilestone.CODE_FINAL,
            name="FINAL",
            is_active=True,
        )
        ResidentMilestoneEligibility.objects.create(
            resident_training_record=self.rtr,
            milestone=milestone,
            status=ResidentMilestoneEligibility.STATUS_PARTIALLY_READY,
            reasons_json=["Thesis not submitted"],
        )

        self.client.force_authenticate(user=self.admin)
        resp = self.client.get("/api/utrmc/eligibility/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["count"], 1)
        item = resp.data["results"][0]
        self.assertIn("reasons", item)
        self.assertNotIn("reasons_json", item)
        self.assertEqual(item["reasons"], ["Thesis not submitted"])


class SystemSettingsAPITests(APITestCase):
    def setUp(self):
        self.pg = _make_user("pg_settings", "pg")

    def test_system_settings_accessible(self):
        self.client.force_authenticate(user=self.pg)
        resp = self.client.get("/api/system/settings/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("WORKSHOP_MANAGEMENT_ENABLED", resp.data)
        self.assertFalse(resp.data["WORKSHOP_MANAGEMENT_ENABLED"])


# =============================================================================
# Phase 6B/6C Tests — Summary Endpoints
# =============================================================================

def _make_milestone(program, code, name):
    """Helper to create a ProgramMilestone for tests."""
    from sims.training.models import ProgramMilestone
    ms, _ = ProgramMilestone.objects.get_or_create(
        program=program, code=code,
        defaults={"name": name, "is_active": True},
    )
    return ms


class ResidentSummaryTests(APITestCase):
    """Tests for GET /api/residents/me/summary/"""

    def setUp(self):
        dept = Department.objects.create(name="Medicine", code="MED")
        hospital = Hospital.objects.create(name="Main Hospital", code="MH")
        self.hd = HospitalDepartment.objects.create(hospital=hospital, department=dept)

        self.prog = TrainingProgram.objects.create(
            name="FCPS Medicine", code="FCPS-MED", degree_type="fcps", duration_months=60
        )
        _make_milestone(self.prog, "IMM", "Intermediate Milestone")
        _make_milestone(self.prog, "FINAL", "Final Milestone")

        self.resident = _make_user("res_summary", "pg")
        self.client.force_authenticate(user=self.resident)

        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.resident,
            program=self.prog,
            start_date=date.today() - timedelta(days=60),
            active=True,
        )

    def test_summary_returns_correct_structure(self):
        resp = self.client.get("/api/residents/me/summary/")
        self.assertEqual(resp.status_code, 200)
        data = resp.data
        # Top-level keys deterministic
        expected_keys = {"training_record", "rotation", "schedule", "leaves", "postings",
                         "research", "thesis", "workshops", "eligibility"}
        self.assertEqual(set(data.keys()), expected_keys)

    def test_training_record_fields(self):
        resp = self.client.get("/api/residents/me/summary/")
        tr = resp.data["training_record"]
        self.assertEqual(tr["id"], self.rtr.id)
        self.assertEqual(tr["program_code"], "FCPS-MED")
        self.assertIn("current_month_index", tr)
        self.assertIsInstance(tr["current_month_index"], int)

    def test_eligibility_keys(self):
        resp = self.client.get("/api/residents/me/summary/")
        eli = resp.data["eligibility"]
        self.assertIn("IMM", eli)
        self.assertIn("FINAL", eli)

    def test_unauthenticated_denied(self):
        self.client.force_authenticate(user=None)
        resp = self.client.get("/api/residents/me/summary/")
        self.assertIn(resp.status_code, [401, 403])

    def test_supervisor_denied(self):
        sup = _make_user("sup_summary_test", "supervisor")
        self.client.force_authenticate(user=sup)
        resp = self.client.get("/api/residents/me/summary/")
        # Supervisor role is rejected by RBAC check before RTR lookup
        self.assertEqual(resp.status_code, 403)


class SupervisorSummaryTests(APITestCase):
    """Tests for GET /api/supervisors/me/summary/"""

    def setUp(self):
        dept = Department.objects.create(name="Surgery", code="SURG")
        hospital = Hospital.objects.create(name="City Hospital", code="CH")
        self.hd = HospitalDepartment.objects.create(hospital=hospital, department=dept)

        self.prog = TrainingProgram.objects.create(
            name="FCPS Surgery", code="FCPS-SURG", degree_type="fcps", duration_months=60
        )
        self.supervisor = _make_user("sup_summary", "supervisor")
        self.resident1 = _make_user("res_sup_sum1", "pg")
        self.resident2 = _make_user("res_sup_sum2", "pg")
        self.client.force_authenticate(user=self.supervisor)

        from sims.users.models import SupervisorResidentLink
        SupervisorResidentLink.objects.create(
            supervisor_user=self.supervisor,
            resident_user=self.resident1,
            active=True,
            start_date=date.today(),
        )

        self.rtr1 = ResidentTrainingRecord.objects.create(
            resident_user=self.resident1,
            program=self.prog,
            start_date=date.today() - timedelta(days=30),
            active=True,
        )

    def test_summary_structure(self):
        resp = self.client.get("/api/supervisors/me/summary/")
        self.assertEqual(resp.status_code, 200)
        data = resp.data
        self.assertIn("pending", data)
        self.assertIn("residents", data)
        pending = data["pending"]
        self.assertIn("rotation_approvals", pending)
        self.assertIn("leave_approvals", pending)
        self.assertIn("research_approvals", pending)

    def test_scoping_only_linked_residents(self):
        """Supervisor sees only linked residents, not unlinked ones."""
        resp = self.client.get("/api/supervisors/me/summary/")
        self.assertEqual(resp.status_code, 200)
        ids = [r["id"] for r in resp.data["residents"]]
        self.assertIn(self.resident1.id, ids)
        self.assertNotIn(self.resident2.id, ids)

    def test_scoping_includes_direct_supervisor_assignment(self):
        resident = _make_user("res_direct_sup", "pg")
        resident.supervisor = self.supervisor
        resident.save()
        ResidentTrainingRecord.objects.create(
            resident_user=resident,
            program=self.prog,
            start_date=date.today() - timedelta(days=15),
            active=True,
        )

        resp = self.client.get("/api/supervisors/me/summary/")
        self.assertEqual(resp.status_code, 200)
        ids = [r["id"] for r in resp.data["residents"]]
        self.assertIn(resident.id, ids)

    def test_residents_sorted_by_name(self):
        from sims.users.models import SupervisorResidentLink
        # Add second resident to same supervisor
        res_a = _make_user("res_alpha", "pg")
        res_a.last_name = "Aardvark"; res_a.save()
        res_z = _make_user("res_zeta", "pg")
        res_z.last_name = "Zebra"; res_z.save()

        for res in [res_a, res_z]:
            SupervisorResidentLink.objects.create(
                supervisor_user=self.supervisor, resident_user=res,
                active=True, start_date=date.today()
            )
            ResidentTrainingRecord.objects.create(
                resident_user=res, program=self.prog,
                start_date=date.today() - timedelta(days=10), active=True
            )

        resp = self.client.get("/api/supervisors/me/summary/")
        names = [r["name"] for r in resp.data["residents"]]
        self.assertEqual(names, sorted(names, key=str.lower))

    def test_resident_denied(self):
        res = _make_user("res_denied_sup", "pg")
        self.client.force_authenticate(user=res)
        resp = self.client.get("/api/supervisors/me/summary/")
        self.assertEqual(resp.status_code, 403)


class ResidentProgressViewTests(APITestCase):
    """Tests for GET /api/supervisors/residents/<id>/progress/"""

    def setUp(self):
        dept = Department.objects.create(name="Pediatrics", code="PED")
        hospital = Hospital.objects.create(name="Peds Hospital", code="PH")
        HospitalDepartment.objects.create(hospital=hospital, department=dept)

        self.prog = TrainingProgram.objects.create(
            name="FCPS Peds", code="FCPS-PEDS", degree_type="fcps", duration_months=60
        )
        self.supervisor = _make_user("sup_progress", "supervisor")
        self.resident = _make_user("res_progress", "pg")
        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.resident,
            program=self.prog,
            start_date=date.today() - timedelta(days=90),
            active=True,
        )

    def test_supervisor_can_view_progress(self):
        self.client.force_authenticate(user=self.supervisor)
        resp = self.client.get(f"/api/supervisors/residents/{self.resident.id}/progress/")
        self.assertEqual(resp.status_code, 200)
        data = resp.data
        self.assertIn("resident", data)
        self.assertIn("training_record", data)
        self.assertIn("eligibility", data)

    def test_resident_cannot_view_own_progress(self):
        self.client.force_authenticate(user=self.resident)
        resp = self.client.get(f"/api/supervisors/residents/{self.resident.id}/progress/")
        self.assertEqual(resp.status_code, 403)
