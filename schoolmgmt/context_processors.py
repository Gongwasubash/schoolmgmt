from .models import AdminLogin, SchoolDetail

def school_context(request):
    """Context processor to make school information available in all templates"""
    school_info = SchoolDetail.get_current_school()
    admin_username = request.session.get('admin_username', '')
    return {
        'school_info': school_info,
        'admin_username': admin_username
    }

def user_permissions(request):
    """Context processor to make user permissions available in all templates"""
    try:
        admin_username = request.session.get('admin_username') or request.session.get('user_username')
        
        if admin_username:
            try:
                admin = AdminLogin.objects.get(username=admin_username, is_active=True)
                
                if admin.is_super_admin:
                    permissions = {
                        'can_view_dashboard': True,
                        'can_view_students': True,
                        'can_view_teachers': True,
                        'can_view_reports': True,
                        'can_view_marksheet': True,
                        'can_view_fee_structure': True,
                        'can_view_fee_receipt': True,
                        'can_view_daily_expenses': True,
                        'can_view_school_settings': True,
                        'can_view_website_settings': True,
                        'can_view_user_management': True,
                        'can_view_attendance': True,
                    }
                else:
                    permissions = {
                        'can_view_dashboard': admin.can_view_dashboard,
                        'can_view_students': admin.can_view_students,
                        'can_view_teachers': admin.can_view_teachers,
                        'can_view_reports': admin.can_view_reports,
                        'can_view_marksheet': admin.can_view_marksheet,
                        'can_view_fee_structure': admin.can_view_fee_structure,
                        'can_view_fee_receipt': admin.can_view_fee_receipt,
                        'can_view_daily_expenses': admin.can_view_daily_expenses,
                        'can_view_school_settings': admin.can_view_school_settings,
                        'can_view_website_settings': admin.can_view_website_settings,
                        'can_view_user_management': admin.can_view_user_management,
                        'can_view_attendance': getattr(admin, 'can_view_attendance', True),
                    }
            except AdminLogin.DoesNotExist:
                # Invalid admin session, show basic permissions
                permissions = {
                    'can_view_dashboard': True,
                    'can_view_students': True,
                    'can_view_teachers': False,
                    'can_view_reports': False,
                    'can_view_marksheet': False,
                    'can_view_fee_structure': False,
                    'can_view_fee_receipt': False,
                    'can_view_daily_expenses': False,
                    'can_view_school_settings': False,
                    'can_view_website_settings': False,
                    'can_view_user_management': False,
                }
        else:
            # For users without admin session, show basic permissions
            permissions = {
                'can_view_dashboard': True,
                'can_view_students': True,
                'can_view_teachers': False,
                'can_view_reports': False,
                'can_view_marksheet': False,
                'can_view_fee_structure': False,
                'can_view_fee_receipt': False,
                'can_view_daily_expenses': False,
                'can_view_school_settings': False,
                'can_view_website_settings': False,
                'can_view_user_management': False,
                'can_view_attendance': False,
            }
        
        return {'user_permissions': permissions}
    except Exception:
        # On any error, show basic permissions to prevent complete lockout
        return {'user_permissions': {
            'can_view_dashboard': True,
            'can_view_students': True,
            'can_view_teachers': False,
            'can_view_reports': False,
            'can_view_marksheet': False,
            'can_view_fee_structure': False,
            'can_view_fee_receipt': False,
            'can_view_daily_expenses': False,
            'can_view_school_settings': False,
            'can_view_website_settings': False,
            'can_view_user_management': False,
        }}