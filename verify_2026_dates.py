#!/usr/bin/env python3
import os
import sys
import django
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent

# Check current 2026 festival dates
festivals_2026 = CalendarEvent.objects.filter(
    event_type='festival',
    event_date__year=2026
).order_by('event_date')

print("Current 2026 festival dates in database:")
for festival in festivals_2026:
    print(f"{festival.event_date} - {festival.title}")

print(f"\nTotal 2026 festivals: {festivals_2026.count()}")

# Verify specific dates mentioned
specific_dates = {
    "Holi": "2026-03-14",
    "Maha Shivaratri": "2026-02-26", 
    "Shree Panchami": "2026-01-23"
}

print(f"\nVerifying specific dates:")
for name, expected_date in specific_dates.items():
    festival = festivals_2026.filter(title__icontains=name.split()[0]).first()
    if festival:
        actual_date = festival.event_date.strftime('%Y-%m-%d')
        status = "✓" if actual_date == expected_date else "✗"
        print(f"{status} {name}: Expected {expected_date}, Got {actual_date}")
    else:
        print(f"✗ {name}: Not found in database")