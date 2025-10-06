#!/usr/bin/env python3
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent, SchoolDetail
from schoolmgmt.nepali_calendar import NepaliCalendar

# Complete Nepali Calendar Events (Baishakh 1 to Chaitra 30)
FESTIVALS = {
    1: {1: "Nepali New Year", 8: "Buddha Jayanti", 15: "Ram Navami"},
    2: {15: "Kumar Shashthi"},
    3: {15: "Harishayani Ekadashi"},
    4: {1: "Shrawan Sankranti", 15: "Janai Purnima", 23: "Gai Jatra"},
    5: {3: "Teej Festival", 18: "Rishi Panchami"},
    6: {7: "Ghatasthapana", 15: "Vijaya Dashami"},
    7: {2: "Gai Tihar", 3: "Goru Tihar", 5: "Bhai Tika", 15: "Chhath Parva"},
    8: {8: "Yomari Punhi"},
    9: {1: "Poush Sankranti"},
    10: {1: "Maghe Sankranti", 5: "Shree Panchami", 14: "Shivaratri"},
    11: {15: "Holi Festival"},
    12: {8: "Chaitra Ashtami", 30: "Chaitra Purnima"}
}

SCHOOL_EVENTS = {
    1: {10: "New Session Begins", 20: "Parent Meeting"},
    2: {15: "Sports Competition", 25: "Cultural Program"},
    3: {10: "Annual Examination", 25: "Exam Results"},
    4: {5: "Teacher's Day", 20: "Science Fair"},
    5: {15: "Cleanliness Campaign", 25: "Tree Plantation"},
    6: {10: "Dashain Holiday Begins", 25: "Dashain Holiday Ends"},
    7: {10: "Tihar Holiday Begins", 20: "Tihar Holiday Ends"},
    8: {15: "Winter Holiday", 30: "Annual Celebration"},
    9: {10: "Winter Sports", 25: "Community Service"},
    10: {15: "Art Exhibition", 25: "Final Exam Preparation"},
    11: {10: "Holi Celebration", 25: "Graduation Ceremony"},
    12: {15: "Annual Review", 29: "Session End"}
}

def populate_complete_calendar(year=2082):
    print(f"Populating complete calendar for Nepali year {year}...")
    print("From Baishakh 1 to Chaitra 30")
    print("="*50)
    
    school = SchoolDetail.get_current_school()
    
    # Clear existing events
    CalendarEvent.objects.filter(
        event_type__in=['festival', 'event', 'holiday']
    ).delete()
    
    total_events = 0
    
    # Add Festivals
    print("\nAdding Festivals:")
    for month in range(1, 13):
        if month in FESTIVALS:
            for day, festival_name in FESTIVALS[month].items():
                try:
                    english_date = NepaliCalendar.nepali_date_to_english_approximate(year, month, day)
                    
                    CalendarEvent.objects.create(
                        title=festival_name,
                        description=f"Traditional Nepali festival on {day} {NepaliCalendar.NEPALI_MONTHS_EN[month-1]}",
                        event_date=english_date,
                        event_type='festival',
                        school=school,
                        created_by='System'
                    )
                    total_events += 1
                    print(f"  {festival_name} - {english_date}")
                    
                except Exception as e:
                    print(f"  Error: {festival_name} - {e}")
    
    # Add School Events
    print("\nAdding School Events:")
    for month in range(1, 13):
        if month in SCHOOL_EVENTS:
            for day, event_name in SCHOOL_EVENTS[month].items():
                try:
                    english_date = NepaliCalendar.nepali_date_to_english_approximate(year, month, day)
                    
                    CalendarEvent.objects.create(
                        title=event_name,
                        description=f"School event on {day} {NepaliCalendar.NEPALI_MONTHS_EN[month-1]}",
                        event_date=english_date,
                        event_type='event',
                        school=school,
                        created_by='System'
                    )
                    total_events += 1
                    print(f"  {event_name} - {english_date}")
                    
                except Exception as e:
                    print(f"  Error: {event_name} - {e}")
    
    # Add Saturday Holidays
    print("\nAdding Saturday Holidays:")
    saturday_count = 0
    for month in range(1, 13):
        days_in_month = NepaliCalendar.NEPALI_DAYS.get(year, [31]*12)[month-1]
        for day in range(1, days_in_month + 1):
            try:
                english_date = NepaliCalendar.nepali_date_to_english_approximate(year, month, day)
                if english_date.weekday() == 5:  # Saturday
                    CalendarEvent.objects.create(
                        title="Saturday Holiday",
                        description="Weekly holiday",
                        event_date=english_date,
                        event_type='holiday',
                        school=school,
                        created_by='System'
                    )
                    saturday_count += 1
                    
            except Exception as e:
                continue
    
    total_events += saturday_count
    print(f"  Added {saturday_count} Saturday holidays")
    
    print("\n" + "="*50)
    print(f"SUMMARY:")
    print(f"Total events created: {total_events}")
    print(f"Festivals: {len([item for sublist in FESTIVALS.values() for item in sublist])}")
    print(f"School Events: {len([item for sublist in SCHOOL_EVENTS.values() for item in sublist])}")
    print(f"Saturday Holidays: {saturday_count}")
    print(f"Calendar populated from Baishakh 1 to Chaitra 30, {year}")
    
    return total_events

def verify_calendar():
    """Verify the populated calendar events"""
    print("\nVerifying Calendar Events:")
    print("="*30)
    
    festivals = CalendarEvent.objects.filter(event_type='festival').count()
    events = CalendarEvent.objects.filter(event_type='event').count()
    holidays = CalendarEvent.objects.filter(event_type='holiday').count()
    
    print(f"Festivals: {festivals}")
    print(f"School Events: {events}")
    print(f"Holidays: {holidays}")
    print(f"Total: {festivals + events + holidays}")
    
    # Show next 5 upcoming events
    from datetime import date
    upcoming = CalendarEvent.objects.filter(
        event_date__gte=date.today()
    ).order_by('event_date')[:5]
    
    print(f"\nNext 5 Upcoming Events:")
    for event in upcoming:
        print(f"  {event.event_date} - {event.title} ({event.event_type})")

if __name__ == "__main__":
    current_year = NepaliCalendar.get_current_nepali_date()['year']
    populate_complete_calendar(current_year)
    verify_calendar()