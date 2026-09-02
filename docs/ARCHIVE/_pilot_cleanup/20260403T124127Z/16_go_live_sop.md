# Go-Live SOP

## 1. Backup Step

Run before any import or cleanup:

```bash
docker exec -e PGPASSWORD="$DB_PASSWORD" pgsims_db \
  pg_dump -U "$DB_USER" -d "$DB_NAME" | gzip > live-pre-import-$(date -u +%Y%m%dT%H%M%SZ).sql.gz

cp .env live-pre-import.env
docker compose --env-file .env -f docker/docker-compose.yml ps > live-pre-import-compose.txt
```

## 2. Import Step

Prerequisites:
- real pilot values entered into:
  - `pilot_data/first_pilot_run/final_pilot_workbook.xlsx` or
  - `pilot_data/first_pilot_run/final_supervisors_list.csv`
  - `pilot_data/first_pilot_run/final_residents_list.csv`
- backend execution context includes `import_pilot_bundle.py`

Recommended command:

```bash
python manage.py import_pilot_bundle \
  --workbook /home/munaim/srv/apps/pgsims/pilot_data/first_pilot_run/final_pilot_workbook.xlsx \
  --supervisors-file /home/munaim/srv/apps/pgsims/pilot_data/first_pilot_run/final_supervisors_list.csv \
  --residents-file /home/munaim/srv/apps/pgsims/pilot_data/first_pilot_run/final_residents_list.csv \
  --apply
```

If needed, run a dry-run first:

```bash
python manage.py import_pilot_bundle \
  --workbook /home/munaim/srv/apps/pgsims/pilot_data/first_pilot_run/final_pilot_workbook.xlsx \
  --supervisors-file /home/munaim/srv/apps/pgsims/pilot_data/first_pilot_run/final_supervisors_list.csv \
  --residents-file /home/munaim/srv/apps/pgsims/pilot_data/first_pilot_run/final_residents_list.csv
```

## 3. Verification Step

Verify:
- `users_user` contains expected supervisors and residents
- `users_supervisorresidentlink` count matches expected pilot mapping
- UI lists show only real pilot users
- `/api/notifications/` contains no demo noise
- dashboard counts reflect only imported pilot data
- admin login still works
- if email is needed, confirm non-console email backend

## 4. Rollback Step

If import or verification fails:

```bash
gunzip -c live-pre-import-YYYYMMDDTHHMMSSZ.sql.gz | \
docker exec -i pgsims_db psql -U "$DB_USER" -d "$DB_NAME"

docker compose --env-file .env -f docker/docker-compose.yml up -d --force-recreate backend worker beat frontend
```

After rollback:
- verify backend health
- verify frontend health
- verify admin login
- verify user and training counts returned to the pre-import baseline
