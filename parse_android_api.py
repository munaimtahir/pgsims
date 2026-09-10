import re
import os
import subprocess

endpoints = set()
try:
    result = subprocess.run(['grep', '-r', '-E', '@(GET|POST|PUT|PATCH|DELETE)\\("', 'android/'], capture_output=True, text=True)
    if result.stdout:
        for line in result.stdout.split('\n'):
            matches = re.findall(r'@(?:GET|POST|PUT|PATCH|DELETE)\(["\'](.*?)["\']\)', line)
            for m in matches:
                if not m.startswith('/'):
                    m = '/' + m
                endpoints.add(m)
except Exception:
    pass

with open('AUDIT/PGSIMS/PARALLEL/A_ARCHITECTURE_TRUTHMAP/09_ANDROID_BACKEND_MAP.md', 'w') as f:
    f.write("# Android to Backend API Map\n\n")
    if not endpoints:
        f.write("No active Android source code or explicit Retrofit API definitions found in the repository.\n")
        f.write("This may indicate the Android client is maintained in a separate repository or offline-only.\n\n")
    else:
        f.write("| Android API Endpoint | Suspected Backend Match |\n")
        f.write("|---|---|\n")
        for ep in sorted(endpoints):
            f.write(f"| {ep} | UNVERIFIED |\n")
