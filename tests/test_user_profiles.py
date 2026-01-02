#!/usr/bin/env python

import requests
import sys

def test_user_profiles():
    print("=== TESTING USER PROFILE PAGES ===\n")
    
    base_url = "http://127.0.0.1:8000"
    
    # Test multiple user profile URLs
    user_ids = [1, 2, 3, 4, 5]
    
    for user_id in user_ids:
        try:
            url = f"{base_url}/users/profile/{user_id}/"
            print(f"Testing: {url}")
            
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print(f"  ✅ Status: 200 OK")
                
                # Check for key elements in the response
                content = response.text.lower()
                
                checks = [
                    ("profile", "profile" in content),
                    ("card", "card" in content),
                    ("user info", any(x in content for x in ["first name", "email", "role"])),
                    ("activity", "activity" in content),
                ]
                
                for check_name, check_result in checks:
                    status = "✅" if check_result else "❌"
                    print(f"    {status} {check_name}")
                    
            elif response.status_code == 302:
                print(f"  🔄 Status: 302 Redirect (need login)")
                print(f"    Location: {response.headers.get('Location', 'N/A')}")
                
            elif response.status_code == 403:
                print(f"  🚫 Status: 403 Forbidden (permissions required)")
                
            elif response.status_code == 404:
                print(f"  ❌ Status: 404 Not Found (user doesn't exist)")
                
            else:
                print(f"  ❌ Status: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"  ❌ Connection Error - Is the server running?")
            break
        except requests.exceptions.Timeout:
            print(f"  ❌ Timeout")
        except Exception as e:
            print(f"  ❌ Error: {e}")
            
        print()
    
    print("=== TEST COMPLETED ===\n")
    
    # Test login page
    print("Testing login page access...")
    try:
        response = requests.get(f"{base_url}/users/login/", timeout=5)
        if response.status_code == 200:
            print("✅ Login page accessible")
            print("💡 To test profile pages, login first with appropriate permissions")
        else:
            print(f"❌ Login page status: {response.status_code}")
    except Exception as e:
        print(f"❌ Login page error: {e}")

if __name__ == "__main__":
    test_user_profiles()
