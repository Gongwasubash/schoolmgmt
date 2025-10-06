from django.shortcuts import render
from django.http import JsonResponse
from .models import CalendarEvent, StudentAttendance, Student
from datetime import date

def school_attendance_calendar(request):
    """Show calendar with school days"""
    school_days = CalendarEvent.objects.filter(
        event_type__in=['school-day', 'event'],
        event_date__gte=date(2025, 4, 14)
    ).order_by('event_date')
    
    return render(request, 'school_attendance_calendar.html', {
        'school_days': school_days
    })

def attendance_by_date(request, date_str):
    """Show attendance list for specific date"""
    try:
        attendance_date = date.fromisoformat(date_str)
        
        # Get all students with their attendance for this date
        students = Student.objects.all().order_by('name')
        attendance_data = []
        
        for student in students:
            try:
                attendance = StudentAttendance.objects.get(
                    student=student, 
                    date=attendance_date
                )
                status = attendance.status
            except StudentAttendance.DoesNotExist:
                status = 'not_marked'
            
            attendance_data.append({
                'student': student,
                'status': status
            })
        
        return render(request, 'attendance_by_date.html', {
            'date': attendance_date,
            'attendance_data': attendance_data
        })
        
    except ValueError:
        return render(request, 'error.html', {'message': 'Invalid date format'})

def mark_attendance_api(request):
    """API to mark attendance"""
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        date_str = request.POST.get('date')
        status = request.POST.get('status')
        
        try:
            student = Student.objects.get(id=student_id)
            attendance_date = date.fromisoformat(date_str)
            
            attendance, created = StudentAttendance.objects.update_or_create(
                student=student,
                date=attendance_date,
                defaults={
                    'status': status,
                    'marked_by': 'Manual Entry'
                }
            )
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})