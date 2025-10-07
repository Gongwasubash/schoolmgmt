from django.conf import settings
from django.urls import include, path
from django.core.wsgi import get_wsgi_application
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from django.urls import get_resolver
from django.conf.urls import include

def print_urls():
    resolver = get_resolver()
    for pattern in resolver.url_patterns:
        if hasattr(pattern, 'pattern'):
            print(f"Pattern: {pattern.pattern}")
        if hasattr(pattern, 'url_patterns'):
            print(f"Include: {pattern}")

if __name__ == "__main__":
    print_urls()