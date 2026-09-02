# Quick Reference Card

**Print this or bookmark it**

---

## Start Here

```
1. First time? Read: 00_README.md (15 min)
2. Understand blockers? Read: 01_blocker_analysis.md (20 min)
3. Plan execution? Read: 02_phase_guide.md (15 min)
4. Need to fix something? Find your blocker below ↓
5. Something broken? See TROUBLESHOOTING ↓
```

---

## The 11 Blockers (Pick One to Fix)

| # | Blocker | Read This | Time | Effort |
|---|---------|-----------|------|--------|
| 1 | Schema (315 errors) | 03_schema_gate_fix.md | 15 min | 3-5 hrs |
| 2 | E2E dashboard fail | 04_e2e_debugging.md | 20 min | 1-6 hrs |
| 3 | E2E logbook | 04_e2e_debugging.md | 20 min | 2-4 hrs |
| 4 | Restart/reseed smoke | 06_testing_procedures.md | 10 min | 1-2 hrs |
| 5 | Backend coverage (54%) | 05_coverage_strategy.md | 20 min | 8-15 hrs |
| 6 | Frontend coverage (8%) | 05_coverage_strategy.md | 20 min | 15-20 hrs |
| 7-11 | Routes/CTAs/etc | 02_phase_guide.md | - | 8-20 hrs |

---

## Commands (Copy-Paste Ready)

### Backend Tests
```bash
cd backend && SECRET_KEY=test-secret pytest sims -q
cd backend && pytest sims --cov=sims --cov-report=html --cov-report=term
cd backend && pytest sims/training/ -v
```

### Frontend Tests
```bash
cd frontend && npm test -- --watch=false
cd frontend && npm run test:coverage -- --watch=false
cd frontend && npm run lint
```

### E2E Tests
```bash
cd frontend && npm run test:e2e:feature-layer:local
./scripts/e2e_seed.sh  # Must run before E2E
```

### Schema Gate
```bash
cd backend && python manage.py spectacular_settings --validate
cd backend && python manage.py spectacular_settings --file /tmp/schema.yaml
```

### Docker
```bash
docker compose up -d
docker compose ps
docker compose logs backend
docker compose down
docker compose build --no-cache backend
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Failed to load dashboard" | Read: 04_e2e_debugging.md → Blocker #2 |
| "Unable to guess serializer" | Read: 03_schema_gate_fix.md → Add @extend_schema() |
| "Permission Denied (403)" | Auth/role issue - Add user or permission |
| "Timeout waiting for selector" | E2E issue - Check mock API and selectors |
| "Element not found" | Frontend test - Check screen.debug() output |
| "Docker unhealthy" | Restart: docker compose restart [service] |
| Coverage too low | Add tests using: 05_coverage_strategy.md |
| "Stale code in Docker" | Rebuild: docker compose build --no-cache [svc] |
| Something weird | Use: 08_decision_tree.md (symptom-based) |

---

## Mandatory GO Thresholds

ALL must be true for GO:

- [ ] Schema gate passes (0 errors)
- [ ] E2E fully passes (7/7 tests)
- [ ] Restart/reseed smoke 100%
- [ ] Routes tested 100%
- [ ] APIs tested 100%
- [ ] CTAs tested 100%
- [ ] Roles tested 100%
- [ ] Workflows 100%
- [ ] Transitions 100%
- [ ] Unauthorized tests 100%
- [ ] Backend coverage ≥95% line / ≥90% branch
- [ ] Frontend coverage ≥90% line / ≥85% branch
- [ ] UTRMC admin fully covered
- [ ] No truth gaps

Currently passing: **5/14** = 36% complete

---

## Document Navigation

```
START HERE
    ↓
00_README.md
    ↓
    ├→ Pick a blocker
    │   ├→ Blocker #1? → 03_schema_gate_fix.md
    │   ├→ Blocker #2? → 04_e2e_debugging.md
    │   └→ Coverage? → 05_coverage_strategy.md
    │
    ├→ Something wrong? → 08_decision_tree.md
    ├→ Known issues? → 07_known_issues.md
    ├→ How to test? → 06_testing_procedures.md
    └→ Execution plan? → 02_phase_guide.md
```

---

## Key Files in Project

```
backend/
  ├─ sims_project/settings.py (Django settings)
  ├─ sims/training/views.py (Need @extend_schema())
  ├─ sims/users/userbase_serializers.py (Fixed in session 3)
  └─ sims/*/test_*.py (Add tests here)

frontend/
  ├─ app/dashboard/resident/page.tsx (E2E issue here)
  ├─ app/__tests__/* (Add component tests)
  ├─ e2e/feature-layer/*.spec.ts (4/7 passing)
  └─ lib/api/client.ts (API configuration)

docs/PROD_GATE_CLOSURE/ (You are here)
  ├─ 00_README.md (Start)
  ├─ 01_blocker_analysis.md (Details)
  ├─ 03_schema_gate_fix.md (Blocker #1)
  ├─ 04_e2e_debugging.md (Blocker #2)
  ├─ 05_coverage_strategy.md (Blockers #5 #6)
  └─ ...more guides
```

---

## Session 3 Status

```
Blocker #1:  ⚠️  (49→31 warnings fixed, 315 errors remain)
Blocker #2:  ❌ (Root cause identified, not fixed)
Blocker #5:  ❌ (54% vs 95% target)
Blocker #6:  ❌ (8% vs 90% target)
Others:      ⏳ (Blocked by #2 fix)

NO-GO verdict expected (normal, this is a sprint)
```

---

## Estimate for YOUR Task

- Fixing schema (#1): **3-5 hours**
- Fixing E2E (#2): **1-6 hours** (depends on root cause)
- Improving coverage (#5-6): **8-20 hours** per module
- Full team sprint: **1-2 weeks**

---

## Quick Checklist

- [ ] Started with 00_README.md
- [ ] Read 01_blocker_analysis.md
- [ ] Picked a blocker to work on
- [ ] Read the relevant technical guide
- [ ] Ran existing tests to understand baseline
- [ ] Implemented fix
- [ ] Ran tests to validate
- [ ] All tests passing locally
- [ ] Ready to commit

---

## Help

- **Confused?** Start with 00_README.md again
- **Stuck?** Use 08_decision_tree.md to diagnose
- **Specific blocker?** Check your technical guide
- **Known problem?** Check 07_known_issues.md
- **Debugging?** Check 06_testing_procedures.md

---

**Last Updated**: 2026-04-23  
**Documentation**: docs/PROD_GATE_CLOSURE/  
**Total Files**: 10 guides + this quick reference  
**Ready to work?** Pick a blocker and start with the relevant guide!

