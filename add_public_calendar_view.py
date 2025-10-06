#!/usr/bin/env python
import os
import sys

# Add the project directory to the Python path
sys.path.append('e:\\schoolmgmt')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
import django
django.setup()

# Now add the view function to views.py
view_function = '''

def public_school_calendar(request):
    """Public school calendar view for homepage navbar"""
    school = SchoolDetail.get_current_school()
    
    context = {
        'school': school,
    }
    
    return render(request, 'public_school_calendar.html', context)
'''

# Read the current views.py file
with open('e:\\schoolmgmt\\schoolmgmt\\views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add the new view function at the end
with open('e:\\schoolmgmt\\schoolmgmt\\views.py', 'w', encoding='utf-8') as f:
    f.write(content + view_function)

print("Added public_school_calendar view function to views.py")