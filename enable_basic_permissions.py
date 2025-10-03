#!/usr/bin/env python
"""
Script to enable all sidebar menu permissions for basic users
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import AdminLogin

def enable_all_permissions_for_basic_users():
    """Enable all sidebar menu permissions for non-super admin users"""
    basic_users = AdminLogin.objects.filter(is_super_admin=False, is_active=True)
    
    print(f"Found {basic_users.count()} basic users")
    
    for user in basic_users:
        print(f"Enabling all permissions for user: {user.username}")
        user.enable_all_permissions()
        print(f"[OK] All permissions enabled for {user.username}")
    
    print("\nAll basic users now have access to all sidebar menu items!")

if __name__ == "__main__":
    enable_all_permissions_for_basic_users()