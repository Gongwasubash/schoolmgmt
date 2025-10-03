#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from django.test import Client
from schoolmgmt.models import AdminLogin

def test_admin_login():
    user = AdminLogin.objects.filter(is_super_admin=False, is_active=True).first()
    print(f"Testing admin login for: {user.username}")
    print(f"can_view_reports: {user.can_view_reports}")
    
    client = Client()
    response = client.post('/admin-login/', {
        'username': user.username,
        'password': user.password
    })
    
    print(f"Admin login response: {response.status_code}")
    
    session = client.session
    print("Session keys after admin login:")
    for key in session.keys():
        if key.startswith('can_') or key in ['admin_logged_in', 'admin_id']:
            print(f"  {key}: {session[key]}")
    
    response = client.get('/reports/')
    print(f"Reports access: {response.status_code}")
    if response.status_code == 302:
        print(f"Redirected to: {response.url}")

if __name__ == "__main__":
    test_admin_login()