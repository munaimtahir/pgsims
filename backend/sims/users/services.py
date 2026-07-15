import string
from django.db.models import Q
from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from sims.audit.models import ActivityLog
from .models import AdminProfile, ResidentProfile, SupervisorProfile, SupportStaffProfile

User = get_user_model()

PROFILE_COMPLETION_REQUIREMENTS = {
    "ADMIN": {
        "schema_version": 1,
        "profile_relation": "admin_profile",
        "required_fields": [
            {
                "field": "full_name",
                "label": "Full Name",
                "source": "user",
                "input_type": "text",
            },
            {
                "field": "phone",
                "label": "Phone Number",
                "source": "user",
                "input_type": "phone",
            },
            {
                "field": "email",
                "label": "Email",
                "source": "user",
                "input_type": "email",
            },
        ],
    },
    "RESIDENT": {
        "schema_version": 1,
        "profile_relation": "resident_profile",
        "required_fields": [
            {
                "field": "full_name",
                "label": "Full Name",
                "source": "user",
                "input_type": "text",
            },
            {
                "field": "phone",
                "label": "Phone Number",
                "source": "user",
                "input_type": "phone",
            },
            {
                "field": "email",
                "label": "Email",
                "source": "user",
                "input_type": "email",
            },
            {
                "field": "hospital",
                "label": "Hospital / Training Site",
                "source": "profile",
                "input_type": "select",
                "options_key": "hospitals",
                "help_text": "Select the primary hospital/training site.",
            },
            {
                "field": "department_ref",
                "label": "Department / Discipline",
                "source": "profile",
                "input_type": "select",
                "options_key": "departments",
                "help_text": "Select the primary department.",
            },
            {
                "field": "program_ref",
                "label": "Postgraduate Program",
                "source": "profile",
                "input_type": "select",
                "options_key": "programs",
                "help_text": "Select your postgraduate program.",
            },
            {
                "field": "academic_session_ref",
                "label": "Academic Session / Induction",
                "source": "profile",
                "input_type": "select",
                "options_key": "academic_sessions",
                "help_text": "Select your induction session.",
            },
        ],
    },
    "SUPERVISOR": {
        "schema_version": 1,
        "profile_relation": "supervisor_profile",
        "required_fields": [
            {
                "field": "full_name",
                "label": "Full Name",
                "source": "user",
                "input_type": "text",
            },
            {
                "field": "phone",
                "label": "Phone Number",
                "source": "user",
                "input_type": "phone",
            },
            {
                "field": "email",
                "label": "Email",
                "source": "user",
                "input_type": "email",
            },
            {
                "field": "hospital",
                "label": "Hospital / Training Site",
                "source": "profile",
                "input_type": "select",
                "options_key": "hospitals",
                "help_text": "Select the primary hospital/training site.",
            },
            {
                "field": "department_ref",
                "label": "Department / Discipline",
                "source": "profile",
                "input_type": "select",
                "options_key": "departments",
                "help_text": "Select the primary department.",
            },
            {
                "field": "designation_ref",
                "label": "Supervisor Designation",
                "source": "profile",
                "input_type": "select",
                "options_key": "designations",
                "help_text": "Select your academic/professional designation.",
            },
        ],
    },
    "SUPPORT_STAFF": {
        "schema_version": 1,
        "profile_relation": "support_staff_profile",
        "required_fields": [
            {
                "field": "full_name",
                "label": "Full Name",
                "source": "user",
                "input_type": "text",
            },
            {
                "field": "phone",
                "label": "Phone Number",
                "source": "user",
                "input_type": "phone",
            },
            {
                "field": "email",
                "label": "Email",
                "source": "user",
                "input_type": "email",
            },
        ],
    },
}


