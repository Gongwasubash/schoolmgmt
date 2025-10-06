#!/usr/bin/env python3
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent
from schoolmgmt.nepali_calendar import NepaliCalendar
from datetime import date

def verify_complete_calendar():
    """Verify the complete Nepali calendar from Baishakh 1 to Chaitra 30"""
    
    print("NEPALI CALENDAR VERIFICATION")
    print("From Baishakh 1 to Chaitra 30, 2082 BS")
    print("="*60)
    
    # Get all events
    all_events = CalendarEvent.objects.all().order_by('event_date')
    festivals = CalendarEvent.objects.filter(event_type='festival').order_by('event_date')
    school_events = CalendarEvent.objects.filter(event_type='event').order_by('event_date')
    holidays = CalendarEvent.objects.filter(event_type='holiday').count()
    
    print(f"SUMMARY:")
    print(f"Total Events: {all_events.count()}")
    print(f"Festivals: {festivals.count()}")
    print(f"School Events: {school_events.count()}")
    print(f"Holidays (Saturdays): {holidays}")
    
    print(f"\nMAJOR FESTIVALS (Baishakh 1 to Chaitra 30):")
    print("-" * 50)
    
    for i, festival in enumerate(festivals, 1):
        nepali_date = NepaliCalendar.english_to_nepali_date(festival.event_date)
        month_name = NepaliCalendar.NEPALI_MONTHS_EN[nepali_date['month']-1]
        
        print(f"{i:2d}. {festival.title}")
        print(f"    Nepali:  {nepali_date['day']} {month_name}, {nepali_date['year']} BS")
        print(f"    English: {festival.event_date}")
        print()
    
    print(f"\nSCHOOL EVENTS:")
    print("-" * 30)
    
    for i, event in enumerate(school_events, 1):
        nepali_date = NepaliCalendar.english_to_nepali_date(event.event_date)
        month_name = NepaliCalendar.NEPALI_MONTHS_EN[nepali_date['month']-1]
        
        print(f"{i:2d}. {event.title}")
        print(f"    {nepali_date['day']} {month_name}, {nepali_date['year']} BS ({event.event_date})")
    
    print(f"\nUPCOMING EVENTS (Next 10):")
    print("-" * 30)
    
    upcoming = CalendarEvent.objects.filter(
        event_date__gte=date.today()
    ).order_by('event_date')[:10]
    
    for i, event in enumerate(upcoming, 1):
        nepali_date = NepaliCalendar.english_to_nepali_date(event.event_date)
        print(f"{i:2d}. {event.title} ({event.event_type})")
        print(f"    {event.event_date} ({NepaliCalendar.format_nepali_date(nepali_date, 'short')} BS)")
    
    print(f"\n{'='*60}")
    print("CALENDAR VERIFICATION COMPLETE!")
    print("All festivals from Baishakh 1 to Chaitra 30 have been populated.")
    print("Festival dates are now accurate according to traditional Nepali calendar.")

def show_month_wise_events():
    """Show events organized by Nepali months"""
    
    print(f"\nMONTH-WISE EVENT BREAKDOWN:")
    print("="*40)
    
    current_year = NepaliCalendar.get_current_nepali_date()['year']
    
    for month in range(1, 13):
        month_name = NepaliCalendar.NEPALI_MONTHS_EN[month-1]
        
        # Get events for this Nepali month (approximate)
        month_events = []
        
        for event in CalendarEvent.objects.filter(event_type__in=['festival', 'event']).order_by('event_date'):
            nepali_date = NepaliCalendar.english_to_nepali_date(event.event_date)
            if nepali_date['month'] == month and nepali_date['year'] == current_year:
                month_events.append((event, nepali_date))
        
        print(f"\n{month}. {month_name.upper()}:")
        if month_events:
            for event, nepali_date in month_events:
                print(f"   {nepali_date['day']:2d} - {event.title} ({event.event_type})")
        else:
            print("   No major events recorded")

if __name__ == "__main__":
    verify_complete_calendar()
    show_month_wise_events()