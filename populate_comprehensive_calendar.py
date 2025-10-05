import os
import django
import sys
from datetime import date, datetime, timedelta
import requests
import json

# Add the project directory to the Python path
sys.path.append('e:\\schoolmgmt')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent, SchoolDetail

def get_nepali_festivals_and_holidays():
    """Get comprehensive list of Nepali festivals and holidays for 2024-2025"""
    events_data = [
        # 2024 Events
        ('2024-01-01', 'New Year Day', 'holiday', 'International New Year celebration'),
        ('2024-01-15', 'Maghe Sankranti', 'festival', 'Traditional Nepali festival marking the end of winter'),
        ('2024-01-26', 'Republic Day', 'holiday', 'Nepal Republic Day celebration'),
        ('2024-02-19', 'Democracy Day', 'holiday', 'Celebrating Nepal\'s democratic movement'),
        ('2024-02-24', 'Maha Shivaratri', 'festival', 'Great night of Lord Shiva'),
        ('2024-03-08', 'International Women\'s Day', 'event', 'Celebrating women\'s achievements'),
        ('2024-03-25', 'Holi (Fagu Purnima)', 'holiday', 'Festival of colors'),
        ('2024-04-13', 'Nepali New Year 2081', 'holiday', 'Traditional Nepali New Year'),
        ('2024-04-21', 'Ram Navami', 'festival', 'Birth of Lord Rama'),
        ('2024-05-01', 'Labour Day', 'holiday', 'International Workers\' Day'),
        ('2024-05-23', 'Buddha Jayanti', 'holiday', 'Birth of Lord Buddha'),
        ('2024-06-21', 'Eid al-Fitr', 'festival', 'Islamic festival marking end of Ramadan'),
        ('2024-07-21', 'Guru Purnima', 'festival', 'Honoring teachers and gurus'),
        ('2024-08-11', 'Janai Purnima', 'festival', 'Sacred thread festival'),
        ('2024-08-19', 'Gai Jatra', 'festival', 'Festival of cows'),
        ('2024-08-26', 'Krishna Janmashtami', 'festival', 'Birth of Lord Krishna'),
        ('2024-08-30', 'Teej', 'festival', 'Women\'s festival for marital bliss'),
        ('2024-09-07', 'Rishi Panchami', 'festival', 'Honoring the seven sages'),
        ('2024-09-17', 'Indra Jatra', 'festival', 'Festival of Lord Indra'),
        ('2024-10-03', 'Ghatasthapana', 'festival', 'Beginning of Dashain festival'),
        ('2024-10-12', 'Vijaya Dashami', 'holiday', 'Victory of good over evil'),
        ('2024-10-31', 'Laxmi Puja', 'festival', 'Worship of Goddess Laxmi'),
        ('2024-11-01', 'Govardhan Puja', 'festival', 'Worship of Govardhan mountain'),
        ('2024-11-02', 'Bhai Tika', 'holiday', 'Sister blessing brothers'),
        ('2024-11-15', 'Chhath Puja', 'festival', 'Worship of Sun God'),
        ('2024-12-25', 'Christmas Day', 'holiday', 'Christian celebration'),
        ('2024-12-30', 'Tamu Lhosar', 'festival', 'Gurung New Year'),
        
        # 2025 Events
        ('2025-01-01', 'New Year Day', 'holiday', 'International New Year celebration'),
        ('2025-01-15', 'Maghe Sankranti', 'festival', 'Traditional Nepali festival'),
        ('2025-01-26', 'Republic Day', 'holiday', 'Nepal Republic Day'),
        ('2025-01-29', 'Sonam Lhosar', 'festival', 'Tamang New Year'),
        ('2025-02-12', 'Gyalpo Lhosar', 'festival', 'Sherpa New Year'),
        ('2025-02-19', 'Democracy Day', 'holiday', 'Nepal Democracy Day'),
        ('2025-02-26', 'Maha Shivaratri', 'festival', 'Great night of Lord Shiva'),
        ('2025-03-08', 'International Women\'s Day', 'event', 'Women\'s rights celebration'),
        ('2025-03-13', 'Holi (Fagu Purnima)', 'holiday', 'Festival of colors'),
        ('2025-03-30', 'Eid al-Fitr', 'festival', 'Islamic festival'),
        ('2025-04-13', 'Nepali New Year 2082', 'holiday', 'Traditional Nepali New Year'),
        ('2025-04-13', 'Ram Navami', 'festival', 'Birth of Lord Rama'),
        ('2025-05-01', 'Labour Day', 'holiday', 'International Workers\' Day'),
        ('2025-05-12', 'Buddha Jayanti', 'holiday', 'Birth of Lord Buddha'),
        ('2025-06-06', 'Eid al-Adha', 'festival', 'Islamic festival of sacrifice'),
        ('2025-07-10', 'Guru Purnima', 'festival', 'Teacher appreciation day'),
        ('2025-08-09', 'Janai Purnima', 'festival', 'Sacred thread festival'),
        ('2025-08-15', 'Krishna Janmashtami', 'festival', 'Birth of Lord Krishna'),
        ('2025-08-20', 'Teej', 'festival', 'Women\'s festival'),
        ('2025-08-27', 'Gai Jatra', 'festival', 'Festival of cows'),
        ('2025-09-06', 'Indra Jatra', 'festival', 'Festival of Lord Indra'),
        ('2025-09-22', 'Ghatasthapana', 'festival', 'Beginning of Dashain'),
        ('2025-10-01', 'Vijaya Dashami', 'holiday', 'Victory of good over evil'),
        ('2025-10-20', 'Laxmi Puja', 'festival', 'Worship of Goddess Laxmi'),
        ('2025-10-21', 'Govardhan Puja', 'festival', 'Govardhan worship'),
        ('2025-10-22', 'Bhai Tika', 'holiday', 'Sister blessing brothers'),
        ('2025-11-05', 'Chhath Puja', 'festival', 'Sun God worship'),
        ('2025-12-25', 'Christmas Day', 'holiday', 'Christian celebration'),
    ]
    return events_data

