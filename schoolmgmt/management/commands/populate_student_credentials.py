from django.core.management.base import BaseCommand
from schoolmgmt.models import Student

class Command(BaseCommand):
    help = 'Populate username and password for all students'

    def handle(self, *args, **options):
        students = Student.objects.filter(username__isnull=True)
        updated_count = 0
        
        for student in students:
            # Generate username from reg_number or student ID
            username = f"student_{student.reg_number}" if student.reg_number else f"student_{student.id}"
            
            # Generate simple password (reg_number + name first 3 chars)
            password = f"{student.reg_number}{student.name[:3].lower()}" if student.reg_number else f"{student.id}{student.name[:3].lower()}"
            
            # Update student credentials
            student.username = username
            student.password = password
            student.save()
            
            updated_count += 1
            self.stdout.write(f"Updated: {student.name} - Username: {username}, Password: {password}")
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} student credentials')
        )