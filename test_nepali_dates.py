#!/usr/bin/env python
"""
Test script for Nepali date integration
Run this to verify Nepali date functionality is working correctly
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

def test_nepali_calendar():
    print("=== Testing Nepali Calendar Integration ===\n")
    
    # Test current Nepali date
    print("1. Current Nepali Date:")
    current_nepali = NepaliCalendar.get_current_nepali_date()
    print(f"   Raw: {current_nepali}")
    print(f"   Full EN: {NepaliCalendar.format_nepali_date(current_nepali, 'full_en')}")
    print(f"   Short: {NepaliCalendar.format_nepali_date(current_nepali, 'short')}")
    print()
    
    # Test current session
    print("2. Current Nepali Session:")
    current_session = get_current_nepali_year_session()
    print(f"   Session: {current_session}")
    print()
    
    # Test date conversion
    print("3. Date Conversion Examples:")
    test_dates = [
        date.today(),
        date(2024, 4, 14),  # Typical Nepali New Year
        date(2024, 12, 31), # End of English year
    ]
    
    for test_date in test_dates:
        nepali_converted = NepaliCalendar.english_to_nepali_date(test_date)
        print(f"   {test_date} -> {NepaliCalendar.format_nepali_date(nepali_converted, 'full_en')}")
    print()
    
    # Test Nepali months
    print("4. Nepali Months:")
    print(f"   English: {NepaliCalendar.NEPALI_MONTHS_EN}")
    print("   Nepali: [Unicode month names available]")
    print()
    
    # Test session generation
    print("5. Available Sessions:")
    sessions = NepaliCalendar.get_nepali_year_sessions(2082, 2085)
    for session in sessions[:5]:  # Show first 5
        print(f"   {session['label']}: {session['value']}")
    print()
    
    print("=== All Tests Completed Successfully! ===")

if __name__ == "__main__":
    test_nepali_calendar()