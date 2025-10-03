from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from .models import Student, FeeStructure, FeePayment, Subject, Exam, Marksheet, Session, StudentMarks, MarksheetData, StudentDailyExpense, SchoolDetail, AdminLogin, StudentRegistration, WelcomeSection, ContactEnquiry, StudentAttendance, Teacher, TeacherClassSubject
from .decorators import permission_required
from django.db import models
from django.db.models import F, Q
import json
from datetime import datetime, date
from django.db.models import Count, Sum, Max
from decimal import Decimal
import csv
import io
from .nepali_calendar import NepaliCalendar
try:
    from nepali_datetime import date as nepali_date
except ImportError:
    nepali_date = None

def get_current_nepali_year_session():
    """Get current Nepali year session (e.g., '2082-83')"""
    return NepaliCalendar.get_nepali_session_from_date()

def convert_english_to_nepali_date_string(english_date, format_type='short'):
    """Convert English date to Nepali date string"""
    if not english_date:
        return ''
    try:
        nepali_date_dict = NepaliCalendar.english_to_nepali_date(english_date)
        return NepaliCalendar.format_nepali_date(nepali_date_dict, format_type)
    except:
        return str(english_date)

def get_nepali_months_list():
    """Get list of Nepali months in English"""
    return NepaliCalendar.NEPALI_MONTHS_EN

def get_comprehensive_nepali_info():
    """Get comprehensive Nepali date information for views"""
    return NepaliCalendar.get_nepali_today_info()

def format_nepali_datetime_for_display(english_datetime):
    """Format datetime for display with Nepali date"""
    if not english_datetime:
        return ''
    try:
        return NepaliCalendar.format_nepali_datetime(english_datetime, 'full')
    except:
        return str(english_datetime)

@permission_required('can_view_dashboard')
def dashboard(request):
    """Original dashboard view - accessible via /dashboard/ URL"""
    # Check if user has dashboard permission or is super admin
    if not (request.session.get('is_super_admin') or request.session.get('can_view_dashboard')):
        return redirect('home')
    
    # Get student statistics
    total_students = Student.objects.count()
    boys_count = Student.objects.filter(gender='Boy').count()
    girls_count = Student.objects.filter(gender='Girl').count()
    
    # Get today's birthdays
    today = date.today()
    todays_birthdays = Student.objects.filter(dob__month=today.month, dob__day=today.day).count()
    
    # Get today's collection
    todays_collection = FeePayment.objects.filter(payment_date=today).aggregate(total=Sum('payment_amount'))['total'] or 0
    
    # Get weekly collection (last 7 days)
    from datetime import timedelta
    week_start = today - timedelta(days=6)
    weekly_collection = FeePayment.objects.filter(payment_date__range=[week_start, today]).aggregate(total=Sum('payment_amount'))['total'] or 0
    
    # Get monthly collection (last 30 days) - total collection for last 30 days
    thirty_days_ago = today - timedelta(days=29)  # 30 days including today
    monthly_payments = FeePayment.objects.filter(
        payment_date__range=[thirty_days_ago, today]
    )
    monthly_collection = monthly_payments.aggregate(total=Sum('payment_amount'))['total']
    if monthly_collection is None:
        monthly_collection = Decimal('0')
    
    # Get yearly collection (current year)
    yearly_collection = FeePayment.objects.filter(payment_date__year=today.year).aggregate(total=Sum('payment_amount'))['total'] or 0
    
    
    # Get pending enquiries count - only count pending registrations and non-closed contact enquiries
    contact_enquiries_count = ContactEnquiry.objects.exclude(status='closed').count()
    pending_registrations_count = StudentRegistration.objects.filter(status='pending').count()
    pending_enquiries = contact_enquiries_count + pending_registrations_count
    
    # Get today's attendance statistics
    todays_attendance = StudentAttendance.objects.filter(date=today)
    total_present = todays_attendance.filter(status='present').count()
    total_absent = todays_attendance.filter(status='absent').count()
    total_late = todays_attendance.filter(status='late').count()
    attendance_percentage = round((total_present / total_students * 100) if total_students > 0 else 0, 1)
    
    # Get class-wise data
    class_data = Student.objects.values('student_class').annotate(count=Count('student_class')).order_by('student_class')
    
    # Get religion-wise data
    religion_data = Student.objects.values('religion').annotate(count=Count('religion')).order_by('religion')
    
    # Get comprehensive Nepali date information
    nepali_info = get_comprehensive_nepali_info()
    
    context = {
        'total_students': total_students,
        'boys_count': boys_count,
        'girls_count': girls_count,
        'todays_birthdays': todays_birthdays,
        'todays_collection': todays_collection,
        'weekly_collection': weekly_collection,
        'monthly_collection': monthly_collection,
        'yearly_collection': yearly_collection,
        'pending_enquiries': pending_enquiries,
        'total_present': total_present,
        'total_absent': total_absent,
        'total_late': total_late,
        'attendance_percentage': attendance_percentage,
        'class_data': class_data,
        'religion_data': religion_data,
        'nepali_info': nepali_info,
        'current_nepali_date': nepali_info['formatted_full'],
        'nepali_year': nepali_info['nepali_date']['year'],
        'current_nepali_session': nepali_info['session'],
        'nepali_fiscal_year': nepali_info['fiscal_year'],
        'nepali_weekday': nepali_info['weekday']['name_english'],
        'is_weekend': nepali_info['is_weekend'],
    }
    
    return render(request, 'index.html', context)


def home(request):
    # Lincoln School Homepage - Modern website homepage
    # Get hero slider images
    from .models import HeroSlider, Blog
    hero_images = HeroSlider.objects.filter(is_active=True).order_by('order')
    blogs = Blog.objects.all()[:3]
    welcome_section = WelcomeSection.get_active_welcome()
    
    # Get basic statistics for potential use
    total_students = Student.objects.count()
    boys_count = Student.objects.filter(gender='Boy').count()
    girls_count = Student.objects.filter(gender='Girl').count()
    
    # Get today's birthdays
    today = date.today()
    todays_birthdays = Student.objects.filter(dob__month=today.month, dob__day=today.day).count()
    
    # Get collection data
    todays_collection = FeePayment.objects.filter(payment_date=today).aggregate(total=Sum('payment_amount'))['total'] or 0
    
    from datetime import timedelta
    week_start = today - timedelta(days=6)
    weekly_collection = FeePayment.objects.filter(payment_date__range=[week_start, today]).aggregate(total=Sum('payment_amount'))['total'] or 0
    
    # Monthly collection calculation - total collection for last 30 days
    thirty_days_ago = today - timedelta(days=29)  # 30 days including today
    monthly_payments = FeePayment.objects.filter(
        payment_date__range=[thirty_days_ago, today]
    )
    monthly_collection = monthly_payments.aggregate(total=Sum('payment_amount'))['total']
    if monthly_collection is None:
        monthly_collection = Decimal('0')
    yearly_collection = FeePayment.objects.filter(payment_date__year=today.year).aggregate(total=Sum('payment_amount'))['total'] or 0
    
    # Get today's attendance statistics
    todays_attendance = StudentAttendance.objects.filter(date=today)
    total_present = todays_attendance.filter(status='present').count()
    total_absent = todays_attendance.filter(status='absent').count()
    total_late = todays_attendance.filter(status='late').count()
    attendance_percentage = round((total_present / total_students * 100) if total_students > 0 else 0, 1)
    
    # Get class-wise and religion-wise data
    class_data = Student.objects.values('student_class').annotate(count=Count('student_class')).order_by('student_class')
    religion_data = Student.objects.values('religion').annotate(count=Count('religion')).order_by('religion')
    
    # Get Nepali date information
    nepali_info = get_comprehensive_nepali_info()
    
    context = {
        'total_students': total_students,
        'boys_count': boys_count,
        'girls_count': girls_count,
        'todays_birthdays': todays_birthdays,
        'todays_collection': todays_collection,
        'weekly_collection': weekly_collection,
        'monthly_collection': monthly_collection,
        'yearly_collection': yearly_collection,
        'total_present': total_present,
        'total_absent': total_absent,
        'total_late': total_late,
        'attendance_percentage': attendance_percentage,
        'class_data': class_data,
        'religion_data': religion_data,
        'nepali_info': nepali_info,
        'current_nepali_date': nepali_info['formatted_full'],
        'nepali_year': nepali_info['nepali_date']['year'],
        'current_nepali_session': nepali_info['session'],
        'nepali_fiscal_year': nepali_info['fiscal_year'],
        'nepali_weekday': nepali_info['weekday']['name_english'],
        'is_weekend': nepali_info['is_weekend'],
    }
    
    # Get school details for homepage
    school = SchoolDetail.get_current_school()
    context['school'] = school
    context['hero_images'] = hero_images
    context['blogs'] = blogs
    context['welcome_section'] = welcome_section
    
    # Render the school homepage with dynamic school data
    return render(request, 'school_homepage.html', context)

from .decorators import permission_required

@permission_required('can_view_students')
def student_admission(request):
    if request.method == 'POST':
        try:
            session_name = get_current_nepali_year_session()
            current_session, created = Session.objects.get_or_create(
                name=session_name,
                defaults={
                    'start_date': date.today().replace(month=4, day=1),
                    'end_date': date.today().replace(year=date.today().year+1, month=3, day=31),
                    'is_active': True
                }
            )
            if created or not current_session.is_active:
                Session.objects.exclude(id=current_session.id).update(is_active=False)
                current_session.is_active = True
                current_session.save()
            
            student = Student(
                name=request.POST.get('name'),
                student_class=request.POST.get('class'),
                section=request.POST.get('section'),
                transport=request.POST.get('transport'),
                address1=request.POST.get('address1'),
                address2=request.POST.get('address2', ''),
                city=request.POST.get('city'),
                mobile=request.POST.get('mobile'),
                gender=request.POST.get('gender'),
                religion=request.POST.get('religion'),
                dob=request.POST.get('dob'),
                admission_date=request.POST.get('admissionDate'),
                reg_number=request.POST.get('regNumber'),
                session=session_name,
                character_cert=request.POST.get('character_cert') == 'Yes',
                report_card=request.POST.get('report_card') == 'Yes',
                dob_cert=request.POST.get('dob_cert') == 'Yes',
                last_school=request.POST.get('lastSchool', ''),
                marks=request.POST.get('marks') or None,
                exam_result=request.POST.get('examResult', ''),
                father_name=request.POST.get('fatherName'),
                father_mobile=request.POST.get('fatherMobile'),
                father_email=request.POST.get('fatherEmail', ''),
                father_occupation=request.POST.get('fatherOccupation', ''),
                father_qualification=request.POST.get('fatherQualification', ''),
                father_dob=request.POST.get('fatherDob') or None,
                father_citizen=request.POST.get('fatherCitizen', ''),
                mother_name=request.POST.get('motherName'),
                mother_mobile=request.POST.get('motherMobile', ''),
                mother_occupation=request.POST.get('motherOccupation', ''),
                mother_qualification=request.POST.get('motherQualification', ''),
                mother_dob=request.POST.get('motherDob') or None,
                mother_citizen=request.POST.get('motherCitizen', ''),
                old_balance=request.POST.get('oldBalance') or 0,
            )
            student.save()
            messages.success(request, 'Student admission submitted successfully!')
            return redirect('students')
        except Exception as e:
            messages.error(request, f'Error submitting admission: {str(e)}')
    
    sessions = Session.objects.all().order_by('-start_date')
    current_session = Session.get_current_session()
    classes = list(Student.objects.values_list('student_class', flat=True).distinct().order_by('student_class'))
    
    context = {
        'is_edit': False,
        'sessions': sessions,
        'current_session': current_session,
        'classes': classes
    }
    return render(request, 'students.html', context)

def students(request):
    # Get session filter from request
    session_filter = request.GET.get('session', '')
    
    # Get current active session
    current_session = Session.get_current_session()
    
    # If no session filter specified, use current active session
    if not session_filter and current_session:
        session_filter = current_session.name
    
    if session_filter:
        students = Student.objects.filter(session=session_filter)
    else:
        students = Student.objects.all()
    
    # Get all available sessions for filter dropdown
    sessions = Session.objects.all().order_by('-start_date')
    
    # Get unique classes from students
    classes = Student.objects.values_list('student_class', flat=True).distinct().order_by('student_class')
    
    context = {
        'students': students,
        'sessions': sessions,
        'current_session': current_session,
        'selected_session': session_filter,
        'classes': classes
    }
    return render(request, 'studentlist.html', context)

def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'student_dashboard.html', {'student': student})

def studentlist(request):
    # Get session filter from request
    session_filter = request.GET.get('session', '')
    
    # Get current active session
    current_session = Session.get_current_session()
    
    # If no session filter specified, use current active session
    if not session_filter and current_session:
        session_filter = current_session.name
    
    if session_filter:
        students = Student.objects.filter(session=session_filter)
    else:
        students = Student.objects.all()
    
    # Get all available sessions for filter dropdown
    sessions = Session.objects.all().order_by('-start_date')
    
    context = {
        'students': students,
        'sessions': sessions,
        'current_session': current_session,
        'selected_session': session_filter
    }
    return render(request, 'studentlist.html', context)

