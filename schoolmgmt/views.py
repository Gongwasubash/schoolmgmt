from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .models import Student, FeeStructure, FeePayment
import json
from datetime import datetime, date
from django.db.models import Count
import csv
import io

def home(request):
    # Get student statistics
    total_students = Student.objects.count()
    boys_count = Student.objects.filter(gender='Boy').count()
    girls_count = Student.objects.filter(gender='Girl').count()
    
    # Get today's birthdays
    today = date.today()
    todays_birthdays = Student.objects.filter(dob__month=today.month, dob__day=today.day).count()
    
    # Get class-wise data
    class_data = Student.objects.values('student_class').annotate(count=Count('student_class')).order_by('student_class')
    
    # Get religion-wise data
    religion_data = Student.objects.values('religion').annotate(count=Count('religion')).order_by('religion')
    
    context = {
        'total_students': total_students,
        'boys_count': boys_count,
        'girls_count': girls_count,
        'todays_birthdays': todays_birthdays,
        'class_data': class_data,
        'religion_data': religion_data,
    }
    
    return render(request, 'index.html', context)

def students(request):
    if request.method == 'POST':
        try:
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
                session=request.POST.get('session'),
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
    
    return render(request, 'students.html', {'is_edit': False})

def studentlist(request):
    students = Student.objects.all()
    return render(request, 'studentlist.html', {'students': students})

def teachers(request):
    return render(request, 'teachers.html')

def classes(request):
    return render(request, 'classes.html')

def reports(request):
    return render(request, 'reports.html')

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
    fee_structures = FeeStructure.objects.all()
    students = Student.objects.all()
    
    # Create fee headings list
    fee_headings = [
        {'field': 'admission_fee', 'name': 'Admission Fee'},
        {'field': 'monthly_fee', 'name': 'Monthly Fee'},
        {'field': 'tuition_fee', 'name': 'Tuition Fee'},
        {'field': 'examination_fee', 'name': 'Examination Fee'},
        {'field': 'library_fee', 'name': 'Library Fee'},
        {'field': 'sports_fee', 'name': 'Sports Fee'},
        {'field': 'laboratory_fee', 'name': 'Laboratory Fee'},
        {'field': 'computer_fee', 'name': 'Computer Fee'},
        {'field': 'transportation_fee', 'name': 'Transportation Fee'},
    ]
    
    return render(request, 'pay.html', {
        'fee_structures': fee_structures, 
        'students': students,
        'fee_headings': fee_headings
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
    fee_structures = FeeStructure.objects.all()
    
    # Create fee headings list
    fee_headings = [
        {'field': 'admission_fee', 'name': 'Admission Fee'},
        {'field': 'monthly_fee', 'name': 'Monthly Fee'},
        {'field': 'tuition_fee', 'name': 'Tuition Fee'},
        {'field': 'examination_fee', 'name': 'Examination Fee'},
        {'field': 'library_fee', 'name': 'Library Fee'},
        {'field': 'sports_fee', 'name': 'Sports Fee'},
        {'field': 'laboratory_fee', 'name': 'Laboratory Fee'},
        {'field': 'computer_fee', 'name': 'Computer Fee'},
        {'field': 'transportation_fee', 'name': 'Transportation Fee'},
    ]
    
    # Get paid months from FeePayment data and calculate balance
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
        
        # Add to total balance
        total_balance += payment.balance
    
    context = {
        'student': student,
        'student_id': f'STU{student.id:03d}',
        'reg_number': student.reg_number,
        'fee_structures': fee_structures,
        'fee_headings': fee_headings,
        'paid_fee_months': json.dumps(paid_fee_months),
        'student_balance': total_balance,
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
    
    return render(request, 'students.html', {'student': student, 'is_edit': True})

def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'S.No', 'ID', 'Registration Number', 'Name', 'Father Name', 'Mother Name', 
        'Class', 'Section', 'Gender', 'Mobile', 'Father Mobile', 'Mother Mobile',
        'Address1', 'Address2', 'City', 'Religion', 'DOB', 'Admission Date',
        'Session', 'Transport', 'Last School', 'Marks', 'Exam Result',
        'Father Email', 'Father Occupation', 'Father Qualification', 'Father DOB', 'Father Citizen',
        'Mother Occupation', 'Mother Qualification', 'Mother DOB', 'Mother Citizen',
        'Character Cert', 'Report Card', 'DOB Cert', 'Old Balance'
    ])
    
    students = Student.objects.all()
    for index, student in enumerate(students, 1):
        writer.writerow([
            index,
            f'STU{student.id:03d}',
            student.reg_number,
            student.name,
            student.father_name,
            student.mother_name,
            student.student_class,
            student.section,
            student.gender,
            student.mobile,
            student.father_mobile,
            student.mother_mobile or '',
            student.address1,
            student.address2 or '',
            student.city,
            student.religion,
            student.dob,
            student.admission_date,
            student.session,
            student.transport,
            student.last_school or '',
            student.marks or '',
            student.exam_result or '',
            student.father_email or '',
            student.father_occupation or '',
            student.father_qualification or '',
            student.father_dob or '',
            student.father_citizen or '',
            student.mother_occupation or '',
            student.mother_qualification or '',
            student.mother_dob or '',
            student.mother_citizen or '',
            'Yes' if student.character_cert else 'No',
            'Yes' if student.report_card else 'No',
            'Yes' if student.dob_cert else 'No',
            student.old_balance
        ])
    
    return response

def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            return JsonResponse({'success': False, 'error': 'No file uploaded'})
        
        try:
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            for row in reader:
                Student.objects.create(
                    name=row.get('Name', ''),
                    student_class=row.get('Class', ''),
                    section=row.get('Section', ''),
                    mobile=row.get('Mobile', ''),
                    father_name=row.get('Father Name', ''),
                    reg_number=row.get('Registration Number', ''),
                    transport='00_No Transport Service | 0 Rs.',
                    address1='',
                    city='',
                    gender='Boy',
                    religion='Hindu',
                    dob='2000-01-01',
                    admission_date='2024-01-01',
                    session='2024-25',
                    mother_name=''
                )
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
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

            payment = FeePayment.objects.create(
                student=student,
                selected_months=data['selected_months'],
                fee_types=data['fee_types'],
                custom_fees=data.get('custom_fees', '[]'),
                total_fee=data['total_fee'],
                payment_amount=data['payment_amount'],
                balance=data['balance'],
                payment_method=data['payment_method'],
                bank_name=data.get('bank_name', ''),
                cheque_dd_no=data.get('cheque_dd_no', ''),
                cheque_date=cheque_date,
                remarks=data.get('remarks', ''),
                sms_sent=data.get('sms_sent', False),
                whatsapp_sent=data.get('whatsapp_sent', False)
            )
            
            return JsonResponse({'success': True, 'payment_id': payment.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})