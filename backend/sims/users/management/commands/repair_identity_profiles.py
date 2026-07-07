from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model
from sims.users.models import AdminProfile, ResidentProfile, SupervisorProfile, SupportStaffProfile
from sims.users.services import recalculate_profile_completion, PROFILE_COMPLETION_REQUIREMENTS

User = get_user_model()


class Command(BaseCommand):
    help = "Scan and repair users and their profiles, ensuring one-to-one synchronization with no orphans."

    def handle(self, *args, **options):
        users = User.objects.all()
        scanned_count = users.count()
        
        admins_created = 0
        residents_created = 0
        supervisors_created = 0
        support_staff_created = 0
        invalid_users = 0
        duplicates_found = 0
        recalculated_count = 0
        
        with transaction.atomic():
            for user in users:
                role = user.role
                
                # Convert old role strings to final four choices
                if role not in ["ADMIN", "RESIDENT", "SUPERVISOR", "SUPPORT_STAFF"]:
                    role_lower = str(role).lower()
                    if role_lower in ["ADMIN", "ADMIN", "ADMIN", "ADMIN"]:
                        user.role = "ADMIN"
                    elif role_lower in ["SUPERVISOR", "SUPERVISOR", "SUPERVISOR"]:
                        user.role = "SUPERVISOR"
                    elif role_lower in ["student", "RESIDENT", "RESIDENT", "RESIDENT", "RESIDENT"]:
                        user.role = "RESIDENT"
                    elif role_lower in ["SUPPORT_STAFF", "SUPPORT_STAFF", "SUPPORT_STAFF", "SUPPORT_STAFF"]:
                        user.role = "SUPPORT_STAFF"
                    else:
                        self.stdout.write(self.style.WARNING(f"User {user.username} has invalid/unknown role: {role}"))
                        invalid_users += 1
                        continue
                    
                    user.save()
                    role = user.role

                # Retrieve existing profile objects
                profiles = {
                    "ADMIN": getattr(user, "admin_profile", None) if hasattr(user, "admin_profile") else None,
                    "RESIDENT": getattr(user, "resident_profile", None) if hasattr(user, "resident_profile") else None,
                    "SUPERVISOR": getattr(user, "supervisor_profile", None) if hasattr(user, "supervisor_profile") else None,
                    "SUPPORT_STAFF": getattr(user, "support_staff_profile", None) if hasattr(user, "support_staff_profile") else None,
                }
                
                # Clean up mismatching profiles (orphan prevention)
                for r, prof in list(profiles.items()):
                    if prof is not None and r != role:
                        prof.delete()
                        profiles[r] = None
                        self.stdout.write(self.style.WARNING(f"Deleted mismatched profile {prof.__class__.__name__} for user {user.username} (role={role})"))
                        duplicates_found += 1

                # Check if correct profile exists, create if missing
                correct_profile = profiles[role]
                if not correct_profile:
                    if role == "ADMIN":
                        AdminProfile.objects.create(user=user, profile_status="INCOMPLETE")
                        admins_created += 1
                    elif role == "RESIDENT":
                        ResidentProfile.objects.create(user=user, profile_status="INCOMPLETE")
                        residents_created += 1
                    elif role == "SUPERVISOR":
                        SupervisorProfile.objects.create(user=user, profile_status="INCOMPLETE")
                        supervisors_created += 1
                    elif role == "SUPPORT_STAFF":
                        SupportStaffProfile.objects.create(user=user, profile_status="INCOMPLETE")
                        support_staff_created += 1

                # Recalculate dynamic completion status
                recalculate_profile_completion(user)
                recalculated_count += 1

        self.stdout.write(f"Users scanned: {scanned_count}")
        self.stdout.write(f"Admin profiles created: {admins_created}")
        self.stdout.write(f"Resident profiles created: {residents_created}")
        self.stdout.write(f"Supervisor profiles created: {supervisors_created}")
        self.stdout.write(f"Support staff profiles created: {support_staff_created}")
        self.stdout.write(f"Invalid users found: {invalid_users}")
        self.stdout.write(f"Duplicate profiles found: {duplicates_found}")
        self.stdout.write(f"Completion states recalculated: {recalculated_count}")
        
        status_verdict = "PASS" if invalid_users == 0 else "FAIL"
        self.stdout.write(f"Final status: {status_verdict}")
