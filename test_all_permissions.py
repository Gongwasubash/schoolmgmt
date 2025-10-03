#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from django.test import Client
from schoolmgmt.models import AdminLogin

def test_all_permissions():
    user = AdminLogin.objects.filter(is_super_admin=False, is_active=True).first()
    print(f"User: {user.username}")
    print("User permissions:")
    print(f"  can_view_dashboard: {user.can_view_dashboard}")
    print(f"  can_view_students: {user.can_view_students}")
    print(f"  can_view_teachers: {user.can_view_teachers}")
    print(f"  can_view_reports: {user.can_view_reports}")
    print(f"  can_view_marksheet: {user.can_view_marksheet}")
    
    client = Client()
    response = client.post('/admin-login/', {
        'username': user.username,
        'password': user.password
    })
    
    session = client.session
    print("\nSession permissions:")
    print(f"  can_view_dashboard: {session.get('can_view_dashboard')}")
    print(f"  can_view_students: {session.get('can_view_students')}")
    print(f"  can_view_teachers: {session.get('can_view_teachers')}")
    print(f"  can_view_reports: {session.get('can_view_reports')}")
    print(f"  can_view_marksheet: {session.get('can_view_marksheet')}")
    
    # Test each page
    pages = [
        ('/dashboard/', 'Dashboard'),
        ('/students/', 'Students'),
        ('/teachers/', 'Teachers'),
        ('/reports/', 'Reports'),
        ('/marksheet/', 'Marksheet')
    ]
    
    print("\nPage access tests:")
    for url, name in pages:
        try:
            response = client.get(url)
            if response.status_code == 200:
                print(f"  {name}: SUCCESS (200)")
            elif response.status_code == 302:
                print(f"  {name}: REDIRECT to {response.url}")
            else:
                print(f"  {name}: ERROR ({response.status_code})")
        except Exception as e:
            print(f"  {name}: EXCEPTION - {e}")

if __name__ == "__main__":
    test_all_permissions()