#!/usr/bin/env python
"""
Script to automatically remove all festival events from the school calendar
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

def auto_remove_festival_events():
    """Automatically remove all festival events from the calendar"""
    try:
        # Get all festival events
        festival_events = CalendarEvent.objects.filter(event_type='festival')
        count = festival_events.count()
        
        if count == 0:
            print("No festival events found in the calendar.")
            return
        
        print(f"Found {count} festival events. Removing all...")
        
        # Delete all festival events
        deleted_count = festival_events.delete()[0]
        print(f"Successfully deleted {deleted_count} festival events from the calendar.")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Auto-removing all festival events from school calendar...")
    print("=" * 50)
    auto_remove_festival_events()