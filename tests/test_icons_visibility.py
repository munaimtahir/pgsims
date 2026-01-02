#!/usr/bin/env python3
"""
Test script to verify icons are visible and bullets are handled correctly.
"""

import os
import re

def test_icons_visibility():
    """Test that icons are still present in the HTML."""
    template_path = r"d:\PMC\sims_project-2\templates\admin\index.html"
    
    if not os.path.exists(template_path):
        print(f"❌ Template file not found: {template_path}")
        return False
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔍 Testing Icon Visibility...")
    print("=" * 50)
    
    # Check for FontAwesome icons in system status
    icons_with_text = [
        ('fas fa-database', 'Database Connection'),
        ('fas fa-folder-open', 'File Storage'),
        ('fas fa-envelope', 'Email Service'),
        ('fas fa-user-shield', 'Admin Session')
    ]
    
    all_passed = True
    
    for icon_class, text in icons_with_text:
        # Look for the icon class in status-label context
        pattern = rf'<span class="status-label">.*?<i class="{re.escape(icon_class)}[^"]*"[^>]*></i>.*?{re.escape(text)}.*?</span>'
        
        if re.search(pattern, content, re.MULTILINE | re.DOTALL):
            print(f"✅ {text}: Icon '{icon_class}' found in HTML")
        else:
            print(f"❌ {text}: Icon '{icon_class}' missing or malformed")
            all_passed = False
    
    # Check that problematic content: none rules are removed
    problematic_patterns = [
        r'content:\s*none\s*!important',
        r'\.status-label.*?content:\s*none',
        r'\.status-item.*?content:\s*none'
    ]
    
    print(f"\n🚫 Checking for problematic CSS rules:")
    
    for pattern in problematic_patterns:
        matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        if matches:
            print(f"⚠️  Found {len(matches)} potentially problematic 'content: none' rules")
            all_passed = False
        else:
            print(f"✅ No problematic 'content: none' rules found")
    
    # Check that list-style removal is still present
    list_style_patterns = [
        r'list-style:\s*none\s*!important',
        r'list-style-type:\s*none\s*!important'
    ]
    
    print(f"\n📋 Checking list-style removal:")
    for pattern in list_style_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            print(f"✅ Found {len(matches)} list-style removal rules")
        else:
            print(f"⚠️  No list-style removal rules found")
    
    print("=" * 50)
    if all_passed:
        print("🎉 Icons should be visible and bullets should be removed!")
    else:
        print("⚠️  Some issues detected - check the output above")
    
    return all_passed

if __name__ == "__main__":
    print("🚀 ICON VISIBILITY TEST")
    print("Testing that icons are visible after bullet removal fix")
    print("=" * 60)
    
    test_icons_visibility()
    
    print("\n✨ Test completed!")
    print("💡 Check the admin dashboard: http://localhost:8000/admin/")
