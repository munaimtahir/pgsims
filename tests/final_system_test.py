#!/usr/bin/env python
"""
Final System Test - Check all major URLs and functionality
"""
import os
import sys
import requests
from urllib.parse import urljoin

def main():
    print("="*60)
    print("FINAL SIMS SYSTEM TEST")
    print("="*60)
    
    base_url = "http://127.0.0.1:8000"
    
    # URLs to test
    test_urls = [
        # Main pages
        ("Homepage", "/"),
        ("Admin", "/admin/"),
        
        # User pages
        ("User Dashboard", "/users/admin-dashboard/"),
        ("User List", "/users/list/"),
        ("Profile", "/users/profile/"),
        
        # Logbook pages
        ("Logbook List", "/logbook/"),
        ("Logbook Dashboard", "/logbook/dashboard/"),
        ("Logbook Analytics", "/logbook/analytics/"),
        
        # Cases pages
        ("Cases List", "/cases/"),
        ("Case Statistics", "/cases/statistics/"),
        
        # Certificates pages
        ("Certificates List", "/certificates/"),
        ("Certificates Dashboard", "/certificates/dashboard/"),
        
        # Rotations pages
        ("Rotations List", "/rotations/"),
        ("Rotations Dashboard", "/rotations/dashboard/"),
    ]
    
    print(f"Testing {len(test_urls)} URLs...")
    print()
    
    results = []
    for name, url in test_urls:
        full_url = urljoin(base_url, url)
        try:
            response = requests.get(full_url, timeout=5)
            status = response.status_code
            
            if status == 200:
                print(f"✅ {name}: {status} OK")
                results.append((name, "PASS", status))
            elif status == 302:
                print(f"🔄 {name}: {status} Redirect (likely needs login)")
                results.append((name, "REDIRECT", status))
            elif status == 403:
                print(f"🔒 {name}: {status} Forbidden (needs permissions)")
                results.append((name, "PERMISSION", status))
            elif status == 404:
                print(f"❌ {name}: {status} Not Found")
                results.append((name, "NOT_FOUND", status))
            elif status == 500:
                print(f"💥 {name}: {status} Server Error")
                results.append((name, "SERVER_ERROR", status))
            else:
                print(f"⚠️  {name}: {status} Other")
                results.append((name, "OTHER", status))
                
        except requests.exceptions.ConnectionError:
            print(f"❌ {name}: Connection Error (Server not running?)")
            results.append((name, "CONNECTION_ERROR", "N/A"))
        except requests.exceptions.Timeout:
            print(f"⏰ {name}: Timeout")
            results.append((name, "TIMEOUT", "N/A"))
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
            results.append((name, "ERROR", str(e)))
    
    print()
    print("="*60)
    print("SUMMARY")
    print("="*60)
    
    # Count results
    pass_count = sum(1 for _, status, _ in results if status == "PASS")
    redirect_count = sum(1 for _, status, _ in results if status == "REDIRECT")
    error_count = sum(1 for _, status, _ in results if status in ["NOT_FOUND", "SERVER_ERROR", "CONNECTION_ERROR", "TIMEOUT", "ERROR"])
    
    print(f"✅ Working: {pass_count}")
    print(f"🔄 Redirects: {redirect_count} (likely need login)")
    print(f"❌ Errors: {error_count}")
    print(f"📊 Total: {len(results)}")
    
    if error_count == 0:
        print("\n🎉 All URLs are accessible! System appears to be working correctly.")
    else:
        print(f"\n⚠️  {error_count} URLs have issues that need attention.")
        
    # Show problematic URLs
    problem_results = [r for r in results if r[1] in ["NOT_FOUND", "SERVER_ERROR", "CONNECTION_ERROR", "TIMEOUT", "ERROR"]]
    if problem_results:
        print("\nProblematic URLs:")
        for name, status, code in problem_results:
            print(f"  - {name}: {status} ({code})")

if __name__ == '__main__':
    main()
