#!/usr/bin/env python3
import os
import sys
import django
import requests

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

# Test the API endpoint
try:
    response = requests.get('http://127.0.0.1:8000/api/festivals/2082/', timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total festivals: {data['total_festivals']}")
        print("\nFirst 3 festivals:")
        for festival in data['festivals'][:3]:
            print(f"- {festival['name_en']} ({festival['name_ne']})")
            print(f"  BS: {festival['date_bs']}, AD: {festival['date_ad']}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Connection error: {e}")
    print("Make sure Django server is running: python manage.py runserver")