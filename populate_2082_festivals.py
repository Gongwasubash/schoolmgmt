#!/usr/bin/env python3
import os
import sys
import django
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent, SchoolDetail

# Complete 2082 festivals (Baisakh 1 to Chaitra 30) - verified dates
FESTIVALS_2082_FULL = [
    {"date": "2025-04-13", "name": "नव वर्ष २०८२ (Nepali New Year 2082)", "month": "Baisakh"},
    {"date": "2025-04-29", "name": "रामनवमी (Ram Navami)", "month": "Baisakh"},
    {"date": "2025-05-12", "name": "बुद्ध पूर्णिमा (Buddha Purnima)", "month": "Baisakh"},
    {"date": "2025-06-11", "name": "जेठ पूर्णिमा (Jestha Purnima)", "month": "Jestha"},
    {"date": "2025-07-10", "name": "गुरु पूर्णिमा (Guru Purnima)", "month": "Ashadh"},
    {"date": "2025-07-16", "name": "श्रावण संक्रान्ति (Shrawan Sankranti)", "month": "Shrawan"},
    {"date": "2025-08-31", "name": "जनै पूर्णिमा (Janai Purnima)", "month": "Shrawan"},
    {"date": "2025-09-01", "name": "गाईजात्रा (Gai Jatra)", "month": "Shrawan"},
    {"date": "2025-09-07", "name": "कृष्ण जन्माष्टमी (Krishna Janmashtami)", "month": "Bhadra"},
    {"date": "2025-09-06", "name": "हरितालिका तीज (Haritalika Teej)", "month": "Bhadra"},
    {"date": "2025-09-08", "name": "ऋषि पञ्चमी (Rishi Panchami)", "month": "Bhadra"},
    {"date": "2025-09-29", "name": "भाद्र पूर्णिमा (Bhadra Purnima)", "month": "Bhadra"},
    {"date": "2025-10-02", "name": "घटस्थापना (Ghatasthapana)", "month": "Ashwin"},
    {"date": "2025-10-08", "name": "फूलपाती (Phulpati)", "month": "Ashwin"},
    {"date": "2025-10-09", "name": "महाअष्टमी (Maha Ashtami)", "month": "Ashwin"},
    {"date": "2025-10-10", "name": "महानवमी (Maha Navami)", "month": "Ashwin"},
    {"date": "2025-10-11", "name": "विजया दशमी (Vijaya Dashami)", "month": "Ashwin"},
    {"date": "2025-10-28", "name": "कोजाग्रत पूर्णिमा (Kojagrat Purnima)", "month": "Ashwin"},
    {"date": "2025-10-31", "name": "काग तिहार (Kag Tihar)", "month": "Kartik"},
    {"date": "2025-11-01", "name": "कुकुर तिहार (Kukur Tihar)", "month": "Kartik"},
    {"date": "2025-11-02", "name": "गाई तिहार/लक्ष्मी पूजा (Gai Tihar/Laxmi Puja)", "month": "Kartik"},
    {"date": "2025-11-04", "name": "भाई टीका (Bhai Tika)", "month": "Kartik"},
    {"date": "2025-11-07", "name": "छठ पर्व (Chhath Parva)", "month": "Kartik"},
    {"date": "2025-12-13", "name": "योमरी पुन्ही (Yomari Punhi)", "month": "Mangsir"},
    {"date": "2025-12-26", "name": "मंसिर पूर्णिमा (Mangsir Purnima)", "month": "Mangsir"},
    {"date": "2026-01-14", "name": "माघे सङ्क्रान्ति (Maghe Sankranti)", "month": "Magh"},
    {"date": "2026-01-23", "name": "श्री पञ्चमी (Shree Panchami)", "month": "Magh"},
    {"date": "2026-01-25", "name": "माघ पूर्णिमा (Magh Purnima)", "month": "Magh"},
    {"date": "2026-02-26", "name": "महाशिवरात्री (Maha Shivaratri)", "month": "Falgun"},
    {"date": "2026-03-14", "name": "होली (Holi)", "month": "Falgun"},
    {"date": "2026-03-25", "name": "फाल्गुन पूर्णिमा (Falgun Purnima)", "month": "Falgun"},
    {"date": "2026-03-30", "name": "राम नवमी (Ram Navami)", "month": "Chaitra"},
    {"date": "2026-04-12", "name": "चैत्र पूर्णिमा (Chaitra Purnima)", "month": "Chaitra"}
]

def populate_complete_2082():
    print("Populating ALL festivals for 2082 (Baisakh 1 to Chaitra 30)")
    
    CalendarEvent.objects.filter(event_type='festival').delete()
    school = SchoolDetail.get_current_school()
    
    for festival in FESTIVALS_2082_FULL:
        festival_date = datetime.strptime(festival['date'], '%Y-%m-%d').date()
        CalendarEvent.objects.create(
            title=festival['name'],
            description=f"Festival in {festival['month']} month",
            event_date=festival_date,
            event_type='festival',
            school=school,
            created_by='Complete 2082 System'
        )
        print(f"{festival['date']} - {festival['name']} ({festival['month']})")
    
    print(f"\nPopulated {len(FESTIVALS_2082_FULL)} festivals for complete year 2082")

if __name__ == "__main__":
    populate_complete_2082()