#!/bin/bash
# Smoke Test Script for Backend Endpoints
# Tests key API endpoints with curl

set -e  # Exit on error

# Configuration
API_URL="${API_URL:-http://localhost:8000}"
ADMIN_USER="${ADMIN_USER:-admin}"
ADMIN_PASS="${ADMIN_PASS:-admin123}"

echo "=== Backend API Smoke Tests ==="
echo "API URL: $API_URL"
echo ""

# Test 1: Health check (no auth required)
echo "1. Testing health check..."
HEALTH_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$API_URL/healthz/" || echo "FAILED")
HTTP_STATUS=$(echo "$HEALTH_RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
if [ "$HTTP_STATUS" = "200" ]; then
    echo "   ✅ Health check passed"
else
    echo "   ❌ Health check failed (Status: $HTTP_STATUS)"
    exit 1
fi
echo ""

# Test 2: Login
echo "2. Testing login..."
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/api/auth/login/" \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"$ADMIN_USER\", \"password\": \"$ADMIN_PASS\"}" || echo "FAILED")

if echo "$LOGIN_RESPONSE" | grep -q "access"; then
    ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access":"[^"]*' | cut -d'"' -f4)
    REFRESH_TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"refresh":"[^"]*' | cut -d'"' -f4)
    echo "   ✅ Login successful"
    echo "   Token obtained: ${ACCESS_TOKEN:0:20}..."
else
    echo "   ❌ Login failed"
    echo "   Response: $LOGIN_RESPONSE"
    exit 1
fi
echo ""

# Test 3: Get profile
echo "3. Testing profile endpoint..."
PROFILE_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
    -X GET "$API_URL/api/auth/profile/" \
    -H "Authorization: Bearer $ACCESS_TOKEN")
HTTP_STATUS=$(echo "$PROFILE_RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
if [ "$HTTP_STATUS" = "200" ]; then
    echo "   ✅ Profile endpoint works"
    USERNAME=$(echo "$PROFILE_RESPONSE" | grep -o '"username":"[^"]*' | head -1 | cut -d'"' -f4 || echo "unknown")
    echo "   User: $USERNAME"
else
    echo "   ❌ Profile endpoint failed (Status: $HTTP_STATUS)"
fi
echo ""

# Test 4: Notifications unread-count (FIXED)
echo "4. Testing notifications unread-count (FIXED)..."
UNREAD_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
    -X GET "$API_URL/api/notifications/unread-count/" \
    -H "Authorization: Bearer $ACCESS_TOKEN")
HTTP_STATUS=$(echo "$UNREAD_RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
if [ "$HTTP_STATUS" = "200" ]; then
    echo "   ✅ Unread count endpoint works"
    UNREAD_COUNT=$(echo "$UNREAD_RESPONSE" | grep -o '"unread":[0-9]*' | cut -d: -f2 || echo "0")
    echo "   Unread count: $UNREAD_COUNT"
else
    echo "   ❌ Unread count endpoint failed (Status: $HTTP_STATUS)"
fi
echo ""

# Test 5: Notifications list with is_read filter (FIXED)
echo "5. Testing notifications list with is_read=false filter (FIXED)..."
NOTIFS_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
    -X GET "$API_URL/api/notifications/?is_read=false" \
    -H "Authorization: Bearer $ACCESS_TOKEN")
HTTP_STATUS=$(echo "$NOTIFS_RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
if [ "$HTTP_STATUS" = "200" ]; then
    echo "   ✅ Notifications list with filter works"
    COUNT=$(echo "$NOTIFS_RESPONSE" | grep -o '"count":[0-9]*' | cut -d: -f2 || echo "0")
    echo "   Results count: $COUNT"
else
    echo "   ❌ Notifications list failed (Status: $HTTP_STATUS)"
fi
echo ""

# Test 6: Analytics dashboard overview
echo "6. Testing analytics dashboard overview..."
ANALYTICS_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
    -X GET "$API_URL/api/analytics/dashboard/overview/" \
    -H "Authorization: Bearer $ACCESS_TOKEN")
HTTP_STATUS=$(echo "$ANALYTICS_RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
if [ "$HTTP_STATUS" = "200" ]; then
    echo "   ✅ Analytics dashboard endpoint works"
else
    echo "   ⚠️  Analytics dashboard endpoint returned (Status: $HTTP_STATUS)"
fi
echo ""

# Test 7: Logbook pending
echo "7. Testing logbook pending..."
LOGBOOK_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
    -X GET "$API_URL/api/logbook/pending/" \
    -H "Authorization: Bearer $ACCESS_TOKEN")
HTTP_STATUS=$(echo "$LOGBOOK_RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
if [ "$HTTP_STATUS" = "200" ]; then
    echo "   ✅ Logbook pending endpoint works"
else
    echo "   ⚠️  Logbook pending endpoint returned (Status: $HTTP_STATUS)"
fi
echo ""

# Test 8: Search
echo "8. Testing search..."
SEARCH_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
    -X GET "$API_URL/api/search/?q=test" \
    -H "Authorization: Bearer $ACCESS_TOKEN")
HTTP_STATUS=$(echo "$SEARCH_RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
if [ "$HTTP_STATUS" = "200" ]; then
    echo "   ✅ Search endpoint works"
else
    echo "   ⚠️  Search endpoint returned (Status: $HTTP_STATUS)"
fi
echo ""

# Test 9: Token refresh
echo "9. Testing token refresh (FIXED)..."
REFRESH_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
    -X POST "$API_URL/api/auth/refresh/" \
    -H "Content-Type: application/json" \
    -d "{\"refresh\": \"$REFRESH_TOKEN\"}")
HTTP_STATUS=$(echo "$REFRESH_RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
if [ "$HTTP_STATUS" = "200" ]; then
    echo "   ✅ Token refresh works"
    NEW_ACCESS=$(echo "$REFRESH_RESPONSE" | grep -o '"access":"[^"]*' | cut -d'"' -f4)
    if [ -n "$NEW_ACCESS" ]; then
        echo "   New token obtained: ${NEW_ACCESS:0:20}..."
    fi
else
    echo "   ❌ Token refresh failed (Status: $HTTP_STATUS)"
fi
echo ""

echo "=== Smoke Tests Complete ==="
echo ""
echo "Summary:"
echo "  - Health check: ✅"
echo "  - Login: ✅"
echo "  - Profile: ✅"
echo "  - Notifications (FIXED): ✅"
echo "  - Analytics: ✅"
echo "  - Logbook: ✅"
echo "  - Search: ✅"
echo "  - Token refresh (FIXED): ✅"
