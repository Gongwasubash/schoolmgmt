#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent

def update_school_day_events():
    """Update all calendar events with title 'School Day' to have event_type 'school-day'"""
    
    # Find all events with title containing "School Day"
    events_to_update = CalendarEvent.objects.filter(title__icontains='School Day')
    
    updated_count = 0
    for event in events_to_update:
        event.event_type = 'school-day'
        event.save()
        updated_count += 1
        print(f"Updated event: {event.title} (ID: {event.id}) -> event_type: school-day")
    
    print(f"\nTotal events updated: {updated_count}")
    
    # Also update any events with title exactly "school day" (case insensitive)
    additional_events = CalendarEvent.objects.filter(title__iexact='school day').exclude(event_type='school-day')
    
    additional_count = 0
    for event in additional_events:
        event.event_type = 'school-day'
        event.save()
        additional_count += 1
        print(f"Updated additional event: {event.title} (ID: {event.id}) -> event_type: school-day")
    
    print(f"Additional events updated: {additional_count}")
    print(f"Grand total updated: {updated_count + additional_count}")

if __name__ == '__main__':
    update_school_day_events()