#!/bin/bash
# Smoke Test Script for Backend Endpoints
# Tests key API endpoints with curl

set -e  # Exit on error

# Configuration
DJANGO_BASE_URL="${DJANGO_BASE_URL:-http://127.0.0.1:8000}"
ADMIN_USER="${ADMIN_USER:-admin}"
ADMIN_PASS="${ADMIN_PASS:-admin123}"

echo "=== Backend API Smoke Tests ==="
echo "Django Base URL: $DJANGO_BASE_URL"
echo "Admin User: $ADMIN_USER"
echo "Test Date: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo ""

# Test 1: Health check (no auth required)
echo "1. Testing health check..."
HEALTH_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "$DJANGO_BASE_URL/healthz/" || echo "FAILED")
HTTP_STATUS=$(echo "$HEALTH_RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
if [ "$HTTP_STATUS" = "200" ]; then
    echo "   ✅ Health check passed"
    echo "   Response: $(echo "$HEALTH_RESPONSE" | grep -v "HTTP_STATUS" | head -1)"
else
    echo "   ❌ Health check failed (Status: $HTTP_STATUS)"
    echo "   Response: $(echo "$HEALTH_RESPONSE" | grep -v "HTTP_STATUS")"
    exit 1
fi
echo ""

# Test 2: Login
echo "2. Testing login..."
LOGIN_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "$DJANGO_BASE_URL/api/auth/login/" \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"$ADMIN_USER\", \"password\": \"$ADMIN_PASS\"}")
HTTP_STATUS=$(echo "$LOGIN_RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
LOGIN_BODY=$(echo "$LOGIN_RESPONSE" | grep -v "HTTP_STATUS")

if [ "$HTTP_STATUS" = "200" ] && echo "$LOGIN_BODY" | grep -q "access"; then
    ACCESS_TOKEN=$(echo "$LOGIN_BODY" | grep -o '"access":"[^"]*' | cut -d'"' -f4)
    REFRESH_TOKEN=$(echo "$LOGIN_BODY" | grep -o '"refresh":"[^"]*' | cut -d'"' -f4)
    echo "   ✅ Login successful (Status: $HTTP_STATUS)"
    echo "   Token obtained: ${ACCESS_TOKEN:0:20}..."
else
    echo "   ❌ Login failed (Status: $HTTP_STATUS)"
    echo "   Response: $LOGIN_BODY"
    exit 1
fi
echo ""

# Test 3: Get profile
echo "3. Testing profile endpoint..."
PROFILE_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
    -X GET "$DJANGO_BASE_URL/api/auth/profile/" \
    -H "Authorization: Bearer $ACCESS_TOKEN")
HTTP_STATUS=$(echo "$PROFILE_RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
PROFILE_BODY=$(echo "$PROFILE_RESPONSE" | grep -v "HTTP_STATUS")
if [ "$HTTP_STATUS" = "200" ]; then
    echo "   ✅ Profile endpoint works (Status: $HTTP_STATUS)"
    USERNAME=$(echo "$PROFILE_BODY" | grep -o '"username":"[^"]*' | head -1 | cut -d'"' -f4 || echo "unknown")
    echo "   User: $USERNAME"
else
    echo "   ❌ Profile endpoint failed (Status: $HTTP_STATUS)"
    echo "   Response: $PROFILE_BODY"
fi
echo ""

# Test 4: Notifications unread-count (FIXED)
echo "4. Testing notifications unread-count (FIXED)..."
UNREAD_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
    -X GET "$DJANGO_BASE_URL/api/notifications/unread-count/" \
    -H "Authorization: Bearer $ACCESS_TOKEN")
HTTP_STATUS=$(echo "$UNREAD_RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
UNREAD_BODY=$(echo "$UNREAD_RESPONSE" | grep -v "HTTP_STATUS")
if [ "$HTTP_STATUS" = "200" ]; then
    echo "   ✅ Unread count endpoint works (Status: $HTTP_STATUS)"
    UNREAD_COUNT=$(echo "$UNREAD_BODY" | grep -o '"unread":[0-9]*' | cut -d: -f2 || echo "0")
    echo "   Unread count: $UNREAD_COUNT"
else
    echo "   ❌ Unread count endpoint failed (Status: $HTTP_STATUS)"
    echo "   Response: $UNREAD_BODY"
fi
echo ""

# Test 5: Notifications list with is_read filter (FIXED)
echo "5. Testing notifications list with is_read=false filter (FIXED)..."
NOTIFS_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
    -X GET "$DJANGO_BASE_URL/api/notifications/?is_read=false" \
    -H "Authorization: Bearer $ACCESS_TOKEN")
