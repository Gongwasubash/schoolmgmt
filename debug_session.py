#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from django.test import Client
from schoolmgmt.models import AdminLogin

def debug_session():
    username = input("Enter username to test: ")
    user = AdminLogin.objects.get(username=username, is_active=True)
    
    print(f"Database permissions for {username}:")
    print(f"  can_view_dashboard: {user.can_view_dashboard}")
    print(f"  can_view_students: {user.can_view_students}")
    print(f"  can_view_teachers: {user.can_view_teachers}")
    print(f"  can_view_reports: {user.can_view_reports}")
    
    client = Client()
    response = client.post('/admin-login/', {
        'username': user.username,
        'password': user.password
    })
    
    session = client.session
    print(f"\nSession permissions after login:")
    print(f"  can_view_dashboard: {session.get('can_view_dashboard')}")
    print(f"  can_view_students: {session.get('can_view_students')}")
    print(f"  can_view_teachers: {session.get('can_view_teachers')}")
    print(f"  can_view_reports: {session.get('can_view_reports')}")
    
    # Test teachers page specifically
    print(f"\nTesting teachers page:")
    response = client.get('/teachers/')
    print(f"Status: {response.status_code}")
    if response.status_code == 302:
        print(f"Redirected to: {response.url}")

if __name__ == "__main__":
    debug_session()