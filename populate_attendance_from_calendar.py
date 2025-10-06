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

def populate_attendance():
    # Get all school days from calendar up to today
    school_days = CalendarEvent.objects.filter(
        event_type__in=['school-day', 'event'],
        event_date__gte=date(2025, 4, 14),  # Baisakh 1, 2082
        event_date__lte=date.today()
    ).order_by('event_date')
    
    # Get all students
    students = Student.objects.all()
    
    attendance_count = 0
    
    for school_day in school_days:
        for student in students:
            # Check if attendance already exists
            if not StudentAttendance.objects.filter(
                student=student, 
                date=school_day.event_date
            ).exists():
                
                # Random attendance status (90% present, 7% late, 3% absent)
                rand = random.randint(1, 100)
                if rand <= 90:
                    status = 'present'
                elif rand <= 97:
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

if __name__ == "__main__":
    populate_attendance()