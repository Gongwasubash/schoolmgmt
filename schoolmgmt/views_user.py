from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AdminLogin, Student, Teacher
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