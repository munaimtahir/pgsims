import json
import re
from collections import defaultdict
from pathlib import Path

root = Path('/home/munaim/srv/apps/pgsims/OUT')
endpoints = json.loads((root/'api_endpoints.json').read_text())
serializers = json.loads((root/'serializers_inventory.json').read_text())


def normalize_path(path: str) -> str:
    path = path.replace('^', '').replace('$', '')
    path = path.replace('\\', '')
    path = re.sub(r'\(\?P<([^>]+)>[^\)]+\)', r'{\1}', path)
    path = path.replace('.(?P<format>[a-z0-9]+)/?', '')
    path = path.replace('<drf_format_suffix:format>', '')
    path = re.sub(r'/+', '/', path)
    return path.rstrip('/') or '/'


cleaned = []
seen = set()
for e in endpoints:
    path = normalize_path(e['path'])
    if '<drf_format_suffix:format>' in e['path'] or '(?P<format>' in e['path']:
        continue
    method = e['method'].upper()
    if method in {'TRACE', 'OPTIONS', 'HEAD'}:
        continue
    key = (path, method, e['view'], e.get('action'))
    if key in seen:
        continue
    seen.add(key)
    item = dict(e)
    item['path'] = path
    cleaned.append(item)

# Endpoint catalog
by_group = defaultdict(list)
for e in cleaned:
    parts = [p for p in e['path'].split('/') if p]
    if not parts:
        group = 'root'
    elif 'api' in parts and parts.index('api') + 1 < len(parts):
        group = parts[parts.index('api') + 1]
    else:
        group = parts[0]
    by_group[group].append(e)

ep_lines = ['# API Endpoints Catalog', '', f'Total endpoints: {len(cleaned)}', '']
for group in sorted(by_group):
    ep_lines.append(f'## {group}')
    ep_lines.append('')
    ep_lines.append('| Method | Path | View | Action | Serializer | Permissions | Auth |')
    ep_lines.append('|---|---|---|---|---|---|---|')
    for e in sorted(by_group[group], key=lambda x: (x['path'], x['method'], x['view'])):
        perms = ', '.join(e.get('permissions') or [])
        auth = 'Public' if 'AllowAny' in perms else 'Authenticated'
        ep_lines.append(
            f"| {e['method']} | `{e['path']}` | `{e['view']}` | `{e['action']}` | `{e.get('serializer')}` | `{perms}` | {auth} |"
        )
    ep_lines.append('')
(root/'24_API_ENDPOINTS_CATALOG.md').write_text('\n'.join(ep_lines) + '\n')

# Serializer payload shapes
ser_lines = ['# Serializers Payload Shapes', '']
for s in serializers:
    ser_lines.append(f"## {s['module']}.{s['name']}")
    if s.get('error'):
        ser_lines.append(f"- Introspection error: `{s['error']}`")
        ser_lines.append('')
        continue
    ser_lines.append('| Field | Type | Required | Read Only | Write Only | Nullable |')
    ser_lines.append('|---|---|---:|---:|---:|---:|')
    response_example = {}
    for f in s.get('fields', []):
        ser_lines.append(
            f"| `{f['name']}` | {f['type']} | {f['required']} | {f['read_only']} | {f['write_only']} | {f['allow_null']} |"
        )
        if not f['write_only']:
            response_example[f['name']] = 'value'
    ser_lines.append('')
    ser_lines.append('Example request payload (synthetic):')
    ser_lines.append('```json')
    ser_lines.append(json.dumps(s.get('example', {}), indent=2))
    ser_lines.append('```')
    ser_lines.append('')
    ser_lines.append('Example response payload (synthetic):')
    ser_lines.append('```json')
    ser_lines.append(json.dumps(response_example, indent=2))
    ser_lines.append('```')
    ser_lines.append('')
(root/'25_SERIALIZERS_PAYLOAD_SHAPES.md').write_text('\n'.join(ser_lines) + '\n')

# Synthetic OpenAPI
openapi = {
    'openapi': '3.0.3',
    'info': {'title': 'PGSIMS API (introspected)', 'version': '0.1.0'},
    'paths': {},
    'components': {
        'securitySchemes': {
            'bearerAuth': {'type': 'http', 'scheme': 'bearer', 'bearerFormat': 'JWT'}
        }
    },
}
for e in cleaned:
    method = e['method'].lower()
    if method == 'any':
        continue
    path_item = openapi['paths'].setdefault(e['path'], {})
    perms = e.get('permissions') or []
    operation = {
        'operationId': f"{e['view']}_{method}_{abs(hash(e['path']))}",
        'summary': f"{e['view']} ({e.get('action')})",
        'responses': {'200': {'description': 'Success'}},
        'x-view': e['view'],
        'x-permissions': perms,
    }
    if 'AllowAny' not in perms:
        operation['security'] = [{'bearerAuth': []}]
    path_item[method] = operation

(root/'openapi.json').write_text(json.dumps(openapi, indent=2) + '\n')
print(f"Endpoints normalized: {len(cleaned)}")