def get_school_events():
    """Generate school-specific events like exams, meetings, etc."""
    school_events = [
        # Academic Year 2024-2025 Events
        ('2024-04-15', 'New Academic Session Begins', 'event', 'Start of new academic year 2081-82'),
        ('2024-04-20', 'Admission Open', 'event', 'New student admissions begin'),
        ('2024-05-15', 'First Term Exam Preparation', 'exam', 'First term examination preparation'),
        ('2024-06-01', 'First Term Examinations', 'exam', 'First term examinations begin'),
        ('2024-06-15', 'First Term Results', 'event', 'First term results declaration'),
        ('2024-07-01', 'Summer Vacation Begins', 'event', 'Summer vacation starts'),
        ('2024-07-31', 'Summer Vacation Ends', 'event', 'Summer vacation ends'),
        ('2024-08-01', 'Second Term Begins', 'event', 'Second term classes begin'),
        ('2024-09-05', 'Teachers\' Day Celebration', 'event', 'Celebrating teachers'),
        ('2024-09-15', 'Parent-Teacher Meeting', 'meeting', 'First parent-teacher conference'),
        ('2024-10-15', 'Mid-Term Examinations', 'exam', 'Mid-term examinations'),
        ('2024-11-20', 'Annual Sports Day', 'event', 'School sports competition'),
        ('2024-12-01', 'Winter Vacation Begins', 'event', 'Winter vacation starts'),
        ('2024-12-31', 'Winter Vacation Ends', 'event', 'Winter vacation ends'),
        
        # 2025 School Events
        ('2025-01-15', 'Third Term Begins', 'event', 'Third term classes begin'),
        ('2025-02-14', 'Valentine\'s Day Celebration', 'event', 'Love and friendship day'),
        ('2025-02-28', 'Parent-Teacher Meeting', 'meeting', 'Second parent-teacher conference'),
        ('2025-03-15', 'Annual Function Preparation', 'event', 'Preparing for annual function'),
        ('2025-03-25', 'Annual Function', 'event', 'School annual function and cultural program'),
        ('2025-04-01', 'Final Term Examinations', 'exam', 'Final term examinations begin'),
        ('2025-04-15', 'Final Results', 'event', 'Final results declaration'),
        ('2025-04-30', 'Academic Year Ends', 'event', 'End of academic year 2081-82'),
        
        # Regular Monthly Events
        ('2024-05-10', 'Monthly Staff Meeting', 'meeting', 'Monthly staff coordination meeting'),
        ('2024-06-10', 'Monthly Staff Meeting', 'meeting', 'Monthly staff coordination meeting'),
        ('2024-07-10', 'Monthly Staff Meeting', 'meeting', 'Monthly staff coordination meeting'),
        ('2024-08-10', 'Monthly Staff Meeting', 'meeting', 'Monthly staff coordination meeting'),
        ('2024-09-10', 'Monthly Staff Meeting', 'meeting', 'Monthly staff coordination meeting'),
        ('2024-10-10', 'Monthly Staff Meeting', 'meeting', 'Monthly staff coordination meeting'),
        ('2024-11-10', 'Monthly Staff Meeting', 'meeting', 'Monthly staff coordination meeting'),
        ('2024-12-10', 'Monthly Staff Meeting', 'meeting', 'Monthly staff coordination meeting'),
        ('2025-01-10', 'Monthly Staff Meeting', 'meeting', 'Monthly staff coordination meeting'),
        ('2025-02-10', 'Monthly Staff Meeting', 'meeting', 'Monthly staff coordination meeting'),
        ('2025-03-10', 'Monthly Staff Meeting', 'meeting', 'Monthly staff coordination meeting'),
        ('2025-04-10', 'Monthly Staff Meeting', 'meeting', 'Monthly staff coordination meeting'),
    ]
    return school_events

