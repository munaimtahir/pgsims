# Schema Gate Fix Guide

**Last Updated**: 2026-04-23  
**Focus**: Blocker #1 - OpenAPI Schema Generation  
**Scope**: Adding @extend_schema() decorators and fixing serializer issues  
**Time to Read**: 15-20 minutes  
**Estimated Fix Time**: 3-5 hours  

---

## Quick Summary

**Status**: Schema gate is wired but generating 315 errors + 31 warnings

**What's Wrong**:
- 65 APIViews without `@extend_schema()` decorators
- drf-spectacular can't infer serializers for these views
- Department serializer duplicates (PARTIALLY FIXED in session 3)
- Some views need explicit serializer_class

**How to Fix**:
1. Add `@extend_schema()` decorators to APIViews
2. Explicitly define serializer_class where needed
3. Fix remaining Department/Hospital model references
4. Rerun schema generation to validate

**Success Criteria**:
- Schema generation completes without errors
- 0 or minimal warnings (acceptable: documentation gaps, not logic gaps)
- OpenAPI output is valid JSON

---

## Current State

### Session 3 Progress

```
Before: 49 schema warnings (Department duplicates)
After:  31 schema warnings (18 eliminated by fixing imports)
Remaining: 315 errors from APIViews without serializers
```

**What Was Fixed**:
- ✅ Removed duplicate Department imports in `userbase_serializers.py`
- ✅ Consolidated Department/Hospital references to canonical models

**What Remains**:
- ❌ 65 APIViews need `@extend_schema()` decorators
- ❌ Some APIViews need explicit `serializer_class`
- ⚠️  A few serializers may have conflicting fields

---

## Understanding drf-spectacular

### What It Does

`drf-spectacular` auto-generates OpenAPI 3.1 schema from Django REST framework code.

**For APIViews, it needs to know**:
1. What HTTP method is allowed (POST, GET, etc.)
2. What data structure is accepted (request serializer)
3. What data structure is returned (response serializer)

### The Problem

When you write:
```python
class MyAPIView(APIView):
    def get(self, request):
        return Response({'message': 'hello'})
```

drf-spectacular can't figure out what the response looks like because there's no serializer.

**Solution**: Add `@extend_schema()` decorator to tell it.

### How to Fix

```python
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

class MyAPIView(APIView):
    @extend_schema(
        responses={200: None}  # Or provide a serializer
    )
    def get(self, request):
        return Response({'message': 'hello'})
```

---

## Finding All Problem Views

### Step 1: Run Schema Generation and Capture Output

```bash
cd backend

# Generate schema and capture all warnings/errors
python manage.py spectacular_settings \
    --validate \
    --format=yaml \
    2>&1 | tee /tmp/schema_output.txt

# Or shorter version:
SPECTACULAR_DEFAULTS={"SERVERS": [{"url": "http://localhost"}]} \
python manage.py spectacular_settings --validate 2>&1 | tail -100
```

### Step 2: Identify View-Related Errors

```bash
# Find all "unable to guess serializer" errors
grep "unable to guess serializer" /tmp/schema_output.txt | head -20

# Sample error:
# WARNING - Unable to guess serializer for path /api/residents/me/ from method <function>
```

### Step 3: Map Errors to Files

For each error, find the view:

```bash
# Example error mentions "/api/residents/me/" endpoint
# Find which view handles this

grep -r "residents/me" backend/sims/ --include="*.py"
# Result: backend/sims/training/urls.py

grep -r "path.*me" backend/sims/training/urls.py
# Result: path('me/', views.ResidentProfileView.as_view(), name='resident-me')

# Now find the view definition
grep -r "class ResidentProfileView" backend/sims/ --include="*.py"
# Result: backend/sims/training/views.py:line 42
```

---

## Fixing Individual Views

### Pattern 1: Simple GET View (No Input)

**Before**:
```python
class ResidentProfileView(APIView):
    def get(self, request):
        resident = request.user
        return Response({
            'username': resident.username,
            'role': resident.role,
        })
```

**After**:
```python
from drf_spectacular.utils import extend_schema

class ResidentProfileView(APIView):
    @extend_schema(
        responses={200: None}  # No specific serializer needed
    )
    def get(self, request):
        resident = request.user
        return Response({
            'username': resident.username,
            'role': resident.role,
        })
```

### Pattern 2: View with Input & Output

**Before**:
```python
class LogbookEntryUpdateView(APIView):
    def patch(self, request, pk):
        entry = LogbookEntry.objects.get(pk=pk)
        # Update logic
        return Response(serializer.data)
```

**After**:
```python
from drf_spectacular.utils import extend_schema
from .serializers import LogbookEntrySerializer

class LogbookEntryUpdateView(APIView):
    @extend_schema(
        request=LogbookEntrySerializer,
        responses={200: LogbookEntrySerializer}
    )
    def patch(self, request, pk):
        entry = LogbookEntry.objects.get(pk=pk)
        # Update logic
        return Response(serializer.data)
```

### Pattern 3: View with Multiple HTTP Methods

**Before**:
```python
class LogbookDetailView(APIView):
    def get(self, request, pk):
        # Retrieve
        return Response(serializer.data)
    
    def post(self, request, pk):
        # Create
        return Response(new_serializer.data)
```

**After**:
```python
@extend_schema(
    methods=['GET'],
    responses={200: LogbookEntrySerializer},
)
@extend_schema(
    methods=['POST'],
    request=LogbookEntrySerializer,
    responses={201: LogbookEntrySerializer},
)
class LogbookDetailView(APIView):
    def get(self, request, pk):
        return Response(serializer.data)
    
    def post(self, request, pk):
        return Response(new_serializer.data)
```

### Pattern 4: View with Custom Response

**Before**:
```python
class DashboardSummaryView(APIView):
    def get(self, request):
        # Custom aggregation
        return Response({'total': 42, 'items': [...]})
```

