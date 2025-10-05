import os
import django
import sys
from datetime import date, timedelta
import argparse

# Add the project directory to the Python path
sys.path.append('e:\\schoolmgmt')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent

def add_saturdays_for_year(year):
    """Add all Saturdays as holidays for a specific year"""
    
    # Start from January 1st of the year
    current_date = date(year, 1, 1)
    
    # Find the first Saturday of the year
    days_until_saturday = (5 - current_date.weekday()) % 7
    first_saturday = current_date + timedelta(days=days_until_saturday)
    
    created_count = 0
    existing_count = 0
    
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
            print(f"[+] Added Saturday holiday: {saturday}")
        else:
            existing_count += 1
            print(f"- Saturday holiday already exists: {saturday}")
        
        # Move to next Saturday
        saturday += timedelta(days=7)
    
    return created_count, existing_count

def remove_saturdays_for_year(year):
    """Remove all Saturday holidays for a specific year"""
    
    # Start from January 1st of the year
    current_date = date(year, 1, 1)
    
    # Find the first Saturday of the year
    days_until_saturday = (5 - current_date.weekday()) % 7
    first_saturday = current_date + timedelta(days=days_until_saturday)
    
    removed_count = 0
    
    # Generate all Saturdays for the year and remove them
    saturday = first_saturday
    while saturday.year == year:
        # Find and delete Saturday holidays
        saturday_events = CalendarEvent.objects.filter(
            event_date=saturday,
            title="Saturday Holiday"
        )
        
        if saturday_events.exists():
            saturday_events.delete()
            removed_count += 1
            print(f"[-] Removed Saturday holiday: {saturday}")
        
        # Move to next Saturday
        saturday += timedelta(days=7)
    
    return removed_count

def list_saturdays_for_year(year):
    """List all Saturday holidays for a specific year"""
    
    saturday_events = CalendarEvent.objects.filter(
        event_date__year=year,
        title="Saturday Holiday"
    ).order_by('event_date')
    
    print(f"\nSaturday holidays for {year}:")
    print("-" * 40)
    
    if saturday_events.exists():
        for event in saturday_events:
            print(f"[*] {event.event_date} - {event.title}")
        print(f"\nTotal: {saturday_events.count()} Saturday holidays")
    else:
        print("No Saturday holidays found for this year.")
    
    return saturday_events.count()

def main():
    parser = argparse.ArgumentParser(description='Manage Saturday holidays in school calendar')
    parser.add_argument('action', choices=['add', 'remove', 'list'], 
                       help='Action to perform: add, remove, or list Saturday holidays')
    parser.add_argument('--year', type=int, default=date.today().year,
                       help='Year to process (default: current year)')
    parser.add_argument('--range', type=str, 
                       help='Year range in format "start-end" (e.g., "2025-2027")')
    
    args = parser.parse_args()
    
    # Determine years to process
    if args.range:
        try:
            start_year, end_year = map(int, args.range.split('-'))
            years = list(range(start_year, end_year + 1))
        except ValueError:
            print("Error: Invalid range format. Use 'start-end' format (e.g., '2025-2027')")
            return
    else:
        years = [args.year]
    
    print(f"Processing years: {years}")
    print("=" * 50)
    
    total_created = 0
    total_existing = 0
    total_removed = 0
    total_listed = 0
    
    for year in years:
        print(f"\nProcessing year {year}:")
        print("-" * 30)
        
        if args.action == 'add':
            created, existing = add_saturdays_for_year(year)
            total_created += created
            total_existing += existing
            print(f"Year {year}: Added {created} new Saturday holidays, {existing} already existed")
            
        elif args.action == 'remove':
            removed = remove_saturdays_for_year(year)
            total_removed += removed
            print(f"Year {year}: Removed {removed} Saturday holidays")
            
        elif args.action == 'list':
            count = list_saturdays_for_year(year)
            total_listed += count
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY:")
    
    if args.action == 'add':
        print(f"[+] Total Saturday holidays added: {total_created}")
        print(f"[-] Total already existing: {total_existing}")
        print(f"[*] Years processed: {len(years)}")
        
    elif args.action == 'remove':
        print(f"[-] Total Saturday holidays removed: {total_removed}")
        print(f"[*] Years processed: {len(years)}")
        
    elif args.action == 'list':
        print(f"[*] Total Saturday holidays found: {total_listed}")
        print(f"[*] Years processed: {len(years)}")

if __name__ == '__main__':
    main()