#!/usr/bin/env python
import os
import django
import requests

# Test the logout URL
url = "http://127.0.0.1:8000/users/logout/"
try:
    response = requests.get(url)
    print(f"Logout URL status: {response.status_code}")
    if response.status_code == 200:
        print("Logout URL is working correctly")
    else:
        print(f"Error: {response.text}")
except requests.exceptions.RequestException as e:
    print(f"Connection error: {e}")

# Test the API endpoint for supervisors
api_url = "http://127.0.0.1:8000/users/api/supervisors/specialty/cardiology/"
try:
    response = requests.get(api_url)
    print(f"\nSupervisor API status: {response.status_code}")
    if response.status_code == 200:
        print(f"API Response: {response.json()}")
    else:
        print(f"API Error: {response.text}")
except requests.exceptions.RequestException as e:
    print(f"API Connection error: {e}")
