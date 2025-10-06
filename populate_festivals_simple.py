#!/usr/bin/env python3
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent, SchoolDetail
from schoolmgmt.nepali_calendar import NepaliCalendar

# Nepali Festival Data (English names)
FESTIVALS = {
    1: {  # Baishakh
        1: "Nepali New Year",
        8: "Buddha Jayanti",
        15: "Ram Navami"
    },
    2: {  # Jestha
        15: "Kumar Shashthi"
    },
    3: {  # Ashadh
        15: "Harishayani Ekadashi"
    },
    4: {  # Shrawan
        1: "Shrawan Sankranti",
        15: "Janai Purnima",
        23: "Gai Jatra"
    },
    5: {  # Bhadra
        3: "Teej Festival",
        18: "Rishi Panchami"
    },
    6: {  # Ashwin
        7: "Ghatasthapana",
        15: "Vijaya Dashami"
    },
    7: {  # Kartik
        2: "Gai Tihar",
        3: "Goru Tihar", 
        5: "Bhai Tika",
        15: "Chhath Parva"
    },
    8: {  # Mangsir
        8: "Yomari Punhi"
    },
    9: {  # Poush
        1: "Poush Sankranti"
    },
    10: {  # Magh
        1: "Maghe Sankranti",
        5: "Shree Panchami",
        14: "Shivaratri"
    },
    11: {  # Falgun
        15: "Holi Festival"
    },
    12: {  # Chaitra
        8: "Chaitra Ashtami",
        30: "Chaitra Purnima"
    }
}

def populate_festivals(year=2082):
    print(f"Populating festivals for Nepali year {year}...")
    
    school = SchoolDetail.get_current_school()
    events_created = 0
    
    # Clear existing festival events
    CalendarEvent.objects.filter(event_type='festival').delete()
    
    for month in range(1, 13):
        if month in FESTIVALS:
            for day, festival_name in FESTIVALS[month].items():
                try:
                    english_date = NepaliCalendar.nepali_date_to_english_approximate(year, month, day)
                    
                    CalendarEvent.objects.create(
                        title=festival_name,
                        description=f"Traditional Nepali festival on {day} {NepaliCalendar.NEPALI_MONTHS_EN[month-1]}",
                        event_date=english_date,
                        event_type='festival',
                        school=school,
                        created_by='System'
                    )
                    events_created += 1
                    print(f"Created: {festival_name} - {english_date}")
                    
                except Exception as e:
                    print(f"Error creating {festival_name}: {e}")
    
    print(f"\nCreated {events_created} festival events successfully!")
    return events_created

if __name__ == "__main__":
    current_year = NepaliCalendar.get_current_nepali_date()['year']
    populate_festivals(current_year)