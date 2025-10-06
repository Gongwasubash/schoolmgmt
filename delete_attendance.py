#!/usr/bin/env python3
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import StudentAttendance

count = StudentAttendance.objects.count()
StudentAttendance.objects.all().delete()
print(f"Deleted {count} attendance records")