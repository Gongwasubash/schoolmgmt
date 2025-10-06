import os
import django
from datetime import date, timedelta
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import Student, SchoolAttendance

def populate_attendance():
    # Delete all existing attendance data
    deleted_count = SchoolAttendance.objects.all().delete()[0]
    print(f"Deleted {deleted_count} existing attendance records")
    
    # Get all students
    students = Student.objects.all()
    if not students:
        print("No students found!")
        return
    
    # Start from April 14, 2025 (Baisakh 1, 2082)
    start_date = date(2025, 4, 14)
    end_date = date.today()
    
    current_date = start_date
    created_count = 0
    
    while current_date <= end_date:
        # Skip Saturdays (weekday 5)
        if current_date.weekday() != 5:
            for student in students:
                # Random attendance: 85% present, 10% absent, 5% late
                rand = random.random()
                if rand < 0.85:
                    status = 'present'
                elif rand < 0.95:
                    status = 'absent'
                else:
                    status = 'late'
                
                attendance, created = SchoolAttendance.objects.get_or_create(
                    student=student,
                    date=current_date,
                    defaults={
                        'status': status,
                        'marked_by': 'System'
                    }
                )
                if created:
                    created_count += 1
        
        current_date += timedelta(days=1)
    
    print(f"Created {created_count} attendance records from {start_date} to {end_date}")

if __name__ == "__main__":
    populate_attendance()