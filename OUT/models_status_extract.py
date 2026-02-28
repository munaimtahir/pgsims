import json
from pathlib import Path
inv = json.loads(Path('/home/munaim/srv/apps/pgsims/OUT/models_inventory.json').read_text())
lines=['# Models With Status-like Fields','']
for m in inv:
    if m.get('status_fields'):
        fields = ', '.join([f"`{s['name']}`" for s in m['status_fields']])
        lines.append(f"- {m['label']}: {fields}")
Path('/home/munaim/srv/apps/pgsims/OUT/models_status_fields.txt').write_text('\n'.join(lines)+'\n')
print('Generated models_status_fields.txt')
