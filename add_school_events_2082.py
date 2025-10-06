#!/usr/bin/env python3
import os
import sys
import django
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent, SchoolDetail

# School events for 2082 BS (Baisakh 1 to Chaitra 30)
SCHOOL_EVENTS_2082 = [
    {"date": "2025-04-15", "name": "New Academic Session Begins", "type": "event"},
    {"date": "2025-04-20", "name": "Parent Meeting", "type": "event"},
    {"date": "2025-05-15", "name": "First Term Exam", "type": "exam"},
    {"date": "2025-05-20", "name": "Sports Day", "type": "event"},
    {"date": "2025-06-10", "name": "Mid Term Exam", "type": "exam"},
    {"date": "2025-06-25", "name": "Result Publication", "type": "event"},
    {"date": "2025-07-05", "name": "Teacher Training Day", "type": "event"},
    {"date": "2025-07-20", "name": "Science Fair", "type": "event"},
    {"date": "2025-08-15", "name": "Second Term Exam", "type": "exam"},
    {"date": "2025-08-25", "name": "Cultural Program", "type": "event"},
    {"date": "2025-09-10", "name": "Pre-Dashain Exam", "type": "exam"},
    {"date": "2025-11-10", "name": "Post-Dashain Classes Resume", "type": "event"},
    {"date": "2025-11-25", "name": "Annual Exam Preparation", "type": "event"},
    {"date": "2025-12-05", "name": "Third Term Exam", "type": "exam"},
    {"date": "2025-12-20", "name": "Winter Break Begins", "type": "event"},
    {"date": "2026-01-05", "name": "Classes Resume", "type": "event"},
    {"date": "2026-01-20", "name": "Final Term Exam", "type": "exam"},
    {"date": "2026-02-10", "name": "Annual Result", "type": "event"},
    {"date": "2026-02-20", "name": "Graduation Ceremony", "type": "event"},
    {"date": "2026-03-05", "name": "Annual Sports Meet", "type": "event"},
    {"date": "2026-03-20", "name": "Final Exam", "type": "exam"},
    {"date": "2026-04-05", "name": "Session End Ceremony", "type": "event"}
]

def add_school_days():
    """Add regular school days (excluding Saturdays and holidays)"""
    school = SchoolDetail.get_current_school()
    
    start_date = datetime(2025, 4, 14).date()  # Baisakh 1, 2082
    end_date = datetime(2026, 4, 13).date()    # Chaitra 30, 2082
    
    current_date = start_date
    school_days = 0
    
    while current_date <= end_date:
        if current_date.weekday() != 5:  # Not Saturday
            # Check if not already a festival/holiday
            existing = CalendarEvent.objects.filter(
                event_date=current_date,
                event_type__in=['festival', 'holiday']
            ).exists()
            
            if not existing:
                CalendarEvent.objects.create(
                    title="School Day",
                    description="Regular school day",
                    event_date=current_date,
                    event_type='school-day',
                    school=school,
                    created_by='School Calendar System'
                )
                school_days += 1
        
        current_date += timedelta(days=1)
    
    return school_days

def add_school_events():
    """Add school events and exams"""
    school = SchoolDetail.get_current_school()
    
    for event in SCHOOL_EVENTS_2082:
        event_date = datetime.strptime(event['date'], '%Y-%m-%d').date()
        CalendarEvent.objects.create(
            title=event['name'],
            description=f"School {event['type']} for academic year 2082",
            event_date=event_date,
            event_type=event['type'],
            school=school,
            created_by='School Events System'
        )
    
    return len(SCHOOL_EVENTS_2082)

# Add school events
events_count = add_school_events()
print(f"Added {events_count} school events and exams")

# Add school days
school_days_count = add_school_days()
print(f"Added {school_days_count} regular school days")

print(f"\nTotal school calendar events added: {events_count + school_days_count}")
print("School calendar complete from Baisakh 1 to Chaitra 30, 2082!")