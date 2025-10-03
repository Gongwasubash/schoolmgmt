#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import AdminLogin

username = input("Enter username: ")
try:
    user = AdminLogin.objects.get(username=username, is_active=True)
    print(f"Found user: {user.username}")
    
    print("\nCurrent permissions:")
    print(f"Dashboard: {user.can_view_dashboard}")
    print(f"Students: {user.can_view_students}")
    print(f"Teachers: {user.can_view_teachers}")
    print(f"Reports: {user.can_view_reports}")
    print(f"Marksheet: {user.can_view_marksheet}")
    
    # Enable specific permissions for testing
    user.can_view_dashboard = False  # Disable dashboard
    user.can_view_students = True    # Enable students
    user.can_view_teachers = True    # Enable teachers
    user.can_view_reports = True     # Enable reports
    user.can_view_marksheet = True   # Enable marksheet
    user.save()
    
    print("\nUpdated permissions:")
    print(f"Dashboard: {user.can_view_dashboard}")
    print(f"Students: {user.can_view_students}")
    print(f"Teachers: {user.can_view_teachers}")
    print(f"Reports: {user.can_view_reports}")
    print(f"Marksheet: {user.can_view_marksheet}")
    
except AdminLogin.DoesNotExist:
    print(f"User '{username}' not found")