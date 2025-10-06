import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import SchoolAttendance, CalendarEvent

def clean_attendance():
    # Get all holiday/festival dates from CalendarEvent
    holiday_dates = CalendarEvent.objects.filter(
        is_active=True,
        event_type__in=['holiday', 'festival']
    ).values_list('event_date', flat=True)
    
    # Get all Saturday dates from attendance records
    saturday_dates = []
    for attendance in SchoolAttendance.objects.all():
        if attendance.date.weekday() == 5:  # Saturday
            saturday_dates.append(attendance.date)
    
    # Combine all non-school days
    non_school_days = list(holiday_dates) + saturday_dates
    
    # Delete attendance records for non-school days
    deleted_count = SchoolAttendance.objects.filter(date__in=non_school_days).delete()[0]
    
    print(f"Deleted {deleted_count} attendance records for holidays, festivals, and Saturdays")

if __name__ == "__main__":
    clean_attendance()