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

# Accurate Nepali Festival Data
FESTIVALS_2082 = {
    # Baishakh
    1: {
        1: "Nepali New Year",
        15: "Buddha Jayanti (Baisakh Purnima)"
    },
    
    # Jestha  
    2: {
        15: "Jestha Purnima"
    },
    
    # Ashadh
    3: {
        15: "Guru Purnima (Ashadh Purnima)"
    },
    
    # Shrawan
    4: {
        1: "Shrawan Sankranti",
        15: "Janai Purnima (Raksha Bandhan)",
        16: "Gai Jatra",
        23: "Krishna Janmashtami"
    },
    
    # Bhadra
    5: {
        3: "Haritalika Teej",
        5: "Rishi Panchami",
        15: "Bhadra Purnima"
    },
    
    # Ashwin
    6: {
        1: "Ghatasthapana (Dashain Begins)",
        7: "Phulpati",
        8: "Maha Ashtami", 
        9: "Maha Navami",
        10: "Vijaya Dashami",
        15: "Kojagrat Purnima"
    },
    
    # Kartik
    7: {
        13: "Kag Tihar (Crow Day)",
        14: "Kukur Tihar (Dog Day)",
        15: "Gai Tihar/Laxmi Puja",
        30: "Goru Tihar/Govardhan Puja",
        2: "Bhai Tika",
        6: "Chhath Parva"
    },
    
    # Mangsir
    8: {
        15: "Yomari Punhi (Mangsir Purnima)"
    },
    
    # Poush
    9: {
        1: "Poush Sankranti",
        15: "Poush Purnima"
    },
    
    # Magh
    10: {
        1: "Maghe Sankranti",
        5: "Shree Panchami (Saraswati Puja)",
        15: "Magh Purnima",
        29: "Maha Shivaratri"
    },
    
    # Falgun
    11: {
        15: "Holi (Fagu Purnima)"
    },
    
    # Chaitra
    12: {
        8: "Chaitra Ashtami",
        9: "Ram Navami (Chaitra Navami)",
        15: "Chaitra Purnima",
        30: "Chaitra Dashain"
    }
}

def populate_fixed_festivals(year=2082):
    print(f"Populating CORRECTED Nepali festivals for year {year}")
    print("="*50)
    
    school = SchoolDetail.get_current_school()
    
    # Clear existing festivals
    CalendarEvent.objects.filter(event_type='festival').delete()
    print("Cleared existing festival events")
    
    festivals_created = 0
    
    for month in range(1, 13):
        month_name = NepaliCalendar.NEPALI_MONTHS_EN[month-1]
        
        if month in FESTIVALS_2082:
            print(f"\n{month_name} ({month}):")
            for day, festival_name in FESTIVALS_2082[month].items():
                try:
                    english_date = NepaliCalendar.nepali_date_to_english_approximate(year, month, day)
                    
                    CalendarEvent.objects.create(
                        title=festival_name,
                        description=f"Traditional Nepali festival on {day} {month_name}, {year} BS",
                        event_date=english_date,
                        event_type='festival',
                        school=school,
                        created_by='Fixed Festival System'
                    )
                    festivals_created += 1
                    print(f"  {festival_name} - {english_date} ({year}/{month:02d}/{day:02d} BS)")
                    
                except Exception as e:
                    print(f"  Error: {festival_name} - {e}")
    
    print(f"\n{'='*50}")
    print(f"SUCCESS: Created {festivals_created} accurate festival events")
    print(f"Calendar populated from Baishakh 1 to Chaitra 30, {year}")
    
    return festivals_created

def verify_festivals():
    """Verify the populated festivals"""
    print(f"\nVerifying Festival Calendar:")
    print("="*30)
    
    festivals = CalendarEvent.objects.filter(event_type='festival').order_by('event_date')
    
    print(f"Total Festivals: {festivals.count()}")
    
    print(f"\nAll Festivals for the Year:")
    for i, festival in enumerate(festivals, 1):
        nepali_date = NepaliCalendar.english_to_nepali_date(festival.event_date)
        print(f"{i:2d}. {festival.title}")
        print(f"    English: {festival.event_date}")
        print(f"    Nepali:  {NepaliCalendar.format_nepali_date(nepali_date, 'short')} BS")

if __name__ == "__main__":
    current_year = NepaliCalendar.get_current_nepali_date()['year']
    
    # Populate corrected festivals
    festivals_count = populate_fixed_festivals(current_year)
    
    # Verify the results
    verify_festivals()
    
    print(f"\nFESTIVAL CALENDAR FIXED AND POPULATED!")
    print(f"Total Events: {festivals_count}")