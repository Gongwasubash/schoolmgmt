import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('e:\\schoolmgmt')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import SchoolDetail

# Get or create school
school = SchoolDetail.get_current_school()
print(f"Current school: {school.school_name}")
print(f"Current logo: {school.logo}")

# Set the logo
school.logo = 'school_logos/Everest-Crest-Square.png'
school.save()

print(f"Logo updated to: {school.logo}")
print("School logo has been set successfully!")