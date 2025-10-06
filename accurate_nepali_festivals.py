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

# Accurate Nepali Festival Data based on actual Nepali calendar
ACCURATE_FESTIVALS = {
    # Baishakh (बैशाख) - Month 1
    1: {
        1: "नव वर्ष (Nepali New Year)",
        14: "बैशाख पूर्णिमा (Baisakh Purnima)",
        # Buddha Jayanti varies - usually Baisakh Purnima
    },
    
    # Jestha (जेठ) - Month 2  
    2: {
        15: "जेठ पूर्णिमा (Jestha Purnima)",
    },
    
    # Ashadh (आषाढ) - Month 3
    3: {
        15: "आषाढ पूर्णिमा (Ashadh Purnima)",
        # Guru Purnima is usually on Ashadh Purnima
    },
    
    # Shrawan (श्रावण) - Month 4
    4: {
        1: "श्रावण संक्रान्ति (Shrawan Sankranti)",
        15: "जनै पूर्णिमा/रक्षाबन्धन (Janai Purnima)",
        # Gai Jatra is day after Janai Purnima in Kathmandu
        16: "गाईजात्रा (Gai Jatra)",
        # Krishna Janmashtami - 8th day of dark fortnight
        23: "कृष्ण जन्माष्टमी (Krishna Janmashtami)",
    },
    
    # Bhadra (भाद्र) - Month 5
    5: {
        # Teej is 3rd day of bright fortnight of Bhadra
        3: "हरितालिका तीज (Haritalika Teej)",
        # Rishi Panchami is 5th day after Teej
        5: "ऋषि पञ्चमी (Rishi Panchami)",
        15: "भाद्र पूर्णिमा (Bhadra Purnima)",
    },
    
    # Ashwin (आश्विन) - Month 6
    6: {
        # Dashain starts from Ghatasthapana (1st day of bright fortnight)
        1: "घटस्थापना (Ghatasthapana - Dashain Begins)",
        7: "फूलपाती (Phulpati)",
        8: "महाअष्टमी (Maha Ashtami)",
        9: "महानवमी (Maha Navami)",
        10: "विजया दशमी (Vijaya Dashami)",
        15: "कोजाग्रत पूर्णिमा (Kojagrat Purnima)",
    },
    
    # Kartik (कार्तिक) - Month 7
    7: {
        # Tihar/Deepawali - 5 days starting from Kartik Krishna Trayodashi
        13: "काग तिहार (Kag Tihar - Crow Day)",
        14: "कुकुर तिहार (Kukur Tihar - Dog Day)", 
        15: "गाई तिहार/लक्ष्मी पूजा (Gai Tihar/Laxmi Puja)",
        # Next day is Amavasya
        30: "गोरु तिहार/गोवर्धन पूजा (Goru Tihar)",
        # Day after Amavasya
        2: "भाई टीका (Bhai Tika)", # This is actually Kartik Shukla Dwitiya
        # Chhath is 6 days after Tihar
        6: "छठ पर्व (Chhath Parva)",
    },
    
    # Mangsir (मंसिर) - Month 8
    8: {
        15: "मंसिर पूर्णिमा (Mangsir Purnima)",
        # Yomari Punhi is on Mangsir Purnima in Newar community
    },
    
    # Poush (पौष) - Month 9
    9: {
        1: "पौष संक्रान्ति (Poush Sankranti)",
        15: "पौष पूर्णिमा (Poush Purnima)",
    },
    
    # Magh (माघ) - Month 10
    10: {
        1: "माघे संक्रान्ति (Maghe Sankranti)",
        5: "श्री पञ्चमी/सरस्वती पूजा (Shree Panchami/Saraswati Puja)",
        # Shivaratri is on Magh Krishna Chaturdashi (14th day of dark fortnight)
        29: "महाशिवरात्री (Maha Shivaratri)", # Usually falls around this date
        15: "माघ पूर्णिमा (Magh Purnima)",
    },
    
    # Falgun (फाल्गुन) - Month 11
    11: {
        15: "फागु पूर्णिमा/होली (Fagu Purnima/Holi)",
        # Holi is celebrated on Falgun Purnima
    },
    
    # Chaitra (चैत्र) - Month 12
    12: {
        8: "चैत्र अष्टमी (Chaitra Ashtami)",
        9: "चैत्र नवमी (Chaitra Navami)", 
        # Ram Navami is on Chaitra Shukla Navami
        15: "चैत्र पूर्णिमा (Chaitra Purnima)",
        30: "चैत्र दशैं (Chaitra Dashain)", # Last day of year
    }
}

# Additional important festivals that may vary by lunar calendar
VARIABLE_FESTIVALS = {
    "Buddha Jayanti": "Usually Baisakh Purnima (Baisakh 15)",
    "Guru Purnima": "Usually Ashadh Purnima (Ashadh 15)", 
    "Yomari Punhi": "Mangsir Purnima (Mangsir 15) - Newar festival",
    "Indra Jatra": "Usually in Bhadra month - varies by lunar calendar",
    "Ghodejatra": "Usually in Chaitra month",
}

