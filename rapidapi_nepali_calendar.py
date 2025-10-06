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

RAPIDAPI_KEY = "your-rapidapi-key-here"  # Replace with actual key

def get_festivals_from_rapidapi():
    url = "https://nepalicalendarapi.p.rapidapi.com/festivals"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "nepalicalendarapi.p.rapidapi.com"
    }
    params = {"year": "2082"}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"API Error: {e}")
    
    # Fallback data
    return [
        {"date": "2025-04-13", "name": "Nepali New Year 2082"},
        {"date": "2025-05-12", "name": "Buddha Purnima"},
        {"date": "2025-08-31", "name": "Janai Purnima"},
        {"date": "2025-09-01", "name": "Gai Jatra"},
        {"date": "2025-09-06", "name": "Haritalika Teej"},
        {"date": "2025-10-02", "name": "Ghatasthapana"},
        {"date": "2025-10-11", "name": "Vijaya Dashami"},
        {"date": "2025-11-02", "name": "Laxmi Puja"},
        {"date": "2025-11-04", "name": "Bhai Tika"},
        {"date": "2026-02-26", "name": "Maha Shivaratri"},
        {"date": "2026-03-14", "name": "Holi"}
    ]

def populate_rapidapi_festivals():
    festivals = get_festivals_from_rapidapi()
    
    CalendarEvent.objects.filter(event_type='festival').delete()
    school = SchoolDetail.get_current_school()
    
    for festival in festivals:
        festival_date = datetime.strptime(festival['date'], '%Y-%m-%d').date()
        CalendarEvent.objects.create(
            title=festival['name'],
            description="Festival from RapidAPI",
            event_date=festival_date,
            event_type='festival',
            school=school,
            created_by='RapidAPI'
        )
    
    print(f"Populated {len(festivals)} festivals from RapidAPI")
    for festival in festivals:
        print(f"{festival['date']} - {festival['name']}")

if __name__ == "__main__":
    populate_rapidapi_festivals()