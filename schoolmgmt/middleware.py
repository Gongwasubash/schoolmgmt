from django.shortcuts import redirect

class AdminAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow public pages
        public_paths = ['/', '/contact/', '/public-registration/', '/application-status/', '/public-school-calendar/']
        if request.path in public_paths or request.path.startswith('/blog/') or request.path.startswith('/application-status/'):
            response = self.get_response(request)
            return response
        
        # Allow login pages
        if request.path in ['/admin-login/', '/user-login/', '/login/', '/student-login/', '/student-dashboard/', '/student-logout/', '/user-profile/']:
            response = self.get_response(request)
            return response
        
        # Allow student access to various pages
        if request.session.get('student_logged_in'):
            student_allowed_paths = [
                '/students/', '/student-payments/', '/student-marksheet/', '/fee-receipt/',
                '/student-attendance-detail/', '/api/student-fee-history/', '/api/student-payments/',
                '/api/attendance-summary/', '/credit-slip/', '/receipt-pdf/', '/generate-receipt-pdf/',
                '/student-performance/', '/student-attendance/'
            ]
            if any(request.path.startswith(path) for path in student_allowed_paths):
                response = self.get_response(request)
                return response
        
        # Allow admin URLs
        if request.path.startswith('/admin/'):
            response = self.get_response(request)
            return response
        
        # Allow media and static files
        if request.path.startswith('/media/') or request.path.startswith('/static/'):
            response = self.get_response(request)
            return response
        
        # Allow social auth URLs
        if request.path.startswith('/auth/'):
            response = self.get_response(request)
            return response
        
        # Check if user is logged in for all other URLs
        if request.session.get('admin_logged_in') or request.session.get('student_logged_in'):
            response = self.get_response(request)
            return response
        
        # Redirect all other URLs to admin login if not authenticated
        return redirect('/admin-login/')