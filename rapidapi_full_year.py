#!/usr/bin/env python3
import os
import sys
import django
import requests
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent, SchoolDetail

RAPIDAPI_KEY = "your-rapidapi-key-here"

def get_all_festivals_2082():
    url = "https://nepalicalendarapi.p.rapidapi.com/festivals"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "nepalicalendarapi.p.rapidapi.com"
    }
    params = {"year": "2082"}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"API failed: {e}")
    
    return None

def populate_full_year_festivals():
    print("Fetching all festivals for 2082 (Baisakh 1 to Chaitra 30)...")
    
    festivals = get_all_festivals_2082()
    
    if not festivals:
        print("API failed, no festivals populated")
        return
    
    CalendarEvent.objects.filter(event_type='festival').delete()
    school = SchoolDetail.get_current_school()
    
    count = 0
    for festival in festivals:
        try:
            festival_date = datetime.strptime(festival['date'], '%Y-%m-%d').date()
            CalendarEvent.objects.create(
                title=festival['name'],
                description=f"Festival from RapidAPI - {festival.get('description', '')}",
                event_date=festival_date,
                event_type='festival',
                school=school,
                created_by='RapidAPI 2082'
            )
            count += 1
            print(f"{festival['date']} - {festival['name']}")
        except Exception as e:
            print(f"Error adding {festival}: {e}")
    
    print(f"\nPopulated {count} festivals for full year 2082 (Baisakh 1 to Chaitra 30)")

if __name__ == "__main__":
    populate_full_year_festivals()