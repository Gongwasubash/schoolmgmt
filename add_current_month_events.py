import os
import django
import sys
from datetime import date, datetime, timedelta

# Add the project directory to the Python path
sys.path.append('e:\\schoolmgmt')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent, SchoolDetail

def add_current_month_events():
    """Add specific events for the current month to make calendar more dynamic"""
    
    school = SchoolDetail.get_current_school()
    current_date = datetime.now().date()
    current_month = current_date.month
    current_year = current_date.year
    
    # Get current month name
    month_names = [
        '', 'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    print(f"Adding events for {month_names[current_month]} {current_year}")
    
    # Current month specific events based on the month
    current_month_events = []
    
    if current_month == 1:  # January
        current_month_events = [
            (f'{current_year}-01-02', 'School Reopening After Winter Break', 'event', 'Classes resume after winter vacation'),
            (f'{current_year}-01-15', 'Maghe Sankranti Celebration', 'festival', 'Traditional festival celebration at school'),
            (f'{current_year}-01-26', 'Republic Day Program', 'event', 'Special assembly for Republic Day'),
            (f'{current_year}-01-30', 'Monthly Assessment', 'exam', 'January monthly test'),
        ]
    elif current_month == 2:  # February
        current_month_events = [
            (f'{current_year}-02-14', 'Friendship Day', 'event', 'Celebrating friendship among students'),
            (f'{current_year}-02-19', 'Democracy Day Celebration', 'event', 'Special program for Democracy Day'),
            (f'{current_year}-02-28', 'Science Exhibition', 'event', 'Student science project display'),
        ]
    elif current_month == 3:  # March
        current_month_events = [
            (f'{current_year}-03-08', 'Women Day Celebration', 'event', 'Special program honoring women'),
            (f'{current_year}-03-15', 'Annual Sports Meet', 'event', 'Inter-house sports competition'),
            (f'{current_year}-03-21', 'World Poetry Day', 'event', 'Poetry recitation competition'),
        ]
    elif current_month == 4:  # April
        current_month_events = [
            (f'{current_year}-04-01', 'April Fools Day Fun', 'event', 'Light-hearted activities for students'),
            (f'{current_year}-04-13', 'Nepali New Year Celebration', 'festival', 'Traditional New Year program'),
            (f'{current_year}-04-22', 'Earth Day Activities', 'event', 'Environmental awareness program'),
        ]
    elif current_month == 5:  # May
        current_month_events = [
            (f'{current_year}-05-01', 'Labour Day Recognition', 'event', 'Honoring school support staff'),
            (f'{current_year}-05-15', 'First Term Examination', 'exam', 'Major examination period'),
            (f'{current_year}-05-23', 'Buddha Jayanti Program', 'festival', 'Special assembly for Buddha Jayanti'),
        ]
    elif current_month == 6:  # June
        current_month_events = [
            (f'{current_year}-06-05', 'World Environment Day', 'event', 'Tree plantation and cleanup drive'),
            (f'{current_year}-06-15', 'Father Day Celebration', 'event', 'Special program for fathers'),
            (f'{current_year}-06-21', 'International Yoga Day', 'event', 'Yoga session for students and staff'),
        ]
    elif current_month == 7:  # July
        current_month_events = [
            (f'{current_year}-07-01', 'Summer Activities Begin', 'event', 'Special summer programs start'),
            (f'{current_year}-07-15', 'Guru Purnima Preparation', 'event', 'Preparing for teacher appreciation'),
            (f'{current_year}-07-21', 'Guru Purnima Celebration', 'festival', 'Honoring teachers and gurus'),
        ]
    elif current_month == 8:  # August
        current_month_events = [
            (f'{current_year}-08-11', 'Janai Purnima Program', 'festival', 'Sacred thread festival celebration'),
            (f'{current_year}-08-15', 'Independence Day (India)', 'event', 'Cultural exchange program'),
            (f'{current_year}-08-26', 'Krishna Janmashtami', 'festival', 'Lord Krishna birthday celebration'),
        ]
    elif current_month == 9:  # September
        current_month_events = [
            (f'{current_year}-09-05', 'Teachers Day Special', 'event', 'Student appreciation program for teachers'),
            (f'{current_year}-09-15', 'Mid-Term Examination', 'exam', 'Second major examination'),
            (f'{current_year}-09-21', 'International Peace Day', 'event', 'Peace and harmony activities'),
        ]
    elif current_month == 10:  # October
        current_month_events = [
            (f'{current_year}-10-01', 'Dashain Vacation Begins', 'holiday', 'Major festival vacation starts'),
            (f'{current_year}-10-12', 'Vijaya Dashami', 'holiday', 'Main day of Dashain festival'),
            (f'{current_year}-10-31', 'Halloween Fun Day', 'event', 'Costume and fun activities'),
        ]
    elif current_month == 11:  # November
        current_month_events = [
            (f'{current_year}-11-02', 'Bhai Tika Holiday', 'holiday', 'Brother-sister festival'),
            (f'{current_year}-11-14', 'Children Day Celebration', 'event', 'Special day for children'),
            (f'{current_year}-11-25', 'Thanksgiving Activities', 'event', 'Gratitude and sharing program'),
        ]
    elif current_month == 12:  # December
        current_month_events = [
            (f'{current_year}-12-01', 'Annual Function Preparation', 'event', 'Preparing for annual program'),
            (f'{current_year}-12-15', 'Final Term Examination', 'exam', 'Year-end major examination'),
            (f'{current_year}-12-25', 'Christmas Celebration', 'holiday', 'Christmas program and activities'),
        ]
    
    # Add weekly events for current month
    today = datetime.now().date()
    first_day_of_month = today.replace(day=1)
    
    # Find all Fridays in current month for weekly tests
    current_date = first_day_of_month
    while current_date.month == current_month:
        if current_date.weekday() == 4:  # Friday
            current_month_events.append(
                (current_date.strftime('%Y-%m-%d'), 'Weekly Test', 'exam', 'Regular weekly assessment')
            )
        current_date += timedelta(days=1)
    
    # Add the events to database
    created_count = 0
    for event_date, title, event_type, description in current_month_events:
        # Check if event already exists
        if not CalendarEvent.objects.filter(event_date=event_date, title=title).exists():
            try:
                CalendarEvent.objects.create(
                    title=title,
                    description=description,
                    event_date=event_date,
                    event_type=event_type,
                    school=school,
                    is_active=True,
                    created_by='Current Month Auto-Add'
                )
                created_count += 1
                print(f"Added: {title} on {event_date}")
            except Exception as e:
                print(f"Error creating event {title}: {e}")
    
    print(f"\nSuccessfully added {created_count} events for {month_names[current_month]} {current_year}")

def add_upcoming_week_events():
    """Add specific events for the upcoming week"""
    
    school = SchoolDetail.get_current_school()
    today = datetime.now().date()
    
    # Get next 7 days
    upcoming_events = []
    for i in range(7):
        future_date = today + timedelta(days=i)
        day_name = future_date.strftime('%A')
        
        # Add daily activities based on day of week
        if day_name == 'Monday':
            upcoming_events.append(
                (future_date.strftime('%Y-%m-%d'), 'Weekly Assembly', 'event', 'Monday morning assembly')
            )
        elif day_name == 'Wednesday':
            upcoming_events.append(
                (future_date.strftime('%Y-%m-%d'), 'Library Day', 'event', 'Special library activities')
            )
        elif day_name == 'Friday':
            upcoming_events.append(
                (future_date.strftime('%Y-%m-%d'), 'Sports Activity', 'event', 'Physical education and sports')
            )
        elif day_name == 'Saturday':
            upcoming_events.append(
                (future_date.strftime('%Y-%m-%d'), 'School Day', 'event', 'Regular Saturday classes')
            )
    
    # Add the events
    created_count = 0
    for event_date, title, event_type, description in upcoming_events:
        # Check if event already exists
        if not CalendarEvent.objects.filter(event_date=event_date, title=title).exists():
            try:
                CalendarEvent.objects.create(
                    title=title,
                    description=description,
                    event_date=event_date,
                    event_type=event_type,
                    school=school,
                    is_active=True,
                    created_by='Weekly Auto-Add'
                )
                created_count += 1
                print(f"Added upcoming: {title} on {event_date}")
            except Exception as e:
                print(f"Error creating upcoming event {title}: {e}")
    
    print(f"Added {created_count} upcoming week events")

if __name__ == '__main__':
    print("Adding current month specific events...")
    add_current_month_events()
    print("\nAdding upcoming week events...")
    add_upcoming_week_events()
    print("\nCurrent month events addition completed!")
    
    # Show total events
    total_events = CalendarEvent.objects.count()
    print(f"Total events in calendar: {total_events}")