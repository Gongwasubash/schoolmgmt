from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import AdminLogin
import hashlib

def admin_login(request):
    """Simple admin login function"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, 'Please enter both username and password')
            return render(request, 'admin_login.html')
        
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        
        try:
            admin = AdminLogin.objects.get(username=username, password=hashed_password, is_active=True)
            request.session['admin_id'] = admin.id
            request.session['admin_username'] = admin.username
            request.session['is_super_admin'] = admin.is_super_admin
            
            # Set permissions in session
            request.session['can_create_users'] = admin.can_create_users or admin.is_super_admin
            request.session['can_delete_users'] = admin.can_delete_users or admin.is_super_admin
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
            request.session['can_view_settings'] = admin.can_view_settings or admin.is_super_admin
            
            messages.success(request, f'Welcome {admin.username}! Logged in successfully.')
            return redirect('dashboard')
        except AdminLogin.DoesNotExist:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'admin_login.html')

def admin_logout(request):
    """Simple admin logout function"""
    request.session.flush()
    messages.success(request, 'Logged out successfully')
    return redirect('admin_login')