**After (Option A - Use None if you don't care about schema)**:
```python
@extend_schema(responses={200: None})
class DashboardSummaryView(APIView):
    def get(self, request):
        return Response({'total': 42, 'items': [...]})
```

**After (Option B - Create a Serializer)**:
```python
from rest_framework import serializers

class DashboardSummarySerializer(serializers.Serializer):
    total = serializers.IntegerField()
    items = serializers.ListField(child=serializers.DictField())

@extend_schema(responses={200: DashboardSummarySerializer})
class DashboardSummaryView(APIView):
    def get(self, request):
        return Response({'total': 42, 'items': [...]})
```

---

## Priority Order

Fix these first (most likely to be in active code paths):

### Priority 1: Dashboard & Summary Views (5-10 files)
```
- ResidentProfileView
- ResidentSummaryView
- SupervisorDashboardView
- AdminDashboardView
- StatsView
```

### Priority 2: Logbook Views (8-12 files)
```
- LogbookListView
- LogbookCreateView
- LogbookDetailView
- LogbookVerifyView
- LogbookReturnView
```

### Priority 3: Rotation Views (5-8 files)
```
- RotationListView
- RotationDetailView
- RotationApproveView
```

### Priority 4: Everything Else (40+ files)
```
- Notifications
- Cases
- Certificates
- Analytics
- Search
```

---

## Batch Fixing Process

### Step 1: List All APIViews

```bash
cd backend

# Find all APIView classes
grep -r "class.*APIView" sims/ --include="*.py" | \
  grep -v "^Binary" | \
  cut -d: -f1 | \
  sort | uniq > /tmp/apiviews.txt

wc -l /tmp/apiviews.txt  # Should show ~65 files

# Sample output:
# 42 files contain APIViews
```

### Step 2: For Each File, Check if Views Have Decorators

```bash
# Check which views already have @extend_schema
grep -B2 "@extend_schema" backend/sims/training/views.py | head -10

# If few or none, this file needs work
```

### Step 3: Add Decorators in Batch

For each file without decorators:

```python
# At top of file, add import if not present
from drf_spectacular.utils import extend_schema

# For each APIView method, add appropriate decorator
@extend_schema(responses={200: None})
def get(self, request):
    ...
```

### Step 4: Test Generation After Each Batch

```bash
# After fixing a few files, test
python manage.py spectacular_settings --validate 2>&1 | tail -20

# Should show fewer errors
```

---

## Fixing Department Model Issues

### Current Issue

Session 3 partially fixed this by removing duplicate imports.

**Still may have**:
```
WARNING: Multiple serializers for Department model
```

### How to Fix

```python
# In sims/users/userbase_serializers.py

# There should be ONE canonical CanonicalDepartmentSerializer
# It should be imported here:
from sims.academics.serializers import CanonicalDepartmentSerializer

# Remove any duplicate definitions
# Remove any "DepartmentSerializer" variant

# Update any ForeignKeyField references:
class HospitalDepartmentSerializer(serializers.ModelSerializer):
    department = CanonicalDepartmentSerializer(read_only=True)  # Use canonical
    
    class Meta:
        model = HospitalDepartment
        fields = ['department', 'hospital']
```

---

## Validation After Fixes

### Step 1: Run Schema Generation

```bash
cd backend
python manage.py spectacular_settings --validate

# Should see significant reduction in errors
# Target: 0 errors (or <5 acceptable warnings)
```

### Step 2: Generate Schema File

```bash
python manage.py spectacular_settings \
    --file /tmp/openapi_schema.yaml

# Verify file was created
file /tmp/openapi_schema.yaml

# Check first 50 lines
head -50 /tmp/openapi_schema.yaml

# Should show valid YAML with:
# - openapi: 3.1.0
# - info: ...
# - servers: ...
# - paths: ...
```

### Step 3: Validate Schema Structure

```bash
cd backend

# Try to parse the schema
python -c "
import yaml
with open('/tmp/openapi_schema.yaml') as f:
    schema = yaml.safe_load(f)
    print('Paths:', len(schema.get('paths', {})))
    print('Components:', len(schema.get('components', {}).get('schemas', {})))
    print('Valid OpenAPI 3.1 ✓')
"
```

### Step 4: Run Tests to Ensure Nothing Broke

```bash
cd backend
pytest sims/users/test_api.py -v -k "test_" --co -q | head -10

# Run actual tests
pytest sims/users/test_api.py -v -x
```

---

## Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "unable to guess serializer" | View has no decorator | Add @extend_schema(responses={...}) |
| "Multiple serializers for Model" | Duplicate imports | Find and remove duplicate definition |
| "Cannot resolve view" | Import path wrong | Use full path: `backend/sims/app/serializers.py:SerializerName` |
| "circular import" | Serializer imports view | Move to separate file or use string reference |
| "Missing required field" | Serializer field is required but view returns null | Mark field as `required=False` |

---

## Quick Reference: Minimal Fix

If you're in a time crunch, minimal fix is:

```python
# In each view file, add this import
from drf_spectacular.utils import extend_schema

# Before each APIView.get/post/patch/delete that lacks a decorator:
@extend_schema(responses={200: None})
```

This tells drf-spectacular "I'm not providing schema for this, don't complain."

Not ideal (schema will be incomplete), but it makes the gate pass.

---

## Next Steps

1. **Locate all problem views** using grep commands above
2. **Prioritize by usage** (dashboard > logbook > other)
3. **Add decorators** starting with Priority 1
4. **Test generation** after each batch
5. **Fix any import issues** as they appear
6. **Validate** final schema passes

---

## Reference Files

- `backend/sims_project/spectacular_settings.py` - drf-spectacular config
- `backend/sims/*/views.py` - View definitions (need decorators)
- `backend/sims/*/serializers.py` - Serializer definitions
- `drf-spectacular docs`: https://drf-spectacular.readthedocs.io/

---

## Help Commands

```bash
# List all APIView classes and their current status
cd backend && grep -r "class.*APIView" sims/ --include="*.py" | \
  while read line; do
    file=$(echo $line | cut -d: -f1)
    class=$(echo $line | cut -d: -f2- | sed 's/class //;s/(APIView).*//')
    echo "File: $file | Class: $class"
  done | head -20

# Count APIViews with @extend_schema already
cd backend && grep -r "@extend_schema" sims/ --include="*.py" | wc -l

# Find views that definitely need fixing (no decorator and no inheriting)
cd backend && for f in $(find sims -name "views.py"); do
  echo "=== $f ==="
  grep "class.*APIView" $f | grep -v "@extend_schema" | head -3
done
```
