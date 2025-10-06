#!/usr/bin/env python3
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent

festivals = CalendarEvent.objects.filter(event_type='festival').order_by('event_date')

print("ACCURATE NEPALI FESTIVALS 2025:")
print("="*40)

for i, festival in enumerate(festivals, 1):
    print(f"{i:2d}. {festival.title}")
    print(f"    Date: {festival.event_date}")
    print()

print(f"Total: {festivals.count()} festivals")