from django.core.management.base import BaseCommand
from schoolmgmt.models import Teacher
import random

class Command(BaseCommand):
    help = 'Assign random photo URLs to all staff members'

    def handle(self, *args, **options):
        # Sample teacher photo URLs (you can replace with actual photo paths)
        photo_urls = [
            'teacher_photos/teacher1.jpg',
            'teacher_photos/teacher2.jpg', 
            'teacher_photos/teacher3.jpg',
            'teacher_photos/teacher4.jpg',
            'teacher_photos/teacher5.jpg',
            'teacher_photos/teacher6.jpg',
            'teacher_photos/teacher7.jpg',
            'teacher_photos/teacher8.jpg',
            'teacher_photos/teacher9.jpg',
            'teacher_photos/teacher10.jpg',
            'teacher_photos/teacher11.jpg',
            'teacher_photos/teacher12.jpg',
            'teacher_photos/teacher13.jpg',
            'teacher_photos/teacher14.jpg',
            'teacher_photos/teacher15.jpg',
            'teacher_photos/teacher16.jpg',
            'teacher_photos/teacher17.jpg',
            'teacher_photos/teacher18.jpg',
            'teacher_photos/teacher19.jpg',
            'teacher_photos/teacher20.jpg',
        ]
        
        # Get all teachers without photos
        teachers_without_photos = Teacher.objects.filter(photo__isnull=True) | Teacher.objects.filter(photo='')
        
        updated_count = 0
        
        for teacher in teachers_without_photos:
            # Assign a random photo URL
            random_photo = random.choice(photo_urls)
            teacher.photo = random_photo
            teacher.save()
            
            updated_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'Assigned photo to {teacher.name} ({teacher.designation}): {random_photo}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully assigned photos to {updated_count} staff members')
        )
        
        # Show summary
        total_teachers = Teacher.objects.count()
        teachers_with_photos = Teacher.objects.exclude(photo__isnull=True).exclude(photo='').count()
        
        self.stdout.write(
            self.style.SUCCESS(f'Summary: {teachers_with_photos}/{total_teachers} teachers now have photo URLs assigned')
        )