@permission_required('can_view_teachers')
def teachers(request):
    if request.method == 'POST':
        try:
            # Validate required fields
            name = request.POST.get('name')
            designation = request.POST.get('designation')
            phone_number = request.POST.get('phone_number')
            email = request.POST.get('email')
            address = request.POST.get('address')
            joining_date = request.POST.get('joining_date')
            
            if not all([name, designation, phone_number, email, address, joining_date]):
                return JsonResponse({'success': False, 'error': 'All required fields must be filled'})
            
            # Handle teacher creation
            teacher = Teacher.objects.create(
                name=name,
                designation=designation,
                phone_number=phone_number,
                email=email,
                address=address,
                gender=request.POST.get('gender', 'Male'),
                joining_date=joining_date,
                qualification=request.POST.get('qualification', ''),
                is_active=bool(request.POST.get('is_active'))
            )
            
            # Handle photo upload
            if 'photo' in request.FILES:
                teacher.photo = request.FILES['photo']
                teacher.save()
            
            # Handle class and subject assignments if provided
            from .forms import TeacherAssignmentForm
            assignment_form = TeacherAssignmentForm(request.POST, teacher=teacher)
            if assignment_form.is_valid():
                assignments_data = assignment_form.get_assignments_data()
                if assignments_data:
                    teacher.assign_classes_subjects(assignments_data)
            
            return JsonResponse({
                'success': True,
                'message': 'Teacher added successfully with assignments',
                'teacher_id': teacher.id
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    # GET request - show teachers list with class filtering
    class_filter = request.GET.get('class', '')
    
    if class_filter:
        # Filter teachers who teach the selected class
        teacher_ids = TeacherClassSubject.objects.filter(class_name=class_filter, is_active=True).values_list('teacher_id', flat=True).distinct()
        teachers = Teacher.objects.filter(id__in=teacher_ids).order_by('name')
    else:
        teachers = Teacher.objects.all().order_by('name')
    
    # Add assignments to each teacher
    for teacher in teachers:
        assignments = TeacherClassSubject.objects.filter(teacher=teacher, is_active=True).select_related('subject')
        teacher.assignments = assignments
        # Also add assignment summary for display
        teacher.assignment_summary = teacher.get_all_assignments()
    
    # Get all unique classes for filter dropdown from TeacherClassSubject
    all_classes = TeacherClassSubject.objects.filter(is_active=True).values_list('class_name', flat=True).distinct().order_by('class_name')
    
    school_info = SchoolDetail.get_current_school()
    
    return render(request, 'teachers.html', {
        'teachers': teachers,
        'school_info': school_info,
        'all_classes': all_classes,
        'selected_class': class_filter,
    })

def teacher_view(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    school_info = SchoolDetail.get_current_school()
    
    # Get teacher's class-subject assignments
    assignments = TeacherClassSubject.objects.filter(teacher=teacher).select_related('subject').order_by('class_name', 'subject__name')
    
    return render(request, 'teacher_detail.html', {
        'teacher': teacher, 
        'school_info': school_info,
        'assignments': assignments
    })

def teacher_edit(request, teacher_id):
    from .forms import TeacherAssignmentForm
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    if request.method == 'POST':
        # Update basic teacher information
        teacher.name = request.POST.get('name')
        teacher.designation = request.POST.get('designation')
        teacher.phone_number = request.POST.get('phone_number')
        teacher.email = request.POST.get('email')
        teacher.address = request.POST.get('address')
        teacher.qualification = request.POST.get('qualification', '')
        teacher.save()
        
        # Handle assignment form
        assignment_form = TeacherAssignmentForm(request.POST, teacher=teacher)
        if assignment_form.is_valid():
            assignments_data = assignment_form.get_assignments_data()
            teacher.assign_classes_subjects(assignments_data)
            messages.success(request, 'Teacher information and assignments updated successfully!')
        else:
            messages.error(request, 'Error updating assignments. Please check the form.')
        
        return redirect('teachers')
    
    # GET request - prepare context
    assignment_form = TeacherAssignmentForm(teacher=teacher)
    
    return render(request, 'teacher_edit.html', {
        'teacher': teacher,
        'assignment_form': assignment_form
    })

@csrf_exempt
def teacher_delete(request, teacher_id):
    if request.method == 'POST':
        teacher = get_object_or_404(Teacher, id=teacher_id)
        teacher.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def teacher_assignment(request, teacher_id):
    """Assign multiple classes and subjects to a teacher"""
    from .forms import TeacherAssignmentForm
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    if request.method == 'POST':
        form = TeacherAssignmentForm(request.POST, teacher=teacher)
        if form.is_valid():
            assignments_data = form.get_assignments_data()
            teacher.assign_classes_subjects(assignments_data)
            messages.success(request, f'Successfully assigned classes and subjects to {teacher.name}')
            return redirect('teachers')
    else:
        form = TeacherAssignmentForm(teacher=teacher)
    
    return render(request, 'teacher_assignment.html', {
        'teacher': teacher,
        'form': form
    })

def classes(request):
    return render(request, 'classes.html')

@permission_required('can_view_reports')
def reports(request):
    # Get statistics
    total_exams = Exam.objects.count()
    total_subjects = Subject.objects.count()
    total_marksheets = Marksheet.objects.count()
    
    # Get recent exams
    recent_exams = Exam.objects.order_by('-exam_date')[:5]
    
    # Get all students for marks entry
    students = Student.objects.all().order_by('name')
    
    # Get all exams for marks entry
    exams = Exam.objects.all().order_by('-exam_date')
    
    # Get all subjects for marks entry
    subjects = Subject.objects.all().order_by('class_name', 'name')
    
    # Get available classes from Student model CLASS_CHOICES and actual database classes
    predefined_classes = [choice[0] for choice in Student.CLASS_CHOICES]
    actual_classes = list(Student.objects.values_list('student_class', flat=True).distinct().order_by('student_class'))
    # Combine and remove duplicates while preserving order
    available_classes = list(dict.fromkeys(predefined_classes + actual_classes))
    
    # Get class statistics
    class_name_mapping = {
        '1st': 'One',
        '2nd': 'Two',
        '3rd': 'Three',
        '4th': 'Four',
        '5th': 'Five',
        '6th': 'Six',
        '7th': 'Seven',
        '8th': 'Eight',
        '9th': 'Nine',
        '10th': 'Ten',
        '11th': 'Eleven',
        '12th': 'Twelve'
    }
    
    class_data = []
    for class_name in available_classes:
        student_count = Student.objects.filter(student_class=class_name).count()
        subject_count = Subject.objects.filter(class_name=class_name).count()
        display_name = class_name_mapping.get(class_name, class_name)
        class_data.append({
            'name': display_name,
            'student_count': student_count,
            'subject_count': subject_count
        })
    
    # Get comprehensive Nepali date and session info
    nepali_info = get_comprehensive_nepali_info()
    nepali_months = get_nepali_months_list()
    
    # Generate Nepali year sessions for dropdown
    nepali_sessions = NepaliCalendar.get_nepali_year_sessions(2082, 2100)
    
    context = {
        'total_exams': total_exams,
        'total_subjects': total_subjects,
        'total_marksheets': total_marksheets,
        'recent_exams': recent_exams,
        'students': students,
        'exams': exams,
        'subjects': subjects,
        'available_classes': available_classes,
        'class_data': class_data,
        'nepali_info': nepali_info,
        'current_nepali_date': nepali_info['formatted_full'],
        'current_nepali_session': nepali_info['session'],
        'nepali_fiscal_year': nepali_info['fiscal_year'],
        'nepali_months': nepali_months,
        'nepali_sessions': nepali_sessions,
        'nepali_weekday': nepali_info['weekday']['name_english'],
    }
    
    return render(request, 'reports.html', context)

@permission_required('can_view_fees')
def fees(request):
    if request.method == 'POST':
        try:
            # Save fee structure data using update_or_create
            for i in range(len(request.POST.getlist('class_name'))):
                class_name = request.POST.getlist('class_name')[i]
                FeeStructure.objects.update_or_create(
                    class_name=class_name,
                    defaults={
                        'admission_fee': float(request.POST.getlist('admission_fee')[i].replace('Rs.', '').replace(',', '')),
                        'monthly_fee': float(request.POST.getlist('monthly_fee')[i].replace('Rs.', '').replace(',', '')),
                        'tuition_fee': float(request.POST.getlist('tuition_fee')[i].replace('Rs.', '').replace(',', '')),
                        'examination_fee': float(request.POST.getlist('examination_fee')[i].replace('Rs.', '').replace(',', '')),
                        'library_fee': float(request.POST.getlist('library_fee')[i].replace('Rs.', '').replace(',', '')),
                        'sports_fee': float(request.POST.getlist('sports_fee')[i].replace('Rs.', '').replace(',', '')),
                        'laboratory_fee': float(request.POST.getlist('laboratory_fee')[i].replace('Rs.', '').replace(',', '')),
                        'computer_fee': float(request.POST.getlist('computer_fee')[i].replace('Rs.', '').replace(',', '')),
                        'transportation_fee': float(request.POST.getlist('transportation_fee')[i].replace('Rs.', '').replace(',', ''))
                    }
                )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    # GET request - load existing data
    fee_structures = FeeStructure.objects.all()
    
    context = {
        'fee_structures': fee_structures,
    }
    
    return render(request, 'fee_structure.html', context)

def pay(request):
    students = Student.objects.all()
    
    # Get default class (1) or first available class
    default_class = '1'
    try:
        fee_structure = FeeStructure.objects.get(class_name=default_class)
    except FeeStructure.DoesNotExist:
        fee_structure = FeeStructure.objects.first()
        if not fee_structure:
            # Create default fee structure for class 1 if none exists
            fee_structure = FeeStructure.objects.create(
                class_name=default_class,
                admission_fee=5000,
                monthly_fee=2500,
                tuition_fee=2000,
                examination_fee=1000,
                library_fee=500,
                sports_fee=800,
                laboratory_fee=1200,
                computer_fee=1500,
                transportation_fee=1500,
            )
    
    # Create fee headings from FeeStructure model fields
    if fee_structure:
        fee_headings = [
            {'field': 'admission_fee', 'name': 'Admission Fee', 'value': float(fee_structure.admission_fee)},
            {'field': 'monthly_fee', 'name': 'Monthly Fee', 'value': float(fee_structure.monthly_fee)},
            {'field': 'tuition_fee', 'name': 'Tuition Fee', 'value': float(fee_structure.tuition_fee)},
            {'field': 'examination_fee', 'name': 'Examination Fee', 'value': float(fee_structure.examination_fee)},
            {'field': 'library_fee', 'name': 'Library Fee', 'value': float(fee_structure.library_fee)},
            {'field': 'sports_fee', 'name': 'Sports Fee', 'value': float(fee_structure.sports_fee)},
            {'field': 'laboratory_fee', 'name': 'Laboratory Fee', 'value': float(fee_structure.laboratory_fee)},
            {'field': 'computer_fee', 'name': 'Computer Fee', 'value': float(fee_structure.computer_fee)},
            {'field': 'transportation_fee', 'name': 'Transportation Fee', 'value': float(fee_structure.transportation_fee)},
        ]
    else:
        # Fallback fee headings with default values
        fee_headings = [
            {'field': 'admission_fee', 'name': 'Admission Fee', 'value': 5000},
            {'field': 'monthly_fee', 'name': 'Monthly Fee', 'value': 2500},
            {'field': 'tuition_fee', 'name': 'Tuition Fee', 'value': 2000},
            {'field': 'examination_fee', 'name': 'Examination Fee', 'value': 1000},
            {'field': 'library_fee', 'name': 'Library Fee', 'value': 500},
            {'field': 'sports_fee', 'name': 'Sports Fee', 'value': 800},
            {'field': 'laboratory_fee', 'name': 'Laboratory Fee', 'value': 1200},
            {'field': 'computer_fee', 'name': 'Computer Fee', 'value': 1500},
            {'field': 'transportation_fee', 'name': 'Transportation Fee', 'value': 1500},
        ]
    
    return render(request, 'pay.html', {
        'students': students,
        'fee_headings': fee_headings,
        'selected_class': default_class
    })

def pay_new(request):
    """New improved pay page with student selection"""
    fee_structures = FeeStructure.objects.all()
    students = Student.objects.all().order_by('name')
    
    # Serialize fee structures for JavaScript
    fee_structures_json = []
    for fs in fee_structures:
        fee_structures_json.append({
            'class_name': fs.class_name,
            'admission_fee': float(fs.admission_fee),
            'monthly_fee': float(fs.monthly_fee),
            'tuition_fee': float(fs.tuition_fee),
            'examination_fee': float(fs.examination_fee),
            'library_fee': float(fs.library_fee),
            'sports_fee': float(fs.sports_fee),
            'laboratory_fee': float(fs.laboratory_fee),
            'computer_fee': float(fs.computer_fee),
            'transportation_fee': float(fs.transportation_fee),
        })
    
    return render(request, 'pay_new.html', {
        'fee_structures': json.dumps(fee_structures_json),
        'students': students
    })

def pay_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    # Get fee structure for student's class
    try:
        student_fee_structure = FeeStructure.objects.get(class_name=student.student_class)
        print(f"Found fee structure for class {student.student_class}")
    except FeeStructure.DoesNotExist:
        print(f"No fee structure found for class {student.student_class}")
        student_fee_structure = None
    
    # Create fee headings from student's class fee structure
    if student_fee_structure:
        fee_headings = [
            {'field': 'admission_fee', 'name': 'Admission Fee', 'value': float(student_fee_structure.admission_fee)},
            {'field': 'monthly_fee', 'name': 'Monthly Fee', 'value': float(student_fee_structure.monthly_fee)},
            {'field': 'tuition_fee', 'name': 'Tuition Fee', 'value': float(student_fee_structure.tuition_fee)},
            {'field': 'examination_fee', 'name': 'Examination Fee', 'value': float(student_fee_structure.examination_fee)},
            {'field': 'library_fee', 'name': 'Library Fee', 'value': float(student_fee_structure.library_fee)},
            {'field': 'sports_fee', 'name': 'Sports Fee', 'value': float(student_fee_structure.sports_fee)},
            {'field': 'laboratory_fee', 'name': 'Laboratory Fee', 'value': float(student_fee_structure.laboratory_fee)},
            {'field': 'computer_fee', 'name': 'Computer Fee', 'value': float(student_fee_structure.computer_fee)},
            {'field': 'transportation_fee', 'name': 'Transportation Fee', 'value': float(student_fee_structure.transportation_fee)},
        ]
        print(f"Created {len(fee_headings)} fee headings from database")
    else:
        # Create default fee structure for this class if it doesn't exist
        FeeStructure.objects.get_or_create(
            class_name=student.student_class,
            defaults={
                'admission_fee': 5000,
                'monthly_fee': 2500,
                'tuition_fee': 2000,
                'examination_fee': 1000,
                'library_fee': 500,
                'sports_fee': 800,
                'laboratory_fee': 1200,
                'computer_fee': 1500,
                'transportation_fee': 1500,
            }
        )
        # Fallback fee headings with default values
        fee_headings = [
            {'field': 'admission_fee', 'name': 'Admission Fee', 'value': 5000},
            {'field': 'monthly_fee', 'name': 'Monthly Fee', 'value': 2500},
            {'field': 'tuition_fee', 'name': 'Tuition Fee', 'value': 2000},
            {'field': 'examination_fee', 'name': 'Examination Fee', 'value': 1000},
            {'field': 'library_fee', 'name': 'Library Fee', 'value': 500},
            {'field': 'sports_fee', 'name': 'Sports Fee', 'value': 800},
            {'field': 'laboratory_fee', 'name': 'Laboratory Fee', 'value': 1200},
            {'field': 'computer_fee', 'name': 'Computer Fee', 'value': 1500},
            {'field': 'transportation_fee', 'name': 'Transportation Fee', 'value': 1500},
        ]
        print(f"Created {len(fee_headings)} fallback fee headings")
    
    # Get paid months and calculate balance
    paid_fee_months = {}
    total_balance = 0
    payments = FeePayment.objects.filter(student=student)
    
    for payment in payments:
        fee_types = json.loads(payment.fee_types)
        for fee_data in fee_types:
            fee_type = fee_data['type']
            months = fee_data['months']
            if fee_type not in paid_fee_months:
                paid_fee_months[fee_type] = months
            else:
                paid_fee_months[fee_type] += months
        total_balance += payment.balance
    
    # Get student daily expenses
    daily_expenses = StudentDailyExpense.objects.filter(student=student)
    daily_expenses_data = []
    for expense in daily_expenses:
        daily_expenses_data.append({
            'id': expense.id,
            'description': expense.description,
            'amount': float(expense.amount),
            'date': expense.expense_date.strftime('%Y-%m-%d')
        })
    
    context = {
        'student': student,
        'student_id': f'STU{student.id:03d}',
        'reg_number': student.reg_number,
        'fee_headings': fee_headings,
        'paid_fee_months': json.dumps(paid_fee_months),
        'student_balance': total_balance,
        'selected_class': student.student_class,
        'daily_expenses': daily_expenses_data
    }
    return render(request, 'pay.html', context)

def events(request):
    return render(request, 'events.html')

def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        try:
            # Update student with form data
            student.name = request.POST.get('name')
            student.student_class = request.POST.get('class')
            student.section = request.POST.get('section')
            student.transport = request.POST.get('transport')
            student.address1 = request.POST.get('address1')
            student.address2 = request.POST.get('address2', '')
            student.city = request.POST.get('city')
            student.mobile = request.POST.get('mobile')
            student.gender = request.POST.get('gender')
            student.religion = request.POST.get('religion')
            student.dob = request.POST.get('dob')
            student.admission_date = request.POST.get('admissionDate')
            student.reg_number = request.POST.get('regNumber')
            student.session = request.POST.get('session')
            student.character_cert = request.POST.get('character_cert') == 'Yes'
            student.report_card = request.POST.get('report_card') == 'Yes'
            student.dob_cert = request.POST.get('dob_cert') == 'Yes'
            student.last_school = request.POST.get('lastSchool', '')
            student.marks = request.POST.get('marks') or None
            student.exam_result = request.POST.get('examResult', '')
            student.father_name = request.POST.get('fatherName')
            student.father_mobile = request.POST.get('fatherMobile')
            student.father_email = request.POST.get('fatherEmail', '')
            student.father_occupation = request.POST.get('fatherOccupation', '')
            student.father_qualification = request.POST.get('fatherQualification', '')
            student.father_dob = request.POST.get('fatherDob') or None
            student.father_citizen = request.POST.get('fatherCitizen', '')
            student.mother_name = request.POST.get('motherName')
            student.mother_mobile = request.POST.get('motherMobile', '')
            student.mother_occupation = request.POST.get('motherOccupation', '')
            student.mother_qualification = request.POST.get('motherQualification', '')
            student.mother_dob = request.POST.get('motherDob') or None
            student.mother_citizen = request.POST.get('motherCitizen', '')
            student.old_balance = request.POST.get('oldBalance') or 0
            
            student.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('studentlist')
        except Exception as e:
            messages.error(request, f'Error updating student: {str(e)}')
    
    # Get available classes for the form
    classes = list(Student.objects.values_list('student_class', flat=True).distinct().order_by('student_class'))
    sessions = Session.objects.all().order_by('-start_date')
    
    return render(request, 'students.html', {
        'student': student, 
        'is_edit': True,
        'classes': classes,
        'sessions': sessions
    })

def download_template(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_template.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Name', 'Father Name', 'Mother Name', 'Class', 'Section', 'Gender', 
        'Mobile', 'Father Mobile', 'Mother Mobile', 'Address1', 'Address2', 
        'City', 'Religion', 'DOB', 'Admission Date', 'Session', 'Transport',
        'Registration Number', 'Father Email', 'Father Occupation', 
        'Father Qualification', 'Mother Occupation', 'Mother Qualification', 
        'Old Balance'
    ])
    
    # Add sample data row
    writer.writerow([
        'John Doe', 'Robert Doe', 'Jane Doe', 'Nursery', 'A', 'Boy',
        '9876543210', '9876543211', '9876543212', '123 Main St', 'Apt 4B',
        'Kathmandu', 'Hindu', '2020-01-15', '2024-01-01', '2024-25', '00_No Transport Service | 0 Rs.',
        'REG2024001', 'robert@email.com', 'Engineer', 'Bachelor',
        'Teacher', 'Master', '0'
    ])
    
    return response

def download_csv(request):
    from django.db.models import Sum
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fee_receipt_book.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'S.No', 'Student ID', 'Name', 'Class', 'Section', 'Roll Number',
        'Total Fee', 'Amount Paid', 'Amount Pending', 'Payment Status',
        'Last Payment Date', 'Father Name', 'Mobile', 'Paid Months'
    ])
    
    students = Student.objects.annotate(
        total_paid=Sum('feepayment__payment_amount'),
        last_payment_date=Max('feepayment__payment_date')
    ).order_by('name')
    
    for index, student in enumerate(students, 1):
        # Calculate total fee
        try:
            fee_structure = FeeStructure.objects.get(class_name=student.student_class)
            total_fee = (
                float(fee_structure.admission_fee) +
                float(fee_structure.monthly_fee) * 12 +
                float(fee_structure.tuition_fee) * 12 +
                float(fee_structure.examination_fee) +
                float(fee_structure.library_fee) +
                float(fee_structure.sports_fee) +
                float(fee_structure.laboratory_fee) +
                float(fee_structure.computer_fee) +
                float(fee_structure.transportation_fee) * 12
            )
        except FeeStructure.DoesNotExist:
            total_fee = 5000 + (2500 * 12) + (2000 * 12) + 1000 + 500 + 800 + 1200 + 1500 + (1500 * 12)
        
        paid_amount = student.total_paid or 0
        pending_amount = max(0, total_fee - paid_amount)
        payment_status = 'Paid' if pending_amount == 0 else 'Pending'
        
        # Get paid months
        payments = FeePayment.objects.filter(student=student)
        paid_months = set()
        for payment in payments:
            if payment.selected_months:
                try:
                    months = json.loads(payment.selected_months)
                    paid_months.update(months)
                except json.JSONDecodeError:
                    pass
        
        writer.writerow([
            index,
            f'STU{student.id:03d}',
            student.name,
            student.student_class,
            student.section,
            student.reg_number,
            f'Rs.{total_fee:,.2f}',
            f'Rs.{paid_amount:,.2f}',
            f'Rs.{pending_amount:,.2f}',
            payment_status,
            student.last_payment_date.strftime('%Y-%m-%d') if student.last_payment_date else 'No payments',
            student.father_name,
            student.mobile,
            ', '.join(sorted(paid_months)) if paid_months else 'None'
        ])
    
    return response

