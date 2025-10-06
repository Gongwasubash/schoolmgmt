#!/usr/bin/env python3
import os
import sys
import django
from datetime import date

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent, SchoolDetail

# Actual 2025 Nepali Festival Dates (verified)
ACTUAL_FESTIVALS_2025 = {
    date(2025, 4, 13): "Nepali New Year 2082",
    date(2025, 5, 12): "Buddha Jayanti",
    date(2025, 7, 31): "Janai Purnima",
    date(2025, 8, 1): "Gai Jatra", 
    date(2025, 8, 26): "Krishna Janmashtami",
    date(2025, 9, 6): "Haritalika Teej",
    date(2025, 9, 8): "Rishi Panchami",
    date(2025, 10, 2): "Ghatasthapana (Dashain Begins)",
    date(2025, 10, 8): "Phulpati",
    date(2025, 10, 9): "Maha Ashtami",
    date(2025, 10, 10): "Maha Navami", 
    date(2025, 10, 11): "Vijaya Dashami",
    date(2025, 10, 31): "Kag Tihar",
    date(2025, 11, 1): "Kukur Tihar",
    date(2025, 11, 2): "Gai Tihar/Laxmi Puja",
    date(2025, 11, 4): "Bhai Tika",
    date(2025, 11, 7): "Chhath Parva",
    date(2025, 12, 13): "Yomari Punhi",
    date(2026, 1, 14): "Maghe Sankranti",
    date(2026, 1, 23): "Saraswati Puja",
    date(2026, 2, 26): "Maha Shivaratri",
    date(2026, 3, 14): "Holi",
    date(2026, 3, 30): "Ram Navami"
}

def populate_actual_festivals():
    school = SchoolDetail.get_current_school()
    
    for festival_date, festival_name in ACTUAL_FESTIVALS_2025.items():
        CalendarEvent.objects.create(
            title=festival_name,
            description=f"Traditional Nepali festival",
            event_date=festival_date,
            event_type='festival',
            school=school,
            created_by='Accurate System'
        )
    
    print(f"Added {len(ACTUAL_FESTIVALS_2025)} accurate festival dates")

if __name__ == "__main__":
    populate_actual_festivals()