from django.core.exceptions import ValidationError
from .models import CalendarEvent

def validate_attendance_date(date):
    """Check if attendance can be recorded on this date"""
    
    # Check if it's a holiday
    holiday = CalendarEvent.objects.filter(
        event_date=date,
        event_type__in=['holiday', 'festival']
    ).exists()
    
    if holiday:
        raise ValidationError(f"Cannot record attendance on {date} - it's a holiday/festival")
    
    # Check if it's Saturday
    if date.weekday() == 5:
        raise ValidationError(f"Cannot record attendance on {date} - it's Saturday")
    
    return True