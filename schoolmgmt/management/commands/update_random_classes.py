from django.core.management.base import BaseCommand
from schoolmgmt.models import Student
import random

class Command(BaseCommand):
    help = 'Randomly update student classes from Nursery to Class 10'

    def handle(self, *args, **options):
        classes = ['Nursery', 'LKG', 'UKG', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th']
        
        students = Student.objects.all()
        updated_count = 0
        
        for student in students:
            new_class = random.choice(classes)
            student.student_class = new_class
            student.save()
            updated_count += 1
            self.stdout.write(f'Updated {student.name} to class {new_class}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} students with random classes')
        )