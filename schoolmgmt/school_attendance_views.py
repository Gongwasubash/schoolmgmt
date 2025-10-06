from django.shortcuts import render
from django.http import JsonResponse
from .models import CalendarEvent, StudentAttendance, Student
from datetime import date

def school_attendance_dates(request):
    """Show list of school dates"""
    school_dates = CalendarEvent.objects.filter(
        event_type__in=['school-day', 'event'],
        event_date__gte=date(2025, 4, 14)
    ).values('event_date').distinct().order_by('-event_date')
    
    return render(request, 'school_attendance_dates.html', {
        'school_dates': school_dates
    })

def school_attendance_records(request, date_str):
    """Show student attendance records for specific date"""
    try:
        attendance_date = date.fromisoformat(date_str)
        
        # Get attendance records for this date
        attendance_records = StudentAttendance.objects.filter(
            date=attendance_date
        ).select_related('student').order_by('student__name')
        
        return render(request, 'school_attendance_records.html', {
            'date': attendance_date,
            'attendance_records': attendance_records
        })
        
    except ValueError:
        return render(request, 'error.html', {'message': 'Invalid date'})