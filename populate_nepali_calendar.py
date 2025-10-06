import os
import django
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent

# Nepali festivals, holidays and important days for 2024-2025
events_data = [
    # Major Nepali Festivals
    ('2024-04-13', 'Nepali New Year 2081', 'holiday'),
    ('2024-04-21', 'Ram Navami', 'holiday'),
    ('2024-05-12', 'Buddha Jayanti', 'holiday'),
    ('2024-08-19', 'Janai Purnima', 'holiday'),
    ('2024-08-26', 'Gai Jatra', 'holiday'),
    ('2024-09-07', 'Krishna Janmashtami', 'holiday'),
    ('2024-09-17', 'Teej', 'holiday'),
    ('2024-10-03', 'Indra Jatra', 'holiday'),
    ('2024-10-12', 'Dashain Ghatasthapana', 'holiday'),
    ('2024-10-20', 'Dashain Fulpati', 'holiday'),
    ('2024-10-21', 'Dashain Maha Ashtami', 'holiday'),
    ('2024-10-22', 'Dashain Maha Navami', 'holiday'),
    ('2024-10-23', 'Dashain Vijaya Dashami', 'holiday'),
    ('2024-11-01', 'Tihar Gai Tihar', 'holiday'),
    ('2024-11-02', 'Tihar Kukur Puja', 'holiday'),
    ('2024-11-03', 'Tihar Gai Tihar & Laxmi Puja', 'holiday'),
    ('2024-11-04', 'Tihar Govardhan Puja', 'holiday'),
    ('2024-11-05', 'Tihar Bhai Tika', 'holiday'),
    ('2024-12-30', 'Tamu Lhosar', 'holiday'),
    
    # 2025 Events
    ('2025-02-12', 'Sonam Lhosar', 'holiday'),
    ('2025-02-26', 'Maha Shivaratri', 'holiday'),
    ('2025-03-13', 'Holi', 'holiday'),
    ('2025-03-30', 'Ram Navami', 'holiday'),
    
    # Public Holidays
    ('2024-01-01', 'New Year Day', 'public-holiday'),
    ('2024-01-15', 'Maghe Sankranti', 'public-holiday'),
    ('2024-01-29', 'Martyrs Day', 'public-holiday'),
    ('2024-02-19', 'Democracy Day', 'public-holiday'),
    ('2024-05-01', 'Labour Day', 'public-holiday'),
    ('2024-05-29', 'Republic Day', 'public-holiday'),
    ('2024-08-20', 'Constitution Day', 'public-holiday'),
    
    # International Days
    ('2024-05-12', 'Mother\'s Day', 'special'),
    ('2024-06-16', 'Father\'s Day', 'special'),
    ('2024-03-08', 'International Women\'s Day', 'special'),
    ('2024-06-05', 'World Environment Day', 'special'),
    ('2024-09-05', 'Teacher\'s Day', 'special'),
    ('2024-10-01', 'International Day of Older Persons', 'special'),
    ('2024-11-20', 'Universal Children\'s Day', 'special'),
    ('2024-12-10', 'Human Rights Day', 'special'),
    
    # 2025 International Days
    ('2025-03-08', 'International Women\'s Day', 'special'),
    ('2025-05-11', 'Mother\'s Day', 'special'),
    ('2025-06-15', 'Father\'s Day', 'special'),
    ('2025-06-05', 'World Environment Day', 'special'),
    ('2025-09-05', 'Teacher\'s Day', 'special'),
]

# Create calendar events
created_count = 0
for date_str, title, event_type in events_data:
    event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # Check if event already exists
    if not CalendarEvent.objects.filter(event_date=event_date, title=title).exists():
        CalendarEvent.objects.create(
            event_date=event_date,
            title=title,
            event_type=event_type,
            description=f"{title} - {event_type.replace('-', ' ').title()}"
        )
        created_count += 1

print(f"Successfully created {created_count} calendar events")
print("Calendar populated with Nepali festivals, holidays, and important days")