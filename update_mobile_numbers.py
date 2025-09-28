import os
import django
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import Student

# Mobile numbers to assign randomly
mobile_numbers = [
    '977 986-6556633',
    '+977 981-8291035', 
    '+977 984-0564096'
]

# Update all students with random mobile numbers
students = Student.objects.all()
for student in students:
    student.mobile = random.choice(mobile_numbers)
    student.save()

print(f"Updated {students.count()} students with random mobile numbers")