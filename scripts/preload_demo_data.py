#!/usr/bin/env python
"""
Preload Demo Data Script for SIMS

This script creates comprehensive test data including:
- Admin, Supervisor, and PG student users
- Assignments between supervisors and students
- Sample logbooks, cases, and certificates
- Rotations and evaluations

Usage:
    python manage.py shell < scripts/preload_demo_data.py

Or:
    python scripts/preload_demo_data.py (if run directly)
"""

import os
import sys
import django
from datetime import date, timedelta
from pathlib import Path

# Setup Django environment
if __name__ == "__main__":
    # Add the project root directory to the Python path
    project_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(project_root))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sims_project.settings")
    django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction
from sims.rotations.models import Hospital, Department, Rotation
from sims.certificates.models import CertificateType, Certificate
from sims.logbook.models import LogbookEntry, Procedure, Diagnosis
from sims.cases.models import CaseCategory, ClinicalCase

User = get_user_model()


def create_demo_users():
    """Create demo users: admin, supervisors, and PG students"""
    print("Creating demo users...")
    
    users_data = {
        'admin': {
            'username': 'admin',
            'email': 'admin@sims.demo',
            'password': 'admin123',
            'role': 'admin',
            'first_name': 'System',
            'last_name': 'Administrator',
            'is_staff': True,
            'is_superuser': True,
        },
        'supervisors': [
            {
                'username': 'dr_smith',
                'email': 'smith@sims.demo',
                'password': 'supervisor123',
                'role': 'supervisor',
                'first_name': 'John',
                'last_name': 'Smith',
                'specialty': 'surgery',
            },
            {
                'username': 'dr_jones',
                'email': 'jones@sims.demo',
                'password': 'supervisor123',
                'role': 'supervisor',
                'first_name': 'Sarah',
                'last_name': 'Jones',
                'specialty': 'medicine',
            },
        ],
        'students': [
            {
                'username': 'pg_ahmed',
                'email': 'ahmed@sims.demo',
                'password': 'student123',
                'role': 'pg',
                'first_name': 'Ahmed',
                'last_name': 'Khan',
                'specialty': 'surgery',
                'year': '1',
                'registration_number': 'PG2024001',
            },
            {
                'username': 'pg_fatima',
                'email': 'fatima@sims.demo',
                'password': 'student123',
                'role': 'pg',
                'first_name': 'Fatima',
                'last_name': 'Ali',
                'specialty': 'medicine',
                'year': '2',
                'registration_number': 'PG2024002',
            },
        ],
    }
    
    # Create admin
    admin_data = users_data['admin']
    admin, created = User.objects.get_or_create(
        username=admin_data['username'],
        defaults=admin_data
    )
    if created:
        admin.set_password(admin_data['password'])
        admin.save()
        print(f"✓ Created admin: {admin.username}")
    else:
        print(f"  Admin already exists: {admin.username}")
    
    # Create supervisors
    supervisors = []
    for sup_data in users_data['supervisors']:
        supervisor, created = User.objects.get_or_create(
            username=sup_data['username'],
            defaults=sup_data
        )
        if created:
            supervisor.set_password(sup_data['password'])
            supervisor.save()
            print(f"✓ Created supervisor: {supervisor.username}")
        else:
            print(f"  Supervisor already exists: {supervisor.username}")
        supervisors.append(supervisor)
    
    # Create PG students and assign to supervisors
    students = []
    for idx, pg_data in enumerate(users_data['students']):
        # Assign supervisor based on specialty match
        supervisor = supervisors[idx % len(supervisors)]
        pg_data['supervisor'] = supervisor
        
        student, created = User.objects.get_or_create(
            username=pg_data['username'],
            defaults=pg_data
        )
        if created:
            student.set_password(pg_data['password'])
            student.save()
            print(f"✓ Created PG student: {student.username} (supervised by {supervisor.username})")
        else:
            print(f"  PG student already exists: {student.username}")
        students.append(student)
    
    return admin, supervisors, students


