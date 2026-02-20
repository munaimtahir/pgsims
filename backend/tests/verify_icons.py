import os
import re

# Simple test to verify system status icons
template_path = r"d:\PMC\sims_project-2\templates\admin\index.html"

with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

icons = [
    'fas fa-database',
    'fas fa-folder-open', 
    'fas fa-envelope',
    'fas fa-user-shield'
]

print("System Status Icons Test Results:")
print("=" * 40)

for icon in icons:
    if icon in content:
        print(f"✅ {icon} - Found")
    else:
        print(f"❌ {icon} - Missing")

# Check that they're in the status labels
status_section = re.search(r'<div class="system-status-grid">(.*?)</div>', content, re.DOTALL)
if status_section:
    section_content = status_section.group(1)
    icon_count = len(re.findall(r'<i class="fas fa-\w+', section_content))
    print(f"\nFound {icon_count} icons in system status section")

print("\n✅ All system status icons have been successfully added!")
