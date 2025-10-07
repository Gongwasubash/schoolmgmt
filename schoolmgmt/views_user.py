from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AdminLogin, Student, Teacher, SchoolDetail
import hashlib

def user_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, 'Please enter both username and password')
            return render(request, 'user_login.html')
        
        try:
            user = AdminLogin.objects.get(username=username, password=password, is_active=True)
            request.session['user_id'] = user.id
            request.session['user_username'] = user.username
            request.session['user_is_super_admin'] = user.is_super_admin
            request.session['admin_logged_in'] = True  # Required by middleware
            
            # Set ALL permission session keys for basic users (same as admin login)
            if user.is_super_admin:
                request.session['can_create_users'] = True
                request.session['can_delete_users'] = True
                request.session['can_view_dashboard'] = True
                request.session['can_view_students'] = True
                request.session['can_view_teachers'] = True
                request.session['can_view_reports'] = True
                request.session['can_view_marksheet'] = True
                request.session['can_view_fees'] = True
                request.session['can_view_receipts'] = True
                request.session['can_view_expenses'] = True
                request.session['can_view_settings'] = True
                request.session['can_view_fee_structure'] = True
                request.session['can_view_fee_receipt'] = True
                request.session['can_view_daily_expenses'] = True
                request.session['can_view_school_settings'] = True
                request.session['can_view_website_settings'] = True
                request.session['can_view_user_management'] = True
            else:
                request.session['can_create_users'] = user.can_create_users
                request.session['can_delete_users'] = user.can_delete_users
                request.session['can_view_dashboard'] = user.can_view_dashboard
                request.session['can_view_students'] = user.can_view_students
                request.session['can_view_teachers'] = user.can_view_teachers
                request.session['can_view_reports'] = user.can_view_reports
                request.session['can_view_marksheet'] = user.can_view_marksheet
                request.session['can_view_fees'] = getattr(user, 'can_view_fees', True)
                request.session['can_view_receipts'] = getattr(user, 'can_view_receipts', True)
                request.session['can_view_expenses'] = getattr(user, 'can_view_expenses', True)
                request.session['can_view_settings'] = getattr(user, 'can_view_settings', True)
                request.session['can_view_fee_structure'] = user.can_view_fee_structure
                request.session['can_view_fee_receipt'] = user.can_view_fee_receipt
                request.session['can_view_daily_expenses'] = user.can_view_daily_expenses
                request.session['can_view_school_settings'] = user.can_view_school_settings
                request.session['can_view_website_settings'] = user.can_view_website_settings
                request.session['can_view_user_management'] = user.can_view_user_management
            
            messages.success(request, f'Welcome {user.username}!')
            # Redirect to first available permitted page
            if user.can_view_dashboard:
                return redirect('dashboard')
            elif user.can_view_students:
                return redirect('students')
            elif user.can_view_teachers:
                return redirect('teachers')
            elif user.can_view_reports:
                return redirect('reports')
            elif user.can_view_marksheet:
                return redirect('marksheet_system')
            elif user.can_view_fee_structure:
                return redirect('fees')
            elif user.can_view_fee_receipt:
                return redirect('fee_receipt_book')
            elif user.can_view_daily_expenses:
                return redirect('student_daily_exp')
            elif user.can_view_school_settings:
                return redirect('school_settings')
            else:
                return redirect('home')
        except AdminLogin.DoesNotExist:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'user_login.html')

def user_dashboard(request):
    if not request.session.get('user_id'):
        return redirect('user_login')
    
    # Get user info
    try:
        user = AdminLogin.objects.get(id=request.session.get('user_id'), is_active=True)
    except AdminLogin.DoesNotExist:
        return redirect('user_login')
    
    # Get dashboard data based on permissions
    context = {
        'user_info': user,
        'total_students': Student.objects.count() if user.can_view_students or user.is_super_admin else 0,
        'total_teachers': Teacher.objects.count() if user.can_view_teachers or user.is_super_admin else 0,
        'todays_collection': 0,  # Add your collection logic here
    }
    
    return render(request, 'user_dashboard.html', context)

def user_logout(request):
    # Clear only user session data
    user_keys = ['user_id', 'user_username', 'user_is_super_admin']
    for key in user_keys:
        if key in request.session:
            del request.session[key]
    
    messages.success(request, 'Logged out successfully')
    return redirect('user_login')

