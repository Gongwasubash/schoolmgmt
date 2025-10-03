#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('e:\\schoolmgmt')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import AdminLogin
import hashlib

def test_login_logic():
    print("Testing login logic...")
    
    # Test users
    test_users = ['basicuser', 'superadmin', 'subashgongwa']
    
    for username in test_users:
        try:
            admin = AdminLogin.objects.get(username=username, is_active=True)
            
            # Check if user has basic permissions (limited access)
            has_basic_permissions = (
                not admin.can_create_users and 
                not admin.can_delete_users and 
                not admin.is_super_admin
            )
            
            redirect_to = 'basic_dashboard' if has_basic_permissions else 'dashboard'
            
            print(f"\nUser: {username}")
            print(f"  - can_create_users: {admin.can_create_users}")
            print(f"  - can_delete_users: {admin.can_delete_users}")
            print(f"  - is_super_admin: {admin.is_super_admin}")
            print(f"  - has_basic_permissions: {has_basic_permissions}")
            print(f"  - redirect_to: {redirect_to}")
            
        except AdminLogin.DoesNotExist:
            print(f"User {username} not found")

if __name__ == "__main__":
    test_login_logic()