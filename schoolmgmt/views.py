from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
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
    
    context = {
        'student': student,
        'student_id': f'STU{student.id:03d}',
        'reg_number': student.reg_number,
        'fee_headings': fee_headings,
        'paid_fee_months': json.dumps(paid_fee_months),
        'student_balance': total_balance,
        'selected_class': student.student_class
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
                        session=row.get('Session', '2024-25').strip(),
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