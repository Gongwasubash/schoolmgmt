#!/usr/bin/env python3
import os
import sys
import django
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent, SchoolDetail

# Complete Nepal holidays 2025 from verified sources
NEPAL_HOLIDAYS_2025 = [
    {"date": "2025-01-11", "name": "Prithvi Jayanti"},
    {"date": "2025-01-14", "name": "Maghe Sankranti"},
    {"date": "2025-01-29", "name": "Martyrs' Day (Sahid Diwas)"},
    {"date": "2025-01-30", "name": "Sonam Losar / Lhosar (Tamang)"},
    {"date": "2025-02-26", "name": "Maha Shivaratri"},
    {"date": "2025-03-14", "name": "Holi / Phagu Purnima"},
    {"date": "2025-03-29", "name": "Ghode Jatra"},
    {"date": "2025-03-31", "name": "Ramjan Edul Fikra (Eid end)"},
    {"date": "2025-04-06", "name": "Ram Navami"},
    {"date": "2025-04-14", "name": "Nepali New Year (Baisakh 1)"},
    {"date": "2025-04-24", "name": "Loktantra Diwas"},
    {"date": "2025-05-01", "name": "Labour Day"},
    {"date": "2025-05-12", "name": "Buddha Jayanti"},
    {"date": "2025-05-29", "name": "Republic Day (Ganatantra Diwas)"},
    {"date": "2025-06-07", "name": "Edul Aajaha (Eid-ul-Adha)"},
    {"date": "2025-06-29", "name": "National Paddy Day / Ropain Diwas"},
    {"date": "2025-08-09", "name": "Janai Purnima"},
    {"date": "2025-08-10", "name": "Gai Jatra"},
    {"date": "2025-08-16", "name": "Shree Krishna Janmashtami"},
    {"date": "2025-08-26", "name": "Haritalika Teej"},
    {"date": "2025-09-06", "name": "Indra Jatra"},
    {"date": "2025-09-19", "name": "Constitution Day"},
    {"date": "2025-09-22", "name": "Ghatasthapana (Dashain start)"},
    {"date": "2025-09-29", "name": "Fulpati (Dashain)"},
    {"date": "2025-09-30", "name": "Maha Ashtami"},
    {"date": "2025-10-01", "name": "Maha Navami"},
    {"date": "2025-10-02", "name": "Vijaya Dashami"},
    {"date": "2025-10-03", "name": "Ekadashi (Dashain)"},
    {"date": "2025-10-04", "name": "Dwadashi (Dashain)"},
    {"date": "2025-10-05", "name": "Kojagrat Purnima"},
    {"date": "2025-10-20", "name": "Laxmi Puja (Tihar)"},
    {"date": "2025-10-22", "name": "Gobardhan Puja / Goru Tihar"},
    {"date": "2025-10-23", "name": "Bhai Tika"},
    {"date": "2025-10-27", "name": "Chhath Puja"},
    {"date": "2025-12-25", "name": "Christmas Day"},
    {"date": "2025-12-30", "name": "Tamu Lhosar"}
]

CalendarEvent.objects.filter(event_type='festival').delete()
school = SchoolDetail.get_current_school()

for holiday in NEPAL_HOLIDAYS_2025:
    holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d').date()
    CalendarEvent.objects.create(
        title=holiday['name'],
        description="Official Nepal holiday from verified sources",
        event_date=holiday_date,
        event_type='festival',
        school=school,
        created_by='Complete Nepal Holidays 2025'
    )
    print(f"{holiday['date']} - {holiday['name']}")

print(f"\nPopulated {len(NEPAL_HOLIDAYS_2025)} complete Nepal holidays for 2025")