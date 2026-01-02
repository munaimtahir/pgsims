#!/usr/bin/env python
"""
Quick SIMS diagnostic check
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and capture output"""
    print(f"\n🔍 {description}")
    print("-" * 50)
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd="d:\\PMC\\sims_project")
        if result.returncode == 0:
            print("✅ SUCCESS")
            if result.stdout.strip():
                print(result.stdout)
        else:
            print("❌ ERROR")
            if result.stderr.strip():
                print(result.stderr)
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")

def main():
    """Run diagnostics"""
    print("="*60)
    print("SIMS QUICK DIAGNOSTIC")
    print("="*60)
    
    # Check Django
    run_command("python manage.py check --deploy", "Django System Check")
    
    # Check migrations
    run_command("python manage.py showmigrations", "Migration Status")
    
    # Check if server is running
    run_command("python manage.py check", "Basic Django Check")
    
    # Test URL patterns
    run_command("python manage.py show_urls", "URL Patterns (if available)")
    
    print("\n" + "="*60)
    print("DIAGNOSTIC COMPLETE")
    print("="*60)
    print("Server should be running at: http://127.0.0.1:8000")
    print("Login page: http://127.0.0.1:8000/users/login/")
    print("Admin dashboard: http://127.0.0.1:8000/users/admin_dashboard/")

if __name__ == "__main__":
    main()
