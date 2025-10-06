import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent

# Delete all calendar events
deleted_count = CalendarEvent.objects.all().delete()[0]
print(f"Successfully deleted {deleted_count} calendar events")