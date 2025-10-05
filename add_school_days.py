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

def add_school_days():
    """Add all remaining days as school days except Saturdays, festivals, and holidays"""
    
    current_year = date.today().year
    years_to_process = [current_year, current_year + 1]
    
    created_count = 0
    
    for year in years_to_process:
        print(f"\nProcessing year {year}...")
        
        # Start from January 1st of the year
        current_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        
        while current_date <= end_date:
            # Skip Saturdays (weekday 5) only - Sunday is now a school day
            if current_date.weekday() != 5:
                # Check if this date already has any event
                existing_event = CalendarEvent.objects.filter(event_date=current_date).first()
                
                if not existing_event:
                    CalendarEvent.objects.create(
                        title="School Day",
                        description="Regular school day",
                        event_date=current_date,
                        event_type="other",
                        is_active=True,
                        created_by="System - School Day Auto-Add"
                    )
                    created_count += 1
                    print(f"[+] Added school day: {current_date}")
            
            # Move to next day
            current_date += timedelta(days=1)
    
    print(f"\n{'='*50}")
    print(f"SUMMARY:")
    print(f"[+] New school days created: {created_count}")
    print(f"[*] Years processed: {len(years_to_process)}")
    print(f"{'='*50}")

if __name__ == '__main__':
    print("Adding school days for all remaining weekdays...")
    add_school_days()
    print("Process completed!")