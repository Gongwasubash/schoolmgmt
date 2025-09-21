from django.core.management.base import BaseCommand
from schoolmgmt.models import Subject

class Command(BaseCommand):
    help = 'Generate Nepali school subjects for all classes'

    def handle(self, *args, **options):
        subjects_data = [
            # Nursery
            {'name': 'English', 'code': 'ENG-N', 'class_name': 'Nursery', 'max_marks': 50, 'pass_marks': 20},
            {'name': 'Nepali', 'code': 'NEP-N', 'class_name': 'Nursery', 'max_marks': 50, 'pass_marks': 20},
            {'name': 'Math', 'code': 'MAT-N', 'class_name': 'Nursery', 'max_marks': 50, 'pass_marks': 20},
            
            # LKG
            {'name': 'English', 'code': 'ENG-L', 'class_name': 'LKG', 'max_marks': 50, 'pass_marks': 20},
            {'name': 'Nepali', 'code': 'NEP-L', 'class_name': 'LKG', 'max_marks': 50, 'pass_marks': 20},
            {'name': 'Math', 'code': 'MAT-L', 'class_name': 'LKG', 'max_marks': 50, 'pass_marks': 20},
            
            # UKG
            {'name': 'English', 'code': 'ENG-U', 'class_name': 'UKG', 'max_marks': 50, 'pass_marks': 20},
            {'name': 'Nepali', 'code': 'NEP-U', 'class_name': 'UKG', 'max_marks': 50, 'pass_marks': 20},
            {'name': 'Math', 'code': 'MAT-U', 'class_name': 'UKG', 'max_marks': 50, 'pass_marks': 20},
            
            # Class 1
            {'name': 'English', 'code': 'ENG-1', 'class_name': '1st', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Nepali', 'code': 'NEP-1', 'class_name': '1st', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Math', 'code': 'MAT-1', 'class_name': '1st', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Social Studies', 'code': 'SOC-1', 'class_name': '1st', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Science', 'code': 'SCI-1', 'class_name': '1st', 'max_marks': 100, 'pass_marks': 35},
            
            # Class 2
            {'name': 'English', 'code': 'ENG-2', 'class_name': '2nd', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Nepali', 'code': 'NEP-2', 'class_name': '2nd', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Math', 'code': 'MAT-2', 'class_name': '2nd', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Social Studies', 'code': 'SOC-2', 'class_name': '2nd', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Science', 'code': 'SCI-2', 'class_name': '2nd', 'max_marks': 100, 'pass_marks': 35},
            
            # Class 3
            {'name': 'English', 'code': 'ENG-3', 'class_name': '3rd', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Nepali', 'code': 'NEP-3', 'class_name': '3rd', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Math', 'code': 'MAT-3', 'class_name': '3rd', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Social Studies', 'code': 'SOC-3', 'class_name': '3rd', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Science', 'code': 'SCI-3', 'class_name': '3rd', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Computer', 'code': 'COM-3', 'class_name': '3rd', 'max_marks': 100, 'pass_marks': 35},
            
            # Class 4
            {'name': 'English', 'code': 'ENG-4', 'class_name': '4th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Nepali', 'code': 'NEP-4', 'class_name': '4th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Math', 'code': 'MAT-4', 'class_name': '4th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Social Studies', 'code': 'SOC-4', 'class_name': '4th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Science', 'code': 'SCI-4', 'class_name': '4th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Computer', 'code': 'COM-4', 'class_name': '4th', 'max_marks': 100, 'pass_marks': 35},
            
            # Class 5
            {'name': 'English', 'code': 'ENG-5', 'class_name': '5th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Nepali', 'code': 'NEP-5', 'class_name': '5th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Math', 'code': 'MAT-5', 'class_name': '5th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Social Studies', 'code': 'SOC-5', 'class_name': '5th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Science', 'code': 'SCI-5', 'class_name': '5th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Computer', 'code': 'COM-5', 'class_name': '5th', 'max_marks': 100, 'pass_marks': 35},
            
            # Class 6
            {'name': 'English', 'code': 'ENG-6', 'class_name': '6th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Nepali', 'code': 'NEP-6', 'class_name': '6th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Math', 'code': 'MAT-6', 'class_name': '6th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Social Studies', 'code': 'SOC-6', 'class_name': '6th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Science', 'code': 'SCI-6', 'class_name': '6th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Computer', 'code': 'COM-6', 'class_name': '6th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Health & Physical Education', 'code': 'HPE-6', 'class_name': '6th', 'max_marks': 100, 'pass_marks': 35},
            
            # Class 7
            {'name': 'English', 'code': 'ENG-7', 'class_name': '7th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Nepali', 'code': 'NEP-7', 'class_name': '7th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Math', 'code': 'MAT-7', 'class_name': '7th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Social Studies', 'code': 'SOC-7', 'class_name': '7th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Science', 'code': 'SCI-7', 'class_name': '7th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Computer', 'code': 'COM-7', 'class_name': '7th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Health & Physical Education', 'code': 'HPE-7', 'class_name': '7th', 'max_marks': 100, 'pass_marks': 35},
            
            # Class 8
            {'name': 'English', 'code': 'ENG-8', 'class_name': '8th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Nepali', 'code': 'NEP-8', 'class_name': '8th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Math', 'code': 'MAT-8', 'class_name': '8th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Social Studies', 'code': 'SOC-8', 'class_name': '8th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Science', 'code': 'SCI-8', 'class_name': '8th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Computer', 'code': 'COM-8', 'class_name': '8th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Health & Physical Education', 'code': 'HPE-8', 'class_name': '8th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Occupation & Business', 'code': 'OCC-8', 'class_name': '8th', 'max_marks': 100, 'pass_marks': 35},
            
            # Class 9
            {'name': 'English', 'code': 'ENG-9', 'class_name': '9th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Nepali', 'code': 'NEP-9', 'class_name': '9th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Math', 'code': 'MAT-9', 'class_name': '9th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Social Studies', 'code': 'SOC-9', 'class_name': '9th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Science', 'code': 'SCI-9', 'class_name': '9th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Computer', 'code': 'COM-9', 'class_name': '9th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Health & Physical Education', 'code': 'HPE-9', 'class_name': '9th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Occupation & Business', 'code': 'OCC-9', 'class_name': '9th', 'max_marks': 100, 'pass_marks': 35},
            
            # Class 10
            {'name': 'English', 'code': 'ENG-10', 'class_name': '10th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Nepali', 'code': 'NEP-10', 'class_name': '10th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Math', 'code': 'MAT-10', 'class_name': '10th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Social Studies', 'code': 'SOC-10', 'class_name': '10th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Science', 'code': 'SCI-10', 'class_name': '10th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Computer', 'code': 'COM-10', 'class_name': '10th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Health & Physical Education', 'code': 'HPE-10', 'class_name': '10th', 'max_marks': 100, 'pass_marks': 35},
            {'name': 'Occupation & Business', 'code': 'OCC-10', 'class_name': '10th', 'max_marks': 100, 'pass_marks': 35},
        ]

        created_count = 0
        for subject_data in subjects_data:
            subject, created = Subject.objects.get_or_create(
                code=subject_data['code'],
                defaults=subject_data
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created: {subject.name} - {subject.class_name}")
            else:
                self.stdout.write(f"Already exists: {subject.name} - {subject.class_name}")

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} subjects')
        )