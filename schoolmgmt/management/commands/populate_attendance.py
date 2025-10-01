from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
import random
from schoolmgmt.models import Student, StudentAttendance

class Command(BaseCommand):
    help = 'Populate 6 months of random attendance data'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing attendance data first')

    def handle(self, *args, **options):
        students = Student.objects.all()
        student_count = students.count()
        
        self.stdout.write(f'Found {student_count} students')
        
        if student_count == 0:
            self.stdout.write('No students found. Please add students first.')
            return

        if options['clear']:
            deleted_count = StudentAttendance.objects.all().delete()[0]
            self.stdout.write(f'Cleared {deleted_count} existing attendance records')

        # Generate dates for last 6 months
        end_date = date.today()
        start_date = end_date - timedelta(days=180)
        
        statuses = ['present', 'absent', 'late']
        weights = [0.8, 0.15, 0.05]  # 80% present, 15% absent, 5% late
        
        created_count = 0
        skipped_count = 0
        current_date = start_date
        
        self.stdout.write(f'Generating attendance from {start_date} to {end_date}')
        
        while current_date <= end_date:
            # Skip weekends
            if current_date.weekday() < 5:  # Monday=0, Sunday=6
                for student in students:
                    if not StudentAttendance.objects.filter(student=student, date=current_date).exists():
                        status = random.choices(statuses, weights=weights)[0]
                        StudentAttendance.objects.create(
                            student=student,
                            date=current_date,
                            status=status,
                            marked_by='System'
                        )
                        created_count += 1
                    else:
                        skipped_count += 1
            
            current_date += timedelta(days=1)
        
        self.stdout.write(f'Created {created_count} new attendance records')
        self.stdout.write(f'Skipped {skipped_count} existing records')
        self.stdout.write(f'Total attendance records: {StudentAttendance.objects.count()}')