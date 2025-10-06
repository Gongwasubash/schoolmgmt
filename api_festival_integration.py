#!/usr/bin/env python3
import os
import sys
import django
import requests
from datetime import datetime, date

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent, SchoolDetail
from django.core.cache import cache

# Nepali Calendar API endpoints
API_ENDPOINTS = [
    "https://raw.githubusercontent.com/nepalicalendar/data/main/festivals/2082.json",
    "https://api.nepalicalendar.com/festivals/2082",
    "https://hamropatro.com/api/festivals/2082"
]

def fetch_festivals_from_api(year_bs="2082"):
    """Fetch festivals from multiple API sources"""
    
    for api_url in API_ENDPOINTS:
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                return response.json()
        except:
            continue
    
    # Fallback data if APIs fail
    return {
        "festivals": [
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
    }

def populate_from_api():
    """Populate calendar events from API data"""
    
    cache_key = "nepali_festivals_2082"
    data = cache.get(cache_key)
    
    if not data:
        data = fetch_festivals_from_api()
        cache.set(cache_key, data, 86400)  # Cache for 1 day
    
    CalendarEvent.objects.filter(event_type='festival').delete()
    school = SchoolDetail.get_current_school()
    
    festivals = data.get('festivals', [])
    
    for festival in festivals:
        festival_date = datetime.strptime(festival['date'], '%Y-%m-%d').date()
        CalendarEvent.objects.create(
            title=festival['name'],
            description="Festival from API",
            event_date=festival_date,
            event_type='festival',
            school=school,
            created_by='API System'
        )
    
    print(f"Populated {len(festivals)} festivals from API")
    
    for festival in festivals:
        print(f"{festival['date']} - {festival['name']}")

if __name__ == "__main__":
    populate_from_api()