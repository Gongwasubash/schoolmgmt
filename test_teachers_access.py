#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from django.test import Client
from schoolmgmt.models import AdminLogin

def test_teachers_access():
    user = AdminLogin.objects.filter(is_super_admin=False, is_active=True).first()
    print(f"Testing teachers access for: {user.username}")
    print(f"can_view_teachers: {user.can_view_teachers}")
    
    client = Client()
    response = client.post('/admin-login/', {
        'username': user.username,
        'password': user.password
    })
    
    print(f"Login response: {response.status_code}")
    
    session = client.session
    print("Session keys:")
    for key in ['admin_logged_in', 'can_view_teachers']:
        print(f"  {key}: {session.get(key)}")
    
    response = client.get('/teachers/')
    print(f"Teachers access: {response.status_code}")
    if response.status_code == 302:
        print(f"Redirected to: {response.url}")

if __name__ == "__main__":
    test_teachers_access()