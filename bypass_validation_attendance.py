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

# Clear existing attendance
with connection.cursor() as cursor:
    cursor.execute("DELETE FROM schoolmgmt_studentattendance")

# Get school days from calendar (Baisakh 1 to current day)
school_days = CalendarEvent.objects.filter(
    event_type__in=['school-day', 'event'],
    event_date__gte=date(2025, 4, 14),
    event_date__lte=date.today()
).order_by('event_date')

students = Student.objects.all()
attendance_count = 0

# Bulk insert to bypass validation
attendance_records = []
for school_day in school_days:
    for student in students:
        rand = random.randint(1, 100)
        if rand <= 85:
            status = 'present'
        elif rand <= 95:
            status = 'late'
        else:
            status = 'absent'
        
        attendance_records.append((
            student.id,
            school_day.event_date.strftime('%Y-%m-%d'),
            status,
            'Auto System',
            school_day.event_date.strftime('%Y-%m-%d %H:%M:%S'),
            school_day.event_date.strftime('%Y-%m-%d %H:%M:%S')
        ))
        attendance_count += 1

# Bulk insert using raw SQL
with connection.cursor() as cursor:
    cursor.executemany(
        "INSERT INTO schoolmgmt_studentattendance (student_id, date, status, marked_by, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
        attendance_records
    )

print(f"Populated {attendance_count} attendance records")
print(f"For {students.count()} students across {school_days.count()} school days")
print(f"From Baisakh 1 to {date.today()}")