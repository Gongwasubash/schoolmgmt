from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .models import Student, FeeStructure, FeePayment
from django.db import models
import json
from datetime import datetime, date
from django.db.models import Count, Sum, Max
from decimal import Decimal
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
            conditions &= models.Q(name__icontains=name)
        if student_class:
            conditions &= models.Q(student_class=student_class)
        if section:
            conditions &= models.Q(section=section)
        if reg_number:
            conditions &= models.Q(reg_number__icontains=reg_number)
        
        # If no search criteria provided
        if not any([query, name, student_class, section, reg_number]):
            return JsonResponse({'success': False, 'error': 'No search criteria provided'})
        
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
            return JsonResponse({'success': False, 'error': 'No students found'})
            
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
            
            # Update admission status if admission fee is paid
            fee_types = json.loads(data['fee_types'])
            for fee_type in fee_types:
                if fee_type['type'] == 'admission_fee':
                    student.admission_paid = True
                    student.save()
                    break
            
            return JsonResponse({'success': True, 'payment_id': payment.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def fee_receipt_book(request):
    from django.db.models import Sum, Max
    from decimal import Decimal
    
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
        student_pending = max(Decimal('0'), student_total_fee - student_paid)
        
        # Add to totals
        total_collected += student_paid
        total_pending += student_pending
        
        # Set student attributes for template
        student.total_fee = float(student_total_fee)
        student.paid_amount = float(student_paid)
        student.pending_amount = float(student_pending)
        student.payment_status = 'paid' if student_pending == 0 else 'pending'
        student.class_name = student.student_class
        student.roll_number = student.reg_number
        
        # Calculate monthly fee amount
        try:
            fee_structure = FeeStructure.objects.get(class_name=student.student_class)
            monthly_fee_amount = float(fee_structure.monthly_fee + fee_structure.tuition_fee)
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
        'search_query': search_query
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
    
    context = {
        'student': student,
        'payment': payment_data,
        'current_date': datetime.now().strftime('%B %d, %Y')
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
    
    selected_months = [m.strip() for m in request.GET.get('months', '').split(',') if m.strip()]
    selected_fee_types = [f.strip() for f in request.GET.get('fee_types', '').split(',') if f.strip()]
    
    try:
        fee_structure = FeeStructure.objects.get(class_name=student.student_class)
    except FeeStructure.DoesNotExist:
        fee_structure = None
    
    pending_fees = []
    total_pending = 0
    
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
                
                # Calculate paid amount for selected fee types
                payments = FeePayment.objects.filter(student=student)
                student_paid = Decimal('0')
                for payment in payments:
                    if payment.fee_types:
                        try:
                            payment_fee_types = json.loads(payment.fee_types)
                            for fee_data in payment_fee_types:
                                if fee_data.get('type') in fee_types_filter:
                                    student_paid += Decimal(str(fee_data.get('amount', 0)))
                        except json.JSONDecodeError:
                            pass
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
            
            student_pending = max(Decimal('0'), student_total_fee - student_paid)
            payment_status = 'paid' if student_pending == 0 else 'pending'
            
            # Apply status filter
            if status_filter and payment_status != status_filter:
                continue
            
            total_collected += student_paid
            total_pending += student_pending
            
            students_data.append({
                'id': student.id,
                'name': student.name,
                'class_name': student.student_class,
                'section': student.section,
                'roll_number': student.reg_number,
                'total_fee': float(student_total_fee),
                'paid_amount': float(student_paid),
                'pending_amount': float(student_pending),
                'payment_status': payment_status,
                'last_payment_date': student.last_payment_date.strftime('%Y-%m-%d') if student.last_payment_date else None
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