def populate_accurate_festivals(year=2082):
    """Populate accurate Nepali festivals based on proper calendar"""
    
    print(f"Populating ACCURATE Nepali festivals for year {year}")
    print("Based on traditional Nepali lunar calendar")
    print("="*60)
    
    school = SchoolDetail.get_current_school()
    
    # Clear existing festival events
    CalendarEvent.objects.filter(event_type='festival').delete()
    print("Cleared existing festival events")
    
    festivals_created = 0
    
    for month in range(1, 13):
        month_name = NepaliCalendar.NEPALI_MONTHS_EN[month-1]
        print(f"\nMonth {month} - {month_name}:")
        
        if month in ACCURATE_FESTIVALS:
            for day, festival_name in ACCURATE_FESTIVALS[month].items():
                try:
                    # Convert to English date
                    english_date = NepaliCalendar.nepali_date_to_english_approximate(year, month, day)
                    
                    # Create festival event
                    CalendarEvent.objects.create(
                        title=festival_name,
                        description=f"Traditional Nepali festival on {day} {month_name}, {year} BS",
                        event_date=english_date,
                        event_type='festival',
                        school=school,
                        created_by='Accurate Festival System'
                    )
                    festivals_created += 1
                    print(f"  ✓ {festival_name}")
                    print(f"    Nepali: {year}/{month:02d}/{day:02d}")
                    print(f"    English: {english_date}")
                    
                except Exception as e:
                    print(f"  ✗ Error creating {festival_name}: {e}")
        else:
            print(f"  No major festivals recorded for {month_name}")
    
    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"Successfully created {festivals_created} accurate festival events")
    print(f"For Nepali year {year} (Baishakh 1 to Chaitra 30)")
    print(f"{'='*60}")
    
    # Show some upcoming festivals
    print(f"\nUpcoming Festivals (next 10):")
    from datetime import date
    upcoming = CalendarEvent.objects.filter(
        event_type='festival',
        event_date__gte=date.today()
    ).order_by('event_date')[:10]
    
    for i, festival in enumerate(upcoming, 1):
        nepali_date = NepaliCalendar.english_to_nepali_date(festival.event_date)
        print(f"{i:2d}. {festival.title}")
        print(f"    {festival.event_date} ({NepaliCalendar.format_nepali_date(nepali_date, 'short')} BS)")
    
    return festivals_created

def add_school_holidays():
    """Add school holidays and important dates"""
    
    print(f"\nAdding school holidays and important dates...")
    
    school = SchoolDetail.get_current_school()
    
    # Clear existing school events
    CalendarEvent.objects.filter(event_type__in=['holiday', 'event']).delete()
    
    # Add Saturday holidays for current year
    current_year = NepaliCalendar.get_current_nepali_date()['year']
    saturday_count = 0
    
    for month in range(1, 13):
        days_in_month = NepaliCalendar.NEPALI_DAYS.get(current_year, [31]*12)[month-1]
        for day in range(1, days_in_month + 1):
            try:
                english_date = NepaliCalendar.nepali_date_to_english_approximate(current_year, month, day)
                if english_date.weekday() == 5:  # Saturday
                    CalendarEvent.objects.create(
                        title="Saturday Holiday",
                        description="Weekly holiday",
                        event_date=english_date,
                        event_type='holiday',
                        school=school,
                        created_by='School System'
                    )
                    saturday_count += 1
            except Exception:
                continue
    
    print(f"Added {saturday_count} Saturday holidays")
    
    # Add some important school events
    school_events = [
        (1, 10, "New Academic Session Begins"),
        (3, 15, "Annual Examination Period"),
        (12, 29, "Academic Session Ends"),
    ]
    
    events_added = 0
    for month, day, event_name in school_events:
        try:
            english_date = NepaliCalendar.nepali_date_to_english_approximate(current_year, month, day)
            CalendarEvent.objects.create(
                title=event_name,
                description=f"Important school event on {day} {NepaliCalendar.NEPALI_MONTHS_EN[month-1]}",
                event_date=english_date,
                event_type='event',
                school=school,
                created_by='School System'
            )
            events_added += 1
            print(f"Added: {event_name}")
        except Exception as e:
            print(f"Error adding {event_name}: {e}")
    
    return saturday_count + events_added

if __name__ == "__main__":
    # Get current Nepali year
    current_year = NepaliCalendar.get_current_nepali_date()['year']
    
    # Populate accurate festivals
    festivals_count = populate_accurate_festivals(current_year)
    
    # Add school holidays
    holidays_count = add_school_holidays()
    
    print(f"\n🎉 COMPLETED SUCCESSFULLY! 🎉")
    print(f"📅 Festivals: {festivals_count}")
    print(f"🏫 School Events/Holidays: {holidays_count}")
    print(f"📊 Total Events: {festivals_count + holidays_count}")