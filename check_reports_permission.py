#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import AdminLogin

# Check a basic user's reports permission
user = AdminLogin.objects.filter(is_super_admin=False, is_active=True).first()
if user:
    print(f"User: {user.username}")
    print(f"can_view_reports: {user.can_view_reports}")
    print(f"All permissions:")
    for field in user._meta.fields:
        if field.name.startswith('can_view_'):
            value = getattr(user, field.name)
            print(f"  {field.name}: {value}")
else:
    print("No basic users found")