def create_hospitals_and_departments():
    """Create demo hospitals and departments"""
    print("\nCreating hospitals and departments...")
    
    hospital_data = [
        {
            'name': 'Faisalabad Medical University Teaching Hospital',
            'code': 'FMU-TH',
            'address': 'Sargodha Road, Faisalabad',
            'phone': '+92-41-9220001',
            'email': 'info@fmu.edu.pk',
        },
        {
            'name': 'Allied Hospital Faisalabad',
            'code': 'AH-FSD',
            'address': 'Sargodha Road, Faisalabad',
            'phone': '+92-41-9220002',
            'email': 'info@alliedhospital.edu.pk',
        },
    ]
    
    hospitals = []
    for hosp_data in hospital_data:
        hospital, created = Hospital.objects.get_or_create(
            code=hosp_data['code'],
            defaults=hosp_data
        )
        if created:
            print(f"✓ Created hospital: {hospital.name}")
        else:
            print(f"  Hospital already exists: {hospital.name}")
        hospitals.append(hospital)
    
    # Create departments
    departments_data = [
        {'name': 'General Surgery', 'head_of_department': 'Prof. Dr. Ali Raza'},
        {'name': 'Internal Medicine', 'head_of_department': 'Prof. Dr. Saima Iqbal'},
        {'name': 'Cardiology', 'head_of_department': 'Prof. Dr. Hassan Ahmed'},
        {'name': 'Orthopedics', 'head_of_department': 'Prof. Dr. Bilal Khan'},
    ]
    
    departments = []
    for dept_data in departments_data:
        for hospital in hospitals:
            dept_data_with_hospital = {**dept_data, 'hospital': hospital}
            department, created = Department.objects.get_or_create(
                name=dept_data['name'],
                hospital=hospital,
                defaults=dept_data_with_hospital
            )
            if created:
                print(f"✓ Created department: {department.name} at {hospital.name}")
            departments.append(department)
    
    return hospitals, departments


def create_rotations(admin, supervisors, students, hospitals, departments):
    """Create sample rotations for students"""
    print("\nCreating rotations...")
    
    rotations = []
    for idx, student in enumerate(students):
        # Create 2 rotations per student
        for rot_idx in range(2):
            department = departments[rot_idx % len(departments)]
            hospital = department.hospital
            supervisor = supervisors[idx % len(supervisors)]
            
            # Past rotation
            if rot_idx == 0:
                start_date = date.today() - timedelta(days=180)
                end_date = date.today() - timedelta(days=30)
                status = 'completed'
            # Current rotation
            else:
                start_date = date.today() - timedelta(days=30)
                end_date = date.today() + timedelta(days=150)
                status = 'ongoing'
            
            rotation_data = {
                'pg': student,
                'department': department,
                'hospital': hospital,
                'supervisor': supervisor,
                'start_date': start_date,
                'end_date': end_date,
                'status': status,
                'objectives': f'Complete training in {department.name}',
                'created_by': admin,
            }
            
            rotation, created = Rotation.objects.get_or_create(
                pg=student,
                department=department,
                start_date=start_date,
                defaults=rotation_data
            )
            
            if created:
                print(f"✓ Created rotation: {student.username} - {department.name} ({status})")
            rotations.append(rotation)
    
    return rotations


