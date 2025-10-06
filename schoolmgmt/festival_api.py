from django.http import JsonResponse
from .models import CalendarEvent
from .nepali_calendar import NepaliCalendar

def festivals_2082_api(request):
    festivals = CalendarEvent.objects.filter(event_type='festival').order_by('event_date')
    
    festival_data = []
    for festival in festivals:
        nepali_date = NepaliCalendar.english_to_nepali_date(festival.event_date)
        
        festival_data.append({
            "name_en": festival.title,
            "name_ne": get_nepali_name(festival.title),
            "date_bs": f"{nepali_date['year']}/{nepali_date['month']:02d}/{nepali_date['day']:02d}",
            "date_ad": festival.event_date.strftime('%Y-%m-%d'),
            "description": festival.description or ""
        })
    
    return JsonResponse({
        "year": 2082,
        "total_festivals": len(festival_data),
        "festivals": festival_data
    })

def get_nepali_name(english_name):
    nepali_names = {
        "Nepali New Year 2082": "नव वर्ष २०८२",
        "Buddha Purnima": "बुद्ध पूर्णिमा",
        "Janai Purnima": "जनै पूर्णिमा",
        "Gai Jatra": "गाईजात्रा",
        "Haritalika Teej": "हरितालिका तीज",
        "Krishna Janmashtami": "कृष्ण जन्माष्टमी",
        "Ghatasthapana": "घटस्थापना",
        "Vijaya Dashami": "विजया दशमी",
        "Laxmi Puja": "लक्ष्मी पूजा",
        "Bhai Tika": "भाई टीका",
        "Chhath Parva": "छठ पर्व",
        "Maha Shivaratri": "महाशिवरात्री",
        "Holi": "होली"
    }
    return nepali_names.get(english_name, english_name)