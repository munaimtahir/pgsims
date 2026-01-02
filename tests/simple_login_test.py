from django.test.client import Client

# Test admin login
client = Client()

# Test GET request to login page
print("Testing admin login page...")
response = client.get('/admin/login/')
print(f"Login page status: {response.status_code}")

# Test POST request with credentials
print("\nTesting login with credentials...")
login_data = {
    'username': 'admin',
    'password': 'admin123',
    'next': '/admin/'
}

response = client.post('/admin/login/', login_data, follow=True)
print(f"Login response status: {response.status_code}")
print(f"Final URL: {response.request['PATH_INFO']}")

content = response.content.decode()
if 'Site administration' in content or 'Welcome' in content:
    print("✅ Login successful - reached admin dashboard")
elif 'errorlist' in content.lower():
    print("❌ Login failed - errors on page")
else:
    print("⚠️ Login status unclear")

print("\nDone.")