def create_certificates(admin, students):
    """Create certificate types and sample certificates"""
    print("\nCreating certificates...")
    
    # Create certificate types
    cert_types_data = [
        {
            'name': 'BLS Certification',
            'category': 'safety',
            'description': 'Basic Life Support Certification',
            'is_required': True,
            'validity_period_months': 24,
        },
        {
            'name': 'ACLS Certification',
            'category': 'safety',
            'description': 'Advanced Cardiovascular Life Support',
            'is_required': True,
            'validity_period_months': 24,
        },
        {
            'name': 'Workshop Attendance',
            'category': 'cme',
            'description': 'Medical Workshop Attendance Certificate',
            'is_required': False,
            'validity_period_months': None,
        },
    ]
    
    cert_types = []
    for cert_type_data in cert_types_data:
        cert_type, created = CertificateType.objects.get_or_create(
            name=cert_type_data['name'],
            defaults=cert_type_data
        )
        if created:
            print(f"✓ Created certificate type: {cert_type.name}")
        cert_types.append(cert_type)
    
    # Create sample certificates for each student
    certificates = []
    for student in students:
        for idx, cert_type in enumerate(cert_types[:2]):  # Create 2 certificates per student
            issue_date = date.today() - timedelta(days=30 * (idx + 1))
            expiry_date = issue_date + timedelta(days=cert_type.validity_period_months * 30) if cert_type.validity_period_months else None
            
            cert_data = {
                'pg': student,
                'certificate_type': cert_type,
                'issue_date': issue_date,
                'expiry_date': expiry_date,
                'issuing_organization': 'American Heart Association',
                'certificate_number': f'CERT-{student.id:04d}-{idx+1:02d}',
                'status': 'approved',
                'verified_by': admin,
                'verified_at': issue_date,
            }
            
            certificate, created = Certificate.objects.get_or_create(
                pg=student,
                certificate_type=cert_type,
                certificate_number=cert_data['certificate_number'],
                defaults=cert_data
            )
            
            if created:
                print(f"✓ Created certificate: {student.username} - {cert_type.name}")
            certificates.append(certificate)
    
    return certificates


def create_diagnoses_and_procedures():
    """Create sample diagnoses and procedures for logbook entries and cases"""
    print("\nCreating diagnoses and procedures...")
    
    # Create diagnoses
    diagnoses_data = [
        {'name': 'Acute Appendicitis', 'category': 'gastrointestinal', 'icd_code': 'K35', 'description': 'Inflammation of the appendix'},
        {'name': 'Pneumonia', 'category': 'respiratory', 'icd_code': 'J18', 'description': 'Infection of the lungs'},
        {'name': 'Hypertension', 'category': 'cardiovascular', 'icd_code': 'I10', 'description': 'High blood pressure'},
        {'name': 'Type 2 Diabetes', 'category': 'endocrine', 'icd_code': 'E11', 'description': 'Diabetes mellitus type 2'},
        {'name': 'Fracture of Radius', 'category': 'musculoskeletal', 'icd_code': 'S52', 'description': 'Broken radius bone'},
    ]
    
    diagnoses = []
    for diag_data in diagnoses_data:
        diagnosis, created = Diagnosis.objects.get_or_create(
            name=diag_data['name'],
            defaults=diag_data
        )
        if created:
            print(f"✓ Created diagnosis: {diagnosis.name}")
        diagnoses.append(diagnosis)
    
    # Create procedures
    procedures_data = [
        {'name': 'Physical Examination', 'category': 'diagnostic', 'description': 'General physical examination', 'difficulty_level': 1, 'duration_minutes': 15},
        {'name': 'Blood Pressure Measurement', 'category': 'diagnostic', 'description': 'BP measurement', 'difficulty_level': 1, 'duration_minutes': 5},
        {'name': 'Venipuncture', 'category': 'basic', 'description': 'Blood sampling', 'difficulty_level': 2, 'duration_minutes': 10},
        {'name': 'Wound Suturing', 'category': 'surgical', 'description': 'Suturing wounds', 'difficulty_level': 3, 'duration_minutes': 30},
        {'name': 'ECG Interpretation', 'category': 'diagnostic', 'description': 'Electrocardiogram reading', 'difficulty_level': 3, 'duration_minutes': 20},
    ]
    
    procedures = []
    for proc_data in procedures_data:
        procedure, created = Procedure.objects.get_or_create(
            name=proc_data['name'],
            defaults=proc_data
        )
        if created:
            print(f"✓ Created procedure: {procedure.name}")
        procedures.append(procedure)
    
    return diagnoses, procedures