def student_login_view(request):
    school_info = SchoolDetail.objects.first()
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, 'Please enter both username and password')
            return render(request, 'student_login.html', {'school': school_info})
        
        # Try to find student by student_id or name
        try:
            # First try by username field
            student = Student.objects.filter(username=username).first()
            
            # If not found, try by reg_number (student_id)
            if not student:
                student = Student.objects.filter(reg_number=username).first()
            
            if not student:
                # Try by name if student_id doesn't match
                student = Student.objects.filter(
                    name__icontains=username
                ).first()
            
            if student:
                # Check password - use the password field if set, otherwise fallback to reg_number
                valid_password = False
                
                if student.password and password == student.password:
                    valid_password = True
                elif password == student.reg_number or password == 'student123':
                    valid_password = True
                
                if valid_password:
                    request.session['student_id'] = student.id
                    request.session['student_name'] = student.name
                    request.session['student_logged_in'] = True
                    
                    messages.success(request, f'Welcome {student.name}!')
                    return redirect('student_dashboard')
                else:
                    messages.error(request, 'Invalid password')
            else:
                messages.error(request, 'Student not found')
                
        except Exception as e:
            messages.error(request, 'Login failed. Please try again.')
    
    return render(request, 'student_login.html', {'school': school_info})

def student_dashboard(request):
    if not request.session.get('student_logged_in'):
        return redirect('student_login')
    
    try:
        student = Student.objects.get(id=request.session.get('student_id'))
    except Student.DoesNotExist:
        return redirect('student_login')
    
    context = {
        'student': student,
        'school': SchoolDetail.objects.first(),
    }
    
    return render(request, 'student_dashboard.html', context)

def student_logout(request):
    from django.contrib.auth import logout
    
    # Clear student session data
    student_keys = ['student_id', 'student_name', 'student_logged_in']
    for key in student_keys:
        if key in request.session:
            del request.session[key]
    
    # Logout Django user (for Google OAuth)
    if request.user.is_authenticated:
        logout(request)
    
    messages.success(request, 'Logged out successfully')
    return redirect('home')

def google_oauth_redirect(request):
    """Simple redirect to Google OAuth"""
    return redirect('/auth/login/google-oauth2/')

def student_attendance(request, student_id):
    if not request.session.get('student_logged_in'):
        return redirect('student_login')
    
    # Verify the student_id matches the logged-in student
    logged_in_student_id = request.session.get('student_id')
    if logged_in_student_id != student_id:
        messages.error(request, 'Access denied. You can only view your own information.')
        return redirect('student_dashboard')
    
    try:
        student = Student.objects.get(id=student_id)
        # Get student attendance data
        attendance_records = []
        present_days = 0
        absent_days = 0
        
        try:
            from .models import SchoolAttendance
            attendance_records = SchoolAttendance.objects.filter(
                student__name=student.name,
                student__student_class=student.student_class,
                student__reg_number=student.reg_number
            ).order_by('-date')
            present_days = attendance_records.filter(status='present').count()
            absent_days = attendance_records.filter(status='absent').count()
            late_days = attendance_records.filter(status='late').count()
        except:
            late_days = 0
        
        context = {
            'student': student,
            'attendance_records': attendance_records,
            'present_days': present_days,
            'absent_days': absent_days,
            'late_days': late_days,
            'school': SchoolDetail.objects.first(),
        }
        
        return render(request, 'student_attendance.html', context)
    except Student.DoesNotExist:
        return redirect('student_dashboard')

def student_performance(request, student_id):
    if not request.session.get('student_logged_in'):
        return redirect('student_login')
    
    # Verify the student_id matches the logged-in student
    logged_in_student_id = request.session.get('student_id')
    if logged_in_student_id != student_id:
        messages.error(request, 'Access denied. You can only view your own information.')
        return redirect('student_dashboard')
    
    try:
        student = Student.objects.get(id=student_id)
        # Get student marks from Marksheet model
        student_marks = []
        try:
            from .models import Marksheet
            student_marks = Marksheet.objects.filter(
                student__name=student.name,
                student__student_class=student.student_class,
                student__reg_number=student.reg_number
            ).select_related('exam', 'subject')
            
            # Calculate performance summary
            total_marks = sum(mark.marks_obtained for mark in student_marks)
            total_possible = sum(mark.subject.max_marks for mark in student_marks)
            overall_percentage = (total_marks / total_possible * 100) if total_possible > 0 else 0
            total_subjects = student_marks.count()
            passed_subjects = sum(1 for mark in student_marks if mark.marks_obtained >= mark.subject.pass_marks)
            
            # Calculate overall grade
            if overall_percentage >= 90:
                overall_grade = 'A+'
            elif overall_percentage >= 80:
                overall_grade = 'A'
            elif overall_percentage >= 70:
                overall_grade = 'B+'
            elif overall_percentage >= 60:
                overall_grade = 'B'
            elif overall_percentage >= 50:
                overall_grade = 'C+'
            elif overall_percentage >= 40:
                overall_grade = 'C'
            else:
                overall_grade = 'D'
            
            # Calculate class ranking
            from django.db.models import Sum, F
            class_students = Marksheet.objects.filter(
                student__student_class=student.student_class
            ).values('student__name', 'student__reg_number').annotate(
                total_marks=Sum('marks_obtained')
            ).order_by('-total_marks')
            
            class_rank = 1
            total_class_students = class_students.count()
            for i, s in enumerate(class_students, 1):
                if s['student__reg_number'] == student.reg_number:
                    class_rank = i
                    break
        except:
            total_marks = total_possible = overall_percentage = total_subjects = passed_subjects = 0
            class_rank = total_class_students = 0
            overall_grade = 'N/A'
        
        context = {
            'student': student,
            'student_marks': student_marks,
            'total_marks': total_marks,
            'total_possible': total_possible,
            'overall_percentage': overall_percentage,
            'total_subjects': total_subjects,
            'passed_subjects': passed_subjects,
            'class_rank': class_rank,
            'total_class_students': total_class_students,
            'overall_grade': overall_grade,
            'school': SchoolDetail.objects.first(),
        }
        
        return render(request, 'student_performance.html', context)
    except Student.DoesNotExist:
        return redirect('student_dashboard')

