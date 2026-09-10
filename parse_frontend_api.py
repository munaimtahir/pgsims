import re

endpoints = set()
with open('frontend/frontend_endpoints.txt', 'r') as f:
    for line in f:
        matches = re.findall(r"'(/(?:api|api/v1)/[^']+)'|\"`(/(?:api|api/v1)/[^`]+)`\"|\"`(/(?:api|api/v1)/[^?$]+)[?\$]\"|`(/\w+[^`]*)`", line)
        for match in matches:
            for m in match:
                if m and not m.startswith('http'):
                    # Strip interpolation parts
                    clean_m = re.sub(r'\$\{.*?\}', '{id}', m)
                    endpoints.add(clean_m)

with open('frontend_api_calls.txt', 'w') as f:
    for ep in sorted(endpoints):
        f.write(ep + '\n')
