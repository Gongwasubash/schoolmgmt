#!/usr/bin/env python3
"""
Nepali Festival Data and Calendar Event Population System
Populates calendar events from Baishakh 1 to Chaitra 30 (full Nepali year)
"""

import os
import sys
import django
from datetime import date, timedelta

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent, SchoolDetail
from schoolmgmt.nepali_calendar import NepaliCalendar

class NepaliFestivalData:
    """Comprehensive Nepali festival and event data"""
    
    FESTIVALS = {
        # Baishakh (Month 1)
        1: {
            1: "नयाँ वर्ष (New Year)",
            8: "बुद्ध जयन्ती (Buddha Jayanti)",
            15: "रामनवमी (Ram Navami)",
            30: "अक्षय तृतीया (Akshaya Tritiya)"
        },
        
        # Jestha (Month 2)
        2: {
            15: "कुमार षष्ठी (Kumar Shashthi)",
            30: "गंगा दशहरा (Ganga Dashahara)"
        },
        
        # Ashadh (Month 3)
        3: {
            15: "हरिशयनी एकादशी (Harishayani Ekadashi)",
            32: "गुरु पूर्णिमा (Guru Purnima)"
        },
        
        # Shrawan (Month 4)
        4: {
            1: "श्रावण सक्रान्ति (Shrawan Sankranti)",
            15: "जनै पूर्णिमा (Janai Purnima)",
            23: "गाईजात्रा (Gai Jatra)",
            30: "कृष्ण जन्माष्टमी (Krishna Janmashtami)"
        },
        
        # Bhadra (Month 5)
        5: {
            3: "तीज (Teej)",
            18: "ऋषि पञ्चमी (Rishi Panchami)",
            22: "इन्द्रजात्रा (Indra Jatra)"
        },
        
        # Ashwin (Month 6)
        6: {
            7: "घटस्थापना (Ghatasthapana)",
            15: "विजया दशमी (Vijaya Dashami)",
            16: "एकादशी (Ekadashi)",
            30: "कोजाग्रत पूर्णिमा (Kojagrat Purnima)"
        },
        
        # Kartik (Month 7)
        7: {
            1: "दीपावली/तिहार सुरु (Tihar Begins)",
            2: "गाई तिहार (Gai Tihar)",
            3: "गोरु तिहार (Goru Tihar)",
            4: "गोवर्धन पूजा (Govardhan Puja)",
            5: "भाई टीका (Bhai Tika)",
            15: "छठ पर्व (Chhath Parva)"
        },
        
        # Mangsir (Month 8)
        8: {
            8: "यमरी पुन्ही (Yomari Punhi)",
            15: "उधौली पर्व (Udhauli Parva)",
            30: "मार्गशीर्ष पूर्णिमा (Margashirsha Purnima)"
        },
        
        # Poush (Month 9)
        9: {
            1: "पौष सक्रान्ति (Poush Sankranti)",
            15: "माघे सक्रान्ति (Maghe Sankranti)",
            30: "पौष पूर्णिमा (Poush Purnima)"
        },
        
        # Magh (Month 10)
        10: {
            1: "माघे सक्रान्ति (Maghe Sankranti)",
            5: "श्री पञ्चमी (Shree Panchami)",
            14: "शिवरात्री (Shivaratri)",
            30: "होली (Holi)"
        },
        
        # Falgun (Month 11)
        11: {
            15: "फागु पूर्णिमा (Fagu Purnima)",
            30: "चैत दशैं (Chait Dashain)"
        },
        
        # Chaitra (Month 12)
        12: {
            8: "चैत्र अष्टमी (Chaitra Ashtami)",
            15: "चैत्र दशैं (Chaitra Dashain)",
            30: "चैत्र पूर्णिमा (Chaitra Purnima)"
        }
    }
    
    SCHOOL_EVENTS = {
        # Regular school events throughout the year
        1: {
            10: "नयाँ सत्र सुरुवात (New Session Begins)",
            20: "अभिभावक भेला (Parent Meeting)"
        },
        2: {
            15: "खेलकुद प्रतियोगिता (Sports Competition)",
            25: "सांस्कृतिक कार्यक्रम (Cultural Program)"
        },
        3: {
            10: "वार्षिक परीक्षा (Annual Examination)",
            25: "परीक्षा परिणाम (Exam Results)"
        },
        4: {
            5: "शिक्षक दिवस (Teacher's Day)",
            20: "विज्ञान मेला (Science Fair)"
        },
        5: {
            15: "सफाई अभियान (Cleanliness Campaign)",
            25: "वृक्षारोपण कार्यक्रम (Tree Plantation)"
        },
        6: {
            10: "दशैं बिदा सुरु (Dashain Holiday Begins)",
            25: "दशैं बिदा समाप्त (Dashain Holiday Ends)"
        },
        7: {
            10: "तिहार बिदा सुरु (Tihar Holiday Begins)",
            20: "तिहार बिदा समाप्त (Tihar Holiday Ends)"
        },
        8: {
            15: "शीतकालीन बिदा (Winter Holiday)",
            30: "वार्षिक उत्सव (Annual Celebration)"
        },
        9: {
            10: "शीतकालीन खेलकुद (Winter Sports)",
            25: "सामुदायिक सेवा (Community Service)"
        },
        10: {
            15: "कला प्रदर्शनी (Art Exhibition)",
            25: "अन्तिम परीक्षा तयारी (Final Exam Preparation)"
        },
        11: {
            10: "होली समारोह (Holi Celebration)",
            25: "स्नातक समारोह (Graduation Ceremony)"
        },
        12: {
            15: "वार्षिक समीक्षा (Annual Review)",
            29: "सत्र समाप्ति (Session End)"
        }
    }

