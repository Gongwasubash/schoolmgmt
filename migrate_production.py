#!/usr/bin/env python
"""
Production migration script - Force create all tables
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
    print("Force creating all migrations and tables...")
    
    try:
        # Remove existing migrations (except __init__.py)
        migrations_dir = os.path.join(project_dir, 'schoolmgmt', 'migrations')
        if os.path.exists(migrations_dir):
            for file in os.listdir(migrations_dir):
                if file.endswith('.py') and file != '__init__.py':
                    file_path = os.path.join(migrations_dir, file)
                    print(f"Removing {file}")
                    os.remove(file_path)
        
        # Create fresh migrations
        print("Creating fresh migrations...")
        execute_from_command_line(['manage.py', 'makemigrations', 'schoolmgmt'])
        
        # Apply migrations
        print("Applying migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("Production database setup completed!")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()