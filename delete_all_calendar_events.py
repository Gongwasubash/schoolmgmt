#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent

def delete_all_calendar_events():
    """Delete all calendar events from the database"""
    try:
        # Get count before deletion
        total_events = CalendarEvent.objects.count()
        print(f"Found {total_events} calendar events in the database.")
        
        if total_events == 0:
            print("No calendar events to delete.")
            return
        
        # Delete all calendar events
        deleted_count, _ = CalendarEvent.objects.all().delete()
        print(f"Successfully deleted {deleted_count} calendar events.")
        print("All calendar event data has been removed from the database.")
            
    except Exception as e:
        print(f"Error occurred while deleting calendar events: {str(e)}")

if __name__ == "__main__":
    delete_all_calendar_events()