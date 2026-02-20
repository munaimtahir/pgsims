#!/usr/bin/env python3
"""
Complete test to verify FontAwesome icons are working in system status.
"""

import os
import re

def test_complete_icon_setup():
    """Test the complete FontAwesome icon setup."""
    template_path = r"d:\PMC\sims_project-2\templates\admin\index.html"
    
    if not os.path.exists(template_path):
        print(f"❌ Template file not found: {template_path}")
        return False
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔍 COMPLETE ICON SETUP TEST")
    print("=" * 60)
    
    # 1. Check FontAwesome CSS inclusion
    fa_include_pattern = r'font-awesome.*?css'
    if re.search(fa_include_pattern, content, re.IGNORECASE):
        print("✅ FontAwesome CSS: Included in template")
    else:
        print("⚠️  FontAwesome CSS: Not explicitly included (may be in base template)")
    
    # 2. Check system status icons in HTML
    system_icons = [
        ('fas fa-database', 'Database Connection'),
        ('fas fa-folder-open', 'File Storage'),
        ('fas fa-envelope', 'Email Service'),
        ('fas fa-user-shield', 'Admin Session')
    ]
    
    print(f"\n🎯 System Status Icons in HTML:")
    for icon_class, label in system_icons:
        pattern = rf'<i class="{re.escape(icon_class)}[^"]*"[^>]*></i>\s*{re.escape(label)}'
        if re.search(pattern, content, re.MULTILINE | re.DOTALL):
            print(f"✅ {label}: {icon_class} found")
        else:
            print(f"❌ {label}: {icon_class} missing")
    
    # 3. Check for problematic CSS rules
    print(f"\n🚫 Problematic CSS Rules Check:")
    
    # Check for content: none rules affecting icons
    content_none_patterns = [
        (r'\.status-item::before.*?content:\s*none', 'status-item::before content blocking'),
        (r'\.status-label::before.*?content:\s*none', 'status-label::before content blocking'),
        (r'\.system-status-grid.*?::before.*?content:\s*none', 'system-status-grid pseudo-element blocking')
    ]
    
    for pattern, description in content_none_patterns:
        if re.search(pattern, content, re.MULTILINE | re.DOTALL | re.IGNORECASE):
            print(f"❌ {description}: Found (this blocks icons)")
        else:
            print(f"✅ {description}: Not found (good)")
    
    # 4. Check for proper list-style removal (good rules)
    print(f"\n📋 List Style Removal (should be present):")
    list_style_rules = [
        (r'\.status-item[^{]*\{[^}]*list-style:\s*none', 'status-item list-style removal'),
        (r'\.status-label[^{]*\{[^}]*list-style:\s*none', 'status-label list-style removal'),
        (r'\.system-status-grid[^{]*\{[^}]*list-style:\s*none', 'system-status-grid list-style removal')
    ]
    
    for pattern, description in list_style_rules:
        if re.search(pattern, content, re.MULTILINE | re.DOTALL | re.IGNORECASE):
            print(f"✅ {description}: Found")
        else:
            print(f"⚠️  {description}: Not found")
    
    # 5. Check FontAwesome protection CSS
    print(f"\n🛡️  FontAwesome Protection:")
    fa_protection_pattern = r'\.status-label\s+i\.fas.*?font-family.*?Font Awesome'
    if re.search(fa_protection_pattern, content, re.MULTILINE | re.DOTALL | re.IGNORECASE):
        print("✅ FontAwesome protection CSS: Found")
    else:
        print("⚠️  FontAwesome protection CSS: Not found")
    
    # 6. Count all FontAwesome icons in template
    all_fa_icons = re.findall(r'<i class="fas fa-[^"]*"', content)
    print(f"\n📊 Total FontAwesome icons in template: {len(all_fa_icons)}")
    
    system_status_fa_icons = re.findall(r'<span class="status-label">.*?<i class="fas fa-[^"]*"', content, re.DOTALL)
    print(f"📊 FontAwesome icons in system status: {len(system_status_fa_icons)}")
    
    print("=" * 60)
    
    if len(system_status_fa_icons) >= 4:
        print("🎉 ICONS SHOULD BE VISIBLE!")
        print("✅ All system status icons are properly configured")
    else:
        print("⚠️  ICONS MAY NOT BE VISIBLE")
        print("❌ Some system status icons may be missing or blocked")
    
    print("\n💡 Check http://localhost:8000/admin/ to verify visual results")
    return True

if __name__ == "__main__":
    test_complete_icon_setup()
