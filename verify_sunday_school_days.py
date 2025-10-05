import os
import django
import sys
from datetime import date, timedelta

# Add the project directory to the Python path
sys.path.append('e:\\schoolmgmt')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent

def verify_sunday_school_days():
    """Verify that Sunday school days have been added"""
    
    # Check for Sunday school days in the next few months
    start_date = date.today()
    end_date = start_date + timedelta(days=90)  # Next 3 months
    
    sunday_school_days = CalendarEvent.objects.filter(
        event_date__gte=start_date,
        event_date__lte=end_date,
        title="School Day",
        event_type="other"
    ).filter(event_date__week_day=1)  # Sunday is 1 in Django's week_day
    
    print(f"Checking Sunday school days from {start_date} to {end_date}")
    print(f"Found {sunday_school_days.count()} Sunday school days")
    
    if sunday_school_days.exists():
        print("\nUpcoming Sunday school days:")
        for event in sunday_school_days[:10]:  # Show first 10
            print(f"  - {event.event_date} ({event.event_date.strftime('%A')}): {event.title}")
    
    # Check total school days by weekday
    all_school_days = CalendarEvent.objects.filter(
        title="School Day",
        event_type="other",
        is_active=True
    )
    
    weekday_counts = {}
    for event in all_school_days:
        weekday = event.event_date.strftime('%A')
        weekday_counts[weekday] = weekday_counts.get(weekday, 0) + 1
    
    print(f"\nTotal school days by weekday:")
    for day, count in sorted(weekday_counts.items()):
        print(f"  {day}: {count} days")
    
    # Verify Sunday is included
    if 'Sunday' in weekday_counts:
        print(f"\n✅ SUCCESS: Sunday is now included as a school day!")
        print(f"   Total Sunday school days: {weekday_counts['Sunday']}")
    else:
        print(f"\n❌ ERROR: Sunday school days not found!")

if __name__ == '__main__':
    verify_sunday_school_days()