def create_logbook_entries(students, supervisors, rotations):
    """Create logbook entries for students with all required fields"""
    print("\nCreating logbook entries...")
    
    # Get or create diagnoses and procedures
    diagnoses, procedures = create_diagnoses_and_procedures()
    
    entries = []
    entry_templates = [
        {
            'case_title': 'Acute Appendicitis Case',
            'location_of_activity': 'Emergency Department',
            'patient_history_summary': '25-year-old male presented with right lower quadrant pain for 12 hours. Pain started around umbilicus and migrated to RLQ. Associated with nausea and vomiting.',
            'management_action': 'Performed physical examination, ordered CBC and CT scan. Diagnosed with acute appendicitis. Referred to surgery for appendectomy.',
            'topic_subtopic': 'General Surgery / Acute Abdomen',
            'patient_age': 25,
            'patient_gender': 'M',
            'clinical_reasoning': 'Classic presentation of appendicitis with migration of pain from periumbilical to RLQ. McBurney point tenderness confirmed diagnosis.',
            'learning_points': 'Importance of thorough history taking and physical examination in acute abdomen cases. Understanding of appendicitis pathophysiology.',
        },
        {
            'case_title': 'Community-Acquired Pneumonia',
            'location_of_activity': 'Medical Ward',
            'patient_history_summary': '65-year-old female with 3-day history of fever, productive cough with yellow sputum, and shortness of breath. No significant past medical history.',
            'management_action': 'Obtained chest X-ray showing right lower lobe consolidation. Started on IV antibiotics (ceftriaxone and azithromycin). Oxygen support provided.',
            'topic_subtopic': 'Internal Medicine / Respiratory Infections',
            'patient_age': 65,
            'patient_gender': 'F',
            'clinical_reasoning': 'Clinical presentation consistent with pneumonia. Chest X-ray confirmed diagnosis. Appropriate antibiotic selection based on local guidelines.',
            'learning_points': 'Recognition of pneumonia symptoms, interpretation of chest X-rays, and antibiotic selection for community-acquired pneumonia.',
        },
        {
            'case_title': 'Hypertension Management',
            'location_of_activity': 'Outpatient Clinic',
            'patient_history_summary': '45-year-old male with newly diagnosed hypertension. BP readings consistently above 140/90. Family history of hypertension and diabetes.',
            'management_action': 'Initiated lifestyle modifications counseling. Started on ACE inhibitor (lisinopril 10mg daily). Scheduled follow-up in 2 weeks.',
            'topic_subtopic': 'Cardiology / Hypertension',
            'patient_age': 45,
            'patient_gender': 'M',
            'clinical_reasoning': 'Primary hypertension diagnosed after ruling out secondary causes. ACE inhibitor chosen as first-line therapy based on guidelines.',
            'learning_points': 'Hypertension diagnosis criteria, lifestyle modifications, and first-line antihypertensive medications.',
        },
        {
            'case_title': 'Diabetic Foot Ulcer',
            'location_of_activity': 'Surgical Outpatient',
            'patient_history_summary': '55-year-old diabetic patient with non-healing ulcer on left foot for 2 months. Poor glycemic control. History of peripheral neuropathy.',
            'management_action': 'Wound debridement performed. Started on appropriate antibiotics. Referred to podiatry and endocrinology for comprehensive management.',
            'topic_subtopic': 'Endocrinology / Diabetes Complications',
            'patient_age': 55,
            'patient_gender': 'M',
            'clinical_reasoning': 'Diabetic foot ulcer requires multidisciplinary approach. Wound care, glycemic control, and vascular assessment are essential.',
            'learning_points': 'Management of diabetic complications, wound care principles, and importance of glycemic control.',
        },
        {
            'case_title': 'Distal Radius Fracture',
            'location_of_activity': 'Orthopedic Emergency',
            'patient_history_summary': '30-year-old female fell on outstretched hand. Immediate pain and swelling in right wrist. Unable to move wrist.',
            'management_action': 'X-ray confirmed Colles fracture. Closed reduction performed under local anesthesia. Plaster cast applied. Follow-up scheduled.',
            'topic_subtopic': 'Orthopedics / Fracture Management',
            'patient_age': 30,
            'patient_gender': 'F',
            'clinical_reasoning': 'Classic mechanism of injury for Colles fracture. X-ray confirmed diagnosis. Closed reduction successful.',
            'learning_points': 'Fracture assessment, reduction techniques, and cast application. Understanding of fracture healing process.',
        },
    ]
    
    for idx, student in enumerate(students):
        # Get student's rotations and supervisor
        student_rotations = [r for r in rotations if r.pg == student]
        student_supervisor = student.supervisor if hasattr(student, 'supervisor') else supervisors[0]
        
        # Create 4-5 entries per student
        num_entries = 4 if idx == 0 else 5
        for entry_idx in range(num_entries):
            template = entry_templates[entry_idx % len(entry_templates)]
            rotation = student_rotations[entry_idx % len(student_rotations)] if student_rotations else None
            
            entry_date = date.today() - timedelta(days=30 * (entry_idx + 1))
            
            # Select appropriate diagnosis and procedures
            primary_diag = diagnoses[entry_idx % len(diagnoses)]
            selected_procedures = procedures[:min(2, len(procedures))]
            
            entry_data = {
                'pg': student,
                'case_title': template['case_title'],
                'date': entry_date,
                'location_of_activity': template['location_of_activity'],
                'patient_history_summary': template['patient_history_summary'],
                'management_action': template['management_action'],
                'topic_subtopic': template['topic_subtopic'],
                'rotation': rotation,
                'supervisor': student_supervisor,
                'patient_age': template['patient_age'],
                'patient_gender': template['patient_gender'],
                'primary_diagnosis': primary_diag,
                'clinical_reasoning': template['clinical_reasoning'],
                'learning_points': template['learning_points'],
                'status': 'approved' if entry_idx < 2 else 'pending',
            }
            
            entry, created = LogbookEntry.objects.get_or_create(
                pg=student,
                case_title=template['case_title'],
                date=entry_date,
                defaults=entry_data
            )
            
            if created:
                # Add many-to-many relationships
                entry.procedures.set(selected_procedures)
                if entry_idx % 2 == 0 and len(diagnoses) > 1:
                    entry.secondary_diagnoses.set([diagnoses[(entry_idx + 1) % len(diagnoses)]])
                
                print(f"✓ Created logbook entry: {entry.case_title} for {student.username}")
            entries.append(entry)
    
    return entries


