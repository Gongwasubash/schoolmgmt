from .models import SchoolDetail

def school_context(request):
    """
    Context processor to make school information available in all templates
    """
    try:
        school_info = SchoolDetail.get_current_school()
        return {
            'school_info': school_info
        }
    except Exception:
        # Fallback data if database is not available
        return {
            'school_info': {
                'school_name': 'Everest Academy',
                'logo': None,
                'address': 'Kathmandu, Nepal',
                'phone': '+977-1-4444444',
                'email': 'info@everestacademy.edu.np'
            }
        }