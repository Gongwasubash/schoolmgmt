#!/usr/bin/env python
"""
Script to fix database issues by running migrations
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')

# Setup Django
django.setup()

def main():
    print("Fixing database issues...")
    
    try:
        # Run makemigrations first
        print("1. Creating migrations...")
        execute_from_command_line(['manage.py', 'makemigrations', 'schoolmgmt'])
        
        # Run migrate
        print("2. Applying migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("Database fixed successfully!")
        print("Your application should now work properly.")
        
    except Exception as e:
        print(f"Error fixing database: {e}")
        print("\nManual steps to fix:")
        print("1. Run: python manage.py makemigrations")
        print("2. Run: python manage.py migrate")
        sys.exit(1)

if __name__ == '__main__':
    main()