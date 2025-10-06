#!/usr/bin/env python3
import os
import sys
import django
import random
from datetime import date

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent, StudentAttendance, Student

# Clear existing attendance first
StudentAttendance.objects.all().delete()

# Get school days from calendar (Baisakh 1 to current day)
school_days = CalendarEvent.objects.filter(
    event_type__in=['school-day', 'event'],
    event_date__gte=date(2025, 4, 14),  # Baisakh 1, 2082
    event_date__lte=date.today()
).order_by('event_date')

students = Student.objects.all()
attendance_count = 0

for school_day in school_days:
    for student in students:
        # Random attendance (85% present, 10% late, 5% absent)
        rand = random.randint(1, 100)
        if rand <= 85:
            status = 'present'
        elif rand <= 95:
            status = 'late'
        else:
            status = 'absent'
        
        StudentAttendance.objects.create(
            student=student,
            date=school_day.event_date,
            status=status,
            marked_by='Auto System'
        )
        attendance_count += 1

print(f"Populated {attendance_count} attendance records")
print(f"For {students.count()} students across {school_days.count()} school days")
print(f"From Baisakh 1 to {date.today()}")