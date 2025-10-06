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

# Nepali Festival Data (Baishakh 1 to Chaitra 30)
NEPALI_FESTIVALS = {
    1: {  # Baishakh
        1: "नयाँ वर्ष (New Year)",
        8: "बुद्ध जयन्ती (Buddha Jayanti)",
        15: "रामनवमी (Ram Navami)"
    },
    2: {  # Jestha
        15: "कुमार षष्ठी (Kumar Shashthi)"
    },
    3: {  # Ashadh
        15: "हरिशयनी एकादशी (Harishayani Ekadashi)"
    },
    4: {  # Shrawan
        1: "श्रावण सक्रान्ति (Shrawan Sankranti)",
        15: "जनै पूर्णिमा (Janai Purnima)",
        23: "गाईजात्रा (Gai Jatra)"
    },
    5: {  # Bhadra
        3: "तीज (Teej)",
        18: "ऋषि पञ्चमी (Rishi Panchami)"
    },
    6: {  # Ashwin
        7: "घटस्थापना (Ghatasthapana)",
        15: "विजया दशमी (Vijaya Dashami)"
    },
    7: {  # Kartik
        2: "गाई तिहार (Gai Tihar)",
        3: "गोरु तिहार (Goru Tihar)",
        5: "भाई टीका (Bhai Tika)",
        15: "छठ पर्व (Chhath Parva)"
    },
    8: {  # Mangsir
        8: "यमरी पुन्ही (Yomari Punhi)"
    },
    9: {  # Poush
        1: "पौष सक्रान्ति (Poush Sankranti)"
    },
    10: {  # Magh
        1: "माघे सक्रान्ति (Maghe Sankranti)",
        5: "श्री पञ्चमी (Shree Panchami)",
        14: "शिवरात्री (Shivaratri)"
    },
    11: {  # Falgun
        15: "फागु पूर्णिमा/होली (Holi)"
    },
    12: {  # Chaitra
        8: "चैत्र अष्टमी (Chaitra Ashtami)",
        30: "चैत्र पूर्णिमा (Chaitra Purnima)"
    }
}

def populate_festivals(year=2082):
    """Populate Nepali festivals for a complete year"""
    
    print(f"Populating festivals for Nepali year {year}...")
    
    school = SchoolDetail.get_current_school()
    events_created = 0
    
    # Clear existing festival events
    CalendarEvent.objects.filter(event_type='festival').delete()
    
    for month in range(1, 13):  # Baishakh (1) to Chaitra (12)
        if month in NEPALI_FESTIVALS:
            for day, festival_name in NEPALI_FESTIVALS[month].items():
                try:
                    # Convert Nepali date to English date
                    english_date = NepaliCalendar.nepali_date_to_english_approximate(year, month, day)
                    
                    # Create calendar event
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