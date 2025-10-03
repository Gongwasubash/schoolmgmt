#!/usr/bin/env python
"""
Test script to verify basic users can access reports
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from django.test import Client
from schoolmgmt.models import AdminLogin

def test_basic_user_reports_access():
    """Test that basic users can access reports page"""
    
    # Get a basic user
    basic_user = AdminLogin.objects.filter(is_super_admin=False, is_active=True).first()
    
    if not basic_user:
        print("No basic users found to test")
        return
    
    print(f"Testing reports access for user: {basic_user.username}")
    print(f"User can_view_reports: {basic_user.can_view_reports}")
    
    # Create a test client
    client = Client()
    
    # Simulate login by setting session
    session = client.session
    session['user_id'] = basic_user.id
    session['user_username'] = basic_user.username
    session['user_is_super_admin'] = basic_user.is_super_admin
    session['admin_logged_in'] = True  # Required by middleware
    session['can_view_reports'] = basic_user.can_view_reports
    session.save()
    
    # Try to access reports page
    try:
        response = client.get('/reports/')
        print(f"Reports page response status: {response.status_code}")
        
        if response.status_code == 200:
            print("[SUCCESS] Basic user can access reports page!")
            
            # Check if it's using the basic template
            if hasattr(response, 'template_name'):
                print(f"Template used: {response.template_name}")
            
            # Check context for debug info
            if 'debug_session_info' in response.context:
                debug_info = response.context['debug_session_info']
                print(f"Template name from context: {debug_info.get('template_name')}")
                print(f"Is basic user: {debug_info.get('is_basic_user')}")
            
        elif response.status_code == 302:
            print(f"[REDIRECT] User redirected to: {response.url}")
        else:
            print(f"[ERROR] Unexpected status code: {response.status_code}")
            
    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")

if __name__ == "__main__":
    test_basic_user_reports_access()