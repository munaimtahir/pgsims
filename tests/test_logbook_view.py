"""
Simple test page to verify logbook access is working.
"""

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def test_logbook_access(request):
    """Simple test view to verify logbook access works"""
    
    user = request.user
    response_lines = [
        f"<h1>Logbook Access Test</h1>",
        f"<p>User: {user.username} ({user.get_full_name()})</p>",
        f"<p>Role: {user.role}</p>",
    ]
    
    if user.role == 'supervisor':
        try:
            # Test the assigned_pgs relationship
            pgs = user.assigned_pgs.filter(is_active=True)
            response_lines.append(f"<p>✓ assigned_pgs relationship works!</p>")
            response_lines.append(f"<p>Assigned PGs: {pgs.count()}</p>")
            
            for pg in pgs[:5]:  # Show first 5
                response_lines.append(f"<li>{pg.username} - {pg.get_full_name()}</li>")
                
        except Exception as e:
            response_lines.append(f"<p>✗ Error with assigned_pgs: {str(e)}</p>")
    
    response_lines.append('<p><a href="/logbook/">Go to actual logbook page</a></p>')
    
    return HttpResponse('\n'.join(response_lines))
