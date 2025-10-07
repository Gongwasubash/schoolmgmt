from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

class StudentAccessMiddleware:
    """Middleware to restrict student access to admin pages"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs that students should NOT access
        self.restricted_paths = [
            '/dashboard/',
            '/students/',
            '/studentlist/',
            '/teachers/',
            '/reports/',
            '/fees/',
            '/marksheet-system/',
            '/admin/',
            '/user-management/',
            '/school-settings/',
            '/website-settings/',
            '/student-daily-exp/',
            '/collection-dashboard/',
            '/attendance-report/',
            '/create-exam/',
            '/create-subject/',
            '/enter-marks/',
            '/generate-results/',
            '/fee-receipt-book/',
            '/admission-fee-table/',
            '/bulk-print-receipts/',
            '/photo-management/',
            '/id-creation/',
            '/whatsapp-balance/',
        ]
    
    def __call__(self, request):
        # Check if user is logged in as student
        if request.session.get('student_logged_in'):
            # Check if trying to access restricted path
            for restricted_path in self.restricted_paths:
                if request.path.startswith(restricted_path):
                    messages.error(request, 'Access denied. Students can only access their own dashboard.')
                    return redirect('student_dashboard')
        
        response = self.get_response(request)
        return response