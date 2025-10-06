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

school_days = CalendarEvent.objects.filter(
    event_type__in=['school-day', 'event'],
    event_date__gte=date(2025, 4, 14),
    event_date__lte=date.today()
).order_by('event_date')

students = Student.objects.all()
attendance_count = 0

for school_day in school_days:
    for student in students:
        # Use get_or_create to avoid duplicates
        attendance, created = StudentAttendance.objects.get_or_create(
            student=student,
            date=school_day.event_date,
            defaults={
                'status': 'present' if random.randint(1, 100) <= 90 else ('late' if random.randint(1, 100) <= 70 else 'absent'),
                'marked_by': 'Auto System'
            }
        )
        if created:
            attendance_count += 1

print(f"Populated {attendance_count} new attendance records")
print(f"For {students.count()} students across {school_days.count()} school days")