def generate_unique_username(role):
    prefix_map = {
        "ADMIN": "admin",
        "RESIDENT": "pgr",
        "SUPERVISOR": "sup",
        "SUPPORT_STAFF": "staff",
    }
    prefix = prefix_map.get(role, "user")
    
    i = 1
    while True:
        username = f"{prefix}{i:03d}"
        if not User.objects.filter(username=username).exists():
            return username
        i += 1


def get_missing_profile_fields(user):
    """
    Detect user role.
    Load correct profile.
    Read required-field registry.
    Check user and profile required fields.
    """
    role = user.role
    if role not in PROFILE_COMPLETION_REQUIREMENTS:
        return []

    req_config = PROFILE_COMPLETION_REQUIREMENTS[role]
    profile_relation = req_config["profile_relation"]
    profile = getattr(user, profile_relation, None)
    
    missing = []
    
    for req in req_config["required_fields"]:
        field_name = req["field"]
        source = req["source"]
        
        val = None
        if source == "user":
            if field_name == "full_name":
                val = user.get_full_name().strip()
            elif field_name == "phone":
                val = user.phone_number
            else:
                val = getattr(user, field_name, None)
        elif source == "profile":
            if profile:
                val = getattr(profile, field_name, None)
                
        if val is None or val == "":
            missing.append({
                "field": field_name,
                "label": req["label"],
                "source": source,
                "input_type": req["input_type"],
                "required": True,
                "options_key": req.get("options_key"),
                "help_text": req.get("help_text", ""),
            })
            
    return missing


def recalculate_profile_completion(user):
    """
    Recalculates profile completion state from registry and updates User and Profile objects.
    """
    role = user.role
    if role not in PROFILE_COMPLETION_REQUIREMENTS:
        return

    req_config = PROFILE_COMPLETION_REQUIREMENTS[role]
    profile_relation = req_config["profile_relation"]
    profile = getattr(user, profile_relation, None)
    if not profile:
        return

    missing = get_missing_profile_fields(user)
    current_schema_version = req_config["schema_version"]

    if missing:
        user.is_profile_complete = False
        user.is_complete_profile = False
        profile.profile_status = "INCOMPLETE"
        profile.save()
        user.save()
    else:
        user.is_profile_complete = True
        user.is_complete_profile = True
        profile.profile_status = "COMPLETE"
        profile.completed_schema_version = current_schema_version
        if not profile.profile_completed_at:
            profile.profile_completed_at = timezone.now()
        profile.save()
        user.save()


