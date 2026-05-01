from django.test import TestCase
from sims.training.eligibility import (
    recompute_for_record, 
    compute_milestone_eligibility
)
from sims.training.models import (
    TrainingProgram, ResidentTrainingRecord, ProgramMilestone,
    ResidentResearchProject, ResidentMilestoneEligibility
)
from django.contrib.auth import get_user_model
from datetime import date, timedelta

User = get_user_model()

class EligibilityTests(TestCase):
    def setUp(self):
        self.pg = User.objects.create_user(username="pg_elig", role="pg")
        self.program = TrainingProgram.objects.create(name="Medicine", code="MED_E", duration_months=48)
        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.pg, program=self.program, 
            start_date=date.today() - timedelta(days=500),
            expected_end_date=date.today() + timedelta(days=500),
            active=True
        )
        self.milestone_imm = ProgramMilestone.objects.create(
            program=self.program, name="IMM", code="IMM", recommended_month=24
        )

    def test_research_eligibility_logic(self):
        # By default, no requirements means ELIGIBLE
        result = compute_milestone_eligibility(self.rtr, self.milestone_imm)
        self.assertEqual(result["status"], ResidentMilestoneEligibility.STATUS_ELIGIBLE)
        
        # Add a requirement
        from sims.training.models import ProgramMilestoneResearchRequirement
        req = ProgramMilestoneResearchRequirement.objects.create(
            milestone=self.milestone_imm,
            requires_synopsis_approved=True
        )
        
        # Reload milestone to get the new requirement (one-to-one)
        self.milestone_imm.refresh_from_db()
        
        result = compute_milestone_eligibility(self.rtr, self.milestone_imm)
        self.assertEqual(result["status"], ResidentMilestoneEligibility.STATUS_NOT_READY)
        self.assertIn("Synopsis submission not yet verified", result["reasons"])

    def test_recompute_for_record_logic(self):
        results = recompute_for_record(self.rtr)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["milestone_code"], "IMM")
        
        # Check if DB row created
        self.assertTrue(ResidentMilestoneEligibility.objects.filter(
            resident_training_record=self.rtr, milestone=self.milestone_imm
        ).exists())
