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

def change_all_saturdays_to_holidays():
    """Change all Saturdays to holidays for current and next year"""
    
    current_year = date.today().year
    years_to_process = [current_year, current_year + 1]
    
    created_count = 0
    updated_count = 0
    
    for year in years_to_process:
        print(f"\nProcessing year {year}...")
        
        # Start from January 1st of the year
        current_date = date(year, 1, 1)
        
        # Find the first Saturday of the year
        days_until_saturday = (5 - current_date.weekday()) % 7
        first_saturday = current_date + timedelta(days=days_until_saturday)
        
        # Generate all Saturdays for the year
        saturday = first_saturday
        while saturday.year == year:
            # Check if this Saturday already exists as any event
            existing_event = CalendarEvent.objects.filter(event_date=saturday).first()
            
            if existing_event:
                # Update existing event to holiday if it's not already
                if existing_event.event_type != 'holiday' or existing_event.title != 'Saturday Holiday':
                    existing_event.title = 'Saturday Holiday'
                    existing_event.description = 'Weekly Saturday holiday'
                    existing_event.event_type = 'holiday'
                    existing_event.is_active = True
                    existing_event.created_by = 'System - Saturday Auto-Update'
                    existing_event.save()
                    updated_count += 1
                    print(f"[U] Updated existing event to Saturday holiday: {saturday}")
                else:
                    print(f"[-] Saturday holiday already exists: {saturday}")
            else:
                # Create new Saturday holiday
                CalendarEvent.objects.create(
                    title='Saturday Holiday',
                    description='Weekly Saturday holiday',
                    event_date=saturday,
                    event_type='holiday',
                    is_active=True,
                    created_by='System - Saturday Auto-Add'
                )
                created_count += 1
                print(f"[+] Added Saturday holiday: {saturday}")
            
            # Move to next Saturday
            saturday += timedelta(days=7)
    
    print(f"\n{'='*50}")
    print(f"SUMMARY:")
    print(f"[+] New Saturday holidays created: {created_count}")
    print(f"[U] Existing events updated to Saturday holidays: {updated_count}")
    print(f"[*] Years processed: {len(years_to_process)}")
    print(f"{'='*50}")

if __name__ == '__main__':
    print("Changing all Saturday school days to holidays...")
    change_all_saturdays_to_holidays()
    print("Process completed!")