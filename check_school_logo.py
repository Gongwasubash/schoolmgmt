#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import SchoolDetail

# Check current school
school = SchoolDetail.get_current_school()
print(f"School Name: {school.school_name}")
print(f"School Logo: {school.logo}")
print(f"Logo Path: {school.logo.name if school.logo else 'No logo'}")

# If no logo, set one
if not school.logo:
    school.logo = 'school_logos/Everest-Crest-Square.png'
    school.save()
    print("Logo updated!")
    print(f"New Logo Path: {school.logo.name}")