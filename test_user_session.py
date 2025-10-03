#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from django.test import Client
from schoolmgmt.models import AdminLogin

def test_user_login_session():
    # Get a basic user
    user = AdminLogin.objects.filter(is_super_admin=False, is_active=True).first()
    print(f"Testing user: {user.username}")
    print(f"can_view_reports: {user.can_view_reports}")
    
    # Test login
    client = Client()
    response = client.post('/user-login/', {
        'username': user.username,
        'password': user.password
    })
    
    print(f"Login response: {response.status_code}")
    
    # Check session
    session = client.session
    print("Session keys:")
    for key in session.keys():
        if key.startswith('can_') or key in ['admin_logged_in', 'user_id']:
            print(f"  {key}: {session[key]}")
    
    # Test reports access
    response = client.get('/reports/')
    print(f"Reports access: {response.status_code}")
    if response.status_code == 302:
        print(f"Redirected to: {response.url}")

if __name__ == "__main__":
    test_user_login_session()