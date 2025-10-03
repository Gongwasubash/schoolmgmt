#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from django.contrib.sessions.models import Session
from schoolmgmt.models import AdminLogin
import pickle
import base64

def refresh_user_permissions():
    username = input("Enter username to refresh permissions: ")
    
    try:
        user = AdminLogin.objects.get(username=username, is_active=True)
        print(f"Found user: {user.username}")
        
        # Find all sessions for this user
        sessions = Session.objects.all()
        updated_sessions = 0
        
        for session in sessions:
            try:
                session_data = session.get_decoded()
                if session_data.get('admin_username') == username or session_data.get('user_username') == username:
                    # Update session with current permissions
                    if user.is_super_admin:
                        session_data.update({
                            'can_view_dashboard': True,
                            'can_view_students': True,
                            'can_view_teachers': True,
                            'can_view_reports': True,
                            'can_view_marksheet': True,
                            'can_view_fees': True,
                            'can_view_receipts': True,
                            'can_view_expenses': True,
                            'can_view_settings': True,
                        })
                    else:
                        session_data.update({
                            'can_view_dashboard': user.can_view_dashboard,
                            'can_view_students': user.can_view_students,
                            'can_view_teachers': user.can_view_teachers,
                            'can_view_reports': user.can_view_reports,
                            'can_view_marksheet': user.can_view_marksheet,
                            'can_view_fees': getattr(user, 'can_view_fees', True),
                            'can_view_receipts': getattr(user, 'can_view_receipts', True),
                            'can_view_expenses': getattr(user, 'can_view_expenses', True),
                            'can_view_settings': getattr(user, 'can_view_settings', True),
                        })
                    
                    # Save updated session
                    session.session_data = Session.objects.encode(session_data)
                    session.save()
                    updated_sessions += 1
                    print(f"Updated session: {session.session_key[:10]}...")
            except:
                continue
        
        print(f"Updated {updated_sessions} sessions for user {username}")
        print("User can now access pages with updated permissions without re-login")
        
    except AdminLogin.DoesNotExist:
        print(f"User '{username}' not found")

if __name__ == "__main__":
    refresh_user_permissions()