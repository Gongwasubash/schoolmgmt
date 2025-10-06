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
        if request.path in ['/admin-login/', '/user-login/', '/login/']:
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
        
        # Check if user is logged in for all other URLs
        if request.session.get('admin_logged_in'):
            response = self.get_response(request)
            return response
        
        # Redirect all other URLs to admin login if not authenticated
        return redirect('/admin-login/')