from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .models import AdminLogin

def permission_required(permission_name):
    """Decorator to check if user has specific permission"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            admin_id = request.session.get('admin_id')
            
            # If no admin session, check if user is logged in
            if not admin_id and not request.session.get('admin_logged_in'):
                return redirect('admin_login_view')
            
            # Check permission from session, default to True for super admin
            if request.session.get('is_super_admin', False):
                has_permission = True
            else:
                has_permission = request.session.get(permission_name, False)
            if not has_permission:
                messages.error(request, 'You do not have permission to access this page')
                # Redirect to first available permitted page
                if request.session.get('can_view_dashboard', False):
                    return redirect('dashboard')
                elif request.session.get('can_view_students', False):
                    return redirect('students')
                elif request.session.get('can_view_teachers', False):
                    return redirect('teachers')
                elif request.session.get('can_view_reports', False):
                    return redirect('reports')
                elif request.session.get('can_view_marksheet', False):
                    return redirect('marksheet_system')
                elif request.session.get('can_view_fees', False):
                    return redirect('fees')
                elif request.session.get('can_view_receipts', False):
                    return redirect('fee_receipt_book')
                elif request.session.get('can_view_expenses', False):
                    return redirect('student_daily_exp')
                elif request.session.get('can_view_settings', False):
                    return redirect('school_settings')
                else:
                    return redirect('home')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator