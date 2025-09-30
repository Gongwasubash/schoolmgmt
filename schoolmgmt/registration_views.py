from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import StudentRegistration, Student, SchoolDetail
from datetime import date, datetime
import json

def public_registration(request):
    """Public registration form for new student admissions"""
    if request.method == 'POST':
        try:
            registration = StudentRegistration(
                name=request.POST.get('name'),
                student_class=request.POST.get('class'),
                section=request.POST.get('section', 'A'),
                gender=request.POST.get('gender'),
                dob=request.POST.get('dob'),
                religion=request.POST.get('religion', 'Hindu'),
                father_name=request.POST.get('fatherName'),
                mother_name=request.POST.get('motherName'),
                mobile=request.POST.get('mobile'),
                address=request.POST.get('address1'),
                city=request.POST.get('city'),
                status='pending'
            )
            registration.save()
            
            from django.shortcuts import redirect
            return redirect('application_status', registration_id=registration.id)
            
        except Exception as e:
            context = {
                'error': f'Error submitting registration: {str(e)}'
            }
            return render(request, 'public_registration.html', context)
    
    try:
        school = SchoolDetail.get_current_school()
    except:
        school = None
    
    return render(request, 'public_registration.html', {'school': school})

@csrf_exempt
def approve_registration(request):
    """Approve a student registration and create Student record"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            registration = get_object_or_404(StudentRegistration, id=data['registration_id'])
            
            if registration.status != 'pending':
                return JsonResponse({'success': False, 'error': 'Registration already processed'})
            
            reg_number = f"REG{datetime.now().year}{Student.objects.count() + 1:04d}"
            
            student = Student.objects.create(
                name=registration.name,
                student_class=registration.student_class,
                section=registration.section,
                gender=registration.gender,
                religion=registration.religion,
                dob=registration.dob,
                address1=registration.address,
                city=registration.city,
                mobile=registration.mobile,
                father_name=registration.father_name,
                mother_name=registration.mother_name,
                admission_date=date.today(),
                reg_number=reg_number,
                transport='00_No Transport Service | 0 Rs.',
                address2=''
            )
            
            registration.status = 'approved'
            registration.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Registration approved. Student created with ID: {student.reg_number}',
                'student_id': student.id
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def application_status(request, registration_id):
    """View application status page"""
    registration = get_object_or_404(StudentRegistration, id=registration_id)
    school = SchoolDetail.get_current_school()
    return render(request, 'application_status.html', {
        'registration': registration,
        'school': school
    })