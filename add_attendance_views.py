import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

# Add these functions to views.py
attendance_views = '''
@csrf_exempt
def save_attendance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            attendance_date = data['date']
            attendance_data = data['attendance']
            
            saved_count = 0
            for student_id, status in attendance_data.items():
                student = get_object_or_404(Student, id=student_id)
                
                SchoolAttendance.objects.update_or_create(
                    student=student,
                    date=attendance_date,
                    defaults={
                        'status': status,
                        'marked_by': request.session.get('admin_username', 'System')
                    }
                )
                saved_count += 1
            
            return JsonResponse({
                'success': True,
                'message': f'Attendance saved for {saved_count} students'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def load_attendance(request):
    try:
        attendance_date = request.GET.get('date', date.today().strftime('%Y-%m-%d'))
        attendance_records = SchoolAttendance.objects.filter(date=attendance_date).select_related('student')
        
        attendance_data = {}
        for record in attendance_records:
            attendance_data[record.student.id] = record.status
        
        return JsonResponse({
            'success': True,
            'attendance': attendance_data,
            'date': attendance_date
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def get_attendance_summary(request, student_id):
    try:
        student = get_object_or_404(Student, id=student_id)
        summary = SchoolAttendance.get_attendance_summary(student)
        
        return JsonResponse({
            'success': True,
            'student': student.name,
            'summary': summary
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def attendance_report(request):
    students = Student.objects.all().order_by('name')
    return render(request, 'attendance_report.html', {'students': students})
'''

print("Add these functions to views.py:")
print(attendance_views)