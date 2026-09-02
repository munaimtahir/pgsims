# Pilot Seed Data

This document records the Brick 7 pilot seed assumptions.

## Seed Goal

Provide a minimal, reproducible supervision graph for verification:

- at least one resident
- at least one supervisor
- at least one active primary assignment
- optional co-supervisor rows
- audit records for seeded actions

## Seed Command

The supervision stack is exercised through the existing seed/test fixtures and the supervision management command:

- `python3 backend/manage.py repair_identity_profiles`
- supervision test fixtures
- legacy pilot seeding paths used by the broader project

## Notes

- The new supervision app can operate without seed data, but the dashboard is easier to verify when at least one assignment exists.
- Pilot seeding must respect the same hospital and department matching rules as manual assignment creation.
