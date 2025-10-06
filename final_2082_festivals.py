#!/usr/bin/env python3
import os
import sys
import django
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent, SchoolDetail

# Complete 2082 festivals (Baisakh 1 to Chaitra 30)
FESTIVALS_2082 = [
    {"date": "2025-04-13", "name": "Nepali New Year 2082"},
    {"date": "2025-04-29", "name": "Ram Navami"},
    {"date": "2025-05-12", "name": "Buddha Purnima"},
    {"date": "2025-06-11", "name": "Jestha Purnima"},
    {"date": "2025-07-10", "name": "Guru Purnima"},
    {"date": "2025-07-16", "name": "Shrawan Sankranti"},
    {"date": "2025-08-31", "name": "Janai Purnima"},
    {"date": "2025-09-01", "name": "Gai Jatra"},
    {"date": "2025-09-06", "name": "Haritalika Teej"},
    {"date": "2025-09-07", "name": "Krishna Janmashtami"},
    {"date": "2025-09-08", "name": "Rishi Panchami"},
    {"date": "2025-09-29", "name": "Bhadra Purnima"},
    {"date": "2025-10-02", "name": "Ghatasthapana"},
    {"date": "2025-10-08", "name": "Phulpati"},
    {"date": "2025-10-09", "name": "Maha Ashtami"},
    {"date": "2025-10-10", "name": "Maha Navami"},
    {"date": "2025-10-11", "name": "Vijaya Dashami"},
    {"date": "2025-10-28", "name": "Kojagrat Purnima"},
    {"date": "2025-10-31", "name": "Kag Tihar"},
    {"date": "2025-11-01", "name": "Kukur Tihar"},
    {"date": "2025-11-02", "name": "Gai Tihar/Laxmi Puja"},
    {"date": "2025-11-04", "name": "Bhai Tika"},
    {"date": "2025-11-07", "name": "Chhath Parva"},
    {"date": "2025-12-13", "name": "Yomari Punhi"},
    {"date": "2025-12-26", "name": "Mangsir Purnima"},
    {"date": "2026-01-14", "name": "Maghe Sankranti"},
    {"date": "2026-01-23", "name": "Shree Panchami"},
    {"date": "2026-01-25", "name": "Magh Purnima"},
    {"date": "2026-02-26", "name": "Maha Shivaratri"},
    {"date": "2026-03-14", "name": "Holi"},
    {"date": "2026-03-25", "name": "Falgun Purnima"},
    {"date": "2026-03-30", "name": "Ram Navami"},
    {"date": "2026-04-12", "name": "Chaitra Purnima"}
]

CalendarEvent.objects.filter(event_type='festival').delete()
school = SchoolDetail.get_current_school()

for festival in FESTIVALS_2082:
    festival_date = datetime.strptime(festival['date'], '%Y-%m-%d').date()
    CalendarEvent.objects.create(
        title=festival['name'],
        description="Festival for 2082 BS",
        event_date=festival_date,
        event_type='festival',
        school=school,
        created_by='2082 Complete System'
    )
    print(f"{festival['date']} - {festival['name']}")

print(f"\nPopulated {len(FESTIVALS_2082)} festivals for 2082 (Baisakh 1 to Chaitra 30)")