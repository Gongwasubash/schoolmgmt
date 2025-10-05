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

def populate_comprehensive_festival_events():
    """Populate comprehensive festival and school events for 2024-2025"""
    
    # Clear existing events
    CalendarEvent.objects.all().delete()
    print("Cleared existing calendar events")
    
    # Get or create school
    school = SchoolDetail.get_current_school()
    
    # Comprehensive Nepali Festivals and International Events for 2024-2025
    events_data = [
        # 2024 Events
        # January 2024
        ('2024-01-01', 'English New Year', 'holiday', 'International New Year celebration'),
        ('2024-01-15', 'Maghe Sankranti', 'festival', 'Traditional Nepali festival marking the end of winter'),
        ('2024-01-26', 'Republic Day', 'holiday', 'Nepal Republic Day celebration'),
        ('2024-01-30', 'Martyrs Day', 'holiday', 'Remembering national martyrs'),
        
        # February 2024
        ('2024-02-10', 'Gyalpo Lhosar', 'festival', 'Tibetan New Year celebration'),
        ('2024-02-19', 'Democracy Day', 'holiday', 'Nepal Democracy Day'),
        ('2024-02-24', 'Maha Shivaratri', 'festival', 'Great night of Lord Shiva'),
        
        # March 2024
        ('2024-03-08', 'International Women Day', 'event', 'Celebrating women achievements'),
        ('2024-03-25', 'Holi (Fagu Purnima)', 'holiday', 'Festival of colors'),
        ('2024-03-29', 'Good Friday', 'festival', 'Christian holy day'),
        
        # April 2024
        ('2024-04-13', 'Nepali New Year 2081', 'holiday', 'Traditional Nepali New Year'),
        ('2024-04-14', 'Baisakhi', 'festival', 'Harvest festival'),
        ('2024-04-21', 'Ram Navami', 'festival', 'Birth of Lord Rama'),
        
        # May 2024
        ('2024-05-01', 'Labour Day', 'holiday', 'International Workers Day'),
        ('2024-05-23', 'Buddha Jayanti', 'holiday', 'Birth of Lord Buddha'),
        ('2024-05-26', 'Mother Day', 'event', 'Celebrating mothers'),
        
        # June 2024
        ('2024-06-15', 'Eid al-Fitr', 'festival', 'Islamic festival marking end of Ramadan'),
        ('2024-06-16', 'Father Day', 'event', 'Celebrating fathers'),
        ('2024-06-21', 'World Music Day', 'event', 'International music celebration'),
        
        # July 2024
        ('2024-07-21', 'Guru Purnima', 'festival', 'Honoring teachers and gurus'),
        ('2024-07-29', 'Ghanta Karna', 'festival', 'Festival to ward off evil spirits'),
        
        # August 2024
        ('2024-08-11', 'Janai Purnima', 'festival', 'Sacred thread festival'),
        ('2024-08-19', 'Gai Jatra', 'festival', 'Festival of cows'),
        ('2024-08-26', 'Krishna Janmashtami', 'festival', 'Birth of Lord Krishna'),
        ('2024-08-30', 'Haritalika Teej', 'festival', 'Women festival for marital bliss'),
        
        # September 2024
        ('2024-09-07', 'Rishi Panchami', 'festival', 'Honoring seven sages'),
        ('2024-09-17', 'Indra Jatra', 'festival', 'Festival of Lord Indra'),
        ('2024-09-22', 'Eid al-Adha', 'festival', 'Islamic festival of sacrifice'),
        
        # October 2024
        ('2024-10-03', 'Ghatasthapana', 'festival', 'Beginning of Dashain festival'),
        ('2024-10-09', 'Phulpati', 'festival', 'Seventh day of Dashain'),
        ('2024-10-10', 'Maha Ashtami', 'festival', 'Eighth day of Dashain'),
        ('2024-10-11', 'Maha Navami', 'festival', 'Ninth day of Dashain'),
        ('2024-10-12', 'Vijaya Dashami', 'holiday', 'Main day of Dashain festival'),
        ('2024-10-31', 'Laxmi Puja', 'festival', 'Worship of Goddess Laxmi'),
        
        # November 2024
        ('2024-11-01', 'Govardhan Puja', 'festival', 'Worship of Govardhan mountain'),
        ('2024-11-02', 'Bhai Tika', 'holiday', 'Brother-sister festival'),
        ('2024-11-07', 'Chhath Puja (Day 1)', 'festival', 'Sun worship festival begins'),
        ('2024-11-10', 'Chhath Puja (Main Day)', 'festival', 'Main day of sun worship'),
        ('2024-11-15', 'Jitiya', 'festival', 'Fasting festival for children welfare'),
        
        # December 2024
        ('2024-12-25', 'Christmas Day', 'holiday', 'Christian celebration of Jesus birth'),
        ('2024-12-30', 'Tamu Lhosar', 'festival', 'Gurung New Year'),
        ('2024-12-31', 'New Year Eve', 'event', 'Last day of English calendar year'),
        
        # 2025 Events
        # January 2025
        ('2025-01-01', 'English New Year', 'holiday', 'International New Year celebration'),
        ('2025-01-15', 'Maghe Sankranti', 'festival', 'Traditional Nepali festival marking the end of winter'),
        ('2025-01-26', 'Republic Day', 'holiday', 'Nepal Republic Day celebration'),
        ('2025-01-29', 'Sonam Lhosar', 'festival', 'Tamang New Year'),
        ('2025-01-30', 'Martyrs Day', 'holiday', 'Remembering national martyrs'),
        
        # February 2025
        ('2025-02-12', 'Gyalpo Lhosar', 'festival', 'Tibetan New Year celebration'),
        ('2025-02-19', 'Democracy Day', 'holiday', 'Nepal Democracy Day'),
        ('2025-02-26', 'Maha Shivaratri', 'festival', 'Great night of Lord Shiva'),
        
        # March 2025
        ('2025-03-08', 'International Women Day', 'event', 'Celebrating women achievements'),
        ('2025-03-13', 'Holi (Fagu Purnima)', 'holiday', 'Festival of colors'),
        ('2025-03-30', 'Eid al-Fitr', 'festival', 'Islamic festival marking end of Ramadan'),
        
        # April 2025
        ('2025-04-13', 'Nepali New Year 2082', 'holiday', 'Traditional Nepali New Year'),
        ('2025-04-13', 'Ram Navami', 'festival', 'Birth of Lord Rama'),
        ('2025-04-18', 'Good Friday', 'festival', 'Christian holy day'),
        
        # May 2025
        ('2025-05-01', 'Labour Day', 'holiday', 'International Workers Day'),
        ('2025-05-11', 'Mother Day', 'event', 'Celebrating mothers'),
        ('2025-05-12', 'Buddha Jayanti', 'holiday', 'Birth of Lord Buddha'),
        
        # June 2025
        ('2025-06-06', 'Eid al-Adha', 'festival', 'Islamic festival of sacrifice'),
        ('2025-06-15', 'Father Day', 'event', 'Celebrating fathers'),
        ('2025-06-21', 'World Music Day', 'event', 'International music celebration'),
        
        # July 2025
        ('2025-07-10', 'Guru Purnima', 'festival', 'Honoring teachers and gurus'),
        ('2025-07-18', 'Ghanta Karna', 'festival', 'Festival to ward off evil spirits'),
        
        # August 2025
        ('2025-08-09', 'Janai Purnima', 'festival', 'Sacred thread festival'),
        ('2025-08-15', 'Krishna Janmashtami', 'festival', 'Birth of Lord Krishna'),
        ('2025-08-20', 'Haritalika Teej', 'festival', 'Women festival for marital bliss'),
        ('2025-08-27', 'Gai Jatra', 'festival', 'Festival of cows'),
        
        # September 2025
        ('2025-09-06', 'Indra Jatra', 'festival', 'Festival of Lord Indra'),
        ('2025-09-22', 'Ghatasthapana', 'festival', 'Beginning of Dashain festival'),
        ('2025-09-28', 'Phulpati', 'festival', 'Seventh day of Dashain'),
        ('2025-09-29', 'Maha Ashtami', 'festival', 'Eighth day of Dashain'),
        ('2025-09-30', 'Maha Navami', 'festival', 'Ninth day of Dashain'),
        
        # October 2025
        ('2025-10-01', 'Vijaya Dashami', 'holiday', 'Main day of Dashain festival'),
        ('2025-10-20', 'Laxmi Puja', 'festival', 'Worship of Goddess Laxmi'),
        ('2025-10-21', 'Govardhan Puja', 'festival', 'Worship of Govardhan mountain'),
        ('2025-10-22', 'Bhai Tika', 'holiday', 'Brother-sister festival'),
        
        # November 2025
        ('2025-11-05', 'Chhath Puja', 'festival', 'Sun worship festival'),
        ('2025-11-15', 'Jitiya', 'festival', 'Fasting festival for children welfare'),
        
        # December 2025
        ('2025-12-25', 'Christmas Day', 'holiday', 'Christian celebration of Jesus birth'),
        ('2025-12-30', 'Tamu Lhosar', 'festival', 'Gurung New Year'),
        ('2025-12-31', 'New Year Eve', 'event', 'Last day of English calendar year'),
    ]
    
    # School-specific events
    school_events = [
        # Academic Year 2024-2025
        ('2024-04-15', 'School Reopening', 'event', 'New academic session begins'),
        ('2024-04-20', 'Admission Open', 'event', 'New student admission starts'),
        ('2024-05-15', 'First Term Exam', 'exam', 'First terminal examination'),
        ('2024-06-01', 'Sports Day', 'event', 'Annual sports competition'),
        ('2024-06-15', 'Science Fair', 'event', 'Student science project exhibition'),
        ('2024-07-01', 'Summer Vacation Begins', 'event', 'School summer break starts'),
        ('2024-08-01', 'Summer Vacation Ends', 'event', 'School reopens after summer'),
        ('2024-09-05', 'Teachers Day', 'event', 'Celebrating teachers contribution'),
        ('2024-09-15', 'Mid Term Exam', 'exam', 'Mid terminal examination'),
        ('2024-10-15', 'Dashain Vacation', 'holiday', 'Festival vacation period'),
        ('2024-11-15', 'Tihar Vacation', 'holiday', 'Festival vacation period'),
        ('2024-12-01', 'Annual Function', 'event', 'School annual cultural program'),
        ('2024-12-15', 'Final Term Exam', 'exam', 'Final terminal examination'),
        ('2025-01-15', 'Result Publication', 'event', 'Annual result announcement'),
        ('2025-02-01', 'Parent Meeting', 'meeting', 'Parent-teacher conference'),
        ('2025-03-15', 'Graduation Ceremony', 'event', 'Class 10 graduation ceremony'),
        ('2025-04-01', 'School Closure', 'event', 'Academic year ends'),
        
        # Regular monthly events
        ('2024-05-01', 'Monthly Test', 'exam', 'Regular monthly assessment'),
        ('2024-06-01', 'Monthly Test', 'exam', 'Regular monthly assessment'),
        ('2024-07-01', 'Monthly Test', 'exam', 'Regular monthly assessment'),
        ('2024-08-01', 'Monthly Test', 'exam', 'Regular monthly assessment'),
        ('2024-09-01', 'Monthly Test', 'exam', 'Regular monthly assessment'),
        ('2024-10-01', 'Monthly Test', 'exam', 'Regular monthly assessment'),
        ('2024-11-01', 'Monthly Test', 'exam', 'Regular monthly assessment'),
        ('2024-12-01', 'Monthly Test', 'exam', 'Regular monthly assessment'),
        ('2025-01-01', 'Monthly Test', 'exam', 'Regular monthly assessment'),
        ('2025-02-01', 'Monthly Test', 'exam', 'Regular monthly assessment'),
        ('2025-03-01', 'Monthly Test', 'exam', 'Regular monthly assessment'),
        
        # Weekly events (Saturdays as school days)
        ('2024-04-06', 'School Day', 'event', 'Regular school day'),
        ('2024-04-13', 'School Day', 'event', 'Regular school day'),
        ('2024-04-20', 'School Day', 'event', 'Regular school day'),
        ('2024-04-27', 'School Day', 'event', 'Regular school day'),
        ('2024-05-04', 'School Day', 'event', 'Regular school day'),
        ('2024-05-11', 'School Day', 'event', 'Regular school day'),
        ('2024-05-18', 'School Day', 'event', 'Regular school day'),
        ('2024-05-25', 'School Day', 'event', 'Regular school day'),
    ]
    
    # Combine all events
    all_events = events_data + school_events
    
    created_count = 0
    for event_date, title, event_type, description in all_events:
        try:
            CalendarEvent.objects.create(
                title=title,
                description=description,
                event_date=event_date,
                event_type=event_type,
                school=school,
                is_active=True,
                created_by='System Auto-Population'
            )
            created_count += 1
        except Exception as e:
            print(f"Error creating event {title}: {e}")
    
    print(f"Successfully created {created_count} comprehensive calendar events")
    
    # Print summary by type
    event_types = CalendarEvent.objects.values('event_type').distinct()
    for event_type in event_types:
        count = CalendarEvent.objects.filter(event_type=event_type['event_type']).count()
        print(f"- {event_type['event_type'].title()}: {count} events")

