from django.shortcuts import redirect
from django.urls import reverse

class AdminAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs that don't require authentication
        public_urls = [
            reverse('admin_login'),
            reverse('home'),
            reverse('public_registration'),
            reverse('blog_list'),
            reverse('contact'),
            '/admin/',
            '/blog/',
            '/blogs/',
            '/media/',  # Allow access to media files (images, etc.)
            '/static/', # Allow access to static files
        ]
        
        # Allow all blog detail URLs
        if request.path.startswith('/blog/'):
            response = self.get_response(request)
            return response
        
        # Allow media and static files
        if request.path.startswith('/media/') or request.path.startswith('/static/'):
            response = self.get_response(request)
            return response
        
        # Check if user is accessing a public URL
        if request.path in public_urls:
            response = self.get_response(request)
            return response
        
        # Check if admin is logged in
        if not request.session.get('admin_logged_in'):
            return redirect('admin_login')
        
        response = self.get_response(request)
        return response