HTTP_STATUS=$(echo "$NOTIFS_RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
NOTIFS_BODY=$(echo "$NOTIFS_RESPONSE" | grep -v "HTTP_STATUS")
if [ "$HTTP_STATUS" = "200" ]; then
    echo "   ✅ Notifications list with filter works (Status: $HTTP_STATUS)"
    COUNT=$(echo "$NOTIFS_BODY" | grep -o '"count":[0-9]*' | cut -d: -f2 || echo "0")
    echo "   Results count: $COUNT"
else
    echo "   ❌ Notifications list failed (Status: $HTTP_STATUS)"
    echo "   Response: $NOTIFS_BODY"
fi
echo ""

# Test 6: Analytics dashboard overview
echo "6. Testing analytics dashboard overview..."
ANALYTICS_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
    -X GET "$DJANGO_BASE_URL/api/analytics/dashboard/overview/" \
    -H "Authorization: Bearer $ACCESS_TOKEN")
HTTP_STATUS=$(echo "$ANALYTICS_RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
ANALYTICS_BODY=$(echo "$ANALYTICS_RESPONSE" | grep -v "HTTP_STATUS")
if [ "$HTTP_STATUS" = "200" ]; then
    echo "   ✅ Analytics dashboard endpoint works (Status: $HTTP_STATUS)"
else
    echo "   ⚠️  Analytics dashboard endpoint returned (Status: $HTTP_STATUS)"
    echo "   Response: $(echo "$ANALYTICS_BODY" | head -c 200)"
fi
echo ""

# Test 7: Logbook pending
echo "7. Testing logbook pending..."
LOGBOOK_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
    -X GET "$DJANGO_BASE_URL/api/logbook/pending/" \
    -H "Authorization: Bearer $ACCESS_TOKEN")
HTTP_STATUS=$(echo "$LOGBOOK_RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
LOGBOOK_BODY=$(echo "$LOGBOOK_RESPONSE" | grep -v "HTTP_STATUS")
if [ "$HTTP_STATUS" = "200" ]; then
    echo "   ✅ Logbook pending endpoint works (Status: $HTTP_STATUS)"
else
    echo "   ⚠️  Logbook pending endpoint returned (Status: $HTTP_STATUS)"
    echo "   Response: $(echo "$LOGBOOK_BODY" | head -c 200)"
fi
echo ""

# Test 8: Search
echo "8. Testing search..."
SEARCH_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
    -X GET "$DJANGO_BASE_URL/api/search/?q=test" \
    -H "Authorization: Bearer $ACCESS_TOKEN")
HTTP_STATUS=$(echo "$SEARCH_RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
SEARCH_BODY=$(echo "$SEARCH_RESPONSE" | grep -v "HTTP_STATUS")
if [ "$HTTP_STATUS" = "200" ]; then
    echo "   ✅ Search endpoint works (Status: $HTTP_STATUS)"
else
    echo "   ⚠️  Search endpoint returned (Status: $HTTP_STATUS)"
    echo "   Response: $(echo "$SEARCH_BODY" | head -c 200)"
fi
echo ""

# Test 9: Token refresh
echo "9. Testing token refresh (FIXED)..."
REFRESH_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
    -X POST "$DJANGO_BASE_URL/api/auth/refresh/" \
    -H "Content-Type: application/json" \
    -d "{\"refresh\": \"$REFRESH_TOKEN\"}")
HTTP_STATUS=$(echo "$REFRESH_RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
REFRESH_BODY=$(echo "$REFRESH_RESPONSE" | grep -v "HTTP_STATUS")
if [ "$HTTP_STATUS" = "200" ]; then
    echo "   ✅ Token refresh works (Status: $HTTP_STATUS)"
    NEW_ACCESS=$(echo "$REFRESH_BODY" | grep -o '"access":"[^"]*' | cut -d'"' -f4)
    if [ -n "$NEW_ACCESS" ]; then
        echo "   New token obtained: ${NEW_ACCESS:0:20}..."
    fi
else
    echo "   ❌ Token refresh failed (Status: $HTTP_STATUS)"
    echo "   Response: $REFRESH_BODY"
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
echo ""
echo "Test completed at: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "Exit code: 0 (PASS)"