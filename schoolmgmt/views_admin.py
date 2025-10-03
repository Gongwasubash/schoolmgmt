from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import AdminLogin, Teacher
import hashlib

def check_admin_session(request):
    """Check if user has admin session and return admin object"""
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return None
    try:
        return AdminLogin.objects.get(id=admin_id, is_active=True)
    except AdminLogin.DoesNotExist:
        return None

def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, 'Please enter both username and password')
            return render(request, 'admin_login.html')
        
        # Debug info
        print(f"Login attempt - Username: '{username}', Password: '{password}'")
        
        # Check if user exists
        user_exists = AdminLogin.objects.filter(username=username).exists()
        if user_exists:
            user = AdminLogin.objects.get(username=username)
            print(f"User found - Stored password: '{user.password}', Active: {user.is_active}")
            print(f"Password match: {user.password == password}")
        else:
            print(f"User '{username}' not found")
        
        try:
            admin = AdminLogin.objects.get(username=username, password=password, is_active=True)
            request.session['admin_id'] = admin.id
            request.session['admin_username'] = admin.username
            request.session['is_super_admin'] = admin.is_super_admin
            request.session['admin_logged_in'] = True
            
            # Set all permissions to True for super admin, otherwise use actual permissions
            if admin.is_super_admin:
                request.session['can_create_users'] = True
                request.session['can_delete_users'] = True
                request.session['can_view_dashboard'] = True
                request.session['can_view_students'] = True
                request.session['can_view_teachers'] = True
                request.session['can_view_reports'] = True
                request.session['can_view_marksheet'] = True
                request.session['can_view_fee_structure'] = True
                request.session['can_view_fee_receipt'] = True
                request.session['can_view_daily_expenses'] = True
                request.session['can_view_school_settings'] = True
                request.session['can_view_website_settings'] = True
                request.session['can_view_user_management'] = True
                request.session['can_view_attendance'] = True
            else:
                request.session['can_create_users'] = admin.can_create_users
                request.session['can_delete_users'] = admin.can_delete_users
                request.session['can_view_dashboard'] = admin.can_view_dashboard
                request.session['can_view_students'] = admin.can_view_students
                request.session['can_view_teachers'] = admin.can_view_teachers
                request.session['can_view_reports'] = admin.can_view_reports
                request.session['can_view_marksheet'] = admin.can_view_marksheet
                request.session['can_view_fee_structure'] = admin.can_view_fee_structure
                request.session['can_view_fee_receipt'] = admin.can_view_fee_receipt
                request.session['can_view_daily_expenses'] = admin.can_view_daily_expenses
                request.session['can_view_school_settings'] = admin.can_view_school_settings
                request.session['can_view_website_settings'] = admin.can_view_website_settings
                request.session['can_view_user_management'] = admin.can_view_user_management
                request.session['can_view_attendance'] = getattr(admin, 'can_view_attendance', True)
            
            messages.success(request, f'Welcome {admin.username}! Logged in successfully.')
            # Redirect users to first available permitted page
            if admin.can_view_dashboard:
                return redirect('dashboard')
            elif admin.can_view_students:
                return redirect('students')
            elif admin.can_view_teachers:
                return redirect('teachers')
            elif admin.can_view_reports:
                return redirect('reports')
            elif admin.can_view_marksheet:
                return redirect('marksheet_system')
            elif admin.can_view_fee_structure:
                return redirect('fees')
            elif admin.can_view_fee_receipt:
                return redirect('fee_receipt_book')
            elif admin.can_view_daily_expenses:
                return redirect('student_daily_exp')
            elif admin.can_view_school_settings:
                return redirect('school_settings')
            else:
                return redirect('home')
        except AdminLogin.DoesNotExist:
            messages.error(request, f'Invalid credentials for username: {username}')
    
    return render(request, 'admin_login.html')

def admin_dashboard(request):
    if not request.session.get('admin_id'):
        return redirect('admin_login_view')
    
    context = {
        'admin_username': request.session.get('admin_username'),
        'is_super_admin': request.session.get('is_super_admin'),
        'can_create_users': request.session.get('can_create_users'),
        'can_delete_users': request.session.get('can_delete_users'),
        'total_users': AdminLogin.objects.filter(is_active=True).count(),
        'total_teachers': Teacher.objects.filter(is_active=True).count(),
    }
    return render(request, 'admin_dashboard.html', context)

def user_management(request):
    users = AdminLogin.objects.all().order_by('-created_at')
    context = {
        'users': users,
        'can_create': True,
        'can_delete': True,
    }
    return render(request, 'user_management.html', context)

