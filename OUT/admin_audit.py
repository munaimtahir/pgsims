import json
from pathlib import Path

root = Path('/home/munaim/srv/apps/pgsims')
registry_text = (root/'OUT/admin_registry_models.txt').read_text().splitlines()
registered = set(line.strip() for line in registry_text if '.' in line and not line.startswith('REGISTRY_COUNT'))

inv = json.loads((root/'OUT/models_inventory.json').read_text())
project_apps = sorted({m['app_label'] for m in inv if m['app_label'] not in {'admin','auth','contenttypes','sessions','django_celery_beat'}})

lines = ['# Admin Audit Data', '']
lines.append(f'Registered models count: {len(registered)}')
lines.append('')
for app in project_apps:
    models = sorted([m['label'] for m in inv if m['app_label']==app])
    missing = [m for m in models if m not in registered]
    lines.append(f'## {app}')
    lines.append(f'- models_total: {len(models)}')
    lines.append(f'- models_registered: {len(models)-len(missing)}')
    lines.append(f'- models_not_registered: {len(missing)}')
    if missing:
        lines.append(f"- missing: {', '.join('`'+x+'`' for x in missing)}")
    lines.append('')

(root/'OUT/admin_models_gap.txt').write_text('\n'.join(lines)+'\n')

app_lines = ['# Admin Files Audit', '']
for appdir in sorted((root/'backend/sims').iterdir()):
    if not appdir.is_dir() or appdir.name.startswith('__'):
        continue
    admin_py = appdir/'admin.py'
    if not admin_py.exists():
        app_lines.append(f'- {appdir.name}: admin.py missing')
        continue
    txt = admin_py.read_text().strip()
    if not txt:
        app_lines.append(f'- {appdir.name}: admin.py empty')
    elif 'register' not in txt:
        app_lines.append(f'- {appdir.name}: admin.py exists, no registrations found')
    else:
        app_lines.append(f'- {appdir.name}: admin.py has registrations')

(root/'OUT/admin_files_audit.txt').write_text('\n'.join(app_lines)+'\n')
print('Generated admin audit outputs')
