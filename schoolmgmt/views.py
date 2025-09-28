from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from .models import Student, FeeStructure, FeePayment, Subject, Exam, Marksheet, Session, StudentMarks, MarksheetData, StudentDailyExpense, SchoolDetail
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

def home(request):
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
    
    # Get monthly collection (current month)
    monthly_collection = FeePayment.objects.filter(payment_date__year=today.year, payment_date__month=today.month).aggregate(total=Sum('payment_amount'))['total'] or 0
    
    # Get yearly collection (current year)
    yearly_collection = FeePayment.objects.filter(payment_date__year=today.year).aggregate(total=Sum('payment_amount'))['total'] or 0
    
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

def students(request):
    if request.method == 'POST':
        try:
            # Use current Nepali session for new students
            session_name = get_current_nepali_year_session()
            
            # Also create/update Session model for compatibility
            current_session, created = Session.objects.get_or_create(
                name=session_name,
                defaults={
                    'start_date': date.today().replace(month=4, day=1),  # Approximate Baisakh 1
                    'end_date': date.today().replace(year=date.today().year+1, month=3, day=31),  # Approximate Chaitra end
                    'is_active': True
                }
            )
            
            # Ensure only one active session
            if created or not current_session.is_active:
                Session.objects.exclude(id=current_session.id).update(is_active=False)
                current_session.is_active = True
                current_session.save()
            
            # Create new student from form data
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
            return redirect('studentlist')
        except Exception as e:
            messages.error(request, f'Error submitting admission: {str(e)}')
    
    # Get available sessions for the form
    sessions = Session.objects.all().order_by('-start_date')
    current_session = Session.get_current_session()
    
    # Get available classes from Student model and database
    classes = list(Student.objects.values_list('student_class', flat=True).distinct().order_by('student_class'))
    
    context = {
        'is_edit': False,
        'sessions': sessions,
        'current_session': current_session,
        'classes': classes
    }
    return render(request, 'students.html', context)

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

def teachers(request):
    return render(request, 'teachers.html')

def classes(request):
    return render(request, 'classes.html')

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
    return render(request, 'fee_structure.html', {'fee_structures': fee_structures})

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
            f'₹{total_fee:,.2f}',
            f'₹{paid_amount:,.2f}',
            f'₹{pending_amount:,.2f}',
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
            
            # Delete paid daily expenses
            daily_expenses = json.loads(data.get('daily_expenses', '[]'))
            if daily_expenses:
                expense_ids = [expense['id'] for expense in daily_expenses]
                StudentDailyExpense.objects.filter(id__in=expense_ids).delete()
            
            return JsonResponse({'success': True, 'payment_ids': payment_ids})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

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
        p.drawString(70, y, f"Amount Paid: ₹{payment.payment_amount}")
        
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
                    p.drawString(70, y, f"{fee_name}: ₹{fee_amount}")
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

def marksheet_system(request):
    """Main marksheet system page"""
    exams = Exam.objects.all().order_by('-exam_date')
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
        subjects = Subject.objects.filter(class_name=class_name).order_by('name')
        subjects_data = []
        
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
        
        display_class_name = class_name_mapping.get(class_name, class_name)
        
        for subject in subjects:
            subjects_data.append({
                'id': subject.id,
                'name': subject.name,
                'code': subject.code,
                'class_name': display_class_name,
                'original_class_name': subject.class_name,
                'max_marks': subject.max_marks,
                'pass_marks': subject.pass_marks
            })
        
        return JsonResponse({
            'success': True,
            'subjects': subjects_data,
            'class_name': display_class_name,
            'original_class_name': class_name
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

def student_attendance_dashboard(request):
    """Student Attendance Dashboard"""
    return render(request, 'student_attendance_dashboard.html')

def print_bill(request):
    """Print bill page"""
    school = SchoolDetail.get_current_school()
    return render(request, 'print_bill.html', {'school': school})

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
    
    # Get payments for the period
    payments = FeePayment.objects.filter(
        payment_date__range=[start_date, end_date]
    ).select_related('student').order_by('-payment_date', '-id')
    
    # Process fee types for display
    for payment in payments:
        payment.fee_types_list = []
        if payment.fee_types:
            try:
                fee_types = json.loads(payment.fee_types)
                payment.fee_types_list = fee_types
            except json.JSONDecodeError:
                pass
    
    # Calculate totals
    total_amount = payments.aggregate(total=Sum('payment_amount'))['total'] or 0
    total_payments = payments.count()
    
    # Payment method summary
    payment_methods = payments.values('payment_method').annotate(
        count=Count('id'),
        total=Sum('payment_amount')
    ).order_by('-total')
    
    context = {
        'payments': payments,
        'period_title': period_title,
        'date_range': date_range,
        'total_amount': total_amount,
        'total_payments': total_payments,
        'payment_methods': payment_methods,
        'period': period,
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'collection_details.html', context)

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

def generate_id(request):
    student_id = request.GET.get('student_id')
    student_ids = request.GET.get('student_ids')
    template = request.GET.get('template', '1')
    design = request.GET.get('design', template)
    
    try:
        school = SchoolDetail.get_current_school()
    except:
        school = None
    
    if student_ids:
        # Bulk mode
        student_id_list = student_ids.split(',')
        students = Student.objects.filter(id__in=student_id_list)
        return render(request, 'generate_id.html', {
            'students': students,
            'is_bulk': True,
            'school': school,
            'template': template,
            'design': design
        })
    elif student_id:
        # Single student mode
        try:
            student = Student.objects.get(id=student_id)
            return render(request, 'generate_id.html', {
                'student': student,
                'is_bulk': False,
                'school': school,
                'template': template,
                'design': design
            })
        except Student.DoesNotExist:
            return render(request, '404.html', status=404)
    
    return render(request, '404.html', status=404)

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