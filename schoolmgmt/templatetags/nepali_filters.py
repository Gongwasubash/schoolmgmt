from django import template
from ..nepali_calendar import NepaliCalendar
from datetime import datetime, date

register = template.Library()

@register.filter
def to_nepali_date(english_date, format_type='full_en'):
    """Convert English date to Nepali date format"""
    if not english_date:
        return ''
    
    try:
        nepali_date = NepaliCalendar.english_to_nepali_date(english_date)
        return NepaliCalendar.format_nepali_date(nepali_date, format_type)
    except:
        return str(english_date)

@register.filter
def to_nepali_datetime(english_datetime, format_type='full'):
    """Convert English datetime to Nepali datetime format"""
    if not english_datetime:
        return ''
    
    try:
        return NepaliCalendar.format_nepali_datetime(english_datetime, format_type)
    except:
        return str(english_datetime)

@register.filter
def nepali_weekday(english_date):
    """Get Nepali weekday from English date"""
    if not english_date:
        return ''
    
    try:
        weekday_info = NepaliCalendar.get_nepali_weekday(english_date)
        return weekday_info['name_english']
    except:
        return ''

@register.filter
def nepali_session(english_date):
    """Get Nepali session from English date"""
    if not english_date:
        return ''
    
    try:
        return NepaliCalendar.get_nepali_session_from_date(english_date)
    except:
        return ''

@register.filter
def nepali_fiscal_year(english_date):
    """Get Nepali fiscal year from English date"""
    if not english_date:
        return ''
    
    try:
        return NepaliCalendar.get_nepali_fiscal_year(english_date)
    except:
        return ''

@register.simple_tag
def current_nepali_date(format_type='full_en'):
    """Get current Nepali date"""
    nepali_date = NepaliCalendar.get_current_nepali_date()
    return NepaliCalendar.format_nepali_date(nepali_date, format_type)

@register.simple_tag
def current_nepali_info():
    """Get comprehensive current Nepali date information"""
    return NepaliCalendar.get_nepali_today_info()

@register.simple_tag
def nepali_year_options(start_year=2075, end_year=2090):
    """Get Nepali year options for forms"""
    return NepaliCalendar.get_nepali_year_range(start_year, end_year)

@register.simple_tag
def nepali_session_options(start_year=2082, end_year=2100):
    """Get Nepali session options for forms"""
    return NepaliCalendar.get_nepali_year_sessions(start_year, end_year)

@register.simple_tag
def nepali_months():
    """Get list of Nepali months in English"""
    return NepaliCalendar.NEPALI_MONTHS_EN

@register.simple_tag
def nepali_months_nepali():
    """Get list of Nepali months in Nepali"""
    return NepaliCalendar.NEPALI_MONTHS

@register.simple_tag
def nepali_weekdays():
    """Get list of Nepali weekdays in English"""
    return NepaliCalendar.NEPALI_WEEKDAYS_EN

@register.simple_tag
def nepali_calendar_month(year, month):
    """Get Nepali calendar for a specific month"""
    try:
        return NepaliCalendar.get_nepali_calendar_month(year, month)
    except:
        return None

@register.filter
def is_valid_nepali_date(date_string):
    """Check if a date string represents a valid Nepali date"""
    try:
        parts = date_string.split('/')
        if len(parts) == 3:
            year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
            return NepaliCalendar.is_valid_nepali_date(year, month, day)
    except:
        pass
    return False

@register.simple_tag
def nepali_events_calendar(year, month):
    """Get Nepali events calendar for a specific month"""
    try:
        return NepaliCalendar.get_nepali_events_calendar(year, month)
    except:
        return None