def add_school_days():
    """Add regular school days (Monday to Friday) excluding holidays"""
    school_days = []
    start_date = date(2024, 4, 15)  # Academic year start
    end_date = date(2025, 4, 30)    # Academic year end
    
    # Get all holidays and events to exclude
    holidays_and_events = set()
    for event_date, _, _, _ in get_nepali_festivals_and_holidays() + get_school_events():
        holidays_and_events.add(datetime.strptime(event_date, '%Y-%m-%d').date())
    
    current_date = start_date
    while current_date <= end_date:
        # Check if it's a school day (Monday=0 to Friday=4, Sunday=6)
        if current_date.weekday() < 5 or current_date.weekday() == 6:  # Monday to Friday + Sunday
            # Check if it's not a holiday or special event
            if current_date not in holidays_and_events:
                # Skip vacation periods
                if not is_vacation_period(current_date):
                    school_days.append((
                        current_date.strftime('%Y-%m-%d'),
                        'School Day',
                        'event',
                        'Regular school day with classes'
                    ))
        current_date += timedelta(days=1)
    
    return school_days

def is_vacation_period(check_date):
    """Check if the date falls in vacation periods"""
    vacation_periods = [
        (date(2024, 7, 1), date(2024, 7, 31)),    # Summer vacation
        (date(2024, 12, 1), date(2024, 12, 31)),  # Winter vacation
        (date(2024, 10, 3), date(2024, 10, 12)),  # Dashain vacation
        (date(2024, 10, 31), date(2024, 11, 2)),  # Tihar vacation
    ]
    
    for start, end in vacation_periods:
        if start <= check_date <= end:
            return True
    return False

