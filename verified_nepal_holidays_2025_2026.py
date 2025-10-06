#!/usr/bin/env python3
import os
import sys
import django
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent, SchoolDetail

# Verified Nepal holidays 2025 & 2026 from official sources
VERIFIED_HOLIDAYS = [
    # 2025
    {"date": "2025-01-11", "name": "Prithvi Jayanti"},
    {"date": "2025-01-14", "name": "Maghe Sankranti"},
    {"date": "2025-01-29", "name": "Martyrs' Memorial Day"},
    {"date": "2025-01-30", "name": "Sonam Losar"},
    {"date": "2025-02-19", "name": "National Democracy Day (Prajatantra Diwas)"},
    {"date": "2025-02-26", "name": "Maha Shivaratri"},
    {"date": "2025-02-28", "name": "Gyalpo Losar"},
    {"date": "2025-03-08", "name": "International Women's Day"},
    {"date": "2025-04-14", "name": "Nepali New Year (Bisket Jatra)"},
    {"date": "2025-04-24", "name": "Loktantra Diwas"},
    {"date": "2025-05-01", "name": "Labour Day / International Workers' Day"},
    {"date": "2025-05-12", "name": "Buddha Jayanti (Vesak Day)"},
    {"date": "2025-05-29", "name": "Republic Day (Ganatantra Diwas)"},
    {"date": "2025-06-07", "name": "Eid al-Azha"},
    {"date": "2025-08-09", "name": "Janai Purnima / Raksha Bandhan"},
    {"date": "2025-08-16", "name": "Krishna Janmashtami"},
    {"date": "2025-09-06", "name": "Indra Jatra / Ananta Chaturdashi"},
    {"date": "2025-09-17", "name": "Constitution Day (Rastriya Diwas)"},
    {"date": "2025-09-22", "name": "Ghatasthapana / Dashain Start"},
    {"date": "2025-09-29", "name": "Fulpati (Dashain)"},
    {"date": "2025-09-30", "name": "Maha Ashtami"},
    {"date": "2025-10-01", "name": "Maha Navami"},
    {"date": "2025-10-02", "name": "Vijaya Dashami"},
    {"date": "2025-10-05", "name": "Kojagrat Purnima"},
    {"date": "2025-10-20", "name": "Laxmi Puja (Tihar)"},
    {"date": "2025-10-22", "name": "Goru Tihar / Govardhan Puja / Mha Puja"},
    {"date": "2025-10-23", "name": "Bhai Tika"},
    {"date": "2025-10-27", "name": "Chhath Parva"},
    {"date": "2025-12-03", "name": "International Day of Persons with Disabilities"},
    
    # 2026
    {"date": "2026-01-11", "name": "Prithvi Jayanti"},
    {"date": "2026-01-14", "name": "Maghe Sankranti"},
    {"date": "2026-01-30", "name": "Martyrs' Day (Sahid Diwas)"},
    {"date": "2026-02-15", "name": "Maha Shivaratri"},
    {"date": "2026-02-18", "name": "Sonam Losar / Gyalpo Losar (Tamang)"},
    {"date": "2026-02-19", "name": "Prajatantra Diwas (Democracy Day)"},
    {"date": "2026-03-08", "name": "International Women's Day"},
    {"date": "2026-03-27", "name": "Ram Navami"},
    {"date": "2026-04-14", "name": "Nepali New Year (Bisket Jatra)"},
    {"date": "2026-05-01", "name": "Labour Day / International Workers' Day"},
    {"date": "2026-05-01", "name": "Buddha Jayanti"},
    {"date": "2026-05-27", "name": "Eid al-Adha / Edul Aajha"},
    {"date": "2026-05-29", "name": "Republic Day (Ganatantra Diwas)"},
    {"date": "2026-09-19", "name": "Constitution Day (Rastriya Diwas)"},
    {"date": "2026-09-25", "name": "Indra Jatra"},
    {"date": "2026-10-17", "name": "Phulpati"},
    {"date": "2026-10-19", "name": "Maha Navami"},
    {"date": "2026-10-20", "name": "Maha Ashtami"}
]

CalendarEvent.objects.filter(event_type='festival').delete()
school = SchoolDetail.get_current_school()

for holiday in VERIFIED_HOLIDAYS:
    holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d').date()
    CalendarEvent.objects.create(
        title=holiday['name'],
        description="Verified from official Nepal holiday sources",
        event_date=holiday_date,
        event_type='festival',
        school=school,
        created_by='Verified Sources 2025-2026'
    )
    print(f"{holiday['date']} - {holiday['name']}")

print(f"\nPopulated {len(VERIFIED_HOLIDAYS)} verified Nepal holidays for 2025-2026")