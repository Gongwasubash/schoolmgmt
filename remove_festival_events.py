#!/usr/bin/env python
"""
Script to remove all festival events from the school calendar
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent

def remove_festival_events():
    """Remove all festival events from the calendar"""
    try:
        # Get all festival events
        festival_events = CalendarEvent.objects.filter(event_type='festival')
        count = festival_events.count()
        
        if count == 0:
            print("No festival events found in the calendar.")
            return
        
        print(f"Found {count} festival events:")
        for event in festival_events:
            print(f"- {event.title} ({event.event_date})")
        
        # Confirm deletion
        confirm = input(f"\nAre you sure you want to delete all {count} festival events? (y/N): ")
        
        if confirm.lower() in ['y', 'yes']:
            # Delete all festival events
            deleted_count = festival_events.delete()[0]
            print(f"\nSuccessfully deleted {deleted_count} festival events from the calendar.")
        else:
            print("Operation cancelled.")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("School Calendar Festival Event Removal Tool")
    print("=" * 50)
    remove_festival_events()