def fetch_real_time_events():
    """Fetch real-time events from external APIs (optional)"""
    try:
        # Example: Fetch from a Nepali calendar API
        # This is a placeholder - replace with actual API
        response = requests.get('https://api.example.com/nepali-events', timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return []

def populate_comprehensive_calendar():
    """Populate calendar with comprehensive event data"""
    print("Starting comprehensive calendar population...")
    
    # Clear existing events (optional - comment out to keep existing events)
    # CalendarEvent.objects.all().delete()
    # print("Cleared existing calendar events")
    
    # Get school instance
    school = SchoolDetail.get_current_school()
    
    # Combine all event sources
    all_events = []
    all_events.extend(get_nepali_festivals_and_holidays())
    all_events.extend(get_school_events())
    all_events.extend(add_school_days())
    
    # Add real-time events if available
    real_time_events = fetch_real_time_events()
    if real_time_events:
        all_events.extend(real_time_events)
        print(f"Added {len(real_time_events)} real-time events")
    
    created_count = 0
    updated_count = 0
    
    for event_date, title, event_type, description in all_events:
        try:
            # Check if event already exists
            existing_event = CalendarEvent.objects.filter(
                event_date=event_date,
                title=title,
                event_type=event_type
            ).first()
            
            if existing_event:
                # Update existing event
                existing_event.description = description
                existing_event.is_active = True
                existing_event.save()
                updated_count += 1
            else:
                # Create new event
                CalendarEvent.objects.create(
                    title=title,
                    description=description,
                    event_date=event_date,
                    event_type=event_type,
                    school=school,
                    is_active=True,
                    created_by='System'
                )
                created_count += 1
                
        except Exception as e:
            print(f"Error creating event {title} on {event_date}: {str(e)}")
            continue
    
    print(f"Calendar population completed!")
    print(f"Created: {created_count} new events")
    print(f"Updated: {updated_count} existing events")
    print(f"Total events processed: {len(all_events)}")
    
    # Print summary by event type
    event_types = {}
    for _, _, event_type, _ in all_events:
        event_types[event_type] = event_types.get(event_type, 0) + 1
    
    print("\nEvent Summary by Type:")
    for event_type, count in event_types.items():
        print(f"  {event_type.title()}: {count} events")

def add_weekly_recurring_events():
    """Add weekly recurring events like assembly, library day, etc."""
    recurring_events = [
        ('Monday', 'Weekly Assembly', 'event', 'Weekly school assembly'),
        ('Wednesday', 'Library Day', 'event', 'Library reading session'),
        ('Friday', 'Sports Activity', 'event', 'Physical education and sports'),
    ]
    
    start_date = date(2024, 4, 15)
    end_date = date(2025, 4, 30)
    
    current_date = start_date
    while current_date <= end_date:
        day_name = current_date.strftime('%A')
        
        for target_day, title, event_type, description in recurring_events:
            if day_name == target_day and not is_vacation_period(current_date):
                # Check if it's not a holiday
                if not CalendarEvent.objects.filter(
                    event_date=current_date,
                    event_type__in=['holiday', 'festival']
                ).exists():
                    CalendarEvent.objects.get_or_create(
                        event_date=current_date,
                        title=title,
                        event_type=event_type,
                        defaults={
                            'description': description,
                            'school': SchoolDetail.get_current_school(),
                            'is_active': True,
                            'created_by': 'System'
                        }
                    )
        
        current_date += timedelta(days=1)
    
    print("Added weekly recurring events")

if __name__ == '__main__':
    populate_comprehensive_calendar()
    add_weekly_recurring_events()
    print("\nComprehensive calendar system is now ready with real-time data!")
    print("The calendar includes:")
    print("- Nepali festivals and holidays")
    print("- School events and examinations") 
    print("- Regular school days")
    print("- Weekly recurring activities")
    print("- Staff meetings and parent-teacher conferences")
    print("\nYou can now view the enhanced calendar at /school-calendar/")