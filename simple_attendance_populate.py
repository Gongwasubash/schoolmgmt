#!/usr/bin/env python3
import os
import sys
import django
import random
from datetime import date

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent, Student
from django.db import connection

# Get school days from calendar (Baisakh 1 to current day)
school_days = CalendarEvent.objects.filter(
    event_type__in=['school-day', 'event'],
    event_date__gte=date(2025, 4, 14),
    event_date__lte=date.today()
).values_list('event_date', flat=True)

students = Student.objects.values_list('id', flat=True)
attendance_count = 0

# Insert one by one with INSERT OR IGNORE
for school_day in school_days:
    for student_id in students:
        rand = random.randint(1, 100)
        if rand <= 85:
            status = 'present'
        elif rand <= 95:
            status = 'late'
        else:
            status = 'absent'
        
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT OR IGNORE INTO schoolmgmt_studentattendance (student_id, date, status, marked_by, created_at, updated_at) VALUES (?, ?, ?, ?, datetime('now'), datetime('now'))",
                [student_id, school_day, status, 'Auto System']
            )
            if cursor.rowcount > 0:
                attendance_count += 1

print(f"Populated {attendance_count} attendance records")
print(f"For {len(students)} students across {len(school_days)} school days")
print(f"From Baisakh 1 to {date.today()}")