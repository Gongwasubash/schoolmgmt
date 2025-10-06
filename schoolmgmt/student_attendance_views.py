from django.shortcuts import render, get_object_or_404
from .models import Student, SchoolAttendance

def student_attendance_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    # Get attendance records for this student
    attendance_records = SchoolAttendance.objects.filter(student=student)
    
    # Calculate statistics
    total_records = attendance_records.count()
    present_count = attendance_records.filter(status='present').count()
    absent_count = attendance_records.filter(status='absent').count()
    late_count = attendance_records.filter(status='late').count()
    
    attendance_percentage = round((present_count / total_records * 100) if total_records > 0 else 0, 1)
    
    context = {
        'student': student,
        'present_count': present_count,
        'absent_count': absent_count,
        'late_count': late_count,
        'attendance_percentage': attendance_percentage,
        'total_records': total_records
    }
    
    return render(request, 'student_attendance_detail.html', context)