def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            return JsonResponse({'success': False, 'error': 'No file uploaded'})
        
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({'success': False, 'error': 'Please upload a CSV file'})
        
        try:
            # Handle different encodings
            try:
                decoded_file = csv_file.read().decode('utf-8')
            except UnicodeDecodeError:
                csv_file.seek(0)
                decoded_file = csv_file.read().decode('utf-8-sig')
            
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            created_count = 0
            errors = []
            
            for row_num, row in enumerate(reader, start=2):
                try:
                    # Skip empty rows
                    if not any(row.values()):
                        continue
                    
                    # Validate required fields
                    name = row.get('Name', '').strip()
                    if not name:
                        errors.append(f'Row {row_num}: Name is required')
                        continue
                    
                    father_name = row.get('Father Name', '').strip()
                    if not father_name:
                        errors.append(f'Row {row_num}: Father Name is required')
                        continue
                    
                    # Generate unique registration number if not provided
                    reg_number = row.get('Registration Number', '').strip()
                    if not reg_number:
                        reg_number = f'REG{datetime.now().year}{created_count+1:04d}'
                    
                    # Check if registration number already exists
                    if Student.objects.filter(reg_number=reg_number).exists():
                        reg_number = f'REG{datetime.now().year}{Student.objects.count()+created_count+1:04d}'
                    
                    # Validate and set defaults
                    student_class = row.get('Class', 'Nursery').strip()
                    section = row.get('Section', 'A').strip()
                    gender = row.get('Gender', 'Boy').strip()
                    religion = row.get('Religion', 'Hindu').strip()
                    
                    # Parse dates
                    dob = row.get('DOB', '2000-01-01').strip()
                    admission_date = row.get('Admission Date', datetime.now().strftime('%Y-%m-%d')).strip()
                    
                    # Always use current active session for consistency
                    current_session = Session.get_current_session()
                    if not current_session:
                        current_session, created = Session.objects.get_or_create(
                            name='2024-25',
                            defaults={
                                'start_date': '2024-04-01',
                                'end_date': '2025-03-31',
                                'is_active': True
                            }
                        )
                    session_name = current_session.name
                    
                    # Create student with proper field mapping
                    student = Student.objects.create(
                        name=name,
                        student_class=student_class,
                        section=section,
                        mobile=row.get('Mobile', '9999999999').strip()[:10],
                        father_name=father_name,
                        mother_name=row.get('Mother Name', '').strip(),
                        reg_number=reg_number,
                        transport=row.get('Transport', '00_No Transport Service | 0 Rs.').strip(),
                        address1=row.get('Address1', 'N/A').strip(),
                        address2=row.get('Address2', '').strip(),
                        city=row.get('City', 'N/A').strip(),
                        gender=gender,
                        religion=religion,
                        dob=dob,
                        admission_date=admission_date,
                        session=session_name,
                        father_mobile=row.get('Father Mobile', '9999999999').strip()[:10],
                        mother_mobile=row.get('Mother Mobile', '').strip()[:10] if row.get('Mother Mobile', '').strip() else '',
                        father_email=row.get('Father Email', '').strip(),
                        father_occupation=row.get('Father Occupation', '').strip(),
                        father_qualification=row.get('Father Qualification', '').strip(),
                        mother_occupation=row.get('Mother Occupation', '').strip(),
                        mother_qualification=row.get('Mother Qualification', '').strip(),
                        old_balance=float(row.get('Old Balance', 0) or 0)
                    )
                    created_count += 1
                except Exception as e:
                    errors.append(f'Row {row_num}: {str(e)}')
            
            if created_count > 0:
                message = f'Successfully imported {created_count} students'
                if errors:
                    message += f'. {len(errors)} rows had errors.'
                return JsonResponse({'success': True, 'message': message, 'errors': errors[:5]})
            else:
                return JsonResponse({'success': False, 'error': 'No valid student records found in CSV'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Error processing CSV: {str(e)}'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def delete_student(request, student_id):
    if request.method == 'POST':
        try:
            student = get_object_or_404(Student, id=student_id)
            student.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def bulk_delete_students(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_ids = data.get('student_ids', [])
            deleted_count = Student.objects.filter(id__in=student_ids).delete()[0]
            return JsonResponse({'success': True, 'deleted_count': deleted_count})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def get_fee_structure(request, class_name):
    try:
        fee_structure = FeeStructure.objects.get(class_name=class_name)
        return JsonResponse({
            'success': True,
            'data': {
                'admission_fee': float(fee_structure.admission_fee),
                'monthly_fee': float(fee_structure.monthly_fee),
                'tuition_fee': float(fee_structure.tuition_fee),
                'examination_fee': float(fee_structure.examination_fee),
                'library_fee': float(fee_structure.library_fee),
                'sports_fee': float(fee_structure.sports_fee),
                'laboratory_fee': float(fee_structure.laboratory_fee),
                'computer_fee': float(fee_structure.computer_fee),
                'transportation_fee': float(fee_structure.transportation_fee)
            }
        })
    except FeeStructure.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Fee structure not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def search_student_page(request):
    return render(request, 'search_student.html')

def search_student_api(request):
    try:
        # Get search parameters
        query = request.GET.get('q', '').strip()
        name = request.GET.get('name', '').strip()
        student_class = request.GET.get('class', '').strip()
        section = request.GET.get('section', '').strip()
        reg_number = request.GET.get('reg', '').strip()
        
        # Build query conditions
        conditions = models.Q()
        
        # Quick search (backward compatibility)
        if query:
            # Try to find by ID format (STU001)
            if query.upper().startswith('STU'):
                try:
                    student_id = int(query[3:])  # Extract number after STU
                    conditions |= models.Q(id=student_id)
                except ValueError:
                    pass
            
            # Add other search conditions
            conditions |= models.Q(reg_number__icontains=query)
            conditions |= models.Q(name__icontains=query)
            conditions |= models.Q(student_class__icontains=query)
            conditions |= models.Q(father_name__icontains=query)
        
        # Advanced search
        if name:
            if conditions:
                conditions &= models.Q(name__icontains=name)
            else:
                conditions = models.Q(name__icontains=name)
        if student_class:
            if conditions:
                conditions &= models.Q(student_class=student_class)
            else:
                conditions = models.Q(student_class=student_class)
        if section:
            if conditions:
                conditions &= models.Q(section=section)
            else:
                conditions = models.Q(section=section)
        if reg_number:
            if conditions:
                conditions &= models.Q(reg_number__icontains=reg_number)
            else:
                conditions = models.Q(reg_number__icontains=reg_number)
        
        # If no search criteria provided, return all students (limited)
        if not any([query, name, student_class, section, reg_number]):
            students = Student.objects.all().order_by('name')[:20]
        else:
            # Execute search
            students = Student.objects.filter(conditions).order_by('name')[:20]  # Limit to 20 results
        
        if students:
            students_data = []
            for student in students:
                students_data.append({
                    'id': student.id,
                    'name': student.name,
                    'reg_number': student.reg_number,
                    'student_class': student.student_class,
                    'section': student.section,
                    'father_name': student.father_name
                })
            
            # For backward compatibility, if only one result and it's a quick search, return single student
            if len(students_data) == 1 and query and not any([name, student_class, section, reg_number]):
                return JsonResponse({
                    'success': True,
                    'student': students_data[0],
                    'students': students_data
                })
            else:
                return JsonResponse({
                    'success': True,
                    'students': students_data
                })
        else:
            # Check if there are any students in the database at all
            total_students = Student.objects.count()
            if total_students == 0:
                return JsonResponse({'success': False, 'error': 'No students found in database. Please add students first.'})
            else:
                return JsonResponse({'success': False, 'error': f'No students found matching search criteria. Total students in database: {total_students}'})
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def submit_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student = get_object_or_404(Student, id=data['student_id'])
            
            # Parse cheque_date if provided
            cheque_date = None
            if data.get('cheque_date'):
                try:
                    cheque_date = datetime.strptime(data['cheque_date'], '%Y-%m-%d').date()
                except ValueError:
                    pass

            # Parse fee types and months
            fee_types = json.loads(data['fee_types'])
            selected_months = json.loads(data['selected_months'])
            custom_fees = json.loads(data.get('custom_fees', '[]'))
            
            payment_ids = []
            
            # Create separate payment record for each fee type with appropriate months
            for fee_type in fee_types:
                # One-time fees don't need months
                one_time_fees = ['admission_fee', 'examination_fee', 'library_fee', 'sports_fee', 'laboratory_fee', 'computer_fee']
                fee_months = [] if fee_type['type'] in one_time_fees else selected_months
                
                payment = FeePayment.objects.create(
                    student=student,
                    selected_months=json.dumps(fee_months),
                    fee_types=json.dumps([fee_type]),
                    custom_fees='[]',
                    total_fee=fee_type.get('total', fee_type.get('amount', 0)),
                    payment_amount=fee_type.get('total', fee_type.get('amount', 0)),
                    balance=0,
                    payment_method=data['payment_method'],
                    bank_name=data.get('bank_name', ''),
                    cheque_dd_no=data.get('cheque_dd_no', ''),
                    cheque_date=cheque_date,
                    remarks=data.get('remarks', ''),
                    sms_sent=data.get('sms_sent', False),
                    whatsapp_sent=data.get('whatsapp_sent', False)
                )
                payment_ids.append(payment.id)
            
            # Create separate payment records for custom fees
            for custom_fee in custom_fees:
                payment = FeePayment.objects.create(
                    student=student,
                    selected_months='[]',
                    fee_types='[]',
                    custom_fees=json.dumps([custom_fee]),
                    total_fee=custom_fee['amount'],
                    payment_amount=custom_fee['amount'],
                    balance=0,
                    payment_method=data['payment_method'],
                    bank_name=data.get('bank_name', ''),
                    cheque_dd_no=data.get('cheque_dd_no', ''),
                    cheque_date=cheque_date,
                    remarks=data.get('remarks', ''),
                    sms_sent=data.get('sms_sent', False),
                    whatsapp_sent=data.get('whatsapp_sent', False)
                )
                payment_ids.append(payment.id)
            
            # Update admission status if admission fee is paid
            for fee_type in fee_types:
                if fee_type['type'] == 'admission_fee':
                    student.admission_paid = True
                    student.save()
                    break
            
            # Record paid daily expenses as FeePayment entries and delete from StudentDailyExpense
            daily_expenses = json.loads(data.get('daily_expenses', '[]'))
            if daily_expenses:
                for expense in daily_expenses:
                    # Create FeePayment record for daily expense
                    FeePayment.objects.create(
                        student=student,
                        selected_months='[]',
                        fee_types='[]',
                        custom_fees=json.dumps([{'name': expense['description'], 'amount': expense['amount']}]),
                        total_fee=expense['amount'],
                        payment_amount=expense['amount'],
                        balance=0,
                        payment_method=data['payment_method'],
                        bank_name=data.get('bank_name', ''),
                        cheque_dd_no=data.get('cheque_dd_no', ''),
                        cheque_date=cheque_date,
                        remarks=f"Daily Expense: {expense['description']}",
                        sms_sent=data.get('sms_sent', False),
                        whatsapp_sent=data.get('whatsapp_sent', False)
                    )
                
                # Delete paid daily expenses
                expense_ids = [expense['id'] for expense in daily_expenses]
                StudentDailyExpense.objects.filter(id__in=expense_ids).delete()
            
            return JsonResponse({'success': True, 'payment_ids': payment_ids, 'daily_expenses_paid': len(daily_expenses) if daily_expenses else 0})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@permission_required('can_view_receipts')
def fee_receipt_book(request):
    from django.db.models import Sum, Max
    from decimal import Decimal
    
    # Get filter parameters
    selected_months = [m.strip() for m in request.GET.get('months', '').split(',') if m.strip()]
    selected_fee_types = [f.strip() for f in request.GET.get('fee_types', '').split(',') if f.strip()]
    
    # Handle search functionality
    search_query = request.GET.get('search', '').strip()
    students_query = Student.objects.all()
    
    if search_query:
        students_query = students_query.filter(
            models.Q(name__icontains=search_query) |
            models.Q(reg_number__icontains=search_query) |
            models.Q(student_class__icontains=search_query) |
            models.Q(father_name__icontains=search_query)
        )
    
    students = students_query.annotate(
        total_paid=Sum('feepayment__payment_amount'),
        last_payment_date=Max('feepayment__payment_date')
    ).order_by('name')
    
    # Get unique classes from students
    available_classes = Student.objects.values_list('student_class', flat=True).distinct().order_by('student_class')
    
    # Calculate statistics
    total_students = students.count()
    total_collected = Decimal('0')
    total_pending = Decimal('0')
    
    # Process each student
    students_with_data = []
    for student in students:
        payments = FeePayment.objects.filter(student=student)
        
        # Calculate total fee for student based on fee structure
        try:
            fee_structure = FeeStructure.objects.get(class_name=student.student_class)
            student_total_fee = (
                fee_structure.admission_fee +
                fee_structure.monthly_fee * 12 +
                fee_structure.tuition_fee * 12 +
                fee_structure.examination_fee +
                fee_structure.library_fee +
                fee_structure.sports_fee +
                fee_structure.laboratory_fee +
                fee_structure.computer_fee +
                fee_structure.transportation_fee * 12
            )
        except FeeStructure.DoesNotExist:
            student_total_fee = Decimal('5000') + (Decimal('2500') * 12) + (Decimal('2000') * 12) + Decimal('1000') + Decimal('500') + Decimal('800') + Decimal('1200') + Decimal('1500') + (Decimal('1500') * 12)
        
        # Calculate paid amount
        student_paid = student.total_paid or Decimal('0')
        
        # Add daily expenses to total fee
        daily_expenses = StudentDailyExpense.objects.filter(student=student).aggregate(
            total_expenses=Sum('amount')
        )['total_expenses'] or Decimal('0')
        
        student_total_fee += daily_expenses
        student_pending = max(Decimal('0'), student_total_fee - student_paid)
        
        # Add to totals
        total_collected += student_paid
        total_pending += student_pending
        
        # Store daily expenses for display
        student.daily_expenses = float(daily_expenses)
        
        # Calculate fee breakdown based on applied filters
        if fee_structure:
            breakdown_parts = []
            
            # Apply fee type filters or show all if none selected
            fee_types_to_show = selected_fee_types if selected_fee_types else ['admission_fee', 'monthly_fee', 'tuition_fee', 'transportation_fee', 'examination_fee', 'library_fee', 'sports_fee', 'laboratory_fee', 'computer_fee']
            
            # Apply month filters for monthly fees
            months_count = len(selected_months) if selected_months else 12
            
            # Calculate components based on filters
            if 'admission_fee' in fee_types_to_show:
                admission_total = int(fee_structure.admission_fee)
                if admission_total > 0: breakdown_parts.append(f"Admission: Rs{admission_total:,}")
            
            if 'monthly_fee' in fee_types_to_show:
                monthly_total = int(fee_structure.monthly_fee * months_count)
                if monthly_total > 0: breakdown_parts.append(f"Monthly: Rs{monthly_total:,} ({months_count}m)")
            
            if 'tuition_fee' in fee_types_to_show:
                tuition_total = int(fee_structure.tuition_fee * months_count)
                if tuition_total > 0: breakdown_parts.append(f"Tuition: Rs{tuition_total:,} ({months_count}m)")
            
            if 'transportation_fee' in fee_types_to_show:
                transport_total = int(fee_structure.transportation_fee * months_count)
                if transport_total > 0: breakdown_parts.append(f"Transport: Rs{transport_total:,} ({months_count}m)")
            
            # Other fees (not affected by months)
            other_fees = ['examination_fee', 'library_fee', 'sports_fee', 'laboratory_fee', 'computer_fee']
            other_total = 0
            for fee in other_fees:
                if fee in fee_types_to_show:
                    other_total += int(getattr(fee_structure, fee, 0))
            if other_total > 0: breakdown_parts.append(f"Others: Rs{other_total:,}")
            
            student.fee_breakdown_text = " | ".join(breakdown_parts) if breakdown_parts else "No fees selected"
        else:
            student.fee_breakdown_text = "No fee structure found"
        
        # Set student attributes for template
        student.total_fee = float(student_total_fee)
        student.paid_amount = float(student_paid)
        student.pending_amount = float(student_pending)
        student.payment_status = 'paid' if student_pending == 0 else 'pending'
        student.class_name = student.student_class
        student.roll_number = student.reg_number
        student.daily_expenses_total = float(daily_expenses)
        student.email = student.email  # Ensure email is available
        
        # Calculate monthly fee amount (monthly_fee + tuition_fee)
        try:
            fee_structure = FeeStructure.objects.get(class_name=student.student_class)
            monthly_fee_amount = float(fee_structure.monthly_fee) + float(fee_structure.tuition_fee)
        except FeeStructure.DoesNotExist:
            monthly_fee_amount = 4500.0  # 2500 + 2000
        
        # Create fee breakdown with months
        months_data = [
            {'name': 'Baisakh', 'short': 'B', 'paid': False, 'amount': monthly_fee_amount},
            {'name': 'Jestha', 'short': 'J', 'paid': False, 'amount': monthly_fee_amount},
            {'name': 'Ashadh', 'short': 'A', 'paid': False, 'amount': monthly_fee_amount},
            {'name': 'Shrawan', 'short': 'S', 'paid': False, 'amount': monthly_fee_amount},
            {'name': 'Bhadra', 'short': 'B', 'paid': False, 'amount': monthly_fee_amount},
            {'name': 'Ashwin', 'short': 'A', 'paid': False, 'amount': monthly_fee_amount},
            {'name': 'Kartik', 'short': 'K', 'paid': False, 'amount': monthly_fee_amount},
            {'name': 'Mangsir', 'short': 'M', 'paid': False, 'amount': monthly_fee_amount},
            {'name': 'Poush', 'short': 'P', 'paid': False, 'amount': monthly_fee_amount},
            {'name': 'Magh', 'short': 'M', 'paid': False, 'amount': monthly_fee_amount},
            {'name': 'Falgun', 'short': 'F', 'paid': False, 'amount': monthly_fee_amount},
            {'name': 'Chaitra', 'short': 'C', 'paid': False, 'amount': monthly_fee_amount}
        ]
        
        # Mark paid months based on payments
        paid_months = set()
        for payment in payments:
            if payment.selected_months:
                try:
                    months = json.loads(payment.selected_months)
                    paid_months.update(months)
                except json.JSONDecodeError:
                    pass
        
        # Update months data
        month_names = ['Baisakh', 'Jestha', 'Ashadh', 'Shrawan', 'Bhadra', 'Ashwin',
                      'Kartik', 'Mangsir', 'Poush', 'Magh', 'Falgun', 'Chaitra']
        
        for i, month_name in enumerate(month_names):
            if month_name in paid_months or str(i+1) in paid_months:
                months_data[i]['paid'] = True
        
        student.fee_breakdown = [{'months': months_data}]
        
        students_with_data.append(student)
    
    context = {
        'students': students_with_data,
        'total_students': total_students,
        'total_collected': float(total_collected),
        'total_pending': float(total_pending),
        'search_query': search_query,
        'available_classes': available_classes
    }
    
    return render(request, 'fee_receipt_book.html', context)

def student_payments(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    payments = FeePayment.objects.filter(student=student).order_by('-payment_date')
    
    # Process payments for better display
    processed_payments = []
    for payment in payments:
        payment_data = {
            'id': payment.id,
            'payment_date': payment.payment_date,
            'payment_amount': payment.payment_amount,
            'payment_method': payment.payment_method,
            'balance': payment.balance,
            'remarks': payment.remarks,
            'fee_types': [],
            'months': []
        }
        
        # Parse fee types
        if payment.fee_types:
            try:
                fee_types = json.loads(payment.fee_types)
                payment_data['fee_types'] = fee_types
            except json.JSONDecodeError:
                pass
        
        # Parse months
        if payment.selected_months:
            try:
                months = json.loads(payment.selected_months)
                payment_data['months'] = months
            except json.JSONDecodeError:
                pass
        
        processed_payments.append(payment_data)
    
    return render(request, 'student_payments.html', {
        'student': student,
        'payments': processed_payments
    })

def student_payments_api(request, student_id):
    try:
        student = get_object_or_404(Student, id=student_id)
        payments = FeePayment.objects.filter(student=student).order_by('-payment_date')
        
        student_data = {
            'id': student.id,
            'name': student.name,
            'student_class': student.student_class,
            'section': student.section,
            'father_name': student.father_name,
            'mobile': student.mobile
        }
        
        payments_data = []
        for payment in payments:
            payments_data.append({
                'payment_date': payment.payment_date.strftime('%Y-%m-%d'),
                'selected_months': payment.selected_months,
                'payment_amount': float(payment.payment_amount),
                'payment_method': payment.payment_method,
                'balance': float(payment.balance),
                'remarks': payment.remarks
            })
        
        return JsonResponse({
            'success': True,
            'student': student_data,
            'payments': payments_data
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def admission_fee_table(request):
    students = Student.objects.all().order_by('name')
    
    # Add paid months data for each student
    students_with_months = []
    for student in students:
        payments = FeePayment.objects.filter(student=student)
        paid_months = set()
        admission_fee_paid = student.admission_paid
        
        for payment in payments:
            if payment.selected_months:
                try:
                    months = json.loads(payment.selected_months)
                    paid_months.update(months)
                except json.JSONDecodeError:
                    pass
            
            # Check if admission fee was paid in this payment
            if not admission_fee_paid and payment.fee_types:
                try:
                    fee_types = json.loads(payment.fee_types)
                    for fee_type in fee_types:
                        if fee_type.get('type') == 'admission_fee':
                            admission_fee_paid = True
                            break
                except json.JSONDecodeError:
                    pass
        
        student.admission_paid = admission_fee_paid
        student.paid_months = list(paid_months)
        # If at least one month is paid, mark admission as paid
        student.has_monthly_payment = len(paid_months) > 0
        students_with_months.append(student)
    
    return render(request, 'admission_fee_table.html', {'students': students_with_months})

def fee_receipt(request, payment_id):
    payment = get_object_or_404(FeePayment, id=payment_id)
    student = payment.student
    
    # Process payment data for display
    payment_data = {
        'id': payment.id,
        'payment_date': payment.payment_date,
        'payment_amount': payment.payment_amount,
        'payment_method': payment.payment_method,
        'balance': payment.balance,
        'remarks': payment.remarks,
        'bank_name': payment.bank_name,
        'cheque_dd_no': payment.cheque_dd_no,
        'cheque_date': payment.cheque_date,
        'fee_types': [],
        'months': []
    }
    
    # Parse fee types
    if payment.fee_types:
        try:
            fee_types = json.loads(payment.fee_types)
            payment_data['fee_types'] = fee_types
        except json.JSONDecodeError:
            pass
    
    # Parse months
    if payment.selected_months:
        try:
            months = json.loads(payment.selected_months)
            payment_data['months'] = months
        except json.JSONDecodeError:
            pass
    
    # Get Nepali date for payment
    payment_date_nepali = ''
    if payment.payment_date:
        try:
            nepali_date_dict = NepaliCalendar.english_to_nepali_date(payment.payment_date)
            payment_date_nepali = NepaliCalendar.format_nepali_date(nepali_date_dict, 'full_en')
        except:
            pass
    
    context = {
        'student': student,
        'payment': payment_data,
        'current_date': datetime.now().strftime('%B %d, %Y'),
        'payment_date_nepali': payment_date_nepali
    }
    
    return render(request, 'fee_receipt.html', context)

def generate_receipt_pdf(request, payment_id):
    """Generate PDF receipt for a payment"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import inch
        from io import BytesIO
        
        payment = get_object_or_404(FeePayment, id=payment_id)
        student = payment.student
        
        # Create PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Header
        p.setFont("Helvetica-Bold", 20)
        p.drawCentredText(width/2, height-50, "School Management System")
        p.setFont("Helvetica", 14)
        p.drawCentredText(width/2, height-70, "Fee Payment Receipt")
        
        # Student Info
        y = height - 120
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, "Student Information:")
        p.setFont("Helvetica", 10)
        y -= 20
        p.drawString(70, y, f"Name: {student.name}")
        y -= 15
        p.drawString(70, y, f"Class: {student.student_class} - {student.section}")
        y -= 15
        p.drawString(70, y, f"Roll Number: {student.reg_number}")
        y -= 15
        p.drawString(70, y, f"Father's Name: {student.father_name}")
        
        # Payment Info
        y -= 30
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, "Payment Information:")
        p.setFont("Helvetica", 10)
        y -= 20
        p.drawString(70, y, f"Receipt No: RCP{payment.id:04d}")
        y -= 15
        p.drawString(70, y, f"Payment Date: {payment.payment_date}")
        y -= 15
        p.drawString(70, y, f"Payment Method: {payment.payment_method}")
        y -= 15
        p.drawString(70, y, f"Amount Paid: Rs.{payment.payment_amount}")
        
        # Fee Details
        if payment.fee_types:
            try:
                fee_types = json.loads(payment.fee_types)
                y -= 30
                p.setFont("Helvetica-Bold", 12)
                p.drawString(50, y, "Fee Details:")
                p.setFont("Helvetica", 10)
                
                for fee_type in fee_types:
                    y -= 20
                    fee_name = fee_type.get('type', '').replace('_', ' ').title()
                    fee_amount = fee_type.get('amount', 0)
                    p.drawString(70, y, f"{fee_name}: Rs.{fee_amount}")
            except json.JSONDecodeError:
                pass
        
        # Footer
        p.setFont("Helvetica", 8)
        p.drawCentredText(width/2, 50, "This is a computer-generated receipt. No signature required.")
        p.drawCentredText(width/2, 35, f"Generated on {datetime.now().strftime('%B %d, %Y')}")
        
        p.showPage()
        p.save()
        
        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="receipt_{payment.id}.pdf"'
        return response
        
    except ImportError:
        # Fallback if reportlab is not installed
        messages.error(request, 'PDF generation not available. Please install reportlab.')
        return redirect('fee_receipt', payment_id=payment_id)

def credit_slip(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    school = SchoolDetail.get_current_school()
    
    selected_months = [m.strip() for m in request.GET.get('months', '').split(',') if m.strip()]
    selected_fee_types = [f.strip() for f in request.GET.get('fee_types', '').split(',') if f.strip()]
    
    try:
        fee_structure = FeeStructure.objects.get(class_name=student.student_class)
    except FeeStructure.DoesNotExist:
        fee_structure = None
    
    pending_fees = []
    total_pending = 0
    
    # Add student daily expenses
    daily_expenses = StudentDailyExpense.objects.filter(student=student)
    for expense in daily_expenses:
        pending_fees.append({
            'name': expense.description,
            'amount': float(expense.amount)
        })
        total_pending += float(expense.amount)
    
    if fee_structure:
        # Get paid months and fee types
        payments = FeePayment.objects.filter(student=student)
        paid_months = set()
        paid_fee_types = set()
        
        for payment in payments:
            if payment.selected_months:
                try:
                    months = json.loads(payment.selected_months)
                    paid_months.update(months)
                except json.JSONDecodeError:
                    pass
            if payment.fee_types:
                try:
                    fee_types = json.loads(payment.fee_types)
                    for fee_data in fee_types:
                        paid_fee_types.add(fee_data.get('type'))
                except json.JSONDecodeError:
                    pass
        
        # Show only selected unpaid items
        if selected_months or selected_fee_types:
            if selected_months and ('monthly_fee' in selected_fee_types or 'tuition_fee' in selected_fee_types or not selected_fee_types):
                unpaid_months = [month for month in selected_months if month not in paid_months]
                if unpaid_months:
                    if 'monthly_fee' in selected_fee_types and 'tuition_fee' in selected_fee_types:
                        monthly_fee = fee_structure.monthly_fee + fee_structure.tuition_fee
                        pending_fees.append({'name': f'Monthly + Tuition Fee ({', '.join(unpaid_months)})', 'amount': float(monthly_fee) * len(unpaid_months)})
                        total_pending += float(monthly_fee) * len(unpaid_months)
                    elif 'monthly_fee' in selected_fee_types:
                        monthly_fee = fee_structure.monthly_fee
                        pending_fees.append({'name': f'Monthly Fee ({', '.join(unpaid_months)})', 'amount': float(monthly_fee) * len(unpaid_months)})
                        total_pending += float(monthly_fee) * len(unpaid_months)
                    elif 'tuition_fee' in selected_fee_types:
                        tuition_fee = fee_structure.tuition_fee
                        pending_fees.append({'name': f'Tuition Fee ({', '.join(unpaid_months)})', 'amount': float(tuition_fee) * len(unpaid_months)})
                        total_pending += float(tuition_fee) * len(unpaid_months)
                    elif not selected_fee_types:
                        monthly_fee = fee_structure.monthly_fee + fee_structure.tuition_fee
                        pending_fees.append({'name': f'Monthly + Tuition Fee ({', '.join(unpaid_months)})', 'amount': float(monthly_fee) * len(unpaid_months)})
                        total_pending += float(monthly_fee) * len(unpaid_months)
            
            if selected_fee_types:
                for fee_type in selected_fee_types:
                    if fee_type not in paid_fee_types and fee_type not in ['monthly_fee', 'tuition_fee']:
                        fee_amount = getattr(fee_structure, fee_type, 0)
                        if fee_amount > 0:
                            fee_name = fee_type.replace('_', ' ').title()
                            pending_fees.append({'name': fee_name, 'amount': float(fee_amount)})
                            total_pending += float(fee_amount)
        else:
            # No filters - show total pending like fee receipt book
            student_total_fee = (
                fee_structure.admission_fee +
                fee_structure.monthly_fee * 12 +
                fee_structure.tuition_fee * 12 +
                fee_structure.examination_fee +
                fee_structure.library_fee +
                fee_structure.sports_fee +
                fee_structure.laboratory_fee +
                fee_structure.computer_fee +
                fee_structure.transportation_fee * 12
            )
            student_paid = sum(float(payment.payment_amount) for payment in payments)
            total_pending = max(0, float(student_total_fee) - student_paid)
            
            if total_pending > 0:
                pending_fees.append({'name': 'Pending Fees', 'amount': total_pending})
    
    context = {
        'student': student,
        'school': school,
        'pending_fees': pending_fees,
        'total_pending': total_pending,
        'current_date': datetime.now().strftime('%B %d, %Y')
    }
    
    return render(request, 'credit_slip.html', context)

def fee_receipt_book_api(request):
    try:
        selected_months = [m.strip() for m in request.GET.get('months', '').split(',') if m.strip()]
        class_filter = request.GET.get('class', '').strip()
        status_filter = request.GET.get('status', '').strip()
        fee_types_filter = [f.strip() for f in request.GET.get('fee_types', '').split(',') if f.strip()]
        
        students = Student.objects.annotate(
            total_paid=Sum('feepayment__payment_amount'),
            last_payment_date=Max('feepayment__payment_date')
        )
        
        if class_filter:
            students = students.filter(student_class=class_filter)
        
        students = students.order_by('name')
        
        students_data = []
        total_collected = Decimal('0')
        total_pending = Decimal('0')
        
        for student in students:
            try:
                fee_structure = FeeStructure.objects.get(class_name=student.student_class)
            except FeeStructure.DoesNotExist:
                fee_structure = None
            
            if fee_types_filter and fee_structure:
                # Calculate fee for selected fee types only
                student_total_fee = Decimal('0')
                for fee_type in fee_types_filter:
                    fee_amount = getattr(fee_structure, fee_type, 0)
                    if fee_type in ['monthly_fee', 'tuition_fee', 'transportation_fee']:
                        student_total_fee += fee_amount * (len(selected_months) if selected_months else 12)
                    else:
                        student_total_fee += fee_amount
                
                # Always show actual total paid amount, not filtered
                student_paid = student.total_paid or Decimal('0')
            elif selected_months and fee_structure:
                # Calculate fee only for selected months
                monthly_fee = fee_structure.monthly_fee + fee_structure.tuition_fee
                student_total_fee = monthly_fee * len(selected_months)
                
                # Calculate paid amount for selected months only
                payments = FeePayment.objects.filter(student=student)
                paid_months = set()
                for payment in payments:
                    if payment.selected_months:
                        try:
                            months = json.loads(payment.selected_months)
                            paid_months.update(months)
                        except json.JSONDecodeError:
                            pass
                
                paid_selected_months = len([m for m in selected_months if m in paid_months])
                student_paid = monthly_fee * paid_selected_months
            else:
                # Default calculation (all months)
                if fee_structure:
                    student_total_fee = (
                        fee_structure.admission_fee +
                        fee_structure.monthly_fee * 12 +
                        fee_structure.tuition_fee * 12 +
                        fee_structure.examination_fee +
                        fee_structure.library_fee +
                        fee_structure.sports_fee +
                        fee_structure.laboratory_fee +
                        fee_structure.computer_fee +
                        fee_structure.transportation_fee * 12
                    )
                else:
                    student_total_fee = Decimal('60000')
                
                student_paid = student.total_paid or Decimal('0')
            
            # Add daily expenses to total fee
            daily_expenses = StudentDailyExpense.objects.filter(student=student).aggregate(
                total_expenses=Sum('amount')
            )['total_expenses'] or Decimal('0')
            
            student_total_fee += daily_expenses
            student_pending = max(Decimal('0'), student_total_fee - student_paid)
            payment_status = 'paid' if student_pending == 0 else 'pending'
            
            # Apply status filter
            if status_filter and payment_status != status_filter:
                continue
            
            total_collected += student_paid
            total_pending += student_pending
            
            # Calculate fee breakdown based on applied filters
            fee_breakdown_text = "Fee breakdown not available"
            if fee_structure:
                breakdown_parts = []
                
                # Apply fee type filters or show all if none selected
                fee_types_to_show = fee_types_filter if fee_types_filter else ['admission_fee', 'monthly_fee', 'tuition_fee', 'transportation_fee', 'examination_fee', 'library_fee', 'sports_fee', 'laboratory_fee', 'computer_fee']
                
                # Apply month filters for monthly fees
                months_count = len(selected_months) if selected_months else 12
                
                # Calculate components based on filters
                if 'admission_fee' in fee_types_to_show:
                    admission_total = int(fee_structure.admission_fee)
                    if admission_total > 0: breakdown_parts.append(f"Admission: Rs{admission_total:,}")
                
                if 'monthly_fee' in fee_types_to_show:
                    monthly_total = int(fee_structure.monthly_fee * months_count)
                    if monthly_total > 0: breakdown_parts.append(f"Monthly: Rs{monthly_total:,} ({months_count}m)")
                
                if 'tuition_fee' in fee_types_to_show:
                    tuition_total = int(fee_structure.tuition_fee * months_count)
                    if tuition_total > 0: breakdown_parts.append(f"Tuition: Rs{tuition_total:,} ({months_count}m)")
                
                if 'transportation_fee' in fee_types_to_show:
                    transport_total = int(fee_structure.transportation_fee * months_count)
                    if transport_total > 0: breakdown_parts.append(f"Transport: Rs{transport_total:,} ({months_count}m)")
                
                # Other fees (not affected by months)
                other_fees = ['examination_fee', 'library_fee', 'sports_fee', 'laboratory_fee', 'computer_fee']
                other_total = 0
                for fee in other_fees:
                    if fee in fee_types_to_show:
                        other_total += int(getattr(fee_structure, fee, 0))
                if other_total > 0: breakdown_parts.append(f"Others: Rs{other_total:,}")
                
                fee_breakdown_text = " | ".join(breakdown_parts) if breakdown_parts else "No fees selected"
            
            students_data.append({
                'id': student.id,
                'name': student.name,
                'class_name': student.student_class,
                'section': student.section,
                'roll_number': student.reg_number,
                'mobile': student.mobile,
                'email': student.email,
                'total_fee': float(student_total_fee),
                'paid_amount': float(student_paid),
                'pending_amount': float(student_pending),
                'payment_status': payment_status,
                'last_payment_date': student.last_payment_date.strftime('%Y-%m-%d') if student.last_payment_date else None,
                'fee_breakdown_text': fee_breakdown_text,
                'daily_expenses_total': float(daily_expenses)
            })
        
        return JsonResponse({
            'success': True,
            'students': students_data,
            'total_students': len(students_data),
            'total_collected': float(total_collected),
            'total_pending': float(total_pending)
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def bulk_print_receipts(request):
    class_filter = request.GET.get('class', '').strip()
    status_filter = request.GET.get('status', '').strip()
    selected_months = [m.strip() for m in request.GET.get('months', '').split(',') if m.strip()]
    selected_fee_types = [f.strip() for f in request.GET.get('fee_types', '').split(',') if f.strip()]
    
    if not class_filter:
        return HttpResponse('Class selection is required for bulk printing.')
    
    students = Student.objects.filter(student_class=class_filter).order_by('name')
    
    # Process each student with fee calculations
    students_with_data = []
    for student in students:
        try:
            fee_structure = FeeStructure.objects.get(class_name=student.student_class)
        except FeeStructure.DoesNotExist:
            fee_structure = None
        
        # Get payments for this student
        payments = FeePayment.objects.filter(student=student)
        paid_months = set()
        paid_fee_types = set()
        total_paid = Decimal('0')
        
        for payment in payments:
            total_paid += payment.payment_amount
            if payment.selected_months:
                try:
                    months = json.loads(payment.selected_months)
                    paid_months.update(months)
                except json.JSONDecodeError:
                    pass
            if payment.fee_types:
                try:
                    fee_types = json.loads(payment.fee_types)
                    for fee_data in fee_types:
                        paid_fee_types.add(fee_data.get('type'))
                except json.JSONDecodeError:
                    pass
        
        # Calculate pending fees based on filters
        pending_fees = []
        total_pending = Decimal('0')
        
        if fee_structure:
            # If specific months are selected, only show those months
            if selected_months:
                # Filter to only selected months that are unpaid
                target_months = [month for month in selected_months if month not in paid_months]
                
                if target_months and (fee_structure.monthly_fee > 0 or fee_structure.tuition_fee > 0):
                    monthly_amount = fee_structure.monthly_fee + fee_structure.tuition_fee
                    pending_amount = monthly_amount * len(target_months)
                    pending_fees.append({
                        'name': f'Monthly Fee ({', '.join(target_months)})',
                        'amount': float(pending_amount)
                    })
                    total_pending += pending_amount
            else:
                # Show all unpaid months if no specific months selected
                all_months = ['Baisakh', 'Jestha', 'Ashadh', 'Shrawan', 'Bhadra', 'Ashwin',
                             'Kartik', 'Mangsir', 'Poush', 'Magh', 'Falgun', 'Chaitra']
                unpaid_months = [month for month in all_months if month not in paid_months]
                
                if unpaid_months and (fee_structure.monthly_fee > 0 or fee_structure.tuition_fee > 0):
                    monthly_amount = fee_structure.monthly_fee + fee_structure.tuition_fee
                    pending_amount = monthly_amount * len(unpaid_months)
                    pending_fees.append({
                        'name': f'Monthly Fee ({len(unpaid_months)} months)',
                        'amount': float(pending_amount)
                    })
                    total_pending += pending_amount
            
            # Add other fees if selected or if no specific fee types selected
            if not selected_fee_types or 'admission_fee' in selected_fee_types:
                if 'admission_fee' not in paid_fee_types and fee_structure.admission_fee > 0:
                    pending_fees.append({'name': 'Admission Fee', 'amount': float(fee_structure.admission_fee)})
                    total_pending += fee_structure.admission_fee
            
            # Other fees
            other_fees = [
                ('examination_fee', 'Examination Fee'),
                ('library_fee', 'Library Fee'),
                ('sports_fee', 'Sports Fee'),
                ('laboratory_fee', 'Laboratory Fee'),
                ('computer_fee', 'Computer Fee')
            ]
            
            for fee_field, fee_name in other_fees:
                if (not selected_fee_types or fee_field in selected_fee_types) and fee_field not in paid_fee_types:
                    fee_amount = getattr(fee_structure, fee_field, 0)
                    if fee_amount > 0:
                        pending_fees.append({'name': fee_name, 'amount': float(fee_amount)})
                        total_pending += fee_amount
        
        # Apply status filter
        payment_status = 'paid' if total_pending == 0 else 'pending'
        if status_filter and payment_status != status_filter:
            continue
        
        # Add calculated data to student
        student.pending_fees = pending_fees
        student.total_pending = float(total_pending)
        student.total_paid = float(total_paid)
        student.payment_status = payment_status
        
        students_with_data.append(student)
    
    context = {
        'students': students_with_data,
        'class_filter': class_filter,
        'selected_months': selected_months,
        'selected_fee_types': selected_fee_types,
        'current_date': datetime.now().strftime('%B %d, %Y')
    }
    
    return render(request, 'bulk_print_receipts.html', context)

def fee_pending_report(request):
    from django.db.models import Sum, Max
    from decimal import Decimal
    
    # Get all students with pending fees
    students_query = Student.objects.annotate(
        total_paid=Sum('feepayment__payment_amount'),
        last_payment_date=Max('feepayment__payment_date')
    ).order_by('name')
    
    # Process students and filter only those with pending fees
    students_with_pending = []
    total_pending_amount = Decimal('0')
    
    for student in students_query:
        try:
            fee_structure = FeeStructure.objects.get(class_name=student.student_class)
            student_total_fee = (
                fee_structure.admission_fee +
                fee_structure.monthly_fee * 12 +
                fee_structure.tuition_fee * 12 +
                fee_structure.examination_fee +
                fee_structure.library_fee +
                fee_structure.sports_fee +
                fee_structure.laboratory_fee +
                fee_structure.computer_fee +
                fee_structure.transportation_fee * 12
            )
        except FeeStructure.DoesNotExist:
            student_total_fee = Decimal('60000')  # Default total fee
        
        student_paid = student.total_paid or Decimal('0')
        student_pending = max(Decimal('0'), student_total_fee - student_paid)
        
        # Only include students with pending fees
        if student_pending > 0:
            student.total_fee = float(student_total_fee)
            student.paid_amount = float(student_paid)
            student.pending_amount = float(student_pending)
            student.payment_status = 'pending'
            student.class_name = student.student_class
            student.roll_number = student.reg_number
            
            students_with_pending.append(student)
            total_pending_amount += student_pending
    
    context = {
        'students': students_with_pending,
        'total_students': len(students_with_pending),
        'total_pending': float(total_pending_amount),
        'page_title': 'Fee Pending Report'
    }
    
    return render(request, 'fee_pending_report.html', context)

@csrf_exempt
def create_exam(request):
    if request.method == 'POST':
        try:
            selected_classes_json = request.POST.get('selected_classes')
            selected_classes = json.loads(selected_classes_json) if selected_classes_json else []
            exam_date = request.POST.get('exam_date')
            
            # Convert exam date to Nepali if provided
            exam_date_nepali = ''
            if exam_date:
                try:
                    nepali_date_dict = NepaliCalendar.english_to_nepali_date(exam_date)
                    exam_date_nepali = NepaliCalendar.format_nepali_date(nepali_date_dict, 'full_en')
                except:
                    pass
            
            created_exams = []
            for class_name in selected_classes:
                exam = Exam.objects.create(
                    name=request.POST.get('name'),
                    exam_type=request.POST.get('exam_type'),
                    class_name=class_name,
                    exam_date=exam_date,
                    exam_date_nepali=exam_date_nepali,
                    session=request.POST.get('session')
                )
                created_exams.append(exam.id)
            
            return JsonResponse({
                'success': True, 
                'message': f'Created exams for {len(selected_classes)} classes', 
                'exam_ids': created_exams
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def create_subject(request):
    if request.method == 'POST':
        try:
            code = request.POST.get('code')
            
            # Check if subject code already exists
            if Subject.objects.filter(code=code).exists():
                return JsonResponse({'success': False, 'error': f'Subject code "{code}" already exists. Please use a different code.'})
            
            subject = Subject.objects.create(
                name=request.POST.get('name'),
                code=code,
                class_name=request.POST.get('class_name'),
                specialization=request.POST.get('specialization') or None,
                max_marks=int(request.POST.get('max_marks', 100)),
                pass_marks=int(request.POST.get('pass_marks', 35))
            )
            return JsonResponse({'success': True, 'subject_id': subject.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def edit_subject(request):
    if request.method == 'POST':
        try:
            subject_id = request.POST.get('subject_id')
            subject = get_object_or_404(Subject, id=subject_id)
            
            code = request.POST.get('code')
            
            # Check if subject code already exists (excluding current subject)
            if Subject.objects.filter(code=code).exclude(id=subject_id).exists():
                return JsonResponse({'success': False, 'error': f'Subject code "{code}" already exists. Please use a different code.'})
            
            subject.name = request.POST.get('name')
            subject.code = code
            subject.class_name = request.POST.get('class_name')
            subject.specialization = request.POST.get('specialization') or None
            subject.max_marks = int(request.POST.get('max_marks', 100))
            subject.pass_marks = int(request.POST.get('pass_marks', 35))
            subject.save()
            
            return JsonResponse({'success': True, 'subject_id': subject.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def enter_marks(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Handle bulk marks entry
            if 'bulk_marks' in data:
                bulk_marks = data['bulk_marks']
                created_count = 0
                
                for mark_data in bulk_marks:
                    exam = get_object_or_404(Exam, id=mark_data['exam_id'])
                    student = get_object_or_404(Student, id=mark_data['student_id'])
                    subject = get_object_or_404(Subject, id=mark_data['subject_id'])
                    
                    marksheet, created = Marksheet.objects.update_or_create(
                        student=student,
                        exam=exam,
                        subject=subject,
                        defaults={
                            'marks_obtained': mark_data['marks_obtained'],
                            'remarks': mark_data.get('remarks', '')
                        }
                    )
                    created_count += 1
                
                return JsonResponse({
                    'success': True,
                    'message': f'Successfully saved marks for {created_count} students'
                })
            
            # Handle single mark entry
            else:
                exam = get_object_or_404(Exam, id=data['exam_id'])
                student = get_object_or_404(Student, id=data['student_id'])
                subject = get_object_or_404(Subject, id=data['subject_id'])
                
                marksheet, created = Marksheet.objects.update_or_create(
                    student=student,
                    exam=exam,
                    subject=subject,
                    defaults={
                        'marks_obtained': data['marks_obtained'],
                        'remarks': data.get('remarks', '')
                    }
                )
                
                return JsonResponse({
                    'success': True,
                    'marksheet_id': marksheet.id,
                    'grade': marksheet.grade,
                    'percentage': marksheet.percentage,
                    'status': marksheet.status
                })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def student_marksheet(request, student_id, exam_id):
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        # Get available student IDs for helpful error message
        available_students = Student.objects.values_list('id', 'name')[:5]
        student_list = ', '.join([f'ID {s[0]}: {s[1]}' for s in available_students])
        return HttpResponse(
            f'<h1>Student Not Found</h1>'
            f'<p>No student found with ID {student_id}.</p>'
            f'<p>Available students (first 5): {student_list}</p>'
            f'<p><a href="/studentlist/">View all students</a></p>',
            status=404
        )
    
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        # Get available exam IDs for helpful error message
        available_exams = Exam.objects.values_list('id', 'name', 'class_name')[:5]
        exam_list = ', '.join([f'ID {e[0]}: {e[1]} ({e[2]})' for e in available_exams])
        return HttpResponse(
            f'<h1>Exam Not Found</h1>'
            f'<p>No exam found with ID {exam_id}.</p>'
            f'<p>Available exams (first 5): {exam_list}</p>'
            f'<p><a href="/reports/">View all exams</a></p>',
            status=404
        )
    
    marksheets = Marksheet.objects.filter(student=student, exam=exam).select_related('subject').order_by('subject__name')
    
    # Initialize default values
    total_marks = 0
    obtained_marks = 0
    percentage = 0
    overall_grade = 'N/A'
    overall_status = 'No Data'
    failed_subjects = 0
    
    # Calculate totals only if marksheets exist
    if marksheets.exists():
        try:
            total_marks = sum(int(m.subject.max_marks) for m in marksheets if m.subject and m.subject.max_marks)
            obtained_marks = sum(int(m.marks_obtained) for m in marksheets if m.marks_obtained is not None)
            percentage = (obtained_marks / total_marks * 100) if total_marks > 0 else 0
            
            # Overall grade
            if percentage >= 90:
                overall_grade = 'A+'
            elif percentage >= 80:
                overall_grade = 'A'
            elif percentage >= 70:
                overall_grade = 'B+'
            elif percentage >= 60:
                overall_grade = 'B'
            elif percentage >= 50:
                overall_grade = 'C+'
            elif percentage >= 40:
                overall_grade = 'C'
            elif percentage >= 35:
                overall_grade = 'D'
            else:
                overall_grade = 'F'
            
            # Overall status
            failed_subjects = marksheets.filter(
                marks_obtained__lt=models.F('subject__pass_marks')
            ).count()
            overall_status = 'Pass' if failed_subjects == 0 and marksheets.count() > 0 else 'Fail'
            
        except Exception as e:
            # Handle any calculation errors gracefully
            print(f"Error calculating marksheet totals: {e}")
            overall_grade = 'Error'
            overall_status = 'Error'
    
    context = {
        'student': student,
        'exam': exam,
        'marksheets': marksheets,
        'total_marks': total_marks,
        'obtained_marks': obtained_marks,
        'percentage': round(percentage, 2),
        'overall_grade': overall_grade,
        'overall_status': overall_status,
        'failed_subjects': failed_subjects
    }
    
    return render(request, 'student_marksheet.html', context)

def update_subject_class(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # This is a placeholder function - implement based on your Subject model
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def delete_exam(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            exam = get_object_or_404(Exam, id=data['exam_id'])
            exam.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def generate_results(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            exam = get_object_or_404(Exam, id=data['exam_id'])
            
            # Get all students for this exam's class
            if exam.class_name == 'All Classes':
                # For "All Classes" exams, we need to process all classes
                all_classes = ['Nursery', 'LKG', 'UKG', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th']
                students = Student.objects.filter(student_class__in=all_classes)
            else:
                students = Student.objects.filter(student_class=exam.class_name)
            
            total_students = 0
            passed_students = 0
            failed_students = 0
            
            for student in students:
                # Get all marksheets for this student and exam
                marksheets = Marksheet.objects.filter(student=student, exam=exam)
                
                if marksheets.exists():
                    total_students += 1
                    
                    # Check if student passed (no failed subjects)
                    failed_subjects = marksheets.filter(marks_obtained__lt=models.F('subject__pass_marks')).count()
                    
                    if failed_subjects == 0:
                        passed_students += 1
                    else:
                        failed_students += 1
            
            return JsonResponse({
                'success': True,
                'total_students': total_students,
                'passed': passed_students,
                'failed': failed_students
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def bulk_edit_subjects(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            class_name = data['class_name']
            max_marks = data['max_marks']
            pass_marks = data['pass_marks']
            
            # Update subjects based on selection
            if class_name == 'All Subjects':
                # Update all subjects across all classes
                updated_count = Subject.objects.all().update(
                    max_marks=max_marks,
                    pass_marks=pass_marks
                )
            else:
                # Update all subjects for the selected class
                updated_count = Subject.objects.filter(class_name=class_name).update(
                    max_marks=max_marks,
                    pass_marks=pass_marks
                )
            
            return JsonResponse({
                'success': True,
                'updated_count': updated_count
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@permission_required('can_view_marksheet')
def marksheet_system(request):
    """Main marksheet system page"""
    exams = Exam.objects.all().order_by('-exam_date')
    
    # Filter subjects based on user's teaching assignments
    admin_username = request.session.get('admin_username')
    if admin_username:
        try:
            admin_user = AdminLogin.objects.get(username=admin_username)
            if admin_user.teacher:
                subjects = Subject.objects.filter(
                    teacherclasssubject__teacher=admin_user.teacher,
                    teacherclasssubject__is_active=True
                ).distinct().order_by('class_name', 'name')
            else:
                subjects = Subject.objects.all().order_by('class_name', 'name')
        except AdminLogin.DoesNotExist:
            subjects = Subject.objects.all().order_by('class_name', 'name')
    else:
        subjects = Subject.objects.all().order_by('class_name', 'name')
    
    # Get current Nepali session for filtering
    current_nepali_session = get_current_nepali_year_session()
    
    # Get available sessions from exams
    available_sessions = list(set(exam.session for exam in exams if exam.session))
    available_sessions.sort(reverse=True)
    
    context = {
        'exams': exams,
        'subjects': subjects,
        'current_nepali_session': current_nepali_session,
        'available_sessions': available_sessions,
    }
    
    return render(request, 'marksheet_system.html', context)

def marksheet_new(request):
    """New improved marksheet system"""
    exams = Exam.objects.all().order_by('-exam_date')
    subjects = Subject.objects.all().order_by('class_name', 'name')
    
    # Get class statistics
    class_stats = {}
    for exam in exams:
        if exam.class_name not in class_stats:
            class_stats[exam.class_name] = {
                'total_students': Student.objects.filter(student_class=exam.class_name).count(),
                'total_subjects': Subject.objects.filter(class_name=exam.class_name).count()
            }
    
    context = {
        'exams': exams,
        'subjects': subjects,
        'class_stats': class_stats,
    }
    
    return render(request, 'marksheet_new.html', context)

def marksheet_advanced(request):
    """Advanced marksheet system with enhanced features"""
    exams = Exam.objects.all().order_by('-exam_date')
    subjects = Subject.objects.all().order_by('class_name', 'name')
    
    # Get comprehensive statistics
    total_exams = exams.count()
    total_subjects = subjects.count()
    total_marksheets = Marksheet.objects.count()
    
    # Get recent activity
    recent_marksheets = Marksheet.objects.select_related('student', 'exam', 'subject').order_by('-id')[:10]
    
    context = {
        'exams': exams,
        'subjects': subjects,
        'total_exams': total_exams,
        'total_subjects': total_subjects,
        'total_marksheets': total_marksheets,
        'recent_marksheets': recent_marksheets,
    }
    
    return render(request, 'marksheet_advanced.html', context)

def subjects_by_class_api(request, class_name):
    """API to get subjects by class"""
    try:
        # Handle class name mapping
        class_mapping = {
            'One': '1st', 'Two': '2nd', 'Three': '3rd', 'Four': '4th', 'Five': '5th',
            'Six': '6th', 'Seven': '7th', 'Eight': '8th', 'Nine': '9th', 'Ten': '10th',
            'Eleven': '11th', 'Twelve': '12th'
        }
        
        # Try both original and mapped class names
        mapped_class = class_mapping.get(class_name, class_name)
        subjects = Subject.objects.filter(
            models.Q(class_name=class_name) | models.Q(class_name=mapped_class)
        ).order_by('name')
        
        subjects_data = []
        for subject in subjects:
            subjects_data.append({
                'id': subject.id,
                'name': subject.name,
                'code': subject.code,
                'class_name': subject.class_name,
                'max_marks': subject.max_marks,
                'pass_marks': subject.pass_marks
            })
        
        return JsonResponse({
            'success': True,
            'subjects': subjects_data,
            'class_name': class_name
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def marksheet_data_api(request, exam_id, subject_id):
    """API to get marksheet data for exam and subject"""
    try:
        exam = get_object_or_404(Exam, id=exam_id)
        subject = get_object_or_404(Subject, id=subject_id)
        
        # Class name mapping for display
        class_name_mapping = {
            '1st': 'One',
            '2nd': 'Two',
            '3rd': 'Three',
            '4th': 'Four',
            '5th': 'Five',
            '6th': 'Six',
            '7th': 'Seven',
            '8th': 'Eight',
            '9th': 'Nine',
            '10th': 'Ten',
            '11th': 'Eleven',
            '12th': 'Twelve'
        }
        
        # Validate that subject belongs to exam's class
        if subject.class_name != exam.class_name:
            display_subject_class = class_name_mapping.get(subject.class_name, subject.class_name)
            display_exam_class = class_name_mapping.get(exam.class_name, exam.class_name)
            return JsonResponse({
                'success': False, 
                'error': f'Subject {subject.name} does not belong to class {display_exam_class}'
            })
        
        # Get students for this exam's class
        students = Student.objects.filter(student_class=exam.class_name).order_by('name')
        
        if not students.exists():
            return JsonResponse({
                'success': False,
                'error': f'No students found in class {exam.class_name}'
            })
        
        students_data = []
        for student in students:
            # Get existing marksheet if any
            try:
                marksheet = Marksheet.objects.get(student=student, exam=exam, subject=subject)
                marks_obtained = marksheet.marks_obtained
                remarks = marksheet.remarks
                percentage = round(marksheet.percentage, 1)
                grade = marksheet.grade
                status = marksheet.status
            except Marksheet.DoesNotExist:
                marks_obtained = None
                remarks = ''
                percentage = 0
                grade = 'F'
                status = 'Fail'
            
            students_data.append({
                'id': student.id,
                'name': student.name,
                'reg_number': student.reg_number,
                'marks_obtained': marks_obtained,
                'remarks': remarks,
                'percentage': percentage,
                'grade': grade,
                'status': status
            })
        
        subject_data = {
            'id': subject.id,
            'name': subject.name,
            'code': subject.code,
            'max_marks': subject.max_marks,
            'pass_marks': subject.pass_marks
        }
        
        return JsonResponse({
            'success': True,
            'students': students_data,
            'subject': subject_data,
            'exam': {
                'id': exam.id,
                'name': exam.name,
                'exam_type': exam.exam_type,
                'class_name': exam.class_name,
                'exam_date': exam.exam_date.strftime('%Y-%m-%d')
            },
            'stats': {
                'total_students': len(students_data),
                'students_with_marks': len([s for s in students_data if s['marks_obtained'] is not None]),
                'passed_students': len([s for s in students_data if s['status'] == 'Pass']),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
def save_marksheet_api(request):
    """API to save marksheet data"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            marks_data = data.get('marks', [])
            
            saved_count = 0
            for mark_data in marks_data:
                student = get_object_or_404(Student, id=mark_data['student_id'])
                exam = get_object_or_404(Exam, id=mark_data['exam_id'])
                subject = get_object_or_404(Subject, id=mark_data['subject_id'])
                
                marksheet, created = Marksheet.objects.update_or_create(
                    student=student,
                    exam=exam,
                    subject=subject,
                    defaults={
                        'marks_obtained': mark_data['marks_obtained'],
                        'remarks': mark_data.get('remarks', '')
                    }
                )
                saved_count += 1
            
            return JsonResponse({
                'success': True,
                'saved_count': saved_count
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def auto_populate_exam_marks(request, exam_id):
    """API to auto-populate marks for a specific exam"""
    if request.method == 'POST':
        try:
            import random
            
            exam = get_object_or_404(Exam, id=exam_id)
            students = Student.objects.filter(student_class=exam.class_name)
            subjects = Subject.objects.filter(class_name=exam.class_name)
            
            total_records = 0
            
            for student in students:
                for subject in subjects:
                    # Check if marksheet already exists with marks
                    existing = Marksheet.objects.filter(
                        student=student, exam=exam, subject=subject
                    ).first()
                    
                    if not existing or not existing.marks_obtained:
                        # Generate random marks (35-95% of max marks)
                        min_marks = max(35, int(subject.max_marks * 0.35))
                        max_marks = int(subject.max_marks * 0.95)
                        random_marks = random.randint(min_marks, max_marks)
                        
                        # Create or update marksheet
                        Marksheet.objects.update_or_create(
                            student=student,
                            exam=exam,
                            subject=subject,
                            defaults={
                                'marks_obtained': random_marks,
                                'remarks': 'Auto-filled'
                            }
                        )
                        total_records += 1
            
            return JsonResponse({
                'success': True,
                'total_records': total_records,
                'exam_name': exam.name,
                'class_name': exam.class_name
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def get_student_marksheet_data(request, student_id):
    """API to get student's marksheet data for dashboard"""
    try:
        student = get_object_or_404(Student, id=student_id)
        marksheets = Marksheet.objects.filter(student=student).select_related('exam', 'subject')
        
        # Group by exam
        exam_data = {}
        subject_performance = {}
        
        for marksheet in marksheets:
            exam_name = marksheet.exam.name
            subject_name = marksheet.subject.name
            
            if exam_name not in exam_data:
                exam_data[exam_name] = {
                    'total_marks': 0,
                    'obtained_marks': 0,
                    'subjects': 0
                }
            
            exam_data[exam_name]['total_marks'] += marksheet.subject.max_marks
            exam_data[exam_name]['obtained_marks'] += marksheet.marks_obtained or 0
            exam_data[exam_name]['subjects'] += 1
            
            # Subject performance
            if subject_name not in subject_performance:
                subject_performance[subject_name] = []
            
            percentage = (marksheet.marks_obtained / marksheet.subject.max_marks * 100) if marksheet.marks_obtained else 0
            subject_performance[subject_name].append({
                'exam': exam_name,
                'percentage': round(percentage, 1),
                'marks': marksheet.marks_obtained or 0,
                'max_marks': marksheet.subject.max_marks
            })
        
        # Calculate exam percentages
        exam_percentages = []
        for exam, data in exam_data.items():
            percentage = (data['obtained_marks'] / data['total_marks'] * 100) if data['total_marks'] > 0 else 0
            exam_percentages.append({
                'exam': exam,
                'percentage': round(percentage, 1)
            })
        
        # Calculate subject averages
        subject_averages = []
        for subject, performances in subject_performance.items():
            avg_percentage = sum(p['percentage'] for p in performances) / len(performances)
            subject_averages.append({
                'subject': subject,
                'average': round(avg_percentage, 1),
                'performances': performances
            })
        
        # Return empty data if no marksheets found
        if not exam_data:
            return JsonResponse({
                'success': True,
                'progression_data': [{'exam': 'No Data', 'percentage': 0}],
                'subject_averages': [{'subject': 'No Data', 'average': 0}],
                'total_exams': 0,
                'total_subjects': 0
            })
        
        # If only one exam, duplicate it for trend visualization
        if len(exam_percentages) == 1:
            single_exam = exam_percentages[0]
            exam_percentages = [
                {'exam': f"{single_exam['exam']} (Start)", 'percentage': max(0, single_exam['percentage'] - 5)},
                single_exam
            ]
        
        return JsonResponse({
            'success': True,
            'progression_data': exam_percentages,
            'subject_averages': subject_averages,
            'total_exams': len(exam_data),
            'total_subjects': len(subject_performance)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
def populate_all_marksheet_data(request):
    """API to populate all students with random marks for all subjects"""
    if request.method == 'POST':
        try:
            import random
            
            students = Student.objects.all()
            subjects = Subject.objects.all()
            exams = Exam.objects.all()
            
            if not students.exists():
                return JsonResponse({'success': False, 'error': 'No students found'})
            if not subjects.exists():
                return JsonResponse({'success': False, 'error': 'No subjects found'})
            if not exams.exists():
                return JsonResponse({'success': False, 'error': 'No exams found'})
            
            total_records = 0
            
            for student in students:
                # Get subjects for student's class
                student_subjects = subjects.filter(class_name=student.student_class)
                
                # Get exams for student's class
                student_exams = exams.filter(class_name=student.student_class)
                
                for exam in student_exams:
                    for subject in student_subjects:
                        # Generate random marks (60-95% of max marks for realistic data)
                        min_marks = int(subject.max_marks * 0.6)
                        max_marks = int(subject.max_marks * 0.95)
                        random_marks = random.randint(min_marks, max_marks)
                        
                        # Create or update marksheet
                        marksheet, created = Marksheet.objects.update_or_create(
                            student=student,
                            exam=exam,
                            subject=subject,
                            defaults={
                                'marks_obtained': random_marks,
                                'remarks': 'Auto-generated'
                            }
                        )
                        total_records += 1
            
            return JsonResponse({
                'success': True,
                'total_records': total_records,
                'students_count': students.count(),
                'subjects_count': subjects.count(),
                'exams_count': exams.count()
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def generate_class_marksheets(request, exam_id):
    """Generate marksheets for all students in an exam"""
    exam = get_object_or_404(Exam, id=exam_id)
    students = Student.objects.filter(student_class=exam.class_name).order_by('name')
    
    marksheets_data = []
    for student in students:
        marksheets = Marksheet.objects.filter(student=student, exam=exam)
        
        if marksheets.exists():
            # Calculate totals
            total_marks = sum(m.subject.max_marks for m in marksheets)
            obtained_marks = sum(m.marks_obtained for m in marksheets)
            percentage = (obtained_marks / total_marks * 100) if total_marks > 0 else 0
            
            # Overall grade
            if percentage >= 90:
                overall_grade = 'A+'
            elif percentage >= 80:
                overall_grade = 'A'
            elif percentage >= 70:
                overall_grade = 'B+'
            elif percentage >= 60:
                overall_grade = 'B'
            elif percentage >= 50:
                overall_grade = 'C+'
            elif percentage >= 40:
                overall_grade = 'C'
            elif percentage >= 30:
                overall_grade = 'D+'
            elif percentage >= 20:
                overall_grade = 'D'
            else:
                overall_grade = 'E'
            
            # Overall status
            failed_subjects = marksheets.filter(marks_obtained__lt=models.F('subject__pass_marks')).count()
            overall_status = 'Pass' if failed_subjects == 0 else 'Fail'
            
            marksheets_data.append({
                'student': student,
                'marksheets': marksheets,
                'total_marks': total_marks,
                'obtained_marks': obtained_marks,
                'percentage': round(percentage, 2),
                'overall_grade': overall_grade,
                'overall_status': overall_status,
                'failed_subjects': failed_subjects
            })
    
    context = {
        'exam': exam,
        'marksheets_data': marksheets_data,
        'current_date': datetime.now().strftime('%B %d, %Y')
    }
    
    return render(request, 'class_marksheets.html', context)

def generate_student_result(request, student_id):
    """Generate complete result for a student with all subjects across all exams"""
    student = get_object_or_404(Student, id=student_id)
    
    # Get all exams for this student's class
    exams = Exam.objects.filter(class_name=student.student_class).order_by('-exam_date')
    
    # Get all subjects for this student's class
    subjects = Subject.objects.filter(class_name=student.student_class).order_by('name')
    
    # Get all marksheets for this student
    marksheets = Marksheet.objects.filter(student=student).select_related('exam', 'subject')
    
    # Organize data by exam
    exam_results = []
    overall_stats = {
        'total_exams': 0,
        'passed_exams': 0,
        'failed_exams': 0,
        'average_percentage': 0,
        'best_percentage': 0,
        'worst_percentage': 100
    }
    
    total_percentage = 0
    
    for exam in exams:
        exam_marksheets = marksheets.filter(exam=exam)
        
        if exam_marksheets.exists():
            # Calculate exam totals
            total_marks = sum(m.subject.max_marks for m in exam_marksheets)
            obtained_marks = sum(m.marks_obtained for m in exam_marksheets)
            percentage = (obtained_marks / total_marks * 100) if total_marks > 0 else 0
            
            # Calculate grade
            if percentage >= 90:
                grade = 'A+'
            elif percentage >= 80:
                grade = 'A'
            elif percentage >= 70:
                grade = 'B+'
            elif percentage >= 60:
                grade = 'B'
            elif percentage >= 50:
                grade = 'C+'
            elif percentage >= 40:
                grade = 'C'
            elif percentage >= 35:
                grade = 'D'
            else:
                grade = 'F'
            
            # Check pass/fail
            failed_subjects = exam_marksheets.filter(marks_obtained__lt=models.F('subject__pass_marks')).count()
            status = 'Pass' if failed_subjects == 0 else 'Fail'
            
            # Subject-wise results
            subject_results = []
            for subject in subjects:
                try:
                    marksheet = exam_marksheets.get(subject=subject)
                    subject_results.append({
                        'subject': subject,
                        'marks_obtained': marksheet.marks_obtained,
                        'max_marks': subject.max_marks,
                        'percentage': marksheet.percentage,
                        'grade': marksheet.grade,
                        'grade_point': marksheet.grade_point,
                        'grade_remarks': marksheet.grade_remarks,
                        'status': marksheet.status,
                        'remarks': marksheet.remarks
                    })
                except Marksheet.DoesNotExist:
                    subject_results.append({
                        'subject': subject,
                        'marks_obtained': 'N/A',
                        'max_marks': subject.max_marks,
                        'percentage': 0,
                        'grade': 'N/A',
                        'grade_point': 0,
                        'grade_remarks': 'Not attempted',
                        'status': 'N/A',
                        'remarks': 'Not attempted'
                    })
            
            exam_results.append({
                'exam': exam,
                'subject_results': subject_results,
                'total_marks': total_marks,
                'obtained_marks': obtained_marks,
                'percentage': round(percentage, 2),
                'grade': grade,
                'status': status,
                'failed_subjects': failed_subjects
            })
            
            # Update overall stats
            overall_stats['total_exams'] += 1
            if status == 'Pass':
                overall_stats['passed_exams'] += 1
            else:
                overall_stats['failed_exams'] += 1
            
            total_percentage += percentage
            overall_stats['best_percentage'] = max(overall_stats['best_percentage'], percentage)
            overall_stats['worst_percentage'] = min(overall_stats['worst_percentage'], percentage)
    
    # Calculate average percentage
    if overall_stats['total_exams'] > 0:
        overall_stats['average_percentage'] = round(total_percentage / overall_stats['total_exams'], 2)
    
    # If no exams taken, reset worst percentage
    if overall_stats['total_exams'] == 0:
        overall_stats['worst_percentage'] = 0
    
    context = {
        'student': student,
        'exam_results': exam_results,
        'subjects': subjects,
        'overall_stats': overall_stats,
        'current_date': datetime.now().strftime('%B %d, %Y')
    }
    
    return render(request, 'student_result.html', context)

@csrf_exempt
def create_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # If setting as active, deactivate all other sessions
            if data.get('is_active', False):
                Session.objects.all().update(is_active=False)
            
            session = Session.objects.create(
                name=data['name'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                is_active=data.get('is_active', False)
            )
            
            return JsonResponse({
                'success': True,
                'session_id': session.id,
                'message': f'Session {session.name} created successfully'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def set_active_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_id = data['session_id']
            
            # Deactivate all sessions
            Session.objects.all().update(is_active=False)
            
            # Activate selected session
            session = get_object_or_404(Session, id=session_id)
            session.is_active = True
            session.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Session {session.name} is now active'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def get_sessions_api(request):
    try:
        sessions = Session.objects.all().order_by('-start_date')
        sessions_data = []
        
        for session in sessions:
            sessions_data.append({
                'id': session.id,
                'name': session.name,
                'start_date': session.start_date.strftime('%Y-%m-%d'),
                'end_date': session.end_date.strftime('%Y-%m-%d'),
                'is_active': session.is_active
            })
        
        current_session = Session.get_current_session()
        
        return JsonResponse({
            'success': True,
            'sessions': sessions_data,
            'current_session': current_session.name if current_session else None
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def students_by_session_api(request, session_name):
    try:
        students = Student.objects.filter(session=session_name).order_by('name')
        students_data = []
        
        for student in students:
            students_data.append({
                'id': student.id,
                'name': student.name,
                'reg_number': student.reg_number,
                'student_class': student.student_class,
                'section': student.section,
                'father_name': student.father_name,
                'mobile': student.mobile,
                'session': student.session
            })
        
        return JsonResponse({
            'success': True,
            'students': students_data,
            'total_count': len(students_data)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
def assign_sessions_to_students(request):
    """API endpoint to assign current session to all students without sessions"""
    if request.method == 'POST':
        try:
            # Get or create current active session
            current_session = Session.get_current_session()
            if not current_session:
                current_session, created = Session.objects.get_or_create(
                    name='2024-25',
                    defaults={
                        'start_date': '2024-04-01',
                        'end_date': '2025-03-31',
                        'is_active': True
                    }
                )

            # Update students without sessions or with empty sessions
            students_without_session = Student.objects.filter(
                models.Q(session__isnull=True) | models.Q(session='')
            )
            count = students_without_session.count()
            
            if count > 0:
                students_without_session.update(session=current_session.name)
                return JsonResponse({
                    'success': True,
                    'message': f'Assigned session "{current_session.name}" to {count} students',
                    'updated_count': count
                })
            else:
                return JsonResponse({
                    'success': True,
                    'message': 'All students already have sessions assigned',
                    'updated_count': 0
                })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def save_student_marks(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            marks_data = data['marks']
            
            current_session = Session.get_current_session()
            session_name = current_session.name if current_session else '2024-25'
            
            saved_count = 0
            for mark_entry in marks_data:
                # Get student name from frontend or database
                student_name = mark_entry.get('student_name')
                if not student_name:
                    student = get_object_or_404(Student, id=mark_entry['student_id'])
                    student_name = student.name
                
                # Save directly to MarksheetData model
                MarksheetData.objects.create(
                    student_name=student_name,
                    subject_name=mark_entry['subject'],
                    marks_obtained=mark_entry['marks_obtained'],
                    max_marks=mark_entry.get('max_marks', 100),
                    session=session_name
                )
                
                saved_count += 1
            
            return JsonResponse({
                'success': True,
                'message': f'{saved_count} students',
                'session': session_name
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def generate_class_marksheets_new_tab(request, exam_id):
    """Generate marksheets for all students in an exam - opens in new tab without sidebar"""
    exam = get_object_or_404(Exam, id=exam_id)
    school = SchoolDetail.get_current_school()
    students = Student.objects.filter(student_class=exam.class_name).order_by('name')
    
    # If no students found, get all students for demo
    if not students.exists():
        students = Student.objects.all().order_by('name')[:10]  # Get first 10 students for demo
    
    # Calculate total school days and attendance for the session
    current_session = Session.get_current_session()
    if current_session:
        # Calculate total school days from session start to today or session end
        from datetime import timedelta
        today = date.today()
        session_start = current_session.start_date
        session_end = min(current_session.end_date, today)
        
        # Calculate total school days up to exam date
        exam_date = exam.exam_date if exam.exam_date else date.today()
        session_end_for_exam = min(exam_date, session_end)
        total_days = (session_end_for_exam - session_start).days + 1
    else:
        total_days = 200  # Default value
    
    marksheets_data = []
    for student in students:
        marksheets = Marksheet.objects.filter(student=student, exam=exam)
        
        # Calculate student attendance, leave, and absent days from actual database records
        if current_session:
            date_range = [current_session.start_date, min(current_session.end_date, date.today())]
        else:
            # Use current academic year if no session
            from datetime import timedelta
            today = date.today()
            year_start = today.replace(month=4, day=1) if today.month >= 4 else today.replace(year=today.year-1, month=4, day=1)
            date_range = [year_start, today]
        
        # Get actual attendance data from StudentAttendance model
        student_present_days = StudentAttendance.objects.filter(
            student=student, date__range=date_range, status='present'
        ).count()
        
        student_leave_days = StudentAttendance.objects.filter(
            student=student, date__range=date_range, status='leave'
        ).count()
        
        student_absent_days = StudentAttendance.objects.filter(
            student=student, date__range=date_range, status='absent'
        ).count()
        
        # If no attendance records exist, use reasonable defaults
        if student_present_days == 0 and student_leave_days == 0 and student_absent_days == 0:
            student_present_days = 165
            student_leave_days = 15
            student_absent_days = 20
        
        # Total attendance days = present + leave (leave is excused attendance)
        student_attendance_days = student_present_days + student_leave_days
        
        if marksheets.exists():
            # Calculate totals
            total_marks = sum(m.subject.max_marks for m in marksheets)
            obtained_marks = sum(m.marks_obtained for m in marksheets)
            percentage = (obtained_marks / total_marks * 100) if total_marks > 0 else 0
            
            # Overall grade and GPA
            if percentage >= 90:
                overall_grade = 'A+'
                gpa = round(3.6 + (percentage - 90) * 0.4 / 10, 2)
            elif percentage >= 80:
                overall_grade = 'A'
                gpa = round(3.2 + (percentage - 80) * 0.4 / 10, 2)
            elif percentage >= 70:
                overall_grade = 'B+'
                gpa = round(2.8 + (percentage - 70) * 0.4 / 10, 2)
            elif percentage >= 60:
                overall_grade = 'B'
                gpa = round(2.4 + (percentage - 60) * 0.4 / 10, 2)
            elif percentage >= 50:
                overall_grade = 'C+'
                gpa = round(2.0 + (percentage - 50) * 0.4 / 10, 2)
            elif percentage >= 40:
                overall_grade = 'C'
                gpa = round(1.6 + (percentage - 40) * 0.4 / 10, 2)
            elif percentage >= 30:
                overall_grade = 'D+'
                gpa = round(1.2 + (percentage - 30) * 0.4 / 10, 2)
            elif percentage >= 20:
                overall_grade = 'D'
                gpa = round(0.8 + (percentage - 20) * 0.4 / 10, 2)
            else:
                overall_grade = 'E'
                gpa = round((percentage) * 0.8 / 20, 2)
            
            # Overall status - FAIL only for grades C, D+, D, and E
            failed_subjects = marksheets.filter(marks_obtained__lt=models.F('subject__pass_marks')).count()
            overall_status = 'FAIL' if overall_grade in ['C', 'D+', 'D', 'E'] else 'PASS'
            
            # Calculate total grade points (GPA)
            total_grade_points = sum(m.grade_point for m in marksheets) / len(marksheets) if marksheets else 0
            
            marksheets_data.append({
                'student': student,
                'marksheets': marksheets,
                'total_marks': total_marks,
                'obtained_marks': obtained_marks,
                'percentage': round(percentage, 2),
                'overall_grade': overall_grade,
                'overall_status': overall_status,
                'failed_subjects': failed_subjects,
                'total_grade_points': round(total_grade_points, 2),
                'gpa': gpa,
                'total_school_days': total_days,
                'student_attendance_days': student_attendance_days,
                'student_present_days': student_present_days,
                'student_leave_days': student_leave_days,
                'student_absent_days': student_absent_days
            })
    
    # Get current Nepali date using our NepaliCalendar class
    try:
        current_nepali_date_dict = NepaliCalendar.get_current_nepali_date()
        current_nepali_date = NepaliCalendar.format_nepali_date(current_nepali_date_dict, 'short')
    except:
        current_nepali_date = '2082/08/15'  # Fallback date
    
    # Add cache busting and debug info
    context = {
        'exam': exam,
        'school': school,
        'marksheets_data': marksheets_data,
        'current_date': datetime.now().strftime('%B %d, %Y'),
        'current_nepali_date': current_nepali_date,
        'cache_buster': datetime.now().timestamp(),
        'debug_info': f'Updated at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    }
    
    # Set no-cache headers
    response = render(request, 'class_marksheets_redesigned.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

def generate_class_marksheets_see_style(request, exam_id):
    """Generate SEE-style marksheets for all students in an exam"""
    exam = get_object_or_404(Exam, id=exam_id)
    school = SchoolDetail.get_current_school()
    students = Student.objects.filter(student_class=exam.class_name).order_by('name')
    
    marksheets_data = []
    for student in students:
        marksheets = Marksheet.objects.filter(student=student, exam=exam)
        
        if marksheets.exists():
            # Calculate totals
            total_marks = sum(m.subject.max_marks for m in marksheets)
            obtained_marks = sum(m.marks_obtained for m in marksheets)
            percentage = (obtained_marks / total_marks * 100) if total_marks > 0 else 0
            
            # Overall grade
            if percentage >= 90:
                overall_grade = 'A+'
            elif percentage >= 80:
                overall_grade = 'A'
            elif percentage >= 70:
                overall_grade = 'B+'
            elif percentage >= 60:
                overall_grade = 'B'
            elif percentage >= 50:
                overall_grade = 'C+'
            elif percentage >= 40:
                overall_grade = 'C'
            elif percentage >= 30:
                overall_grade = 'D+'
            elif percentage >= 20:
                overall_grade = 'D'
            else:
                overall_grade = 'E'
            
            # Overall status
            failed_subjects = marksheets.filter(marks_obtained__lt=models.F('subject__pass_marks')).count()
            overall_status = 'Pass' if failed_subjects == 0 else 'Fail'
            
            # Calculate total grade points (GPA)
            total_grade_points = sum(m.grade_point for m in marksheets) / len(marksheets) if marksheets else 0
            
            marksheets_data.append({
                'student': student,
                'marksheets': marksheets,
                'total_marks': total_marks,
                'obtained_marks': obtained_marks,
                'percentage': round(percentage, 2),
                'overall_grade': overall_grade,
                'overall_status': overall_status,
                'failed_subjects': failed_subjects,
                'total_grade_points': round(total_grade_points, 2)
            })
    
    context = {
        'exam': exam,
        'school': school,
        'marksheets_data': marksheets_data,
        'current_date': datetime.now().strftime('%B %d, %Y')
    }
    
    # Set no-cache headers
    response = render(request, 'generate-class-marksheets-see-style.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

def generate_class_marksheets_print_see_style(request, exam_id):
    """Generate improved SEE-style marksheets for printing in A4 format"""
    exam = get_object_or_404(Exam, id=exam_id)
    school = SchoolDetail.get_current_school()
    students = Student.objects.filter(student_class=exam.class_name).order_by('name')
    
    marksheets_data = []
    for student in students:
        marksheets = Marksheet.objects.filter(student=student, exam=exam)
        
        if marksheets.exists():
            # Calculate totals
            total_marks = sum(m.subject.max_marks for m in marksheets)
            obtained_marks = sum(m.marks_obtained for m in marksheets)
            percentage = (obtained_marks / total_marks * 100) if total_marks > 0 else 0
            
            # Overall grade
            if percentage >= 90:
                overall_grade = 'A+'
            elif percentage >= 80:
                overall_grade = 'A'
            elif percentage >= 70:
                overall_grade = 'B+'
            elif percentage >= 60:
                overall_grade = 'B'
            elif percentage >= 50:
                overall_grade = 'C+'
            elif percentage >= 40:
                overall_grade = 'C'
            elif percentage >= 30:
                overall_grade = 'D+'
            elif percentage >= 20:
                overall_grade = 'D'
            else:
                overall_grade = 'E'
            
            # Overall status
            failed_subjects = marksheets.filter(marks_obtained__lt=models.F('subject__pass_marks')).count()
            overall_status = 'Pass' if failed_subjects == 0 else 'Fail'
            
            # Calculate total grade points (GPA)
            total_grade_points = sum(m.grade_point for m in marksheets) / len(marksheets) if marksheets else 0
            
            marksheets_data.append({
                'student': student,
                'marksheets': marksheets,
                'total_marks': total_marks,
                'obtained_marks': obtained_marks,
                'percentage': round(percentage, 2),
                'overall_grade': overall_grade,
                'overall_status': overall_status,
                'failed_subjects': failed_subjects,
                'total_grade_points': round(total_grade_points, 2)
            })
    
    context = {
        'exam': exam,
        'school': school,
        'marksheets_data': marksheets_data,
        'current_date': datetime.now().strftime('%B %d, %Y')
    }
    
    # Set no-cache headers for fresh content
    response = render(request, 'generate-class-marksheets-print-see-style.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

def generate_sarathi_pathshala_marksheets(request, exam_id):
    """Generate SARATHI PATHSHALA specific grade sheets"""
    exam = get_object_or_404(Exam, id=exam_id)
    students = Student.objects.filter(student_class=exam.class_name).order_by('name')
    
    marksheets_data = []
    for student in students:
        marksheets = Marksheet.objects.filter(student=student, exam=exam)
        
        if marksheets.exists():
            # Calculate totals
            total_marks = sum(m.subject.max_marks for m in marksheets)
            obtained_marks = sum(m.marks_obtained for m in marksheets)
            percentage = (obtained_marks / total_marks * 100) if total_marks > 0 else 0
            
            # Overall grade
            if percentage >= 90:
                overall_grade = 'A+'
            elif percentage >= 80:
                overall_grade = 'A'
            elif percentage >= 70:
                overall_grade = 'B+'
            elif percentage >= 60:
                overall_grade = 'B'
            elif percentage >= 50:
                overall_grade = 'C+'
            elif percentage >= 40:
                overall_grade = 'C'
            elif percentage >= 30:
                overall_grade = 'D+'
            elif percentage >= 20:
                overall_grade = 'D'
            else:
                overall_grade = 'E'
            
            # Overall status
            failed_subjects = marksheets.filter(marks_obtained__lt=models.F('subject__pass_marks')).count()
            overall_status = 'Pass' if failed_subjects == 0 else 'Fail'
            
            # Calculate total grade points (GPA)
            total_grade_points = sum(m.grade_point for m in marksheets) / len(marksheets) if marksheets else 0
            
            marksheets_data.append({
                'student': student,
                'marksheets': marksheets,
                'total_marks': total_marks,
                'obtained_marks': obtained_marks,
                'percentage': round(percentage, 2),
                'overall_grade': overall_grade,
                'overall_status': overall_status,
                'failed_subjects': failed_subjects,
                'total_grade_points': round(total_grade_points, 2)
            })
    
    context = {
        'exam': exam,
        'marksheets_data': marksheets_data,
        'current_date': datetime.now().strftime('%B %d, %Y')
    }
    
    # Set no-cache headers for fresh content
    response = render(request, 'sarathi_pathshala_marksheet.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

def generate_sarathi_pathshala_see_marksheets(request, exam_id):
    """Generate SARATHI PATHSHALA SEE Style grade sheets"""
    exam = get_object_or_404(Exam, id=exam_id)
    students = Student.objects.filter(student_class=exam.class_name).order_by('name')
    
    marksheets_data = []
    for student in students:
        marksheets = Marksheet.objects.filter(student=student, exam=exam)
        
        if marksheets.exists():
            # Calculate totals
            total_marks = sum(m.subject.max_marks for m in marksheets)
            obtained_marks = sum(m.marks_obtained for m in marksheets)
            percentage = (obtained_marks / total_marks * 100) if total_marks > 0 else 0
            
            # Overall grade
            if percentage >= 90:
                overall_grade = 'A+'
            elif percentage >= 80:
                overall_grade = 'A'
            elif percentage >= 70:
                overall_grade = 'B+'
            elif percentage >= 60:
                overall_grade = 'B'
            elif percentage >= 50:
                overall_grade = 'C+'
            elif percentage >= 40:
                overall_grade = 'C'
            elif percentage >= 30:
                overall_grade = 'D+'
            elif percentage >= 20:
                overall_grade = 'D'
            else:
                overall_grade = 'E'
            
            # Overall status
            failed_subjects = marksheets.filter(marks_obtained__lt=models.F('subject__pass_marks')).count()
            overall_status = 'Pass' if failed_subjects == 0 else 'Fail'
            
            # Calculate total grade points (GPA)
            total_grade_points = sum(m.grade_point for m in marksheets) / len(marksheets) if marksheets else 0
            
            marksheets_data.append({
                'student': student,
                'marksheets': marksheets,
                'total_marks': total_marks,
                'obtained_marks': obtained_marks,
                'percentage': round(percentage, 2),
                'overall_grade': overall_grade,
                'overall_status': overall_status,
                'failed_subjects': failed_subjects,
                'total_grade_points': round(total_grade_points, 2)
            })
    
    context = {
        'exam': exam,
        'marksheets_data': marksheets_data,
        'current_date': datetime.now().strftime('%B %d, %Y')
    }
    
    # Set no-cache headers for fresh content
    response = render(request, 'sarathi_pathshala_see_marksheet.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

def grade_sheet_certificate(request):
    """Standalone Grade Sheet Certificate template"""
    return render(request, 'grade_sheet_certificate.html')

def student_marksheet_finder(request):
    """Helper view to find valid student-exam combinations"""
    students = Student.objects.all().order_by('name')[:20]  # First 20 students
    exams = Exam.objects.all().order_by('-exam_date')[:10]  # First 10 exams
    
    # Get some existing marksheets as examples
    existing_marksheets = Marksheet.objects.select_related('student', 'exam').distinct('student', 'exam')[:10]
    
    context = {
        'students': students,
        'exams': exams,
        'existing_marksheets': existing_marksheets
    }
    
    return render(request, 'student_marksheet_finder.html', context)

def populate_grade_sheet_certificate(request):
    """Generate populated grade sheet certificates - same as generate_class_marksheets_print_see_style"""
    # Get exam_id from request or use the latest exam
    exam_id = request.GET.get('exam_id')
    if exam_id:
        try:
            exam = get_object_or_404(Exam, id=exam_id)
        except:
            exam = Exam.objects.order_by('-exam_date').first()
    else:
        exam = Exam.objects.order_by('-exam_date').first()
    
    if not exam:
        # Create sample data if no exam exists
        context = {
            'marksheets_data': [{
                'student': type('obj', (object,), {
                    'name': 'SAMPLE STUDENT',
                    'reg_number': '001',
                    'student_class': '10',
                    'section': 'A'
                }),
                'marksheets': [{
                    'subject': type('obj', (object,), {'name': 'English'}),
                    'marks_obtained': 85,
                    'grade': 'A',
                    'status': 'Pass'
                }],
                'total_marks': 100,
                'obtained_marks': 85,
                'percentage': 85.0,
                'overall_grade': 'A',
                'overall_status': 'Pass',
                'total_grade_points': 3.6
            }],
            'exam': type('obj', (object,), {
                'exam_type': 'Terminal',
                'session': '2081 BS'
            }),
            'current_date': datetime.now().strftime('%B %d, %Y')
        }
        return render(request, 'generate-class-marksheets-print-see-style.html', context)
    
    students = Student.objects.filter(student_class=exam.class_name).order_by('name')
    
    marksheets_data = []
    for student in students:
        marksheets = Marksheet.objects.filter(student=student, exam=exam)
        
        if marksheets.exists():
            # Calculate totals
            total_marks = sum(m.subject.max_marks for m in marksheets)
            obtained_marks = sum(m.marks_obtained for m in marksheets)
            percentage = (obtained_marks / total_marks * 100) if total_marks > 0 else 0
            
            # Overall grade
            if percentage >= 90: overall_grade = 'A+'
            elif percentage >= 80: overall_grade = 'A'
            elif percentage >= 70: overall_grade = 'B+'
            elif percentage >= 60: overall_grade = 'B'
            elif percentage >= 50: overall_grade = 'C+'
            elif percentage >= 40: overall_grade = 'C'
            elif percentage >= 30: overall_grade = 'D+'
            elif percentage >= 20: overall_grade = 'D'
            else: overall_grade = 'E'
            
            # Overall status
            failed_subjects = marksheets.filter(marks_obtained__lt=models.F('subject__pass_marks')).count()
            overall_status = 'Pass' if failed_subjects == 0 else 'Fail'
            
            # Calculate total grade points (GPA)
            total_grade_points = sum(m.grade_point for m in marksheets) / len(marksheets) if marksheets else 0
            
            marksheets_data.append({
                'student': student,
                'marksheets': marksheets,
                'total_marks': total_marks,
                'obtained_marks': obtained_marks,
                'percentage': round(percentage, 2),
                'overall_grade': overall_grade,
                'overall_status': overall_status,
                'failed_subjects': failed_subjects,
                'total_grade_points': round(total_grade_points, 2)
            })
    
    context = {
        'exam': exam,
        'marksheets_data': marksheets_data,
        'current_date': datetime.now().strftime('%B %d, %Y')
    }
    
    return render(request, 'generate-class-marksheets-print-see-style.html', context)

@permission_required('can_view_attendance')
def student_attendance_dashboard(request):
    """Student Attendance Dashboard with StudentAttendance model integration"""
    # Get unique classes and sections from students
    classes = Student.objects.values_list('student_class', flat=True).distinct().order_by('student_class')
    sections = Student.objects.values_list('section', flat=True).distinct().order_by('section')
    
    # Get all students by default
    students = Student.objects.all().order_by('name')
    
    # Get today's date
    today = date.today()
    
    # Get existing attendance for today
    today_attendance = StudentAttendance.objects.filter(date=today).select_related('student')
    attendance_dict = {att.student.id: att.status for att in today_attendance}
    
    # Add attendance status to each student
    for student in students:
        student.attendance_status = attendance_dict.get(student.id, 'present')
    
    context = {
        'classes': classes,
        'sections': sections,
        'students': students,
        'today': today.strftime('%Y-%m-%d'),
        'attendance_marked': len(attendance_dict) > 0
    }
    return render(request, 'student_attendance.html', context)

def print_bill(request):
    """Print bill page"""
    school = SchoolDetail.get_current_school()
    return render(request, 'print_bill.html', {'school': school})

@permission_required('can_view_expenses')
def student_daily_exp(request):
    """Student daily expenses page"""
    context = {
        'current_date': datetime.now().strftime('%B %d, %Y')
    }
    
    return render(request, 'student_daily_exp.html', context)

# Nepali Date API Endpoints
def get_nepali_date_api(request):
    """API to get current Nepali date information"""
    try:
        current_nepali_date = NepaliCalendar.get_current_nepali_date()
        current_session = get_current_nepali_year_session()
        
        return JsonResponse({
            'success': True,
            'nepali_date': {
                'year': current_nepali_date['year'],
                'month': current_nepali_date['month'],
                'day': current_nepali_date['day'],
                'month_name': current_nepali_date['month_name_en'],
                'formatted_full': NepaliCalendar.format_nepali_date(current_nepali_date, 'full_en'),
                'formatted_short': NepaliCalendar.format_nepali_date(current_nepali_date, 'short'),
            },
            'current_session': current_session,
            'nepali_months': NepaliCalendar.NEPALI_MONTHS_EN
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def convert_date_api(request):
    """API to convert English date to Nepali date"""
    try:
        english_date = request.GET.get('date')
        if not english_date:
            return JsonResponse({'success': False, 'error': 'Date parameter required'})
        
        nepali_date_dict = NepaliCalendar.english_to_nepali_date(english_date)
        
        return JsonResponse({
            'success': True,
            'english_date': english_date,
            'nepali_date': {
                'year': nepali_date_dict['year'],
                'month': nepali_date_dict['month'],
                'day': nepali_date_dict['day'],
                'month_name': nepali_date_dict['month_name_en'],
                'formatted_full': NepaliCalendar.format_nepali_date(nepali_date_dict, 'full_en'),
                'formatted_short': NepaliCalendar.format_nepali_date(nepali_date_dict, 'short'),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def get_nepali_sessions_api(request):
    """API to get available Nepali sessions"""
    try:
        # Generate sessions from 2082 to 2100
        sessions = []
        for year in range(2082, 2101):
            sessions.append({
                'value': f"{year}-{str(year+1)[-2:]}",
                'label': f"{year}-{str(year+1)[-2:]} BS"
            })
        
        current_session = get_current_nepali_year_session()
        
        return JsonResponse({
            'success': True,
            'sessions': sessions,
            'current_session': current_session
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
def delete_subject(request):
    """Delete a subject"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            subject_id = data.get('subject_id')
            
            if not subject_id:
                return JsonResponse({'success': False, 'error': 'Subject ID required'})
            
            subject = get_object_or_404(Subject, id=subject_id)
            subject_name = subject.name
            subject.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Subject "{subject_name}" deleted successfully'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def add_student_expense(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student = get_object_or_404(Student, id=data['student_id'])
            
            expense = StudentDailyExpense.objects.create(
                student=student,
                description=data['description'],
                amount=data['amount']
            )
            
            return JsonResponse({
                'success': True,
                'expense': {
                    'id': expense.id,
                    'description': expense.description,
                    'amount': float(expense.amount),
                    'time': expense.created_at.strftime('%H:%M')
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def delete_student_expense(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            expense = get_object_or_404(StudentDailyExpense, id=data['expense_id'])
            expense.delete()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def get_student_expenses_api(request, student_id):
    try:
        student = get_object_or_404(Student, id=student_id)
        today = date.today()
        expenses = StudentDailyExpense.objects.filter(
            student=student,
            expense_date=today
        ).order_by('-created_at')
        
        expenses_data = []
        total_amount = 0
        
        for expense in expenses:
            expenses_data.append({
                'id': expense.id,
                'description': expense.description,
                'amount': float(expense.amount),
                'time': expense.created_at.strftime('%H:%M')
            })
            total_amount += float(expense.amount)
        
        return JsonResponse({
            'success': True,
            'student': {
                'id': student.id,
                'name': student.name,
                'class': student.student_class,
                'roll': student.reg_number
            },
            'expenses': expenses_data,
            'total_amount': total_amount
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def get_class_expenses_api(request, class_name):
    try:
        today = date.today()
        expenses = StudentDailyExpense.objects.filter(
            student__student_class=class_name,
            expense_date=today
        ).select_related('student').order_by('-created_at')
        
        expenses_data = []
        total_amount = 0
        students_with_expenses = {}
        
        for expense in expenses:
            expense_data = {
                'id': expense.id,
                'description': expense.description,
                'amount': float(expense.amount),
                'time': expense.created_at.strftime('%H:%M'),
                'student_name': expense.student.name,
                'student_id': expense.student.id
            }
            expenses_data.append(expense_data)
            total_amount += float(expense.amount)
            
            # Group by student
            if expense.student.id not in students_with_expenses:
                students_with_expenses[expense.student.id] = {
                    'student': {
                        'id': expense.student.id,
                        'name': expense.student.name,
                        'class': expense.student.student_class,
                        'roll': expense.student.reg_number
                    },
                    'expenses': [],
                    'total': 0
                }
            
            students_with_expenses[expense.student.id]['expenses'].append(expense_data)
            students_with_expenses[expense.student.id]['total'] += float(expense.amount)
        
        return JsonResponse({
            'success': True,
            'class_name': class_name,
            'expenses': expenses_data,
            'students_with_expenses': list(students_with_expenses.values()),
            'total_amount': total_amount,
            'total_students': len(students_with_expenses)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def get_todays_all_expenses_api(request):
    try:
        today = date.today()
        expenses = StudentDailyExpense.objects.filter(
            expense_date=today
        ).select_related('student').order_by('-created_at')
        
        expenses_data = []
        total_amount = 0
        
        for expense in expenses:
            expenses_data.append({
                'id': expense.id,
                'description': expense.description,
                'amount': float(expense.amount),
                'expense_date': expense.expense_date.strftime('%Y-%m-%d'),
                'time': expense.created_at.strftime('%H:%M'),
                'student_id': expense.student.id,
                'student_name': expense.student.name,
                'student_reg_number': expense.student.reg_number,
                'student_class': expense.student.student_class
            })
            total_amount += float(expense.amount)
        
        return JsonResponse({
            'success': True,
            'expenses': expenses_data,
            'total_amount': total_amount,
            'total_count': len(expenses_data)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def school_settings_test(request):
    """Test view to debug template loading"""
    try:
        school = SchoolDetail.get_current_school()
        return render(request, 'school_settings_test.html', {'school': school})
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')

def registration(request):
    """Public registration page - no login required"""
    return render(request, 'registration.html')

@csrf_exempt
def register_student_api(request):
    """API endpoint to register new student"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Generate unique registration number
            reg_number = f"REG{datetime.now().year}{Student.objects.count() + 1:04d}"
            
            student = Student.objects.create(
                name=data['name'],
                student_class=data['student_class'],
                section=data['section'],
                gender=data['gender'],
                religion=data.get('religion', 'Hindu'),
                dob=data['dob'],
                address1=data['address1'],
                city=data['city'],
                mobile=data['mobile'],
                father_name=data['father_name'],
                father_mobile=data.get('father_mobile', ''),
                mother_name=data['mother_name'],
                admission_date=data['admission_date'],
                session=data['session'],
                reg_number=reg_number,
                transport=data.get('transport', '00_No Transport Service | 0 Rs.'),
                address2=data.get('address2', '')
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Registration successful',
                'reg_number': reg_number,
                'student_id': student.id
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})



def collection_dashboard(request):
    """Collection dashboard showing overview of all collections"""
    from datetime import timedelta
    
    today = date.today()
    
    # Get today's collection
    todays_collection = FeePayment.objects.filter(payment_date=today).aggregate(total=Sum('payment_amount'))['total'] or 0
    
    # Get weekly collection (last 7 days)
    week_start = today - timedelta(days=6)
    weekly_collection = FeePayment.objects.filter(payment_date__range=[week_start, today]).aggregate(total=Sum('payment_amount'))['total'] or 0
    
    # Get monthly collection (last 30 days)
    thirty_days_ago = today - timedelta(days=29)  # 30 days including today
    monthly_collection = FeePayment.objects.filter(payment_date__range=[thirty_days_ago, today]).aggregate(total=Sum('payment_amount'))['total'] or 0
    
    # Get yearly collection (current year)
    yearly_collection = FeePayment.objects.filter(payment_date__year=today.year).aggregate(total=Sum('payment_amount'))['total'] or 0
    
    context = {
        'todays_collection': todays_collection,
        'weekly_collection': weekly_collection,
        'monthly_collection': monthly_collection,
        'yearly_collection': yearly_collection,
    }
    
    return render(request, 'collection_dashboard.html', context)

def collection_details(request, period='today'):
    """Collection details page showing payments for specified period"""
    from datetime import timedelta
    
    today = date.today()
    
    # Define date ranges based on period
    if period == 'today':
        start_date = today
        end_date = today
        period_title = "Today's"
        date_range = today.strftime('%B %d, %Y')
    elif period == 'weekly':
        start_date = today - timedelta(days=6)
        end_date = today
        period_title = "Weekly"
        date_range = f"{start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')}"
    elif period == 'monthly':
        start_date = today.replace(day=1)
        end_date = today
        period_title = "Monthly"
        date_range = f"{today.strftime('%B %Y')}"
    elif period == 'yearly':
        start_date = today.replace(month=1, day=1)
        end_date = today
        period_title = "Yearly"
        date_range = f"{today.year}"
    else:
        # Default to today if invalid period
        start_date = today
        end_date = today
        period_title = "Today's"
        date_range = today.strftime('%B %d, %Y')
    
    # Get payments for the period (FeePayment)
    payments = FeePayment.objects.filter(
        payment_date__range=[start_date, end_date]
    ).select_related('student').order_by('-payment_date', '-id')
    
    # Get daily expenses for the period
    daily_expenses = StudentDailyExpense.objects.filter(
        expense_date__range=[start_date, end_date]
    ).select_related('student').order_by('-expense_date', '-id')
    
    # Process fee types for display
    for payment in payments:
        payment.fee_types_list = []
        if payment.fee_types:
            try:
                fee_types = json.loads(payment.fee_types)
                payment.fee_types_list = fee_types
            except json.JSONDecodeError:
                pass
    
    # Calculate totals (FeePayment + StudentDailyExpense)
    fee_total = payments.aggregate(total=Sum('payment_amount'))['total'] or 0
    expense_total = daily_expenses.aggregate(total=Sum('amount'))['total'] or 0
    total_amount = fee_total + expense_total
    total_payments = payments.count() + daily_expenses.count()
    
    # Payment method summary
    payment_methods = payments.values('payment_method').annotate(
        count=Count('id'),
        total=Sum('payment_amount')
    ).order_by('-total')
    
    context = {
        'payments': payments,
        'daily_expenses': daily_expenses,
        'period_title': period_title,
        'date_range': date_range,
        'total_amount': total_amount,
        'total_payments': total_payments,
        'fee_total': fee_total,
        'expense_total': expense_total,
        'payment_methods': payment_methods,
        'period': period,
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'collection_details.html', context)

def weekly_collection_details(request):
    """Weekly collection details view"""
    return collection_details(request, 'weekly')

def monthly_collection_details(request):
    """Monthly collection details view - Last 30 days"""
    from datetime import timedelta
    
    today = date.today()
    
    # Get monthly collection (last 30 days)
    start_date = today - timedelta(days=29)  # 30 days including today
    end_date = today
    period_title = "Monthly (Last 30 Days)"
    date_range = f"{start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')}"
    
    # Get payments for the period (FeePayment)
    payments = FeePayment.objects.filter(
        payment_date__range=[start_date, end_date]
    ).select_related('student').order_by('-payment_date', '-id')
    
    # Get daily expenses for the period
    daily_expenses = StudentDailyExpense.objects.filter(
        expense_date__range=[start_date, end_date]
    ).select_related('student').order_by('-expense_date', '-id')
    
    # Process fee types for display
    for payment in payments:
        payment.fee_types_list = []
        if payment.fee_types:
            try:
                fee_types = json.loads(payment.fee_types)
                payment.fee_types_list = fee_types
            except json.JSONDecodeError:
                pass
    
    # Calculate totals (FeePayment + StudentDailyExpense)
    fee_total = payments.aggregate(total=Sum('payment_amount'))['total'] or 0
    expense_total = daily_expenses.aggregate(total=Sum('amount'))['total'] or 0
    total_amount = fee_total + expense_total
    total_payments = payments.count() + daily_expenses.count()
    
    # Payment method summary
    payment_methods = payments.values('payment_method').annotate(
        count=Count('id'),
        total=Sum('payment_amount')
    ).order_by('-total')
    
    # Debug: Check if we have any data at all
    all_payments_count = FeePayment.objects.count()
    all_expenses_count = StudentDailyExpense.objects.count()
    
    # If no data for last 30 days, get some recent data for display
    if not payments.exists() and not daily_expenses.exists():
        # Get last 30 payments regardless of date to show some data
        payments = FeePayment.objects.select_related('student').order_by('-payment_date', '-id')[:30]
        daily_expenses = StudentDailyExpense.objects.select_related('student').order_by('-expense_date', '-id')[:30]
        
        # Update totals if we found some data
        if payments.exists() or daily_expenses.exists():
            fee_total = sum(p.payment_amount for p in payments)
            expense_total = sum(e.amount for e in daily_expenses)
            total_amount = fee_total + expense_total
            total_payments = len(payments) + len(daily_expenses)
            period_title = "Recent Transactions"
            date_range = "Last 30 transactions (no data in last 30 days)"
    
    # Ensure all required template variables are present
    context = {
        'payments': payments,
        'daily_expenses': daily_expenses,
        'period_title': period_title,
        'date_range': date_range,
        'total_amount': total_amount,
        'total_payments': total_payments,
        'fee_total': fee_total,
        'expense_total': expense_total,
        'payment_methods': payment_methods,
        'period': 'monthly',
        'start_date': start_date,
        'end_date': end_date,
        'debug_info': {
            'all_payments_count': all_payments_count,
            'all_expenses_count': all_expenses_count,
            'last_30_days_payments': FeePayment.objects.filter(payment_date__range=[start_date, end_date]).count(),
            'last_30_days_expenses': StudentDailyExpense.objects.filter(expense_date__range=[start_date, end_date]).count(),
            'date_range_used': f'{start_date} to {end_date}',
        }
    }
    
    return render(request, 'monthly_collection_details.html', context)

def yearly_collection_details(request):
    """Yearly collection details view"""
    return collection_details(request, 'yearly')

# Missing API function for subjects by class
def api_subjects_by_class(request, class_name):
    """API to get subjects by class - alias for subjects_by_class_api"""
    return subjects_by_class_api(request, class_name)

@permission_required('can_view_settings')
def school_settings(request):
    try:
        from .models import SchoolDetail
        school = SchoolDetail.get_current_school()
        
        if request.method == 'POST':
            # Handle form submission
            school.school_name = request.POST.get('school_name', school.school_name)
            school.address = request.POST.get('address', school.address)
            school.phone = request.POST.get('phone', school.phone)
            school.email = request.POST.get('email', school.email)
            
            # Handle logo upload
            if 'logo' in request.FILES:
                school.logo = request.FILES['logo']
            
            school.save()
            messages.success(request, 'School settings updated successfully!')
            return redirect('school_settings')
        
        return render(request, 'school_settings.html', {'school': school})
    except Exception as e:
        # Fallback with default values if there's an issue
        default_school = type('obj', (object,), {
            'school_name': 'Everest Academy',
            'address': 'Kathmandu, Nepal',
            'phone': '+977-1-4444444',
            'email': 'info@everestacademy.edu.np',
            'logo': None
        })
        return render(request, 'school_settings.html', {'school': default_school})

def website_settings(request):
    from .models import HeroSlider, Blog
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_hero':
            title = request.POST.get('hero_title', 'New Hero Image')
            HeroSlider.objects.create(
                title=title,
                image=request.FILES['hero_image'],
                is_active=True
            )
            messages.success(request, 'Hero image added successfully!')
        
        elif action == 'update_hero':
            hero_id = request.POST.get('hero_id')
            hero = get_object_or_404(HeroSlider, id=hero_id)
            hero.title = request.POST.get('hero_title')
            if 'hero_image' in request.FILES:
                hero.image = request.FILES['hero_image']
            hero.save()
            messages.success(request, 'Hero image updated successfully!')
        
        elif action == 'delete_hero':
            hero_id = request.POST.get('hero_id')
            HeroSlider.objects.filter(id=hero_id).delete()
            messages.success(request, 'Hero image deleted successfully!')
        
        elif action == 'add_blog':
            Blog.objects.create(
                heading=request.POST.get('blog_heading'),
                description=request.POST.get('blog_description'),
                photo=request.FILES['blog_image']
            )
            messages.success(request, 'Blog post added successfully!')
        
        elif action == 'update_blog':
            blog_id = request.POST.get('blog_id')
            blog = get_object_or_404(Blog, id=blog_id)
            blog.heading = request.POST.get('blog_heading')
            blog.description = request.POST.get('blog_description')
            if 'blog_image' in request.FILES:
                blog.photo = request.FILES['blog_image']
            blog.save()
            messages.success(request, 'Blog post updated successfully!')
        
        elif action == 'delete_blog':
            blog_id = request.POST.get('blog_id')
            Blog.objects.filter(id=blog_id).delete()
            messages.success(request, 'Blog post deleted successfully!')
        
        elif action == 'add_welcome':
            WelcomeSection.objects.update(is_active=False)
            welcome_data = {
                'title': request.POST.get('welcome_title'),
                'content': request.POST.get('welcome_content'),
                'is_active': True
            }
            if 'welcome_image' in request.FILES:
                welcome_data['image'] = request.FILES['welcome_image']
            WelcomeSection.objects.create(**welcome_data)
            messages.success(request, 'Welcome section added successfully!')
        
        elif action == 'update_welcome':
            welcome_id = request.POST.get('welcome_id')
            welcome = get_object_or_404(WelcomeSection, id=welcome_id)
            welcome.title = request.POST.get('welcome_title')
            welcome.content = request.POST.get('welcome_content')
            if 'welcome_image' in request.FILES:
                welcome.image = request.FILES['welcome_image']
            welcome.save()
            messages.success(request, 'Welcome section updated successfully!')
        
        elif action == 'delete_welcome':
            welcome_id = request.POST.get('welcome_id')
            WelcomeSection.objects.filter(id=welcome_id).delete()
            messages.success(request, 'Welcome section deleted successfully!')
        
        return redirect('website_settings')
    
    hero_images = HeroSlider.objects.all().order_by('order')
    blogs = Blog.objects.all().order_by('-created_at')
    welcome_sections = WelcomeSection.objects.all().order_by('-created_at')
    
    return render(request, 'website_settings.html', {
        'hero_images': hero_images,
        'blogs': blogs,
        'welcome_sections': welcome_sections
    })

def id_creation(request):
    """ID Creation page for generating student ID cards"""
    students = Student.objects.all().order_by('name')
    
    # Get unique classes from students
    classes = Student.objects.values_list('student_class', flat=True).distinct().order_by('student_class')
    
    # Add random photo URL to each student
    for student in students:
        student.random_photo_url = student.get_random_photo_url()
    
    return render(request, 'id_creation.html', {
        'students': students,
        'classes': classes
    })

def photo_management(request):
    """Photo management page for managing student photos"""
    students = Student.objects.all().order_by('name')
    return render(request, 'photo_management.html', {'students': students})

def photo_gallery(request):
    """Photo gallery page"""
    return render(request, 'photo_gallery.html')

@csrf_exempt
def assign_photo(request):
    """API to assign photo to student"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            return JsonResponse({'success': True, 'message': 'Photo assigned successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def remove_photo(request):
    """API to remove photo from student"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            return JsonResponse({'success': True, 'message': 'Photo removed successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})



def generate_id(request):
    student_id = request.GET.get('student_id')
    student_ids = request.GET.get('student_ids')
    
    try:
        school = SchoolDetail.get_current_school()
    except:
        school = None
    
    students_data = []
    
    if student_ids:
        # Bulk mode
        student_id_list = student_ids.split(',')
        students = Student.objects.filter(id__in=student_id_list)
        for student in students:
            students_data.append({
                'id': student.id,
                'name': student.name,
                'student_class': student.student_class,
                'section': student.section,
                'reg_number': student.reg_number,
                'dob': student.dob.strftime('%Y-%m-%d') if student.dob else '',
                'session': student.session,
                'mobile': student.mobile,
                'photo_url': student.get_random_photo_url()
            })
    elif student_id:
        # Single student mode
        try:
            student = Student.objects.get(id=student_id)
            students_data.append({
                'id': student.id,
                'name': student.name,
                'student_class': student.student_class,
                'section': student.section,
                'reg_number': student.reg_number,
                'dob': student.dob.strftime('%Y-%m-%d') if student.dob else '',
                'session': student.session,
                'mobile': student.mobile,
                'photo_url': student.get_random_photo_url()
            })
        except Student.DoesNotExist:
            return HttpResponse('Student not found', status=404)
    
    if not students_data:
        return HttpResponse('No students found', status=404)
    
    import json
    return render(request, 'generate_id.html', {
        'students': json.dumps(students_data),
        'school': school
    })

def print_id_cards(request):
    """Print ID cards with complete student database details"""
    student_ids = request.GET.get('student_ids', '')
    template = request.GET.get('template', '1')
    
    try:
        school = SchoolDetail.get_current_school()
    except:
        school = None
    
    if student_ids:
        student_id_list = [int(id.strip()) for id in student_ids.split(',') if id.strip()]
        students = Student.objects.filter(id__in=student_id_list).order_by('name')
    else:
        students = Student.objects.none()
    
    return render(request, 'print_id_cards.html', {
        'students': students,
        'school': school,
        'template': template
    })

def whatsapp_balance(request):
    """WhatsApp balance details page"""
    return render(request, 'whatsapp_balance.html')

def fee_payment_report_dashboard(request):
    """Fee Payment Report Dashboard"""
    from django.db.models import Sum, Count
    from datetime import datetime
    
    # Calculate statistics
    total_collected = FeePayment.objects.aggregate(total=Sum('payment_amount'))['total'] or 0
    total_students = Student.objects.count()
    total_payments = FeePayment.objects.count()
    
    # Calculate pending fees
    total_pending = 0
    for student in Student.objects.all():
        try:
            fee_structure = FeeStructure.objects.get(class_name=student.student_class)
            student_total_fee = (
                fee_structure.admission_fee +
                fee_structure.monthly_fee * 12 +
                fee_structure.tuition_fee * 12 +
                fee_structure.examination_fee +
                fee_structure.library_fee +
                fee_structure.sports_fee +
                fee_structure.laboratory_fee +
                fee_structure.computer_fee +
                fee_structure.transportation_fee * 12
            )
        except FeeStructure.DoesNotExist:
            student_total_fee = 60000
        
        student_paid = FeePayment.objects.filter(student=student).aggregate(total=Sum('payment_amount'))['total'] or 0
        student_pending = max(0, student_total_fee - student_paid)
        total_pending += student_pending
    
    # Get recent payments
    recent_payments = FeePayment.objects.select_related('student').order_by('-payment_date')[:10]
    
    context = {
        'total_collected': total_collected,
        'total_pending': total_pending,
        'total_students': total_students,
        'total_payments': total_payments,
        'recent_payments': recent_payments,
        'current_date': datetime.now().strftime('%B %d, %Y')
    }
    
    return render(request, 'fee_payment_report.html', context)

@csrf_exempt
def send_fee_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = data['student_id']
            email = data['email']
            student_name = data['student_name']
            
            student = get_object_or_404(Student, id=student_id)
            
            # Get fee details
            try:
                fee_structure = FeeStructure.objects.get(class_name=student.student_class)
                total_fee = (
                    fee_structure.admission_fee +
                    fee_structure.monthly_fee * 12 +
                    fee_structure.tuition_fee * 12 +
                    fee_structure.examination_fee +
                    fee_structure.library_fee +
                    fee_structure.sports_fee +
                    fee_structure.laboratory_fee +
                    fee_structure.computer_fee +
                    fee_structure.transportation_fee * 12
                )
            except FeeStructure.DoesNotExist:
                total_fee = 60000
            
            # Calculate paid amount
            payments = FeePayment.objects.filter(student=student)
            paid_amount = sum(float(payment.payment_amount) for payment in payments)
            
            # Add daily expenses
            daily_expenses = StudentDailyExpense.objects.filter(student=student).aggregate(
                total_expenses=Sum('amount')
            )['total_expenses'] or 0
            
            total_fee += float(daily_expenses)
            pending_amount = max(0, total_fee - paid_amount)
            
            # Create email content
            subject = f'Fee Statement - {student_name}'
            message = f'''Dear Parent,

Greetings from our school!

Fee Statement for {student_name}:

Total Outstanding: Rs{pending_amount:,.0f}
Amount Paid: Rs{paid_amount:,.0f}

Kindly visit the school office at your earliest convenience to complete the payment.

For any queries, please feel free to contact us.

Thank you for your cooperation.

Best regards,
School Administration'''
            
            # Send email
            send_mail(
                subject,
                message,
                'noreply@school.com',  # From email
                [email],  # To email
                fail_silently=False,
            )
            
            return JsonResponse({'success': True, 'message': 'Email sent successfully'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
@csrf_exempt
@csrf_exempt
def update_enquiry_status_api(request):
    """API endpoint to update contact enquiry status"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            enquiry_id = data.get('enquiry_id')
            status = data.get('status')
            remarks = data.get('remarks', '')
            
            if not enquiry_id or not status:
                return JsonResponse({'success': False, 'error': 'Enquiry ID and status are required'})
            
            enquiry = get_object_or_404(ContactEnquiry, id=enquiry_id)
            enquiry.status = status
            if remarks:
                enquiry.remarks = remarks
            enquiry.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Enquiry status updated to {status.title()}',
                'enquiry_id': enquiry.id,
                'new_status': status
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def update_registration_status_api(request):
    """API endpoint to update student registration status"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            registration_id = data.get('registration_id')
            status = data.get('status')
            remarks = data.get('remarks', '')
            
            if not registration_id or not status:
                return JsonResponse({'success': False, 'error': 'Registration ID and status are required'})
            
            registration = get_object_or_404(StudentRegistration, id=registration_id)
            registration.status = status
            if remarks:
                registration.remarks = remarks
            registration.save()
            
            # If approved, create student record
            if status == 'approved':
                if not Student.objects.filter(reg_number=registration.application_number).exists():
                    Student.objects.create(
                        name=registration.name,
                        student_class=registration.student_class,
                        section=registration.section,
                        gender=registration.gender,
                        dob=registration.dob,
                        address1=registration.address,
                        city=registration.city,
                        mobile=registration.mobile,
                        father_name=registration.father_name,
                        mother_name=registration.mother_name,
                        religion=registration.religion,
                        reg_number=registration.application_number,
                        admission_date=registration.registration_date,
                        session=get_current_nepali_year_session(),
                        transport='00_No Transport Service | 0 Rs.'
                    )
                    message = f'Registration approved and student {registration.name} added to system'
                else:
                    message = f'Registration status updated to {status.title()}'
            else:
                message = f'Registration status updated to {status.title()}'
            
            return JsonResponse({
                'success': True,
                'message': message,
                'registration_id': registration.id,
                'new_status': status
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def admin_login(request):
    """Admin login page - handles /login/ URL"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        admin = None
        
        # Try MD5 hash first
        try:
            import hashlib
            password_hash = hashlib.md5(password.encode()).hexdigest()
            admin = AdminLogin.objects.get(username=username, password=password_hash, is_active=True)
        except AdminLogin.DoesNotExist:
            # Try plain text password as fallback
            try:
                admin = AdminLogin.objects.get(username=username, password=password, is_active=True)
            except AdminLogin.DoesNotExist:
                messages.error(request, 'Invalid username or password')
                return render(request, 'admin_login.html')
        
        # Set session data
        request.session['admin_logged_in'] = True
        request.session['admin_username'] = admin.username
        request.session['is_super_admin'] = admin.is_super_admin
        
        # Set all permissions in session
        request.session['can_create_users'] = admin.can_create_users
        request.session['can_delete_users'] = admin.can_delete_users
        request.session['can_view_dashboard'] = admin.can_view_dashboard
        request.session['can_view_charts'] = admin.can_view_charts
        request.session['can_view_stats'] = admin.can_view_stats
        request.session['can_view_students'] = admin.can_view_students
        request.session['can_view_teachers'] = admin.can_view_teachers
        request.session['can_view_reports'] = admin.can_view_reports
        request.session['can_view_marksheet'] = admin.can_view_marksheet
        request.session['can_view_fees'] = admin.can_view_fees
        request.session['can_view_receipts'] = admin.can_view_receipts
        request.session['can_view_expenses'] = admin.can_view_expenses
        request.session['can_view_settings'] = admin.can_view_settings
        
        # Redirect based on permissions
        if not admin.can_create_users and not admin.can_delete_users and not admin.is_super_admin:
            return redirect('basic_dashboard')
        else:
            return redirect('dashboard')
    
    return render(request, 'admin_login.html')

def basic_dashboard(request):
    """Basic dashboard for users with limited permissions"""
    from datetime import datetime
    
    # Get basic statistics
    total_students = Student.objects.count()
    current_date = datetime.now().strftime('%B %d, %Y')
    
    context = {
        'total_students': total_students,
        'current_date': current_date,
        'user_username': request.session.get('admin_username', 'User')
    }
    
    return render(request, 'basic_dashboard.html', context)

def admin_logout(request):
    """Admin logout"""
    request.session.flush()
    return redirect('admin_login')

def public_registration(request):
    """Public registration form for new student admissions"""
    if request.method == 'POST':
        try:
            # Use current Nepali session for new students
            session_name = get_current_nepali_year_session()
            
            # Create new student from form data
            student = Student(
                name=request.POST.get('name'),
                student_class=request.POST.get('class'),
                section=request.POST.get('section', 'A'),
                address1=request.POST.get('address1'),
                city=request.POST.get('city'),
                mobile=request.POST.get('mobile'),
                gender=request.POST.get('gender'),
                religion=request.POST.get('religion', 'Hindu'),
                dob=request.POST.get('dob'),
                admission_date=date.today(),
                session=session_name,
                father_name=request.POST.get('fatherName'),
                mother_name=request.POST.get('motherName'),
                transport='00_No Transport Service | 0 Rs.',
                reg_number=f'REG{date.today().year}{Student.objects.count()+1:04d}'
            )
            student.save()
            
            # Success message
            context = {
                'success': True,
                'message': f'Registration submitted successfully! Registration Number: {student.reg_number}',
                'student': student
            }
            return render(request, 'public_registration.html', context)
            
        except Exception as e:
            context = {
                'error': f'Error submitting registration: {str(e)}'
            }
            return render(request, 'public_registration.html', context)
    
    # GET request - show the form
    try:
        school = SchoolDetail.get_current_school()
    except:
        school = None
    
    return render(request, 'public_registration.html', {'school': school})

def contact(request):
    """Contact page"""
    if request.method == 'POST':
        try:
            from .models import ContactEnquiry
            ContactEnquiry.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone', ''),
                subject=request.POST.get('subject'),
                enquiry=request.POST.get('enquiry')
            )
            context = {
                'success': True,
                'message': 'Your enquiry has been submitted successfully. We will get back to you soon.',
                'school': SchoolDetail.get_current_school()
            }
            return render(request, 'contact.html', context)
        except Exception as e:
            context = {
                'error': f'Error submitting enquiry: {str(e)}',
                'school': SchoolDetail.get_current_school()
            }
            return render(request, 'contact.html', context)
    
    try:
        school = SchoolDetail.get_current_school()
    except:
        school = None
    return render(request, 'contact.html', {'school': school})

def blog_detail(request, blog_id):
    """Blog detail page"""
    from .models import Blog
    from django.core.paginator import Paginator
    
    blog = get_object_or_404(Blog, id=blog_id)
    
    # Handle AJAX request for more other blogs
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        page = request.GET.get('page', 1)
        all_other_blogs = Blog.objects.exclude(id=blog_id).order_by('-created_at')
        paginator = Paginator(all_other_blogs, 5)
        other_blogs_page = paginator.get_page(page)
        return render(request, 'blog_detail_other_items.html', {'other_blogs': other_blogs_page})
    
    other_blogs = Blog.objects.exclude(id=blog_id).order_by('-created_at')[:5]
    has_more_other_blogs = Blog.objects.exclude(id=blog_id).count() > 5
    school = SchoolDetail.get_current_school()
    
    return render(request, 'blog_detail.html', {
        'blog': blog, 
        'other_blogs': other_blogs,
        'has_more_other_blogs': has_more_other_blogs,
        'school': school
    })

def pending_enquiry(request):
    """Pending enquiry page - Enhanced with proper data fetching"""
    from .models import ContactEnquiry, StudentRegistration
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_status':
            registration_id = request.POST.get('registration_id')
            status = request.POST.get('status')
            remarks = request.POST.get('remarks', '')
            
            registration = get_object_or_404(StudentRegistration, id=registration_id)
            registration.status = status
            registration.remarks = remarks
            registration.save()
            
            # If approved, create student record
            if status == 'approved':
                # Check if student already exists
                if not Student.objects.filter(reg_number=registration.application_number).exists():
                    Student.objects.create(
                        name=registration.name,
                        student_class=registration.student_class,
                        section=registration.section,
                        gender=registration.gender,
                        dob=registration.dob,
                        address1=registration.address,
                        city=registration.city,
                        mobile=registration.mobile,
                        father_name=registration.father_name,
                        mother_name=registration.mother_name,
                        religion=registration.religion,
                        reg_number=registration.application_number,
                        admission_date=registration.registration_date,
                        session=get_current_nepali_year_session(),
                        transport='00_No Transport Service | 0 Rs.'
                    )
                    messages.success(request, f'Registration approved and student {registration.name} added to system')
                else:
                    messages.success(request, f'Registration status updated to {status.title()}')
            else:
                messages.success(request, f'Registration status updated to {status.title()}')
            
            return redirect('pending_enquiry')
        
        elif action == 'update_enquiry_status':
            enquiry_id = request.POST.get('enquiry_id')
            status = request.POST.get('status')
            remarks = request.POST.get('remarks', '')
            
            enquiry = get_object_or_404(ContactEnquiry, id=enquiry_id)
            enquiry.status = status
            if remarks:
                enquiry.remarks = remarks
            enquiry.save()
            
            messages.success(request, f'Contact enquiry status updated to {status.title()}')
            return redirect('pending_enquiry')
        
        elif action == 'delete_registration':
            registration_id = request.POST.get('registration_id')
            registration = get_object_or_404(StudentRegistration, id=registration_id)
            student_name = registration.name
            
            # If approved, also delete the corresponding student record
            if registration.status == 'approved':
                try:
                    student = Student.objects.get(reg_number=registration.application_number)
                    student.delete()
                except Student.DoesNotExist:
                    pass
            
            registration.delete()
            messages.success(request, f'Registration for {student_name} has been permanently deleted')
            return redirect('pending_enquiry')
    
    # GET request - Fetch data with filtering support
    enquiry_status_filter = request.GET.get('enquiry_status', '')
    registration_status_filter = request.GET.get('registration_status', '')
    
    try:
        # Filter contact enquiries based on status
        enquiries = ContactEnquiry.objects.all()
        if enquiry_status_filter:
            enquiries = enquiries.filter(status=enquiry_status_filter)
        enquiries = enquiries.order_by('-created_at')
        enquiries_count = enquiries.count()
        
        # Filter student registrations based on status
        registrations = StudentRegistration.objects.all()
        if registration_status_filter:
            registrations = registrations.filter(status=registration_status_filter)
        registrations = registrations.order_by('-registration_date')
        registrations_count = registrations.count()
        
        # Calculate status counts for enquiries
        enquiry_status_counts = {
            'new': enquiries.filter(status='new').count(),
            'contacted': enquiries.filter(status='contacted').count(),
            'resolved': enquiries.filter(status='resolved').count(), 
            'closed': enquiries.filter(status='closed').count(),
        }
        
        # Calculate status counts for registrations
        registration_status_counts = {
            'pending': registrations.filter(status='pending').count(),
            'approved': registrations.filter(status='approved').count(),
            'rejected': registrations.filter(status='rejected').count(),
        }
        

        
    except Exception as e:
        print(f"ERROR fetching data: {e}")
        # Fallback empty data
        enquiries = ContactEnquiry.objects.none()
        registrations = StudentRegistration.objects.none()
        enquiries_count = 0
        registrations_count = 0
        enquiry_status_counts = {'new': 0, 'contacted': 0, 'resolved': 0, 'closed': 0}
        registration_status_counts = {'pending': 0, 'approved': 0, 'rejected': 0}
    
    # Prepare context with all required data
    context = {
        'enquiries': enquiries,
        'registrations': registrations,
        'enquiries_count': enquiries_count,
        'registrations_count': registrations_count,
        'enquiry_status_counts': enquiry_status_counts,
        'registration_status_counts': registration_status_counts,
        # Filter values for dropdowns
        'selected_enquiry_status': enquiry_status_filter,
        'selected_registration_status': registration_status_filter,

    }
    

    
    # Render template with no-cache headers
    response = render(request, 'pending_enquiry.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

@csrf_exempt
def filter_enquiries_api(request):
    """API endpoint for filtering enquiries and registrations"""
    if request.method == 'GET':
        try:
            enquiry_status = request.GET.get('enquiry_status', '')
            registration_status = request.GET.get('registration_status', '')
            
            # Filter enquiries
            enquiries = ContactEnquiry.objects.all()
            if enquiry_status:
                enquiries = enquiries.filter(status=enquiry_status)
            enquiries = enquiries.order_by('-created_at')
            
            # Filter registrations
            registrations = StudentRegistration.objects.all()
            if registration_status:
                registrations = registrations.filter(status=registration_status)
            registrations = registrations.order_by('-registration_date')
            
            # Prepare response data
            enquiries_data = []
            for enquiry in enquiries:
                enquiries_data.append({
                    'id': enquiry.id,
                    'name': enquiry.name or 'No Name',
                    'email': enquiry.email,
                    'phone': enquiry.phone or '',
                    'subject': enquiry.subject or 'No Subject',
                    'enquiry': enquiry.enquiry,
                    'status': enquiry.status or 'new',
                    'created_at': enquiry.created_at.strftime('%Y-%m-%d')
                })
            
            registrations_data = []
            for registration in registrations:
                registrations_data.append({
                    'id': registration.id,
                    'name': registration.name or 'No Name',
                    'student_class': registration.student_class or 'N/A',
                    'section': registration.section or 'N/A',
                    'gender': registration.gender,
                    'dob': registration.dob.strftime('%Y-%m-%d') if registration.dob else '',
                    'father_name': registration.father_name,
                    'mother_name': registration.mother_name,
                    'mobile': registration.mobile,
                    'address': registration.address,
                    'city': registration.city,
                    'application_number': registration.application_number,
                    'registration_date': registration.registration_date.strftime('%Y-%m-%d') if registration.registration_date else '',
                    'status': registration.status or 'pending'
                })
            
            return JsonResponse({
                'success': True,
                'enquiries': enquiries_data,
                'registrations': registrations_data,
                'enquiries_count': len(enquiries_data),
                'registrations_count': len(registrations_data)
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def blog_list(request):
    """Public blog list page"""
    from .models import Blog
    from django.core.paginator import Paginator
    
    blogs = Blog.objects.all().order_by('-created_at')
    paginator = Paginator(blogs, 6)  # Show 6 blogs per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    school = SchoolDetail.get_current_school()
    
    # For AJAX requests, return only the blog items
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'blog_items.html', {'blogs': page_obj})
    
    return render(request, 'blog_list.html', {
        'blogs': page_obj,
        'school': school,
        'has_next': page_obj.has_next(),
        'next_page': page_obj.next_page_number() if page_obj.has_next() else None
    })

def test_enquiry_status(request):
    """Test view to check enquiry status display"""
    from .models import ContactEnquiry
    
    enquiries = ContactEnquiry.objects.all().order_by('-created_at')
    
    response = render(request, 'test_enquiry_status.html', {
        'enquiries': enquiries
    })
    
    # Add cache-busting headers
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

@csrf_exempt
def save_attendance(request):
    """API to save student attendance data"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            attendance_date = data.get('date')
            attendance_data = data.get('attendance', {})
            marked_by = data.get('marked_by', 'System')
            
            if not attendance_date:
                return JsonResponse({'success': False, 'error': 'Date is required'})
            
            # Parse date
            try:
                attendance_date = datetime.strptime(attendance_date, '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid date format'})
            
            saved_count = 0
            updated_count = 0
            
            for student_id, status in attendance_data.items():
                try:
                    student = Student.objects.get(id=int(student_id))
                    attendance, created = StudentAttendance.objects.update_or_create(
                        student=student,
                        date=attendance_date,
                        defaults={
                            'status': status,
                            'marked_by': marked_by
                        }
                    )
                    
                    if created:
                        saved_count += 1
                    else:
                        updated_count += 1
                        
                except Student.DoesNotExist:
                    continue
            
            return JsonResponse({
                'success': True,
                'message': f'Attendance saved: {saved_count} new, {updated_count} updated',
                'saved_count': saved_count,
                'updated_count': updated_count
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def load_attendance(request):
    """API to load attendance data for a specific date"""
    try:
        attendance_date = request.GET.get('date')
        student_class = request.GET.get('class', '')
        section = request.GET.get('section', '')
        
        if not attendance_date:
            return JsonResponse({'success': False, 'error': 'Date is required'})
        
        # Parse date
        try:
            attendance_date = datetime.strptime(attendance_date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid date format'})
        
        # Get attendance records for the date
        attendance_records = StudentAttendance.get_attendance_for_date(
            attendance_date, student_class, section
        )
        
        attendance_data = {}
        for record in attendance_records:
            attendance_data[record.student.id] = record.status
        
        return JsonResponse({
            'success': True,
            'attendance': attendance_data,
            'date': attendance_date.strftime('%Y-%m-%d'),
            'total_records': len(attendance_data)
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def get_attendance_summary(request, student_id):
    """API to get attendance summary for a student"""
    try:
        student = get_object_or_404(Student, id=student_id)
        
        # Get date range from request or default to current month
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        summary = StudentAttendance.get_student_attendance_summary(
            student, start_date, end_date
        )
        
        return JsonResponse({
            'success': True,
            'student': {
                'id': student.id,
                'name': student.name,
                'class': student.student_class,
                'section': student.section
            },
            'summary': summary
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def attendance_report(request):
    """Attendance report page showing today's attendance data"""
    today = date.today()
    
    # Get today's attendance data
    attendance_records = StudentAttendance.objects.filter(date=today).select_related('student')
    
    # Get all students for comparison
    all_students = Student.objects.all().order_by('student_class', 'name')
    
    # Create attendance data with status
    students_data = []
    for student in all_students:
        try:
            attendance = attendance_records.get(student=student)
            status = attendance.status
        except StudentAttendance.DoesNotExist:
            status = 'not_marked'
        
        students_data.append({
            'student': student,
            'status': status
        })
    
    # Calculate statistics
    total_students = all_students.count()
    total_present = attendance_records.filter(status='present').count()
    total_absent = attendance_records.filter(status='absent').count()
    total_late = attendance_records.filter(status='late').count()
    not_marked = total_students - attendance_records.count()
    attendance_percentage = round((total_present / total_students * 100) if total_students > 0 else 0, 1)
    
    context = {
        'students_data': students_data,
        'today': today,
        'total_students': total_students,
        'total_present': total_present,
        'total_absent': total_absent,
        'total_late': total_late,
        'not_marked': not_marked,
        'attendance_percentage': attendance_percentage
    }
    
    return render(request, 'attendance_report.html', context)
def api_subjects_by_class(request, class_name):
    """API to get subjects by class for teacher edit"""
    try:
        subjects = Subject.objects.filter(class_name=class_name).order_by('name')
        subjects_data = []
        
        for subject in subjects:
            subjects_data.append({
                'id': subject.id,
                'name': subject.name,
                'code': subject.code
            })
        
        return JsonResponse({
            'success': True,
            'subjects': subjects_data
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

# Missing view functions that might be referenced
def save_attendance(request):
    """Save student attendance"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            attendance_date = data.get('date')
            attendance_data = data.get('attendance', [])
            
            # Clear existing attendance for the date
            StudentAttendance.objects.filter(date=attendance_date).delete()
            
            # Save new attendance records
            for record in attendance_data:
                student = get_object_or_404(Student, id=record['student_id'])
                StudentAttendance.objects.create(
                    student=student,
                    date=attendance_date,
                    status=record['status']
                )
            
            return JsonResponse({'success': True, 'message': 'Attendance saved successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def load_attendance(request):
    """Load student attendance for a specific date"""
    try:
        attendance_date = request.GET.get('date')
        if not attendance_date:
            return JsonResponse({'success': False, 'error': 'Date parameter required'})
        
        attendance_records = StudentAttendance.objects.filter(date=attendance_date).select_related('student')
        attendance_data = []
        
        for record in attendance_records:
            attendance_data.append({
                'student_id': record.student.id,
                'student_name': record.student.name,
                'status': record.status
            })
        
        return JsonResponse({'success': True, 'attendance': attendance_data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def get_attendance_summary(request, student_id):
    """Get attendance summary for a student"""
    try:
        student = get_object_or_404(Student, id=student_id)
        
        # Get attendance records for current month
        today = date.today()
        start_date = today.replace(day=1)
        
        attendance_records = StudentAttendance.objects.filter(
            student=student,
            date__range=[start_date, today]
        )
        
        present_count = attendance_records.filter(status='present').count()
        absent_count = attendance_records.filter(status='absent').count()
        late_count = attendance_records.filter(status='late').count()
        
        return JsonResponse({
            'success': True,
            'student_name': student.name,
            'present': present_count,
            'absent': absent_count,
            'late': late_count,
            'total_days': attendance_records.count()
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def attendance_report(request):
    """Attendance report view"""
    students = Student.objects.all().order_by('name')
    today = date.today()
    
    # Get attendance statistics for each student
    students_with_attendance = []
    for student in students:
        attendance_records = StudentAttendance.objects.filter(
            student=student,
            date__month=today.month,
            date__year=today.year
        )
        
        present_count = attendance_records.filter(status='present').count()
        absent_count = attendance_records.filter(status='absent').count()
        late_count = attendance_records.filter(status='late').count()
        total_days = attendance_records.count()
        
        attendance_percentage = (present_count / total_days * 100) if total_days > 0 else 0
        
        student.present_days = present_count
        student.absent_days = absent_count
        student.late_days = late_count
        student.total_days = total_days
        student.attendance_percentage = round(attendance_percentage, 1)
        
        students_with_attendance.append(student)
    
    context = {
        'students': students_with_attendance,
        'current_month': today.strftime('%B %Y')
    }
    
    return render(request, 'attendance_report.html', context)

# Missing views for contact and blog functionality
def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        try:
            ContactEnquiry.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                message=request.POST.get('message'),
                status='pending'
            )
            messages.success(request, 'Your enquiry has been submitted successfully!')
            return redirect('contact')
        except Exception as e:
            messages.error(request, f'Error submitting enquiry: {str(e)}')
    
    return render(request, 'contact.html')

def blog_list(request):
    """Blog list view"""
    from .models import Blog
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blog_list.html', {'blogs': blogs})

def blog_detail(request, blog_id):
    """Blog detail view"""
    from .models import Blog
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})

def pending_enquiry(request):
    """Pending enquiry view"""
    enquiries = ContactEnquiry.objects.exclude(status='closed').order_by('-created_at')
    registrations = StudentRegistration.objects.filter(status='pending').order_by('-registration_date')
    
    context = {
        'enquiries': enquiries,
        'registrations': registrations
    }
    
    return render(request, 'pending_enquiry.html', context)

def test_enquiry_status(request):
    """Test enquiry status view"""
    return render(request, 'test_enquiry_status.html')

@csrf_exempt
def update_registration_status_api(request):
    """API to update registration status"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            registration_id = data.get('registration_id')
            status = data.get('status')
            
            registration = get_object_or_404(StudentRegistration, id=registration_id)
            registration.status = status
            registration.save()
            
            return JsonResponse({'success': True, 'message': 'Status updated successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def pending_enquiry(request):
    """Pending enquiry management page with filtering"""
    # Get filter parameters
    enquiry_status = request.GET.get('enquiry_status', '')
    registration_status = request.GET.get('registration_status', '')
    
    # Handle POST requests for status updates
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_enquiry_status':
            enquiry_id = request.POST.get('enquiry_id')
            status = request.POST.get('status')
            remarks = request.POST.get('remarks', '')
            
            try:
                enquiry = get_object_or_404(ContactEnquiry, id=enquiry_id)
                enquiry.status = status
                if remarks:
                    enquiry.enquiry += f'\n\nRemarks: {remarks}'
                enquiry.save()
                messages.success(request, f'Enquiry status updated to {status.title()}')
            except Exception as e:
                messages.error(request, f'Error updating enquiry: {str(e)}')
        
        elif action == 'update_status':
            registration_id = request.POST.get('registration_id')
            status = request.POST.get('status')
            remarks = request.POST.get('remarks', '')
            
            try:
                registration = get_object_or_404(StudentRegistration, id=registration_id)
                registration.status = status
                registration.save()
                messages.success(request, f'Registration status updated to {status.title()}')
            except Exception as e:
                messages.error(request, f'Error updating registration: {str(e)}')
        
        return redirect('pending_enquiry')
    
    # Filter enquiries
    enquiries = ContactEnquiry.objects.all().order_by('-created_at')
    if enquiry_status:
        enquiries = enquiries.filter(status=enquiry_status)
    
    # Filter registrations
    registrations = StudentRegistration.objects.all().order_by('-registration_date')
    if registration_status:
        registrations = registrations.filter(status=registration_status)
    
    # Get counts for statistics
    enquiries_count = ContactEnquiry.objects.count()
    registrations_count = StudentRegistration.objects.count()
    
    # Get status counts for enquiries
    enquiry_status_counts = {
        'new': ContactEnquiry.objects.filter(status='new').count(),
        'contacted': ContactEnquiry.objects.filter(status='contacted').count(),
        'resolved': ContactEnquiry.objects.filter(status='resolved').count(),
        'closed': ContactEnquiry.objects.filter(status='closed').count(),
    }
    
    # Get status counts for registrations
    registration_status_counts = {
        'pending': StudentRegistration.objects.filter(status='pending').count(),
        'approved': StudentRegistration.objects.filter(status='approved').count(),
        'rejected': StudentRegistration.objects.filter(status='rejected').count(),
    }
    
    # Debug data
    debug_enquiry_list = list(ContactEnquiry.objects.values_list('name', 'status')[:5])
    debug_registration_list = list(StudentRegistration.objects.values_list('name', 'status')[:5])
    
    context = {
        'enquiries': enquiries,
        'registrations': registrations,
        'enquiries_count': enquiries_count,
        'registrations_count': registrations_count,
        'enquiry_status_counts': enquiry_status_counts,
        'registration_status_counts': registration_status_counts,
        'selected_enquiry_status': enquiry_status,
        'selected_registration_status': registration_status,
        'debug_enquiry_list': debug_enquiry_list,
        'debug_registration_list': debug_registration_list,
    }
    
    return render(request, 'pending_enquiry.html', context)

@csrf_exempt
def update_enquiry_status_api(request):
    """API to update enquiry status"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            enquiry_id = data.get('enquiry_id')
            status = data.get('status')
            
            enquiry = get_object_or_404(ContactEnquiry, id=enquiry_id)
            enquiry.status = status
            enquiry.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Enquiry status updated to {status.title()}'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def update_registration_status_api(request):
    """API to update registration status"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            registration_id = data.get('registration_id')
            status = data.get('status')
            
            registration = get_object_or_404(StudentRegistration, id=registration_id)
            registration.status = status
            registration.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Registration status updated to {status.title()}'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def filter_enquiries_api(request):
    """API to filter enquiries"""
    try:
        enquiry_status = request.GET.get('enquiry_status', '')
        registration_status = request.GET.get('registration_status', '')
        
        # Filter enquiries
        enquiries = ContactEnquiry.objects.all().order_by('-created_at')
        if enquiry_status:
            enquiries = enquiries.filter(status=enquiry_status)
        
        # Filter registrations
        registrations = StudentRegistration.objects.all().order_by('-registration_date')
        if registration_status:
            registrations = registrations.filter(status=registration_status)
        
        enquiries_data = []
        for enquiry in enquiries:
            enquiries_data.append({
                'id': enquiry.id,
                'name': enquiry.name,
                'email': enquiry.email,
                'phone': enquiry.phone,
                'subject': enquiry.subject,
                'enquiry': enquiry.enquiry,
                'status': enquiry.status,
                'created_at': enquiry.created_at.strftime('%Y-%m-%d')
            })
        
        registrations_data = []
        for registration in registrations:
            registrations_data.append({
                'id': registration.id,
                'name': registration.name,
                'student_class': registration.student_class,
                'section': registration.section,
                'gender': registration.gender,
                'dob': registration.dob.strftime('%Y-%m-%d') if registration.dob else '',
                'father_name': registration.father_name,
                'mother_name': registration.mother_name,
                'mobile': registration.mobile,
                'address': registration.address,
                'city': registration.city,
                'application_number': registration.application_number,
                'status': registration.status,
                'registration_date': registration.registration_date.strftime('%Y-%m-%d')
            })
        
        return JsonResponse({
            'success': True,
            'enquiries': enquiries_data,
            'registrations': registrations_data
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def contact(request):
    """Contact page with enquiry form"""
    if request.method == 'POST':
        try:
            ContactEnquiry.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone', ''),
                subject=request.POST.get('subject'),
                enquiry=request.POST.get('message'),
                status='new'
            )
            messages.success(request, 'Your enquiry has been submitted successfully!')
            return redirect('contact')
        except Exception as e:
            messages.error(request, f'Error submitting enquiry: {str(e)}')
    
    return render(request, 'contact.html')

def blog_list(request):
    """Blog list page"""
    from .models import Blog
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blog_list.html', {'blogs': blogs})

def blog_detail(request, blog_id):
    """Blog detail page"""
    from .models import Blog
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})

def test_enquiry_status(request):
    """Test view to check enquiry status"""
    enquiries = ContactEnquiry.objects.all()
    registrations = StudentRegistration.objects.all()
    
    context = {
        'enquiries': enquiries,
        'registrations': registrations,
        'enquiries_count': enquiries.count(),
        'registrations_count': registrations.count()
    }
    
    return render(request, 'test_enquiry_status.html', context)

@csrf_exempt
def save_attendance(request):
    """API to save student attendance"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            attendance_date = data.get('date')
            attendance_data = data.get('attendance', [])
            
            # Delete existing attendance for this date
            StudentAttendance.objects.filter(date=attendance_date).delete()
            
            # Save new attendance records
            for record in attendance_data:
                student = get_object_or_404(Student, id=record['student_id'])
                StudentAttendance.objects.create(
                    student=student,
                    date=attendance_date,
                    status=record['status']
                )
            
            return JsonResponse({
                'success': True,
                'message': f'Attendance saved for {len(attendance_data)} students'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def load_attendance(request):
    """API to load student attendance for a date"""
    try:
        attendance_date = request.GET.get('date')
        if not attendance_date:
            return JsonResponse({'success': False, 'error': 'Date parameter required'})
        
        attendance_records = StudentAttendance.objects.filter(date=attendance_date).select_related('student')
        attendance_data = {}
        
        for record in attendance_records:
            attendance_data[record.student.id] = record.status
        
        return JsonResponse({
            'success': True,
            'attendance': attendance_data
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def get_attendance_summary(request, student_id):
    """API to get attendance summary for a student"""
    try:
        student = get_object_or_404(Student, id=student_id)
        
        # Get attendance records for current month
        from datetime import datetime, timedelta
        today = date.today()
        month_start = today.replace(day=1)
        
        attendance_records = StudentAttendance.objects.filter(
            student=student,
            date__range=[month_start, today]
        )
        
        present_count = attendance_records.filter(status='present').count()
        absent_count = attendance_records.filter(status='absent').count()
        late_count = attendance_records.filter(status='late').count()
        leave_count = attendance_records.filter(status='leave').count()
        
        total_days = (today - month_start).days + 1
        attendance_percentage = (present_count / total_days * 100) if total_days > 0 else 0
        
        return JsonResponse({
            'success': True,
            'student': {
                'id': student.id,
                'name': student.name,
                'class': student.student_class,
                'section': student.section
            },
            'summary': {
                'present': present_count,
                'absent': absent_count,
                'late': late_count,
                'leave': leave_count,
                'total_days': total_days,
                'attendance_percentage': round(attendance_percentage, 1)
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def attendance_report(request):
    """Attendance report page"""
    # Get filter parameters
    class_filter = request.GET.get('class', '')
    date_filter = request.GET.get('date', '')
    
    if not date_filter:
        date_filter = date.today().strftime('%Y-%m-%d')
    
    # Get students based on class filter
    if class_filter:
        students = Student.objects.filter(student_class=class_filter).order_by('name')
    else:
        students = Student.objects.all().order_by('name')
    
    # Get attendance for the selected date
    attendance_records = StudentAttendance.objects.filter(date=date_filter).select_related('student')
    attendance_dict = {record.student.id: record.status for record in attendance_records}
    
    # Add attendance status to students
    students_with_attendance = []
    for student in students:
        student.attendance_status = attendance_dict.get(student.id, 'not_marked')
        students_with_attendance.append(student)
    
    # Calculate statistics
    total_students = len(students_with_attendance)
    present_count = len([s for s in students_with_attendance if s.attendance_status == 'present'])
    absent_count = len([s for s in students_with_attendance if s.attendance_status == 'absent'])
    late_count = len([s for s in students_with_attendance if s.attendance_status == 'late'])
    leave_count = len([s for s in students_with_attendance if s.attendance_status == 'leave'])
    not_marked_count = len([s for s in students_with_attendance if s.attendance_status == 'not_marked'])
    
    attendance_percentage = (present_count / total_students * 100) if total_students > 0 else 0
    
    # Get unique classes for filter
    classes = Student.objects.values_list('student_class', flat=True).distinct().order_by('student_class')
    
    context = {
        'students': students_with_attendance,
        'classes': classes,
        'selected_class': class_filter,
        'selected_date': date_filter,
        'statistics': {
            'total_students': total_students,
            'present': present_count,
            'absent': absent_count,
            'late': late_count,
            'leave': leave_count,
            'not_marked': not_marked_count,
            'attendance_percentage': round(attendance_percentage, 1)
        }
    }
    
    return render(request, 'attendance_report.html', context)

@csrf_exempt
def delete_registration_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            registration = get_object_or_404(StudentRegistration, id=data['registration_id'])
            registration.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Registration deleted successfully'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})