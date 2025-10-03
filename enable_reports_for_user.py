#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import AdminLogin

username = input("Enter username to enable reports for: ")
try:
    user = AdminLogin.objects.get(username=username, is_active=True)
    print(f"Found user: {user.username}")
    print(f"Current can_view_reports: {user.can_view_reports}")
    
    user.can_view_reports = True
    user.save()
    
    print(f"Updated can_view_reports: {user.can_view_reports}")
    print("User can now access reports!")
    
except AdminLogin.DoesNotExist:
    print(f"User '{username}' not found")