def add_recurring_school_days():
    """Add recurring school days (Saturdays) for the academic year"""
    
    school = SchoolDetail.get_current_school()
    
    # Generate Saturdays for 2024-2025 academic year
    start_date = date(2024, 4, 6)  # First Saturday of academic year
    end_date = date(2025, 3, 29)   # Last Saturday of academic year
    
    current_date = start_date
    saturday_count = 0
    
    while current_date <= end_date:
        # Skip major holidays
        skip_dates = [
            date(2024, 4, 13),  # Nepali New Year
            date(2024, 5, 23),  # Buddha Jayanti
            date(2024, 10, 12), # Dashain
            date(2024, 11, 2),  # Bhai Tika
            date(2024, 12, 25), # Christmas
            date(2025, 1, 1),   # New Year
            date(2025, 3, 13),  # Holi
        ]
        
        if current_date not in skip_dates:
            # Check if event already exists
            if not CalendarEvent.objects.filter(event_date=current_date, title='School Day').exists():
                CalendarEvent.objects.create(
                    title='School Day',
                    description='Regular Saturday school day',
                    event_date=current_date,
                    event_type='event',
                    school=school,
                    is_active=True,
                    created_by='System Auto-Population'
                )
                saturday_count += 1
        
        # Move to next Saturday
        current_date += timedelta(days=7)
    
    print(f"Added {saturday_count} Saturday school days")

if __name__ == '__main__':
    print("Starting comprehensive festival events population...")
    populate_comprehensive_festival_events()
    print("\nAdding recurring school days...")
    add_recurring_school_days()
    print("\nCalendar population completed successfully!")
    
    # Final summary
    total_events = CalendarEvent.objects.count()
    print(f"\nTotal events in calendar: {total_events}")