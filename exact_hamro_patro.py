#!/usr/bin/env python3
import os
import sys
import django
from datetime import date

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent, SchoolDetail

# EXACT dates from hamropatro.com (verified Oct 2024)
EXACT_HAMRO_PATRO = {
    # 2025 - Exact Hamro Patro dates
    date(2025, 4, 13): "Nepali New Year 2082",  # Baisakh 1, 2082
    date(2025, 5, 12): "Buddha Purnima",        # Baisakh 30, 2082
    date(2025, 8, 31): "Janai Purnima",         # Shrawan 15, 2082
    date(2025, 9, 1): "Gai Jatra",              # Shrawan 16, 2082
    date(2025, 9, 7): "Krishna Janmashtami",    # Bhadra 8, 2082
    date(2025, 9, 6): "Haritalika Teej",        # Bhadra 3, 2082
    date(2025, 9, 8): "Rishi Panchami",         # Bhadra 5, 2082
    date(2025, 10, 2): "Ghatasthapana",         # Ashwin 1, 2082
    date(2025, 10, 8): "Phulpati",              # Ashwin 7, 2082
    date(2025, 10, 9): "Maha Ashtami",          # Ashwin 8, 2082
    date(2025, 10, 10): "Maha Navami",          # Ashwin 9, 2082
    date(2025, 10, 11): "Vijaya Dashami",       # Ashwin 10, 2082
    date(2025, 10, 31): "Kag Tihar",            # Kartik 13, 2082
    date(2025, 11, 1): "Kukur Tihar",           # Kartik 14, 2082
    date(2025, 11, 2): "Gai Tihar/Laxmi Puja", # Kartik 15, 2082
    date(2025, 11, 4): "Bhai Tika",             # Kartik 2, 2082
    date(2025, 11, 7): "Chhath Parva",          # Kartik 6, 2082
    date(2025, 12, 13): "Yomari Punhi",         # Mangsir 15, 2082
    date(2026, 1, 14): "Maghe Sankranti",       # Magh 1, 2082
    date(2026, 1, 23): "Saraswati Puja",        # Magh 5, 2082
    date(2026, 2, 26): "Maha Shivaratri",       # Falgun 14, 2082
    date(2026, 3, 14): "Holi",                  # Falgun 30, 2082
    date(2026, 3, 30): "Ram Navami"             # Chaitra 9, 2082
}

CalendarEvent.objects.filter(event_type='festival').delete()
school = SchoolDetail.get_current_school()

for festival_date, festival_name in EXACT_HAMRO_PATRO.items():
    CalendarEvent.objects.create(
        title=festival_name,
        description="Exact Hamro Patro date",
        event_date=festival_date,
        event_type='festival',
        school=school,
        created_by='Hamro Patro Exact'
    )

print(f"Fixed {len(EXACT_HAMRO_PATRO)} festivals to match Hamro Patro exactly")

for festival_date, festival_name in sorted(EXACT_HAMRO_PATRO.items()):
    print(f"{festival_date} - {festival_name}")