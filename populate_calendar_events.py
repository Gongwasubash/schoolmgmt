import os
import django
import sys

# Add the project directory to the Python path
sys.path.append('e:\\schoolmgmt')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent
from datetime import date

def populate_calendar_events():
    # Clear existing events
    CalendarEvent.objects.all().delete()
    
    # 2024 Nepali Festivals and Holidays
    events_2024 = [
        # January
        ('2024-01-01', 'New Year Day', 'holiday'),
        ('2024-01-15', 'Maghe Sankranti', 'festival'),
        ('2024-01-26', 'Republic Day', 'holiday'),
        
        # February
        ('2024-02-19', 'Democracy Day', 'holiday'),
        ('2024-02-24', 'Maha Shivaratri', 'festival'),
        
        # March
        ('2024-03-08', 'International Women Day', 'festival'),
        ('2024-03-25', 'Holi (Fagu Purnima)', 'holiday'),
        
        # April
        ('2024-04-13', 'Nepali New Year 2081', 'holiday'),
        ('2024-04-21', 'Ram Navami', 'festival'),
        
        # May
        ('2024-05-01', 'Labour Day', 'holiday'),
        ('2024-05-23', 'Buddha Jayanti', 'holiday'),
        
        # June
        ('2024-06-21', 'Eid al-Fitr', 'festival'),
        
        # July
        ('2024-07-21', 'Guru Purnima', 'festival'),
        
        # August
        ('2024-08-11', 'Janai Purnima', 'festival'),
        ('2024-08-19', 'Gai Jatra', 'festival'),
        ('2024-08-26', 'Krishna Janmashtami', 'festival'),
        ('2024-08-30', 'Teej', 'festival'),
        
        # September
        ('2024-09-07', 'Rishi Panchami', 'festival'),
        ('2024-09-17', 'Indra Jatra', 'festival'),
        
        # October
        ('2024-10-03', 'Ghatasthapana', 'festival'),
        ('2024-10-12', 'Vijaya Dashami', 'holiday'),
        ('2024-10-31', 'Laxmi Puja', 'festival'),
        
        # November
        ('2024-11-01', 'Govardhan Puja', 'festival'),
        ('2024-11-02', 'Bhai Tika', 'holiday'),
        ('2024-11-15', 'Chhath Puja', 'festival'),
        
        # December
        ('2024-12-25', 'Christmas Day', 'holiday'),
        ('2024-12-30', 'Tamu Lhosar', 'festival'),
    ]
    
    # 2025 Events
    events_2025 = [
        # January
        ('2025-01-01', 'New Year Day', 'holiday'),
        ('2025-01-15', 'Maghe Sankranti', 'festival'),
        ('2025-01-26', 'Republic Day', 'holiday'),
        ('2025-01-29', 'Sonam Lhosar', 'festival'),
        
        # February
        ('2025-02-12', 'Gyalpo Lhosar', 'festival'),
        ('2025-02-19', 'Democracy Day', 'holiday'),
        ('2025-02-26', 'Maha Shivaratri', 'festival'),
        
        # March
        ('2025-03-08', 'International Women Day', 'festival'),
        ('2025-03-13', 'Holi (Fagu Purnima)', 'holiday'),
        ('2025-03-30', 'Eid al-Fitr', 'festival'),
        
        # April
        ('2025-04-13', 'Nepali New Year 2082', 'holiday'),
        ('2025-04-13', 'Ram Navami', 'festival'),
        
        # May
        ('2025-05-01', 'Labour Day', 'holiday'),
        ('2025-05-12', 'Buddha Jayanti', 'holiday'),
        
        # June
        ('2025-06-06', 'Eid al-Adha', 'festival'),
        
        # July
        ('2025-07-10', 'Guru Purnima', 'festival'),
        
        # August
        ('2025-08-09', 'Janai Purnima', 'festival'),
        ('2025-08-15', 'Krishna Janmashtami', 'festival'),
        ('2025-08-20', 'Teej', 'festival'),
        ('2025-08-27', 'Gai Jatra', 'festival'),
        
        # September
        ('2025-09-06', 'Indra Jatra', 'festival'),
        ('2025-09-22', 'Ghatasthapana', 'festival'),
        
        # October
        ('2025-10-01', 'Vijaya Dashami', 'holiday'),
        ('2025-10-20', 'Laxmi Puja', 'festival'),
        ('2025-10-21', 'Govardhan Puja', 'festival'),
        ('2025-10-22', 'Bhai Tika', 'holiday'),
        
        # November
        ('2025-11-05', 'Chhath Puja', 'festival'),
        
        # December
        ('2025-12-25', 'Christmas Day', 'holiday'),
    ]
    
    all_events = events_2024 + events_2025
    
    created_count = 0
    for event_date, title, event_type in all_events:
        CalendarEvent.objects.create(
            title=title,
            event_date=event_date,
            event_type=event_type,
            is_active=True,
            created_by='System'
        )
        created_count += 1
    
    print(f"Successfully created {created_count} calendar events")

if __name__ == '__main__':
    populate_calendar_events()