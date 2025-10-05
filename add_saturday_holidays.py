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

def add_all_saturdays_as_holidays():
    """Add all Saturdays as holidays for current and next year"""
    
    current_year = date.today().year
    years_to_process = [current_year, current_year + 1]
    
    created_count = 0
    
    for year in years_to_process:
        # Start from January 1st of the year
        current_date = date(year, 1, 1)
        
        # Find the first Saturday of the year
        days_until_saturday = (5 - current_date.weekday()) % 7
        first_saturday = current_date + timedelta(days=days_until_saturday)
        
        # Generate all Saturdays for the year
        saturday = first_saturday
        while saturday.year == year:
            # Check if this Saturday already exists as a holiday
            existing_event = CalendarEvent.objects.filter(
                event_date=saturday,
                title="Saturday Holiday"
            ).first()
            
            if not existing_event:
                CalendarEvent.objects.create(
                    title="Saturday Holiday",
                    description="Weekly Saturday holiday",
                    event_date=saturday,
                    event_type="holiday",
                    is_active=True,
                    created_by="System - Saturday Auto-Add"
                )
                created_count += 1
                print(f"Added Saturday holiday: {saturday}")
            else:
                print(f"Saturday holiday already exists: {saturday}")
            
            # Move to next Saturday
            saturday += timedelta(days=7)
    
    print(f"\nSuccessfully added {created_count} Saturday holidays")
    print(f"Total Saturdays processed for years {years_to_process}")

if __name__ == '__main__':
    add_all_saturdays_as_holidays()