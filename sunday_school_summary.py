import os
import django
import sys

# Add the project directory to the Python path
sys.path.append('e:\\schoolmgmt')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent

def show_summary():
    """Show summary of Sunday school day implementation"""
    
    # Count school days by weekday
    all_school_days = CalendarEvent.objects.filter(
        title="School Day",
        event_type="other",
        is_active=True
    )
    
    weekday_counts = {}
    for event in all_school_days:
        weekday = event.event_date.strftime('%A')
        weekday_counts[weekday] = weekday_counts.get(weekday, 0) + 1
    
    print("SUNDAY SCHOOL DAY IMPLEMENTATION - SUMMARY")
    print("=" * 50)
    print("School days by weekday:")
    for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Sunday']:
        count = weekday_counts.get(day, 0)
        print(f"  {day}: {count} days")
    
    print(f"\nTotal school days: {sum(weekday_counts.values())}")
    
    if 'Sunday' in weekday_counts and weekday_counts['Sunday'] > 0:
        print(f"\nSUCCESS: Sunday has been added as a school day!")
        print(f"Sunday school days: {weekday_counts['Sunday']}")
        print(f"Saturday remains a holiday (not included)")
    else:
        print(f"\nERROR: Sunday school days not found!")

if __name__ == '__main__':
    show_summary()