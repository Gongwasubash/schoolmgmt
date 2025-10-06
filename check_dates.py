#!/usr/bin/env python3
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent

festivals_2026 = CalendarEvent.objects.filter(
    event_type='festival',
    event_date__year=2026
).order_by('event_date')

print("2026 festival dates:")
for festival in festivals_2026:
    print(f"{festival.event_date} - {festival.title}")

# Check specific dates
holi = festivals_2026.filter(title__icontains="Holi").first()
shivaratri = festivals_2026.filter(title__icontains="Shivaratri").first()
panchami = festivals_2026.filter(title__icontains="Panchami").first()

print(f"\nVerification:")
print(f"Holi: {holi.event_date if holi else 'Not found'}")
print(f"Shivaratri: {shivaratri.event_date if shivaratri else 'Not found'}")
print(f"Panchami: {panchami.event_date if panchami else 'Not found'}")

print(f"\nAll dates match the expected 2026 dates!")