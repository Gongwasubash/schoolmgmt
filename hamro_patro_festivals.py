#!/usr/bin/env python3
import os
import sys
import django
from datetime import date

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent, SchoolDetail

# Exact dates matching Hamro Patro 2025
HAMRO_PATRO_FESTIVALS = {
    # 2025 festivals (exact Hamro Patro dates)
    date(2025, 4, 14): "Nepali New Year 2082",
    date(2025, 5, 23): "Buddha Purnima",
    date(2025, 8, 19): "Janai Purnima", 
    date(2025, 8, 20): "Gai Jatra",
    date(2025, 8, 26): "Krishna Janmashtami",
    date(2025, 9, 20): "Haritalika Teej",
    date(2025, 9, 22): "Rishi Panchami",
    date(2025, 10, 3): "Ghatasthapana",
    date(2025, 10, 9): "Phulpati", 
    date(2025, 10, 10): "Maha Ashtami",
    date(2025, 10, 11): "Maha Navami",
    date(2025, 10, 12): "Vijaya Dashami",
    date(2025, 11, 1): "Kag Tihar",
    date(2025, 11, 2): "Kukur Tihar",
    date(2025, 11, 3): "Gai Tihar/Laxmi Puja",
    date(2025, 11, 5): "Bhai Tika",
    date(2025, 11, 7): "Chhath Parva",
    date(2025, 12, 15): "Yomari Punhi",
    date(2026, 1, 14): "Maghe Sankranti",
    date(2026, 2, 3): "Saraswati Puja",
    date(2026, 2, 26): "Maha Shivaratri", 
    date(2026, 3, 14): "Holi",
    date(2026, 4, 6): "Ram Navami"
}

def populate_hamro_patro_festivals():
    CalendarEvent.objects.filter(event_type='festival').delete()
    school = SchoolDetail.get_current_school()
    
    for festival_date, festival_name in HAMRO_PATRO_FESTIVALS.items():
        CalendarEvent.objects.create(
            title=festival_name,
            description=f"Festival date from Hamro Patro",
            event_date=festival_date,
            event_type='festival',
            school=school,
            created_by='Hamro Patro System'
        )
    
    print(f"Added {len(HAMRO_PATRO_FESTIVALS)} Hamro Patro festival dates")
    
    # Verify
    festivals = CalendarEvent.objects.filter(event_type='festival').order_by('event_date')
    print("\nHamro Patro Festivals:")
    for festival in festivals:
        print(f"{festival.event_date} - {festival.title}")

if __name__ == "__main__":
    populate_hamro_patro_festivals()