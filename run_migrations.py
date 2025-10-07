#!/usr/bin/env python
"""
Script to run Django migrations to create missing database tables
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
    django.setup()
    
    print("Running Django migrations...")
    
    try:
        # Run makemigrations first
        print("1. Creating migrations...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        
        # Run migrate
        print("2. Applying migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("✅ Migrations completed successfully!")
        
    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        sys.exit(1)