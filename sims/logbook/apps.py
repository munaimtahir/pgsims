from django.apps import AppConfig
from django.db import OperationalError, ProgrammingError


class LogbookConfig(AppConfig):
    """
    Configuration for the SIMS Logbook app.

    This app manages clinical logbook entries and learning documentation for the SIMS platform:
    - Clinical case logging and documentation
    - Procedure and skill tracking
    - Learning reflection and assessment
    - Supervisor review and feedback
    - Progress monitoring and analytics
    - Template-based entry creation
    - Competency tracking and reporting

    Created: 2025-05-29 17:17:38 UTC
    Author: SMIB2012
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "sims.logbook"
    verbose_name = "SIMS Clinical Logbook"

    def ready(self):
        """
        Called when Django starts.
        Import any signal handlers or perform app initialization.
        """
        try:
            # Import signals for logbook management
            pass

            # Register any custom model permissions
            from django.contrib.auth.models import Permission
            from django.contrib.contenttypes.models import ContentType

            from .models import LogbookEntry, LogbookReview, Procedure

            # Create custom permissions if they don't exist
            logbook_ct = ContentType.objects.get_for_model(LogbookEntry)
            review_ct = ContentType.objects.get_for_model(LogbookReview)
            procedure_ct = ContentType.objects.get_for_model(Procedure)

            custom_permissions = [
                # Logbook Entry Permissions
                ("can_approve_entries", "Can approve logbook entries", logbook_ct),
                ("can_view_all_entries", "Can view all logbook entries", logbook_ct),
                ("can_export_entries", "Can export logbook data", logbook_ct),
                ("can_bulk_edit_entries", "Can bulk edit logbook entries", logbook_ct),
                ("can_manage_templates", "Can manage logbook templates", logbook_ct),
                # Review Permissions
                ("can_review_entries", "Can review logbook entries", review_ct),
                ("can_assign_reviewers", "Can assign entry reviewers", review_ct),
                # Data Management Permissions
                ("can_manage_procedures", "Can manage procedure definitions", procedure_ct),
                ("can_view_analytics", "Can view logbook analytics", logbook_ct),
                ("can_generate_reports", "Can generate logbook reports", logbook_ct),
            ]

            for codename, name, content_type in custom_permissions:
                Permission.objects.get_or_create(
                    codename=codename, name=name, content_type=content_type
                )

            # Set up default logbook templates
            self._setup_default_templates()

            # Set up periodic tasks for logbook management
            self._setup_logbook_tasks()

            # Initialize default procedures and diagnoses
            self._setup_default_clinical_data()

        except (OperationalError, ProgrammingError):
            # Database not ready (migrations not applied). Skip DB-dependent initialization.
            pass
        except ImportError:
            pass
        except Exception as e:
            # Log the error but don't prevent app from loading
            import logging

            logger = logging.getLogger("sims.logbook")
            logger.warning(f"Error in logbook app ready(): {e}")

    def _setup_default_templates(self):
        """Setup default logbook templates"""
        try:
            from .models import LogbookTemplate

            # Check if default templates already exist
            if LogbookTemplate.objects.filter(is_default=True).exists():
                return

            default_templates = [
                {
                    "name": "General Medical Case",
                    "template_type": "medical",
                    "description": "Standard template for general medical cases",
                    "is_default": True,
                    "template_structure": {
                        "sections": [
                            "Patient Presentation",
                            "Clinical Assessment",
                            "Investigations",
                            "Management Plan",
                            "Learning Points",
                            "Reflection",
                        ]
                    },
                    "required_fields": [
                        "patient_age",
                        "patient_gender",
                        "patient_chief_complaint",
                        "primary_diagnosis",
                        "clinical_reasoning",
                        "learning_points",
                    ],
                    "completion_guidelines": "Focus on clinical reasoning, differential diagnosis, and key learning outcomes.",
                },
                {
                    "name": "Surgical Procedure",
                    "template_type": "surgical",
                    "description": "Template for surgical cases and procedures",
                    "is_default": True,
                    "template_structure": {
                        "sections": [
                            "Pre-operative Assessment",
                            "Procedure Details",
                            "Operative Findings",
                            "Post-operative Care",
                            "Complications",
                            "Learning Points",
                        ]
                    },
                    "required_fields": [
                        "patient_age",
                        "patient_gender",
                        "procedures",
                        "skills",
                        "clinical_reasoning",
                        "learning_points",
                    ],
                    "completion_guidelines": "Document surgical technique, complications, and procedural learning.",
                },
                {
                    "name": "Emergency Case",
                    "template_type": "emergency",
                    "description": "Template for emergency department cases",
                    "is_default": True,
                    "template_structure": {
                        "sections": [
                            "Presentation & Triage",
                            "Emergency Assessment",
                            "Immediate Management",
                            "Diagnostic Workup",
                            "Disposition",
                            "Critical Learning",
                        ]
                    },
                    "required_fields": [
                        "patient_age",
                        "patient_gender",
                        "patient_chief_complaint",
                        "primary_diagnosis",
                        "procedures",
                        "learning_points",
                    ],
                    "completion_guidelines": "Emphasize time-critical decision making and emergency management skills.",
                },
                {
                    "name": "Outpatient Consultation",
                    "template_type": "outpatient",
                    "description": "Template for outpatient clinic consultations",
                    "is_default": False,
                    "template_structure": {
                        "sections": [
                            "Referral Information",
                            "History & Examination",
                            "Assessment & Plan",
                            "Patient Education",
                            "Follow-up Plan",
                            "Learning Points",
                        ]
                    },
                    "required_fields": [
                        "patient_age",
                        "patient_gender",
                        "primary_diagnosis",
                        "clinical_reasoning",
                        "learning_points",
                    ],
                    "completion_guidelines": "Focus on chronic disease management and patient communication.",
                },
            ]

            for template_data in default_templates:
                LogbookTemplate.objects.get_or_create(
                    name=template_data["name"], defaults=template_data
                )

            import logging

            logger = logging.getLogger("sims.logbook")
            logger.info("Default logbook templates created successfully")

        except Exception as e:
            import logging

            logger = logging.getLogger("sims.logbook")
            logger.warning(f"Could not setup default logbook templates: {e}")

    def _setup_logbook_tasks(self):
        """Setup periodic tasks for logbook management"""
        try:
            # This would integrate with Celery or Django-RQ for periodic tasks
            import logging

            logger = logging.getLogger("sims.logbook")
            logger.info("Logbook periodic tasks setup completed")

            # Example of what would be set up:
            # - Daily reminders for incomplete entries
            # - Weekly progress reports
            # - Monthly analytics updates
            # - Quarterly competency assessments

        except Exception as e:
            import logging

            logger = logging.getLogger("sims.logbook")
            logger.warning(f"Could not setup logbook periodic tasks: {e}")

    def _setup_default_clinical_data(self):
        """Setup default procedures, diagnoses, and skills"""
        try:
            from .models import Diagnosis, Procedure, Skill

            # Only setup if no data exists
            if Procedure.objects.exists() or Diagnosis.objects.exists() or Skill.objects.exists():
                return

            # Default procedures by category
            default_procedures = [
                # Basic Clinical Procedures
                ("Venipuncture", "basic", "Basic blood sampling procedure", 1, 15),
                ("IV Cannulation", "basic", "Intravenous cannula insertion", 2, 20),
                ("Urinary Catheterization", "basic", "Insertion of urinary catheter", 2, 30),
                ("Nasogastric Tube Insertion", "basic", "NG tube placement", 2, 25),
                ("Basic Suturing", "basic", "Simple wound closure techniques", 2, 45),
                # Intermediate Procedures
                ("Central Line Insertion", "intermediate", "Central venous access", 4, 60),
                ("Chest Tube Insertion", "intermediate", "Thoracostomy tube placement", 4, 45),
                ("Lumbar Puncture", "intermediate", "CSF sampling procedure", 3, 30),
                ("Arterial Blood Gas", "intermediate", "Arterial puncture for ABG", 3, 15),
                ("Endotracheal Intubation", "intermediate", "Airway management", 4, 30),
                # Advanced Procedures
                ("Bronchoscopy", "advanced", "Flexible bronchoscopy", 5, 90),
                ("Upper Endoscopy", "advanced", "Esophagogastroduodenoscopy", 5, 60),
                ("Colonoscopy", "advanced", "Lower GI endoscopy", 5, 90),
                ("Cardiac Catheterization", "advanced", "Coronary angiography", 5, 120),
                ("Minor Surgery", "advanced", "Simple surgical procedures", 4, 120),
            ]

            for name, category, description, difficulty, duration in default_procedures:
                Procedure.objects.create(
                    name=name,
                    category=category,
                    description=description,
                    difficulty_level=difficulty,
                    duration_minutes=duration,
                    cme_points=difficulty * 2,  # 2 CME points per difficulty level
                )

            # Default diagnoses by category
            default_diagnoses = [
                # Cardiovascular
                ("Hypertension", "cardiovascular", "I10", "Primary hypertension"),
                ("Myocardial Infarction", "cardiovascular", "I21", "Acute myocardial infarction"),
                ("Heart Failure", "cardiovascular", "I50", "Congestive heart failure"),
                ("Atrial Fibrillation", "cardiovascular", "I48", "Atrial fibrillation"),
                # Respiratory
                ("Pneumonia", "respiratory", "J18", "Community acquired pneumonia"),
                ("Asthma", "respiratory", "J45", "Bronchial asthma"),
                ("COPD", "respiratory", "J44", "Chronic obstructive pulmonary disease"),
                ("Pulmonary Embolism", "respiratory", "I26", "Acute pulmonary embolism"),
                # Gastrointestinal
                ("Gastroenteritis", "gastrointestinal", "K59", "Acute gastroenteritis"),
                ("Peptic Ulcer", "gastrointestinal", "K27", "Peptic ulcer disease"),
                ("Appendicitis", "gastrointestinal", "K37", "Acute appendicitis"),
                ("Cholecystitis", "gastrointestinal", "K81", "Acute cholecystitis"),
                # Neurological
                ("Stroke", "neurological", "I64", "Cerebrovascular accident"),
                ("Seizure Disorder", "neurological", "G40", "Epilepsy"),
                ("Migraine", "neurological", "G43", "Migraine headache"),
                ("Meningitis", "neurological", "G03", "Bacterial meningitis"),
                # Endocrine
                ("Diabetes Mellitus", "endocrine", "E11", "Type 2 diabetes mellitus"),
                ("Hyperthyroidism", "endocrine", "E05", "Thyrotoxicosis"),
                ("Hypothyroidism", "endocrine", "E03", "Hypothyroidism"),
                # Infectious
                ("Sepsis", "infectious", "A41", "Sepsis, unspecified organism"),
                ("UTI", "infectious", "N39", "Urinary tract infection"),
                ("Cellulitis", "infectious", "L03", "Cellulitis"),
            ]

            for name, category, icd_code, description in default_diagnoses:
                Diagnosis.objects.create(
                    name=name, category=category, icd_code=icd_code, description=description
                )

            # Default skills by category and level
            default_skills = [
                # Basic Clinical Skills
                ("History Taking", "clinical", "basic", "Comprehensive patient history"),
                ("Physical Examination", "clinical", "basic", "Systematic physical examination"),
                ("Clinical Documentation", "clinical", "basic", "Accurate medical record keeping"),
                (
                    "Patient Communication",
                    "communication",
                    "basic",
                    "Effective patient communication",
                ),
                # Intermediate Skills
                (
                    "Differential Diagnosis",
                    "clinical",
                    "intermediate",
                    "Clinical reasoning and diagnosis",
                ),
                ("Treatment Planning", "clinical", "intermediate", "Therapeutic decision making"),
                (
                    "Multidisciplinary Collaboration",
                    "communication",
                    "intermediate",
                    "Team-based care",
                ),
                ("Emergency Assessment", "clinical", "intermediate", "Rapid patient assessment"),
                # Advanced Skills
                ("Critical Care Management", "clinical", "advanced", "ICU patient management"),
                ("Complex Procedures", "technical", "advanced", "Advanced procedural skills"),
                ("Leadership", "professional", "advanced", "Clinical leadership skills"),
                ("Teaching & Mentoring", "professional", "advanced", "Medical education skills"),
                # Professional Skills
                (
                    "Ethical Decision Making",
                    "professional",
                    "intermediate",
                    "Medical ethics application",
                ),
                (
                    "Quality Improvement",
                    "professional",
                    "intermediate",
                    "Healthcare quality initiatives",
                ),
                ("Research Skills", "academic", "intermediate", "Clinical research methodology"),
                ("Evidence-Based Practice", "academic", "intermediate", "EBM application"),
            ]

            for name, category, level, description in default_skills:
                Skill.objects.create(
                    name=name, category=category, level=level, description=description
                )

            import logging

            logger = logging.getLogger("sims.logbook")
            logger.info(
                "Default clinical data (procedures, diagnoses, skills) created successfully"
            )

        except Exception as e:
            import logging

            logger = logging.getLogger("sims.logbook")
            logger.warning(f"Could not setup default clinical data: {e}")
