#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from django.test import Client
from schoolmgmt.models import AdminLogin

def test_teachers_simple():
    user = AdminLogin.objects.filter(is_super_admin=False, is_active=True).first()
    print(f"User: {user.username}")
    print(f"can_view_teachers: {user.can_view_teachers}")
    
    client = Client()
    
    # Login via admin login
    response = client.post('/admin-login/', {
        'username': user.username,
        'password': user.password
    })
    print(f"Login status: {response.status_code}")
    
    # Check session
    session = client.session
    print(f"Session can_view_teachers: {session.get('can_view_teachers')}")
    print(f"Session admin_logged_in: {session.get('admin_logged_in')}")
    
    # Try teachers page
    response = client.get('/teachers/')
    print(f"Teachers page status: {response.status_code}")
    if response.status_code == 302:
        print(f"Redirected to: {response.url}")

if __name__ == "__main__":
    test_teachers_simple()