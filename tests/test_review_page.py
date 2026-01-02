#!/usr/bin/env python3
"""
Simple test to check if we can access the review page and get more specific error details.

Created: 2025-01-27
Author: GitHub Copilot
"""

import requests
import sys

def test_review_page():
    """Test the review page to get specific error details"""
    print("=== Testing Review Page Access ===")
    
    # Test if the server is running
    try:
        url = "http://127.0.0.1:8000/logbook/entry/1/review/"
        print(f"Testing URL: {url}")
        
        response = requests.get(url, timeout=10)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            print("Page loaded successfully!")
        elif response.status_code in [403, 401]:
            print("Permission denied - user might not be logged in or lack permissions")
        elif response.status_code == 404:
            print("Entry not found - entry ID 1 might not exist")
        elif response.status_code == 500:
            print("Server error - there's an issue with the code")
            print("Response text (truncated):")
            print(response.text[:1000])
        else:
            print(f"Unexpected status code: {response.status_code}")
            print("Response text (truncated):")
            print(response.text[:500])
            
    except requests.ConnectionError:
        print("❌ Cannot connect to server. Is the Django server running?")
        return False
    except Exception as e:
        print(f"❌ Error testing page: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_review_page()
