from .models import AdminLogin, SchoolDetail

def user_permissions(request):
    """Context processor for user permissions"""
    try:
        user_id = request.session.get('user_id')
        
        if user_id:
            try:
                user = AdminLogin.objects.get(id=user_id, is_active=True)
                
                if user.is_super_admin:
                    permissions = {
                        'can_view_dashboard': True,
                        'can_view_charts': True,
                        'can_view_stats': True,
                        'can_view_students': True,
                        'can_view_teachers': True,
                        'can_view_reports': True,
                        'can_view_marksheet': True,
                        'can_view_fees': True,
                        'can_view_receipts': True,
                        'can_view_expenses': True,
                        'can_view_settings': True,
                    }
                else:
                    permissions = {
                        'can_view_dashboard': user.can_view_dashboard,
                        'can_view_charts': getattr(user, 'can_view_charts', True),
                        'can_view_stats': getattr(user, 'can_view_stats', True),
                        'can_view_students': user.can_view_students,
                        'can_view_teachers': user.can_view_teachers,
                        'can_view_reports': user.can_view_reports,
                        'can_view_marksheet': user.can_view_marksheet,
                        'can_view_fees': getattr(user, 'can_view_fees', True),
                        'can_view_receipts': getattr(user, 'can_view_receipts', True),
                        'can_view_expenses': getattr(user, 'can_view_expenses', True),
                        'can_view_settings': getattr(user, 'can_view_settings', True),
                    }
                
                return {
                    'user_permissions': permissions,
                    'user_info': user
                }
            except AdminLogin.DoesNotExist:
                pass
        
        return {
            'user_permissions': {
                'can_view_dashboard': False,
                'can_view_charts': False,
                'can_view_stats': False,
                'can_view_students': False,
                'can_view_teachers': False,
                'can_view_reports': False,
                'can_view_marksheet': False,
                'can_view_fees': False,
                'can_view_receipts': False,
                'can_view_expenses': False,
                'can_view_settings': False,
            },
            'user_info': None
        }
    except Exception:
        return {
            'user_permissions': {
                'can_view_dashboard': False,
                'can_view_charts': False,
                'can_view_stats': False,
                'can_view_students': False,
                'can_view_teachers': False,
                'can_view_reports': False,
                'can_view_marksheet': False,
                'can_view_fees': False,
                'can_view_receipts': False,
                'can_view_expenses': False,
                'can_view_settings': False,
            },
            'user_info': None
        }