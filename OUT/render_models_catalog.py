import json
from collections import defaultdict
from pathlib import Path

root = Path('/home/munaim/srv/apps/pgsims')
inv = json.loads((root / 'OUT/models_inventory.json').read_text())
by_app = defaultdict(list)
for m in inv:
    by_app[m['app_label']].append(m)

out = []
out.append('# Models Catalog')
out.append('')
out.append(f'Total models: {len(inv)}')
out.append('')
for app in sorted(by_app):
    out.append(f'## {app}')
    out.append('')
    for m in sorted(by_app[app], key=lambda x: x['model_name']):
        out.append(f"### {m['label']}")
        out.append(f"- **DB Table**: `{m['db_table']}`")
        if m['status_fields']:
            sf = ', '.join([f"`{s['name']}`" for s in m['status_fields']])
            out.append(f"- **Status/State Fields**: {sf}")
        else:
            out.append('- **Status/State Fields**: None detected')
        out.append('')
        out.append('| Field | Type | Null | Blank | PK | Unique | Choices | Relation |')
        out.append('|---|---|---:|---:|---:|---:|---:|---|')
        for f in m['fields']:
            relation_target = ''
            if f.get('is_relation'):
                rel = next((r for r in m['relations'] if r['field'] == f['name']), None)
                relation_target = rel['target'] if rel else ''
            out.append(f"| `{f['name']}` | {f['type']} | {f['null']} | {f['blank']} | {f['primary_key']} | {f['unique']} | {f['has_choices']} | {relation_target} |")
        out.append('')
        if m['relations']:
            out.append('- **Relations**:')
            for r in m['relations']:
                out.append(f"  - `{r['field']}` ({r['relation_type']}) -> `{r['target']}` (related_name={r['related_name']})")
            out.append('')

(root / 'OUT/21_MODELS_CATALOG.md').write_text('\n'.join(out) + '\n')

lines = ['digraph models {', '  rankdir=LR;']
for m in inv:
    lines.append(f'  "{m["label"]}" [shape=box];')
for m in inv:
    for r in m['relations']:
        if r['target']:
            lines.append(f'  "{m["label"]}" -> "{r["target"]}" [label="{r["field"]}"];')
lines.append('}')
(root / 'OUT/models_graph.dot').write_text('\n'.join(lines) + '\n')
print(f'Models: {len(inv)}')
