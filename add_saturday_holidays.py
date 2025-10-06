#!/usr/bin/env python3
import os
import sys
import django
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent, SchoolDetail

def add_all_saturdays():
    school = SchoolDetail.get_current_school()
    
    # Remove existing Saturday holidays
    CalendarEvent.objects.filter(event_type='holiday', title='Saturday Holiday').delete()
    
    # Add Saturdays for 2025 and 2026
    start_date = datetime(2025, 1, 1).date()
    end_date = datetime(2026, 12, 31).date()
    
    current_date = start_date
    saturday_count = 0
    
    while current_date <= end_date:
        if current_date.weekday() == 5:  # Saturday
            CalendarEvent.objects.create(
                title="Saturday Holiday",
                description="Weekly holiday",
                event_date=current_date,
                event_type='holiday',
                school=school,
                created_by='Saturday System'
            )
            saturday_count += 1
        current_date += timedelta(days=1)
    
    print(f"Added {saturday_count} Saturday holidays for 2025-2026")

if __name__ == "__main__":
    add_all_saturdays()