#!/usr/bin/env python
"""
Simple test for Nepali date integration
"""

import os
import sys
import django
from datetime import date

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.nepali_calendar import NepaliCalendar
from schoolmgmt.views import get_current_nepali_year_session

def test_basic_functionality():
    print("Testing Nepali Calendar Integration...")
    
    # Test current session
    try:
        current_session = get_current_nepali_year_session()
        print(f"Current Nepali Session: {current_session}")
    except Exception as e:
        print(f"Error getting current session: {e}")
        return False
    
    # Test date conversion
    try:
        today = date.today()
        nepali_date = NepaliCalendar.english_to_nepali_date(today)
        formatted = NepaliCalendar.format_nepali_date(nepali_date, 'short')
        print(f"Today ({today}) in Nepali: {formatted}")
    except Exception as e:
        print(f"Error converting date: {e}")
        return False
    
    # Test English months
    try:
        months = NepaliCalendar.NEPALI_MONTHS_EN
        print(f"Nepali months available: {len(months)} months")
        print(f"First few months: {months[:3]}")
    except Exception as e:
        print(f"Error getting months: {e}")
        return False
    
    print("All basic tests passed!")
    return True

if __name__ == "__main__":
    success = test_basic_functionality()
    if success:
        print("Nepali date integration is working correctly!")
    else:
        print("There are issues with the integration.")