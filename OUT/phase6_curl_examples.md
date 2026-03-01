# Phase 6 — Curl Examples

## Authentication
```bash
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}' | jq -r '.access')
```

## Programs
```bash
# List programs
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/programs/

# Get program policy
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/programs/1/policy/

# Update program policy
curl -X PUT -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  http://localhost:8000/api/programs/1/policy/ \
  -d '{"allow_program_change":false,"imm_allowed_from_month":24,"final_allowed_from_month":48}'

# List milestones
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/programs/1/milestones/
```

## Research Project (resident)
```bash
# Create research project
curl -X POST -H "Authorization: Bearer $PG_TOKEN" -H "Content-Type: application/json" \
  http://localhost:8000/api/my/research/ \
  -d '{"title":"Effect of laparoscopy on outcomes","topic_area":"Urology"}'

# Submit to supervisor
curl -X POST -H "Authorization: Bearer $PG_TOKEN" -H "Content-Type: application/json" \
  http://localhost:8000/api/my/research/action/submit-to-supervisor/ -d '{}'

# Supervisor approves
curl -X POST -H "Authorization: Bearer $SUP_TOKEN" -H "Content-Type: application/json" \
  http://localhost:8000/api/my/research/action/supervisor-approve/ \
  -d '{"project_id":1,"feedback":"Well structured."}'
```

## Workshop Completions
```bash
# Record manual completion
curl -X POST -H "Authorization: Bearer $PG_TOKEN" -H "Content-Type: application/json" \
  http://localhost:8000/api/my/workshops/ \
  -d '{"workshop":1,"completed_at":"2026-03-01"}'

# List completions
curl -H "Authorization: Bearer $PG_TOKEN" http://localhost:8000/api/my/workshops/
```

## Eligibility
```bash
# Resident's own eligibility snapshot
curl -H "Authorization: Bearer $PG_TOKEN" http://localhost:8000/api/my/eligibility/

# UTRMC eligibility overview
curl -H "Authorization: Bearer $ADMIN_TOKEN" "http://localhost:8000/api/utrmc/eligibility/?status=NOT_READY"
```

## System Settings
```bash
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/system/settings/
```