def create_clinical_cases(students, supervisors, rotations):
    """Create sample clinical cases with all required fields"""
    print("\nCreating clinical cases...")
    
    # Get or create case categories
    categories_data = [
        {'name': 'Cardiology', 'description': 'Cardiovascular cases', 'color_code': '#FF5722'},
        {'name': 'General Surgery', 'description': 'Surgical cases', 'color_code': '#2196F3'},
        {'name': 'Internal Medicine', 'description': 'Medical cases', 'color_code': '#4CAF50'},
        {'name': 'Emergency Medicine', 'description': 'Emergency cases', 'color_code': '#F44336'},
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = CaseCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        if created:
            print(f"✓ Created case category: {category.name}")
        categories.append(category)
    
    # Get diagnoses and procedures
    diagnoses, procedures = create_diagnoses_and_procedures()
    
    cases = []
    case_templates = [
        {
            'case_title': 'Acute Myocardial Infarction',
            'category': 'Cardiology',
            'patient_age': 58,
            'patient_gender': 'M',
            'chief_complaint': 'Severe chest pain radiating to left arm, associated with sweating and nausea',
            'history_of_present_illness': '58-year-old male with history of hypertension and smoking presented with sudden onset severe chest pain. Pain started 2 hours ago, described as crushing sensation. Associated with diaphoresis and nausea.',
            'past_medical_history': 'Hypertension for 10 years, smoking 20 pack-years, family history of CAD',
            'physical_examination': 'BP 150/95, HR 95 bpm regular, no murmurs, clear lungs, no peripheral edema',
            'investigations': 'ECG showed ST elevation in leads II, III, aVF. Troponin elevated. Echo showed inferior wall hypokinesia.',
            'primary_diagnosis': 'Acute Myocardial Infarction',
            'differential_diagnosis': 'Aortic dissection, pulmonary embolism, pericarditis',
            'management_plan': 'Immediate aspirin 300mg, clopidogrel 600mg loading. Primary PCI performed. Started on dual antiplatelet therapy, statin, ACE inhibitor, and beta-blocker.',
            'clinical_reasoning': 'Classic presentation of STEMI. ECG findings consistent with inferior MI. Immediate reperfusion therapy indicated.',
            'learning_points': 'Recognition of STEMI, importance of timely reperfusion, post-MI medication management',
            'outcome': 'Patient underwent successful PCI. Discharged on day 3 with medications and lifestyle counseling.',
            'complexity': 'complex',
        },
        {
            'case_title': 'Acute Appendicitis',
            'category': 'General Surgery',
            'patient_age': 28,
            'patient_gender': 'F',
            'chief_complaint': 'Right lower quadrant abdominal pain for 18 hours',
            'history_of_present_illness': '28-year-old female with pain starting around umbilicus, migrating to RLQ. Associated with nausea, vomiting, and low-grade fever.',
            'past_medical_history': 'No significant past medical history',
            'physical_examination': 'Tender at McBurney point, positive Rovsing sign, rebound tenderness present, guarding noted',
            'investigations': 'CBC showed leukocytosis. CT abdomen confirmed appendicitis with no perforation.',
            'primary_diagnosis': 'Acute Appendicitis',
            'differential_diagnosis': 'Ovarian cyst rupture, PID, gastroenteritis, mesenteric adenitis',
            'management_plan': 'NPO, IV fluids, IV antibiotics. Emergency appendectomy performed laparoscopically. Post-op recovery uneventful.',
            'clinical_reasoning': 'Classic presentation and examination findings. CT confirmed diagnosis. Surgical intervention indicated.',
            'learning_points': 'Appendicitis diagnosis, surgical decision-making, laparoscopic appendectomy technique',
            'outcome': 'Successful laparoscopic appendectomy. Patient discharged on day 2 post-op.',
            'complexity': 'moderate',
        },
        {
            'case_title': 'Community-Acquired Pneumonia',
            'category': 'Internal Medicine',
            'patient_age': 72,
            'patient_gender': 'M',
            'chief_complaint': 'Fever, cough with productive sputum, and shortness of breath for 4 days',
            'history_of_present_illness': '72-year-old male with progressive respiratory symptoms. Productive cough with yellow-green sputum. Associated with fever and chills.',
            'past_medical_history': 'COPD, diabetes type 2, hypertension',
            'physical_examination': 'Febrile (38.5°C), tachypneic, decreased breath sounds and crackles in right lower lobe, oxygen saturation 88% on room air',
            'investigations': 'Chest X-ray showed right lower lobe consolidation. CBC showed leukocytosis. Blood cultures negative.',
            'primary_diagnosis': 'Pneumonia',
            'differential_diagnosis': 'Pulmonary embolism, heart failure, lung cancer, tuberculosis',
            'management_plan': 'Oxygen support, IV ceftriaxone and azithromycin. Improved on day 3, switched to oral antibiotics.',
            'clinical_reasoning': 'Clinical and radiological findings consistent with pneumonia. Appropriate antibiotic selection for CAP.',
            'learning_points': 'Pneumonia diagnosis, antibiotic selection, oxygen therapy, management in elderly with comorbidities',
            'outcome': 'Patient improved significantly. Discharged on day 5 with oral antibiotics and follow-up.',
            'complexity': 'moderate',
        },
    ]
    
    for idx, student in enumerate(students):
        # Get student's rotations and supervisor
        student_rotations = [r for r in rotations if r.pg == student]
        student_supervisor = student.supervisor if hasattr(student, 'supervisor') else supervisors[0]
        
        # Create 2-3 cases per student
        num_cases = 2 if idx == 0 else 3
        for case_idx in range(num_cases):
            template = case_templates[case_idx % len(case_templates)]
            rotation = student_rotations[case_idx % len(student_rotations)] if student_rotations else None
            category = next((c for c in categories if c.name == template['category']), categories[0])
            
            case_date = date.today() - timedelta(days=45 * (case_idx + 1))
            
            # Find matching diagnosis
            primary_diag = next((d for d in diagnoses if template['primary_diagnosis'].lower() in d.name.lower()), diagnoses[0])
            selected_procedures = procedures[:min(2, len(procedures))]
            
            case_data = {
                'pg': student,
                'case_title': template['case_title'],
                'category': category,
                'date_encountered': case_date,
                'rotation': rotation,
                'supervisor': student_supervisor,
                'patient_age': template['patient_age'],
                'patient_gender': template['patient_gender'],
                'chief_complaint': template['chief_complaint'],
                'history_of_present_illness': template['history_of_present_illness'],
                'past_medical_history': template['past_medical_history'],
                'physical_examination': template['physical_examination'],
                'investigations': template['investigations'],
                'primary_diagnosis': primary_diag,
                'differential_diagnosis': template['differential_diagnosis'],
                'management_plan': template['management_plan'],
                'clinical_reasoning': template['clinical_reasoning'],
                'learning_points': template['learning_points'],
                'outcome': template['outcome'],
                'complexity': template['complexity'],
                'status': 'approved' if case_idx == 0 else 'submitted',
            }
            
            case, created = ClinicalCase.objects.get_or_create(
                pg=student,
                case_title=template['case_title'],
                date_encountered=case_date,
                defaults=case_data
            )
            
            if created:
                # Add many-to-many relationships
                case.procedures_performed.set(selected_procedures)
                if len(diagnoses) > 1:
                    case.secondary_diagnoses.set([diagnoses[(case_idx + 1) % len(diagnoses)]])
                
                print(f"✓ Created clinical case: {case.case_title} for {student.username}")
            cases.append(case)
    
    return cases


@transaction.atomic
def main():
    """Main function to run all demo data creation"""
    print("=" * 70)
    print("SIMS Demo Data Preload Script")
    print("=" * 70)
    
    try:
        # Create users
        admin, supervisors, students = create_demo_users()
        
        # Create hospitals and departments
        hospitals, departments = create_hospitals_and_departments()
        
        # Create rotations
        rotations = create_rotations(admin, supervisors, students, hospitals, departments)
        
        # Create certificates
        certificates = create_certificates(admin, students)
        
        # Create logbook entries
        entries = create_logbook_entries(students, supervisors, rotations)
        
        # Create clinical cases
        cases = create_clinical_cases(students, supervisors, rotations)
        
        print("\n" + "=" * 70)
        print("✓ Demo data created successfully!")
        print("=" * 70)
        print("\nSummary:")
        print(f"  • Users: 1 admin, {len(supervisors)} supervisors, {len(students)} PG students")
        print(f"  • Hospitals: {len(hospitals)}")
        print(f"  • Departments: {len(departments)}")
        print(f"  • Rotations: {len(rotations)}")
        print(f"  • Certificates: {len(certificates)}")
        print(f"  • Logbook Entries: {len(entries)}")
        print(f"  • Clinical Cases: {len(cases)}")
        print("\nLogin Credentials:")
        print("  Admin:      username: admin,     password: admin123")
        print("  Supervisor: username: dr_smith,  password: supervisor123")
        print("  Supervisor: username: dr_jones,  password: supervisor123")
        print("  PG Student: username: pg_ahmed,  password: student123")
        print("  PG Student: username: pg_fatima, password: student123")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
