from django.core.management.base import BaseCommand
from schoolmgmt.models import Student

class Command(BaseCommand):
    help = 'Update all student class data from ordinal numbers to text format'

    def handle(self, *args, **options):
        class_mapping = {
            '1st': 'One',
            '2nd': 'Two', 
            '3rd': 'Three',
            '4th': 'Four',
            '5th': 'Five',
            '6th': 'Six',
            '7th': 'Seven',
            '8th': 'Eight',
            '9th': 'Nine',
            '10th': 'Ten',
            '11th': 'Eleven',
            '12th': 'Twelve'
        }
        
        updated_count = 0
        
        for old_class, new_class in class_mapping.items():
            students = Student.objects.filter(student_class=old_class)
            count = students.update(student_class=new_class)
            if count > 0:
                self.stdout.write(f"Updated {count} students from '{old_class}' to '{new_class}'")
                updated_count += count
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} student records')
        )