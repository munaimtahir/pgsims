#!/usr/bin/env python3
"""
Test script to verify system status icons have been added to the admin dashboard.
"""

import os
import re

def test_system_status_icons():
    """Test that icons have been added to system status items."""
    template_path = r"d:\PMC\sims_project-2\templates\admin\index.html"
    
    if not os.path.exists(template_path):
        print(f"❌ Template file not found: {template_path}")
        return False
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define expected icons for each status item
    expected_icons = [
        ('Database Connection', 'fas fa-database'),
        ('File Storage', 'fas fa-folder-open'),
        ('Email Service', 'fas fa-envelope'),
        ('Admin Session', 'fas fa-user-shield')
    ]
    
    all_passed = True
    print("🔍 Testing System Status Icons...")
    print("=" * 50)
    
    for item_name, icon_class in expected_icons:
        # Look for the pattern: icon class followed by status label
        pattern = rf'<i class="{re.escape(icon_class)}[^"]*"[^>]*></i>\s*{re.escape(item_name)}'
        
        if re.search(pattern, content, re.MULTILINE | re.DOTALL):
            print(f"✅ {item_name}: Found icon '{icon_class}'")
        else:
            print(f"❌ {item_name}: Missing icon '{icon_class}'")
            all_passed = False
    
    # Check that icons have proper styling classes
    icon_pattern = r'<i class="fas fa-\w+\s+me-2\s+text-primary"[^>]*></i>'
    icon_matches = re.findall(icon_pattern, content)
    
    print(f"\n🎨 Icon Styling Check:")
    print(f"Found {len(icon_matches)} properly styled icons")
    
    if len(icon_matches) >= 4:
        print("✅ All system status icons have proper styling (me-2 text-primary)")
    else:
        print("❌ Some icons may be missing proper styling")
        all_passed = False
    
    # Check system status card structure
    status_card_pattern = r'<h5 class="card-title-modern">\s*<i class="fas fa-heartbeat[^"]*"></i>\s*System Status\s*</h5>'
    
    if re.search(status_card_pattern, content, re.MULTILINE | re.DOTALL):
        print("✅ System Status card header found with heartbeat icon")
    else:
        print("❌ System Status card header structure issue")
        all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 All system status icons have been successfully added!")
        print("📋 Summary of added icons:")
        for item_name, icon_class in expected_icons:
            print(f"   • {item_name}: {icon_class}")
    else:
        print("⚠️  Some issues found with system status icons")
    
    return all_passed

def test_icon_visibility():
    """Test that icons are properly spaced and visible."""
    template_path = r"d:\PMC\sims_project-2\templates\admin\index.html"
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("\n🔍 Testing Icon Visibility and Spacing...")
    print("=" * 50)
    
    # Check for proper spacing class (me-2)
    spacing_pattern = r'<i class="fas fa-\w+\s+me-2'
    spacing_matches = re.findall(spacing_pattern, content)
    
    if len(spacing_matches) >= 4:
        print("✅ All system status icons have proper spacing (me-2)")
    else:
        print(f"⚠️  Found only {len(spacing_matches)} icons with proper spacing")
    
    # Check for color class (text-primary)
    color_pattern = r'text-primary'
    icon_sections = re.findall(r'<span class="status-label">.*?</span>', content, re.DOTALL)
    
    colored_icons = 0
    for section in icon_sections:
        if 'text-primary' in section:
            colored_icons += 1
    
    if colored_icons >= 4:
        print("✅ All system status icons have proper color (text-primary)")
    else:
        print(f"⚠️  Found only {colored_icons} icons with proper color")
    
    return True

if __name__ == "__main__":
    print("🚀 SYSTEM STATUS ICONS TEST")
    print("Testing icons added to admin dashboard system status card")
    print("=" * 60)
    
    test_system_status_icons()
    test_icon_visibility()
    
    print("\n✨ Test completed!")
    print("💡 To view the results, start the server and visit: http://localhost:8000/admin/")
