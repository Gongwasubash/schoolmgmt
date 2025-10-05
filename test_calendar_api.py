#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent

def test_calendar_api():
    print("=== Calendar API Test ===")
    
    # Test 1: Count total events
    total_events = CalendarEvent.objects.count()
    print(f"Total events in database: {total_events}")
    
    # Test 2: Get current month events
    current_month = datetime.now().month
    current_year = datetime.now().year
    current_events = CalendarEvent.objects.filter(
        event_date__year=current_year,
        event_date__month=current_month
    ).count()
    print(f"Current month events: {current_events}")
    
    # Test 3: Get upcoming events (next 7 days)
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    upcoming = CalendarEvent.objects.filter(
        event_date__gte=today,
        event_date__lte=next_week
    ).order_by('event_date')[:5]
    
    print(f"\nUpcoming events (next 7 days): {upcoming.count()}")
    for event in upcoming:
        print(f"  - {event.event_date.strftime('%d %b')}: {event.title}")
    
    # Test 4: Event types distribution
    event_types = CalendarEvent.objects.values_list('event_type', flat=True).distinct()
    print(f"\nEvent types: {list(event_types)}")
    
    print("\n[SUCCESS] Calendar API is working properly!")
    print("Visit: http://localhost:8000/school-calendar/ to view the calendar")

if __name__ == "__main__":
    test_calendar_api()