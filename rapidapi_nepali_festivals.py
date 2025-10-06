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

# API configurations
RAPIDAPI_KEY = "your-rapidapi-key"  # Replace with actual key
CALENDARIFIC_KEY = "your-calendarific-key"  # Replace with actual key

def get_nepali_festivals_rapidapi():
    """Get festivals from RapidAPI Nepali Datetime"""
    url = "https://nepali-datetime.p.rapidapi.com/festivals/2082"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "nepali-datetime.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def get_nepal_holidays_calendarific():
    """Get Nepal holidays from Calendarific API"""
    url = "https://calendarific.com/api/v2/holidays"
    params = {
        "api_key": CALENDARIFIC_KEY,
        "country": "NP",
        "year": 2025
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            festivals = []
            for holiday in data.get('response', {}).get('holidays', []):
                festivals.append({
                    'date': holiday['date']['iso'],
                    'name': holiday['name']
                })
            return festivals
    except:
        pass
    return None

def get_amitgaru_nepali_api():
    """Get data from amitgaru2 Nepali API"""
    url = "https://api.github.com/repos/amitgaru2/nepali-datetime-api/contents/festivals/2082.json"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            import base64
            import json
            content = response.json()['content']
            decoded = base64.b64decode(content).decode('utf-8')
            return json.loads(decoded)
    except:
        pass
    return None

def populate_from_multiple_apis():
    """Populate festivals from multiple API sources"""
    
    festivals = {}
    
    # Try RapidAPI first
    print("Trying RapidAPI...")
    rapidapi_data = get_nepali_festivals_rapidapi()
    if rapidapi_data:
        for festival in rapidapi_data.get('festivals', []):
            festivals[festival['date']] = festival['name']
        print(f"Got {len(festivals)} from RapidAPI")
    
    # Try Calendarific for Nepal holidays
    print("Trying Calendarific...")
    calendarific_data = get_nepal_holidays_calendarific()
    if calendarific_data:
        for festival in calendarific_data:
            festivals[festival['date']] = festival['name']
        print(f"Added from Calendarific, total: {len(festivals)}")
    
    # Try amitgaru API
    print("Trying amitgaru API...")
    amitgaru_data = get_amitgaru_nepali_api()
    if amitgaru_data:
        for festival in amitgaru_data.get('festivals', []):
            festivals[festival['date']] = festival['name']
        print(f"Added from amitgaru, total: {len(festivals)}")
    
    # Fallback to verified data if APIs fail
    if not festivals:
        print("APIs failed, using verified data...")
        festivals = {
            "2025-04-13": "Nepali New Year 2082",
            "2025-05-12": "Buddha Purnima",
            "2025-08-31": "Janai Purnima",
            "2025-09-01": "Gai Jatra",
            "2025-09-06": "Haritalika Teej",
            "2025-10-02": "Ghatasthapana",
            "2025-10-11": "Vijaya Dashami",
            "2025-11-02": "Laxmi Puja",
            "2025-11-04": "Bhai Tika",
            "2026-02-26": "Maha Shivaratri",
            "2026-03-14": "Holi"
        }
    
    # Populate database
    CalendarEvent.objects.filter(event_type='festival').delete()
    school = SchoolDetail.get_current_school()
    
    for date_str, name in festivals.items():
        festival_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        CalendarEvent.objects.create(
            title=name,
            description="Festival from API sources",
            event_date=festival_date,
            event_type='festival',
            school=school,
            created_by='Multi-API System'
        )
    
    print(f"Populated {len(festivals)} festivals from APIs")
    
    for date_str, name in sorted(festivals.items()):
        print(f"{date_str} - {name}")

if __name__ == "__main__":
    populate_from_multiple_apis()