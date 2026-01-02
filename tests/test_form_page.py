import requests

try:
    print("=== TESTING LOGBOOK ENTRY FORM ===\n")
    
    # Test if the server is running
    response = requests.get('http://127.0.0.1:8000/logbook/entry/new/', timeout=5)
    
    print(f"Status Code: {response.status_code}")
    print(f"Content Length: {len(response.content)}")
    
    if response.status_code == 200:
        print("✅ Page loads successfully")
        
        # Check for form elements
        content = response.text.lower()
        form_elements = [
            'case_title',
            'patient_age',
            'patient_gender', 
            'patient_chief_complaint',
            'specialty',
            'clinical_setting',
            'competency_level',
            'learning_points',
            'management_plan'
        ]
        
        print("\n📋 Checking for enhanced form fields:")
        found_fields = 0
        for field in form_elements:
            if field in content:
                print(f"  ✅ {field}")
                found_fields += 1
            else:
                print(f"  ❌ {field}")
        
        print(f"\nFound {found_fields}/{len(form_elements)} enhanced fields")
        
        if found_fields >= len(form_elements) * 0.7:  # At least 70% of fields found
            print("✅ Enhanced form appears to be working")
        else:
            print("⚠️  Enhanced form may have issues")
            
    elif response.status_code == 302:
        print("⚠️  Page redirects (probably need to login)")
        print(f"Redirect location: {response.headers.get('Location', 'N/A')}")
    elif response.status_code == 403:
        print("❌ Access forbidden (need proper permissions)")
    elif response.status_code == 500:
        print("❌ Server error - check form code")
    else:
        print(f"❌ Unexpected response: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to server. Make sure Django server is running.")
except requests.exceptions.Timeout:
    print("❌ Request timed out")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n=== TEST COMPLETED ===")
