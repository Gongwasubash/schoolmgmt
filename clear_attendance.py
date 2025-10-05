import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import StudentAttendance

# Clear all student attendance data
deleted_count = StudentAttendance.objects.all().delete()[0]
print(f'Deleted {deleted_count} student attendance records')
print('All student attendance data has been removed')