def create_user(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        teacher_id = request.POST.get('teacher_id')
        is_super_admin = request.POST.get('is_super_admin') == 'on'
        can_create_users = request.POST.get('can_create_users') == 'on'
        can_delete_users = request.POST.get('can_delete_users') == 'on'
        can_view_dashboard = request.POST.get('can_view_dashboard') == 'on'
        can_view_students = request.POST.get('can_view_students') == 'on'
        can_view_teachers = request.POST.get('can_view_teachers') == 'on'
        can_view_reports = request.POST.get('can_view_reports') == 'on'
        can_view_marksheet = request.POST.get('can_view_marksheet') == 'on'
        can_view_fee_structure = request.POST.get('can_view_fee_structure') == 'on'
        can_view_fee_receipt = request.POST.get('can_view_fee_receipt') == 'on'
        can_view_daily_expenses = request.POST.get('can_view_daily_expenses') == 'on'
        can_view_school_settings = request.POST.get('can_view_school_settings') == 'on'
        can_view_website_settings = request.POST.get('can_view_website_settings') == 'on'
        can_view_user_management = request.POST.get('can_view_user_management') == 'on'
        
        if AdminLogin.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            teacher = Teacher.objects.get(id=teacher_id) if teacher_id else None
            
            AdminLogin.objects.create(
                username=username,
                password=password,
                teacher=teacher,
                is_super_admin=is_super_admin,
                can_create_users=can_create_users,
                can_delete_users=can_delete_users,
                can_view_dashboard=can_view_dashboard,
                can_view_students=can_view_students,
                can_view_teachers=can_view_teachers,
                can_view_reports=can_view_reports,
                can_view_marksheet=can_view_marksheet,
                can_view_fee_structure=can_view_fee_structure,
                can_view_fee_receipt=can_view_fee_receipt,
                can_view_daily_expenses=can_view_daily_expenses,
                can_view_school_settings=can_view_school_settings,
                can_view_website_settings=can_view_website_settings,
                can_view_user_management=can_view_user_management,
                can_view_attendance=can_view_attendance,
                is_active=True
            )
            messages.success(request, f'User {username} created successfully')
            return redirect('user_management')
    
    teachers = Teacher.objects.filter(is_active=True).order_by('name')
    return render(request, 'create_user.html', {'teachers': teachers})

def delete_user(request, user_id):
    
    try:
        user = get_object_or_404(AdminLogin, id=user_id)
        if user.username == 'superadmin':
            return JsonResponse({'success': False, 'message': 'Cannot delete super admin'})
        
        user.delete()
        return JsonResponse({'success': True, 'message': f'User {user.username} deleted successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

def edit_user(request, user_id):
    
    user = get_object_or_404(AdminLogin, id=user_id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        teacher_id = request.POST.get('teacher_id')
        is_super_admin = request.POST.get('is_super_admin') == 'on'
        can_create_users = request.POST.get('can_create_users') == 'on'
        can_delete_users = request.POST.get('can_delete_users') == 'on'
        can_view_dashboard = request.POST.get('can_view_dashboard') == 'on'
        can_view_students = request.POST.get('can_view_students') == 'on'
        can_view_teachers = request.POST.get('can_view_teachers') == 'on'
        can_view_reports = request.POST.get('can_view_reports') == 'on'
        can_view_marksheet = request.POST.get('can_view_marksheet') == 'on'
        can_view_fee_structure = request.POST.get('can_view_fee_structure') == 'on'
        can_view_fee_receipt = request.POST.get('can_view_fee_receipt') == 'on'
        can_view_daily_expenses = request.POST.get('can_view_daily_expenses') == 'on'
        can_view_school_settings = request.POST.get('can_view_school_settings') == 'on'
        can_view_website_settings = request.POST.get('can_view_website_settings') == 'on'
        can_view_user_management = request.POST.get('can_view_user_management') == 'on'
        can_view_attendance = request.POST.get('can_view_attendance') == 'on'
        class_teacher_for = request.POST.get('class_teacher_for')
        is_active = request.POST.get('is_active') == 'on'
        
        if AdminLogin.objects.filter(username=username).exclude(id=user_id).exists():
            messages.error(request, 'Username already exists')
        else:
            user.username = username
            if password:  # Only update password if provided
                user.password = password
            user.teacher_id = teacher_id if teacher_id else None
            user.is_super_admin = is_super_admin
            user.can_create_users = can_create_users
            user.can_delete_users = can_delete_users
            user.can_view_dashboard = can_view_dashboard
            user.can_view_students = can_view_students
            user.can_view_teachers = can_view_teachers
            user.can_view_reports = can_view_reports
            user.can_view_marksheet = can_view_marksheet
            user.can_view_fee_structure = can_view_fee_structure
            user.can_view_fee_receipt = can_view_fee_receipt
            user.can_view_daily_expenses = can_view_daily_expenses
            user.can_view_school_settings = can_view_school_settings
            user.can_view_website_settings = can_view_website_settings
            user.can_view_user_management = can_view_user_management
            user.can_view_attendance = can_view_attendance
            user.is_active = is_active
            user.save()
            
            # Update class teacher assignment if teacher is linked
            if user.teacher:
                user.teacher.class_teacher_for = class_teacher_for if class_teacher_for else None
                user.teacher.save()
            
            messages.success(request, f'User {username} updated successfully')
            return redirect('user_management')
    
    teachers = Teacher.objects.filter(is_active=True).order_by('name')
    return render(request, 'edit_user.html', {'user': user, 'teachers': teachers})

def enable_all_permissions(request, user_id):
    """Enable all sidebar menu permissions for a user"""
    try:
        user = get_object_or_404(AdminLogin, id=user_id)
        if user.is_super_admin:
            return JsonResponse({'success': False, 'message': 'User is already a super admin with all permissions'})
        
        user.enable_all_permissions()
        return JsonResponse({'success': True, 'message': f'All permissions enabled for user {user.username}'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

def admin_logout(request):
    request.session.flush()
    messages.success(request, 'Logged out successfully')
    return redirect('admin_login_view')