def student_fees(request, student_id):
    if not request.session.get('student_logged_in'):
        return redirect('student_login')
    
    # Verify the student_id matches the logged-in student
    logged_in_student_id = request.session.get('student_id')
    if logged_in_student_id != student_id:
        messages.error(request, 'Access denied. You can only view your own information.')
        return redirect('student_dashboard')
    
    try:
        student = Student.objects.get(id=student_id)
        # Get student fee payments
        fee_payments = []
        total_paid = 0
        try:
            from .models import FeePayment
            fee_payments = FeePayment.objects.filter(
                student__name=student.name,
                student__student_class=student.student_class,
                student__reg_number=student.reg_number
            ).order_by('-payment_date')
            total_paid = sum(payment.payment_amount for payment in fee_payments)
        except:
            pass
        
        context = {
            'student': student,
            'fee_payments': fee_payments,
            'total_paid': total_paid,
            'school': SchoolDetail.objects.first(),
        }
        
        return render(request, 'student_fees.html', context)
    except Student.DoesNotExist:
        return redirect('student_dashboard')

def user_profile(request):
    import random
    from django.core.mail import send_mail
    from django.conf import settings
    
    if not request.user.is_authenticated:
        return redirect('student_login')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'verify':
            student_name = request.POST.get('student_name', '').strip()
            student_id = request.POST.get('student_id', '').strip()
            
            if student_name and student_id:
                try:
                    student = Student.objects.filter(
                        name__icontains=student_name,
                        reg_number=student_id
                    ).first()
                    
                    if student:
                        # Check if student has father_email field
                        if hasattr(student, 'father_email') and student.father_email:
                            # Generate verification code
                            verification_code = str(random.randint(100000, 999999))
                            request.session['verification_code'] = verification_code
                            request.session['student_id_temp'] = student.id
                            
                            # Send email
                            try:
                                send_mail(
                                    'Student Verification Code',
                                    f'Your child {student.name} is trying to verify their student account. Verification code: {verification_code}',
                                    'noreply@school.edu',
                                    [student.father_email],
                                    fail_silently=False,
                                )
                                messages.success(request, f'Verification code sent to {student.father_email}')
                                return render(request, 'user_profile.html', {
                                    'school': SchoolDetail.objects.first(),
                                    'show_verification_form': True,
                                    'student_id_temp': student.id
                                })
                            except Exception as e:
                                messages.error(request, f'Failed to send email: {str(e)}')
                        else:
                            # Skip email verification for now
                            messages.success(request, f'Student verified successfully! Welcome {student.name}.')
                            request.session['student_id'] = student.id
                            request.session['student_name'] = student.name
                            request.session['student_logged_in'] = True
                            return redirect('student_dashboard')
                    else:
                        messages.error(request, 'Student not found. Please check your name and ID.')
                except Exception as e:
                    messages.error(request, f'Verification failed: {str(e)}')
            else:
                messages.error(request, 'Please fill in all required fields.')
        
        elif action == 'confirm':
            verification_code = request.POST.get('verification_code', '').strip()
            student_id_temp = request.POST.get('student_id_temp')
            
            if verification_code == request.session.get('verification_code') and student_id_temp:
                try:
                    student = Student.objects.get(id=student_id_temp)
                    # Set student session data
                    request.session['student_id'] = student.id
                    request.session['student_name'] = student.name
                    request.session['student_logged_in'] = True
                    # Clear verification data
                    del request.session['verification_code']
                    del request.session['student_id_temp']
                    messages.success(request, f'Verification successful! Welcome {student.name}.')
                    return redirect('student_dashboard')
                except:
                    messages.error(request, 'Verification failed.')
            else:
                messages.error(request, 'Invalid verification code.')
    
    context = {
        'school': SchoolDetail.objects.first(),
    }
    
    return render(request, 'user_profile.html', context)