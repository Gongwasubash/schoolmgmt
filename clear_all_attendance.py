#!/usr/bin/env python3
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import StudentAttendance, SchoolAttendance

# Delete all StudentAttendance records
count1 = StudentAttendance.objects.count()
StudentAttendance.objects.all().delete()

# Delete all SchoolAttendance records  
count2 = SchoolAttendance.objects.count()
SchoolAttendance.objects.all().delete()

print(f"Deleted {count1} StudentAttendance records")
print(f"Deleted {count2} SchoolAttendance records")
print("All attendance data cleared from backend")