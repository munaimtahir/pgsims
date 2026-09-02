# Schema Fixes

## Files Changed

- `backend/sims/academics/serializers.py`
- `backend/sims/bulk/views.py`
- `backend/sims/notifications/views.py`
- `backend/sims/training/serializers.py`
- `backend/sims/training/views.py`
- `backend/sims/users/api_views.py`
- `backend/sims/users/userbase_serializers.py`
- `backend/sims/users/userbase_views.py`
- `backend/sims_project/settings.py`

## Changes

- Added explicit schema serializers for APIViews where `drf-spectacular` could not infer response/request shapes.
- Added named empty schema serializers to avoid blank component-name warnings.
- Added `swagger_fake_view` guards to queryset methods that evaluated request user or path kwargs during schema generation.
- Added return type hints for serializer method fields.
- Added a serializer-level `Decimal` min/max override for `StudentProfileSerializer.cgpa` to avoid DRF float validator warnings.
- Added explicit operation IDs for colliding bulk import and workshop endpoints.
- Added `CertificateStatusEnum` override for the shared issued/verified certificate status enum.

## Contract Impact

No API route, request payload, response payload, or frontend SDK shape was changed.

These are schema/introspection fixes only.

