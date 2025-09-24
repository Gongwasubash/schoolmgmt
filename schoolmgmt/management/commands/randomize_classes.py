from django.core.management.base import BaseCommand
from schoolmgmt.models import Student
import random

class Command(BaseCommand):
    help = 'Randomly change student classes to different dropdown values'

    def handle(self, *args, **options):
        class_choices = [choice[0] for choice in Student.CLASS_CHOICES]
        students = Student.objects.all()
        
        for student in students:
            new_class = random.choice(class_choices)
            student.student_class = new_class
            student.save()
            self.stdout.write(f'{student.name} -> {new_class}')
        
        self.stdout.write(self.style.SUCCESS(f'Updated {students.count()} students'))