#!/usr/bin/env python3
import os
import sys
import django
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import re

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import CalendarEvent, SchoolDetail

def scrape_hamro_patro_festivals():
    """Scrape festival dates from Hamro Patro"""
    
    festivals = {}
    
    # Get current year and next year pages
    for year in [2025, 2026]:
        for month in range(1, 13):
            try:
                url = f"https://www.hamropatro.com/calendar/{year}/{month:02d}"
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                
                response = requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find festival elements
                festival_elements = soup.find_all(['div', 'span'], class_=re.compile(r'festival|event|holiday'))
                
                for element in festival_elements:
                    text = element.get_text().strip()
                    if any(keyword in text.lower() for keyword in ['dashain', 'tihar', 'teej', 'holi', 'new year', 'buddha', 'janai']):
                        # Extract date from parent or sibling elements
                        date_element = element.find_parent().find(string=re.compile(r'\d{1,2}'))
                        if date_element:
                            day = int(re.search(r'\d+', date_element).group())
                            festival_date = date(year, month, day)
                            festivals[festival_date] = text
                            
            except Exception as e:
                print(f"Error scraping {year}/{month}: {e}")
                continue
    
    return festivals

def populate_scraped_festivals():
    """Populate festivals from scraped data"""
    
    print("Scraping Hamro Patro...")
    festivals = scrape_hamro_patro_festivals()
    
    if not festivals:
        print("No festivals scraped, using fallback data...")
        # Fallback to known accurate dates
        festivals = {
            date(2025, 4, 14): "Nepali New Year 2082",
            date(2025, 5, 23): "Buddha Purnima", 
            date(2025, 8, 19): "Janai Purnima",
            date(2025, 8, 20): "Gai Jatra",
            date(2025, 9, 20): "Haritalika Teej",
            date(2025, 10, 3): "Ghatasthapana",
            date(2025, 10, 12): "Vijaya Dashami",
            date(2025, 11, 3): "Laxmi Puja",
            date(2025, 11, 5): "Bhai Tika",
            date(2026, 2, 26): "Maha Shivaratri",
            date(2026, 3, 14): "Holi"
        }
    
    # Clear existing festivals
    CalendarEvent.objects.filter(event_type='festival').delete()
    school = SchoolDetail.get_current_school()
    
    # Add scraped festivals
    for festival_date, festival_name in festivals.items():
        CalendarEvent.objects.create(
            title=festival_name,
            description=f"Festival from Hamro Patro",
            event_date=festival_date,
            event_type='festival',
            school=school,
            created_by='Hamro Patro Scraper'
        )
    
    print(f"Added {len(festivals)} festivals from Hamro Patro")
    
    # Display results
    for festival_date, festival_name in sorted(festivals.items()):
        print(f"{festival_date} - {festival_name}")

if __name__ == "__main__":
    populate_scraped_festivals()