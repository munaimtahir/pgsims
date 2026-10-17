"""Resident draft updates and document boundaries through the public API."""
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient
from sims.academics.models import Department, AcademicSession, Specialty
from sims.rotations.models import Hospital
from sims.training.models import TrainingProgram, ResidentTrainingRecord, ResidentResearchProject, ResidentThesis, Workshop, ResidentWorkshopCompletion
from sims.users.models import ResidentDocumentRequirement, ResidentDocument
from sims.users.services import create_user_with_profile
from sims.users.onboarding_api import get_resident_onboarding_state


class OnboardingBoundaryTests(TestCase):
    def setUp(self):
        self.user = create_user_with_profile(role='RESIDENT', full_name='Draft Resident')
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.program = TrainingProgram.objects.create(code='BOUND', name='Boundary Program', duration_months=48)

    def update(self, fields):
        return self.client.patch('/api/auth/onboarding/', {'fields': fields}, format='json')

    def enroll(self):
        response = self.update({'program_ref': self.program.pk})
        self.assertEqual(response.status_code, 200, response.data)
        return ResidentTrainingRecord.objects.get(resident_user=self.user)

    def test_profile_and_training_references_stay_synchronized(self):
        hospital = Hospital.objects.create(code='BOUND', name='Boundary Hospital')
        department = Department.objects.create(code='BOUND', name='Boundary Department')
        session = AcademicSession.objects.create(code='BOUND', name='Boundary Session')
        specialty = Specialty.objects.create(code='BOUND', name='Boundary Specialty')
        response=self.update({'program_ref':self.program.pk,'hospital':hospital.pk,'department_ref':department.pk,'academic_session_ref':session.code,'specialty_ref':specialty.code})
        self.assertEqual(response.status_code,200,response.data)
        self.user.resident_profile.refresh_from_db()
        profile=self.user.resident_profile
        training=ResidentTrainingRecord.objects.get(resident_user=self.user)
        self.assertEqual((profile.hospital_id,profile.department_ref_id,profile.academic_session_ref_id,profile.specialty_ref_id),(hospital.pk,department.pk,session.code,specialty.code))
        self.assertEqual((training.training_site_id,training.department_id,training.academic_session_id),(hospital.pk,department.pk,session.pk))
        self.assertEqual(self.update({'hospital':None,'academic_session_ref':None}).status_code,200)
        training.refresh_from_db()
        self.assertIsNone(training.training_site_id)
        self.assertIsNone(training.academic_session_id)

    def test_optional_identity_fields_clear_and_single_part_name(self):
        self.assertEqual(self.update({'full_name':'Resident','phone':'123','email':'a@example.invalid','registration_no':'REG','cnic':'12345'}).status_code,200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name,'')
        self.assertEqual(self.user.resident_profile.registration_no,'REG')
        self.assertEqual(self.update({'phone':None,'email':None,'registration_no':None,'cnic':None}).status_code,200)
        self.user.refresh_from_db()
        self.user.resident_profile.refresh_from_db()
        self.assertEqual(self.user.phone_number,'')
        self.assertEqual(self.user.resident_profile.cnic,'')

    def test_invalid_reference_and_unknown_field_roll_back_earlier_edits(self):
        for field,value in [('hospital',999999),('department_ref','not-an-id'),('program_ref',999999),('academic_session_ref','absent'),('specialty_ref','absent'),('unsupported','value')]:
            with self.subTest(field=field):
                response=self.update({'full_name':'Must Roll Back',field:value})
                self.assertEqual(response.status_code,400,response.data)
                self.user.refresh_from_db()
                self.assertEqual(self.user.get_full_name(),'Draft Resident')

    def test_training_and_research_require_program_first(self):
        for field,value in [('training_start_date','2026-01-01'),('current_level','1'),('research_title','Title'),('thesis_notes','Notes'),('workshop_completion:1','2026-01-01')]:
            with self.subTest(field=field):
                response=self.update({field:value})
                self.assertEqual(response.status_code,400,response.data)
        self.assertFalse(ResidentTrainingRecord.objects.filter(resident_user=self.user).exists())

    def test_training_dates_and_notes_persist_and_optional_end_date_clears(self):
        training=self.enroll()
        response=self.update({'training_start_date':'2026-01-01','expected_end_date':'2030-01-01','current_level':'2','notes':'Training notes'})
        self.assertEqual(response.status_code,200,response.data)
        training.refresh_from_db()
        self.assertEqual(training.start_date,date(2026,1,1))
        self.assertEqual(training.current_level,'2')
        self.assertEqual(training.notes,'Training notes')
        self.assertEqual(self.update({'expected_end_date':None,'notes':None}).status_code,200)
        training.refresh_from_db()
        self.assertIsNone(training.expected_end_date)
        self.assertEqual(training.notes,'')

    def test_invalid_dates_are_validation_errors_and_atomic(self):
        training=self.enroll()
        before=training.start_date
        for field,value in [('training_start_date','wrong'),('training_start_date',None),('expected_end_date','2026-02-31'),('training_start_date',42)]:
            with self.subTest(field=field,value=value):
                response=self.update({'notes':'must roll back',field:value})
                self.assertEqual(response.status_code,400,response.data)
                training.refresh_from_db()
                self.assertEqual(training.start_date,before)
                self.assertEqual(training.notes,'')

    def test_research_thesis_and_supervisor_drafts_are_returned_in_state(self):
        training=self.enroll()
        response=self.update({'research_title':'New title','research_topic_area':'Medicine','research_status':'DRAFT','thesis_status':'IN_PROGRESS','thesis_notes':'Draft notes','supervisor_status':'NOT_ASSIGNED'})
        self.assertEqual(response.status_code,200,response.data)
        project=ResidentResearchProject.objects.get(resident_training_record=training)
        thesis=ResidentThesis.objects.get(resident_training_record=training)
        self.assertEqual((project.title,project.topic_area),('New title','Medicine'))
        self.assertEqual((thesis.status,thesis.notes),('IN_PROGRESS','Draft notes'))
        self.assertEqual(self.update({'supervisor_status':None}).status_code,200)
        for field in ['research_status','thesis_status']:
            self.assertEqual(self.update({field:'INVALID'}).status_code,400)
        project.refresh_from_db(); thesis.refresh_from_db()
        self.assertEqual(project.status,'DRAFT'); self.assertEqual(thesis.status,'IN_PROGRESS')

    def test_workshop_create_replace_delete_and_validation(self):
        training=self.enroll()
        workshop=Workshop.objects.create(code='BOUND',name='Boundary workshop')
        field=f'workshop_completion:{workshop.pk}'
        for value in ['2026-01-01','2026-02-01']:
            self.assertEqual(self.update({field:value}).status_code,200)
            self.assertEqual(ResidentWorkshopCompletion.objects.get(resident_training_record=training,workshop=workshop).completed_at,date.fromisoformat(value))
        self.assertEqual(self.update({field:None}).status_code,200)
        self.assertFalse(ResidentWorkshopCompletion.objects.filter(resident_training_record=training).exists())
        self.assertEqual(self.update({field:None}).status_code,200)
        for key,value in [(field,'bad-date'),('workshop_completion:bad','2026-01-01'),('workshop_completion:999999','2026-01-01')]:
            self.assertEqual(self.update({key:value}).status_code,400)

    def test_single_field_patch_and_nonresident_denial(self):
        response=self.client.patch('/api/auth/onboarding/',{'field':'registration_no','value':'REG'},format='json')
        self.assertEqual(response.status_code,200,response.data)
        self.assertEqual(self.client.patch('/api/auth/onboarding/',{},format='json').status_code,200)
        for role in ['ADMIN','SUPERVISOR','SUPPORT_STAFF']:
            user=create_user_with_profile(role=role,full_name=role)
            self.client.force_authenticate(user)
            self.assertEqual(self.update({'registration_no':'denied'}).status_code,403)

    def test_upload_validation_download_and_missing_storage(self):
        requirement=ResidentDocumentRequirement.objects.create(document_type='OTHER',display_name='Boundary Document')
        get_resident_onboarding_state(self.user)
        document=ResidentDocument.objects.get(resident=self.user.resident_profile,requirement=requirement)
        url=f'/api/resident-documents/{document.pk}/'
        self.assertEqual(self.client.get(url+'file/').status_code,404)
        self.assertEqual(self.client.post(url+'upload/',{},format='multipart').status_code,400)
        for filename,body in [('bad.exe',b'exe'),('large.pdf',b'x'*(10*1024*1024+1))]:
            response=self.client.post(url+'upload/',{'file':SimpleUploadedFile(filename,body)},format='multipart')
            self.assertEqual(response.status_code,400,response.data)
        response=self.client.post(url+'upload/',{'file':SimpleUploadedFile('document.PDF',b'document bytes')},format='multipart')
        self.assertEqual(response.status_code,200,response.data)
        for action in ['file/','download/']:
            response=self.client.get(url+action)
            self.assertEqual(response.status_code,200)
            self.assertEqual(b''.join(response.streaming_content),b'document bytes')
            self.assertIn('no-store',response['Cache-Control'])
            self.assertEqual(response['X-Content-Type-Options'],'nosniff')
            response.close()
        document.refresh_from_db()
        document.file.storage.delete(document.file.name)
        self.assertEqual(self.client.get(url+'file/').status_code,404)