def create_user_with_profile(
    *,
    role,
    username=None,
    password=None,
    full_name,
    email=None,
    phone=None,
    profile_payload=None,
    actor=None,
    source="manual",
):
    """
    Service to universally create a User + Profile + AuditLog atomically.
    """
    valid_roles = ["ADMIN", "RESIDENT", "SUPERVISOR", "SUPPORT_STAFF"]
    if role not in valid_roles:
        raise ValidationError(f"Invalid role: {role}")

    profile_payload = profile_payload or {}

    with transaction.atomic():
        # Generate username if not provided
        if not username:
            username = generate_unique_username(role)
        elif User.objects.filter(username=username).exists():
            raise ValidationError(f"Username {username} already exists.")

        # Set default temporary password if not provided
        if not password:
            password = "pgfmu123"

        names = full_name.strip().split(" ", 1)
        first_name = names[0]
        last_name = names[1] if len(names) > 1 else ""

        # Create User
        user = User.objects.create(
            username=username,
            email=email or "",
            phone_number=phone or "",
            first_name=first_name,
            last_name=last_name,
            role=role,
            must_change_password=True,
            is_profile_complete=False,
            is_complete_profile=False,
            is_active=True,
        )
        user.set_password(password)
        user.save()

        # Create Profile
        profile = None
        if role == "ADMIN":
            profile = AdminProfile.objects.create(
                user=user,
                designation=profile_payload.get("designation", ""),
                phone=profile_payload.get("phone", phone or ""),
                email=profile_payload.get("email", email or ""),
                admin_scope=profile_payload.get("admin_scope", ""),
                profile_status="INCOMPLETE",
                created_by=actor,
            )
        elif role == "RESIDENT":
            academic_session_val = profile_payload.get("academic_session_ref")
            if isinstance(academic_session_val, str) and academic_session_val:
                from sims.academics.models import AcademicSession
                academic_session_ref = AcademicSession.objects.filter(Q(code=academic_session_val) | Q(name=academic_session_val)).first()
            else:
                academic_session_ref = academic_session_val

            specialty_val = profile_payload.get("specialty_ref")
            if isinstance(specialty_val, str) and specialty_val:
                from sims.academics.models import Specialty
                specialty_ref = Specialty.objects.filter(Q(code=specialty_val) | Q(name=specialty_val)).first()
            else:
                specialty_ref = specialty_val

            profile = ResidentProfile.objects.create(
                user=user,
                registration_no=profile_payload.get("registration_no"),
                cnic=profile_payload.get("cnic"),
                phone=profile_payload.get("phone", phone or ""),
                email=profile_payload.get("email", email or ""),
                hospital=profile_payload.get("hospital"),
                department_ref=profile_payload.get("department_ref"),
                program_ref=profile_payload.get("program_ref"),
                academic_session_ref=academic_session_ref,
                specialty_ref=specialty_ref,
                profile_status="INCOMPLETE",
                created_by=actor,
            )
        elif role == "SUPERVISOR":
            designation_val = profile_payload.get("designation_ref")
            if isinstance(designation_val, str) and designation_val:
                from sims.academics.models import Designation
                designation_ref = Designation.objects.filter(Q(code=designation_val) | Q(name=designation_val)).first()
            else:
                designation_ref = designation_val

            specialty_val = profile_payload.get("specialty_ref")
            if isinstance(specialty_val, str) and specialty_val:
                from sims.academics.models import Specialty
                specialty_ref = Specialty.objects.filter(Q(code=specialty_val) | Q(name=specialty_val)).first()
            else:
                specialty_ref = specialty_val

            profile = SupervisorProfile.objects.create(
                user=user,
                pmdc_no=profile_payload.get("pmdc_no"),
                official_email=profile_payload.get("official_email", ""),
                phone=profile_payload.get("phone", phone or ""),
                email=profile_payload.get("email", email or ""),
                hospital=profile_payload.get("hospital"),
                department_ref=profile_payload.get("department_ref"),
                designation_ref=designation_ref,
                program_ref=profile_payload.get("program_ref"),
                specialty_ref=specialty_ref,
                profile_status="INCOMPLETE",
                created_by=actor,
            )
        elif role == "SUPPORT_STAFF":
            profile = SupportStaffProfile.objects.create(
                user=user,
                designation=profile_payload.get("designation"),
                department_ref=profile_payload.get("department_ref"),
                hospital=profile_payload.get("hospital"),
                phone=profile_payload.get("phone", phone or ""),
                email=profile_payload.get("email", email or ""),
                scope_notes=profile_payload.get("scope_notes", ""),
                profile_status="INCOMPLETE",
                created_by=actor,
            )

        # Audit event logs
        ActivityLog.log(
            actor=actor,
            action="create",
            verb="USER_CREATED",
            target=user,
            metadata={"role": role, "username": username, "source": source}
        )

        ActivityLog.log(
            actor=actor,
            action="create",
            verb="PROFILE_CREATED",
            target=profile,
            metadata={"role": role, "profile_type": profile.__class__.__name__, "profile_id": profile.id, "source": source}
        )

        ActivityLog.log(
            actor=actor,
            action="create",
            verb="IDENTITY_CREATED",
            target=user,
            metadata={"role": role, "profile_type": profile.__class__.__name__, "profile_id": profile.id, "source": source}
        )

        recalculate_profile_completion(user)
        user.refresh_from_db()
        return user
