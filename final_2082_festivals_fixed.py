#!/usr/bin/env python3
import os
import sys
import django
import datetime
from nepali_datetime import date as nep_date

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent, SchoolDetail

festivals = [
    {"date_ad": "2025-04-13", "name": "Nepali New Year 2082"},
    {"date_ad": "2025-04-29", "name": "Ram Navami"},
    {"date_ad": "2025-05-12", "name": "Buddha Purnima"},
    {"date_ad": "2025-06-11", "name": "Jestha Purnima"},
    {"date_ad": "2025-07-10", "name": "Guru Purnima"},
    {"date_ad": "2025-07-16", "name": "Shrawan Sankranti"},
    {"date_ad": "2025-08-31", "name": "Janai Purnima"},
    {"date_ad": "2025-09-01", "name": "Gai Jatra"},
    {"date_ad": "2025-09-06", "name": "Haritalika Teej"},
    {"date_ad": "2025-09-07", "name": "Krishna Janmashtami"},
    {"date_ad": "2025-09-08", "name": "Rishi Panchami"},
    {"date_ad": "2025-09-29", "name": "Bhadra Purnima"},
    {"date_ad": "2025-10-02", "name": "Ghatasthapana"},
    {"date_ad": "2025-10-08", "name": "Phulpati"},
    {"date_ad": "2025-10-09", "name": "Maha Ashtami"},
    {"date_ad": "2025-10-10", "name": "Maha Navami"},
    {"date_ad": "2025-10-11", "name": "Vijaya Dashami"},
    {"date_ad": "2025-10-28", "name": "Kojagrat Purnima"},
    {"date_ad": "2025-10-31", "name": "Kag Tihar"},
    {"date_ad": "2025-11-01", "name": "Kukur Tihar"},
    {"date_ad": "2025-11-02", "name": "Gai Tihar/Laxmi Puja"},
    {"date_ad": "2025-11-04", "name": "Bhai Tika"},
    {"date_ad": "2025-11-07", "name": "Chhath Parva"},
    {"date_ad": "2025-12-13", "name": "Yomari Punhi"},
    {"date_ad": "2025-12-26", "name": "Mangsir Purnima"},
    {"date_ad": "2026-01-14", "name": "Maghe Sankranti"},
    {"date_ad": "2026-01-23", "name": "Shree Panchami"},
    {"date_ad": "2026-01-25", "name": "Magh Purnima"},
    {"date_ad": "2026-02-26", "name": "Maha Shivaratri"},
    {"date_ad": "2026-03-14", "name": "Holi"},
    {"date_ad": "2026-03-25", "name": "Falgun Purnima"},
    {"date_ad": "2026-03-30", "name": "Ram Navami"},
    {"date_ad": "2026-04-12", "name": "Chaitra Purnima"}
]

def convert_ad_to_bs(ad_date):
    y, m, d = map(int, ad_date.split('-'))
    ad = datetime.date(y, m, d)
    bs = nep_date.from_datetime_date(ad)
    return f"{bs.year}-{bs.month:02d}-{bs.day:02d}"

print("Converting AD to BS dates and populating calendar...")

CalendarEvent.objects.filter(event_type='festival').delete()
school = SchoolDetail.get_current_school()

for f in festivals:
    f["date_bs"] = convert_ad_to_bs(f["date_ad"])
    
    festival_date = datetime.datetime.strptime(f["date_ad"], '%Y-%m-%d').date()
    CalendarEvent.objects.create(
        title=f["name"],
        description=f"BS: {f['date_bs']} | AD: {f['date_ad']}",
        event_date=festival_date,
        event_type='festival',
        school=school,
        created_by='BS Conversion System'
    )
    
    print(f"{f['date_bs']} (BS) - {f['date_ad']} (AD) - {f['name']}")

print(f"\nPopulated {len(festivals)} festivals with accurate BS dates!")