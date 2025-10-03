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

def check_and_create_users():
    print("Checking AdminLogin users...")
    
    # List all users
    users = AdminLogin.objects.all()
    print(f"Found {users.count()} users:")
    
    for user in users:
        print(f"- {user.username}: super_admin={user.is_super_admin}, can_create={user.can_create_users}, can_delete={user.can_delete_users}, can_settings={user.can_view_settings}")
    
    # Create a basic user if none exists with limited permissions
    basic_user_exists = AdminLogin.objects.filter(
        can_create_users=False,
        can_delete_users=False,
        can_view_settings=False,
        is_super_admin=False
    ).exists()
    
    if not basic_user_exists:
        print("\nCreating basic user...")
        basic_password = "basic123"
        basic_password_hash = hashlib.md5(basic_password.encode()).hexdigest()
        
        AdminLogin.objects.create(
            username="basicuser",
            password=basic_password_hash,
            is_active=True,
            is_super_admin=False,
            can_create_users=False,
            can_delete_users=False,
            can_view_dashboard=True,
            can_view_charts=True,
            can_view_stats=True,
            can_view_students=True,
            can_view_teachers=False,
            can_view_reports=True,
            can_view_marksheet=False,
            can_view_fees=False,
            can_view_receipts=False,
            can_view_expenses=False,
            can_view_settings=False
        )
        print("Basic user created: basicuser/basic123")
    else:
        print("Basic user already exists")

if __name__ == "__main__":
    check_and_create_users()