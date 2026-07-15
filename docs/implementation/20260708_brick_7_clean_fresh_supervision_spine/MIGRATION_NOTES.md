# MIGRATION NOTES — PGMS Brick 7 Clean Fresh Pilot Supervision Spine

This document outlines the database schema migrations for **Brick 7**.

---

## 1. Migration Strategy

- **Fresh Supervision App**:
  - We will create a new Django app `supervision` inside `backend/sims/supervision/`.
  - The new model `ResidentSupervisorAssignment` will be defined inside this app.
  - A clean Django migration will be generated: `python manage.py makemigrations supervision`.
- **Legacy Models**:
  - The legacy `SupervisorResidentLink` model located in `sims/users/models.py` is ignored and left unchanged to prevent breaking existing code or historic migrations. No schema tables are altered for this model.
- **Seeding/Baseline**:
  - After running the migrations (`python manage.py migrate`), we can baseline the database using our seed command: `python manage.py seed_pilot_supervision`.