def populate_nepali_calendar_events(year=2082):
    """Populate calendar events for a full Nepali year"""
    
    print(f"Populating Nepali calendar events for year {year}...")
    
    # Get or create school
    school = SchoolDetail.get_current_school()
    
    # Clear existing festival events for the year
    CalendarEvent.objects.filter(
        event_type__in=['festival', 'event'],
        event_date_nepali__contains=str(year)
    ).delete()
    
    events_created = 0
    
    # Populate festivals and events for each month
    for month in range(1, 13):  # Baishakh (1) to Chaitra (12)
        month_name = NepaliCalendar.NEPALI_MONTHS_EN[month-1]
        
        # Add festivals
        if month in NepaliFestivalData.FESTIVALS:
            for day, festival_name in NepaliFestivalData.FESTIVALS[month].items():
                # Convert to English date (approximate)
                try:
                    english_date = NepaliCalendar.nepali_date_to_english_approximate(year, month, day)
                    
                    # Create festival event
                    event = CalendarEvent.objects.create(
                        title=festival_name,
                        description=f"Traditional Nepali festival celebrated on {day} {month_name}",
                        event_date=english_date,
                        event_type='festival',
                        school=school,
                        created_by='System'
                    )
                    events_created += 1
                    print(f"Created festival: {festival_name} on {english_date}")
                    
                except Exception as e:
                    print(f"Error creating festival event for {day} {month_name}: {e}")
        
        # Add school events
        if month in NepaliFestivalData.SCHOOL_EVENTS:
            for day, event_name in NepaliFestivalData.SCHOOL_EVENTS[month].items():
                try:
                    english_date = NepaliCalendar.nepali_date_to_english_approximate(year, month, day)
                    
                    # Create school event
                    event = CalendarEvent.objects.create(
                        title=event_name,
                        description=f"School event scheduled for {day} {month_name}",
                        event_date=english_date,
                        event_type='event',
                        school=school,
                        created_by='System'
                    )
                    events_created += 1
                    print(f"Created school event: {event_name} on {english_date}")
                    
                except Exception as e:
                    print(f"Error creating school event for {day} {month_name}: {e}")
    
    print(f"\nSuccessfully created {events_created} calendar events for Nepali year {year}")
    return events_created

def populate_multiple_years(start_year=2082, end_year=2084):
    """Populate calendar events for multiple Nepali years"""
    
    total_events = 0
    
    for year in range(start_year, end_year + 1):
        print(f"\n{'='*50}")
        print(f"Processing Nepali Year: {year}")
        print(f"{'='*50}")
        
        events_count = populate_nepali_calendar_events(year)
        total_events += events_count
    
    print(f"\n{'='*60}")
    print(f"SUMMARY: Created {total_events} total events for years {start_year}-{end_year}")
    print(f"{'='*60}")

def add_weekly_school_days(year=2082):
    """Add regular school days (excluding Saturdays)"""
    
    print(f"\nAdding weekly school days for Nepali year {year}...")
    
    school = SchoolDetail.get_current_school()
    school_days_created = 0
    
    # Clear existing school-day events
    CalendarEvent.objects.filter(
        event_type='school-day',
        event_date_nepali__contains=str(year)
    ).delete()
    
    for month in range(1, 13):
        # Get days in this Nepali month
        days_in_month = NepaliCalendar.NEPALI_DAYS.get(year, [31]*12)[month-1]
        
        for day in range(1, days_in_month + 1):
            try:
                english_date = NepaliCalendar.nepali_date_to_english_approximate(year, month, day)
                weekday = english_date.weekday()  # Monday=0, Sunday=6
                
                # Skip Saturdays (5) - weekend in Nepal
                if weekday != 5:
                    # Check if it's not already a festival/holiday
                    existing_events = CalendarEvent.objects.filter(
                        event_date=english_date,
                        event_type__in=['festival', 'holiday']
                    ).exists()
                    
                    if not existing_events:
                        CalendarEvent.objects.create(
                            title="School Day",
                            description="Regular school day",
                            event_date=english_date,
                            event_type='school-day',
                            school=school,
                            created_by='System'
                        )
                        school_days_created += 1
                        
            except Exception as e:
                print(f"Error creating school day for {day}/{month}/{year}: {e}")
    
    print(f"Created {school_days_created} school day events for year {year}")
    return school_days_created

def main():
    """Main function to populate all calendar events"""
    
    print("Nepali Festival and Calendar Event Population System")
    print("="*60)
    
    # Get current Nepali year
    current_nepali = NepaliCalendar.get_current_nepali_date()
    current_year = current_nepali['year']
    
    print(f"Current Nepali Year: {current_year}")
    print(f"Current Date: {NepaliCalendar.format_nepali_date(current_nepali, 'full_en')}")
    
    # Populate events for current year and next 2 years
    start_year = current_year
    end_year = current_year + 2
    
    # Populate festivals and events
    populate_multiple_years(start_year, end_year)
    
    # Add school days for current year
    add_weekly_school_days(current_year)
    
    print(f"\n✅ Calendar population completed successfully!")
    print(f"📅 Events created for Nepali years {start_year} to {end_year}")
    print(f"🏫 School days added for year {current_year}")

if __name__ == "__main__":
    main()