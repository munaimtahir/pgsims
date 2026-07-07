# Profile Requirement Registry — Update 0

## Required Fields Registry
All fields classified as required for onboarding are registered centrally in `backend/sims/users/services.py` under `PROFILE_COMPLETION_REQUIREMENTS`.

### ADMIN
* `full_name` (user model, text)
* `phone` (user model, phone)
* `email` (user model, email)

### RESIDENT
* `full_name` (user model, text)
* `phone` (user model, phone)
* `email` (user model, email)

### SUPERVISOR
* `full_name` (user model, text)
* `phone` (user model, phone)
* `email` (user model, email)

### SUPPORT_STAFF
* `full_name` (user model, text)
* `phone` (user model, phone)
* `email` (user model, email)
