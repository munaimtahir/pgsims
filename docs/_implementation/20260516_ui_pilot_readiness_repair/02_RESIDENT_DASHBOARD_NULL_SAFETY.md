# Resident Dashboard Null Safety

## Problem

The resident dashboard dereferenced `summary.training_record` directly even when the cleaned baseline had no active resident record linked to the account.

## Fix

- Guarded the resident dashboard against missing `training_record` data.
- Added a calm empty state instead of a crash.
- Kept schedule and logbook links available so the page still feels intentional.

## User-Facing Fallback

- `No active resident training record is linked yet.`
- `This page will show your training progress once UTRMC/admin completes your setup.`
- `Please contact the UTRMC office if this is unexpected.`

