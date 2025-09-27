import os
import random
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from schoolmgmt.models import Student

class Command(BaseCommand):
    help = 'Assign random photos from students folder to all students'

    def handle(self, *args, **options):
        # Path to the students photos folder
        source_folder = os.path.join(settings.BASE_DIR, 'static', 'img', 'students')
        
        # Get all photo files from the students folder
        if not os.path.exists(source_folder):
            self.stdout.write(self.style.ERROR(f'Students folder not found: {source_folder}'))
            return
        
        photo_files = [f for f in os.listdir(source_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        
        if not photo_files:
            self.stdout.write(self.style.ERROR('No photo files found in students folder'))
            return
        
        self.stdout.write(f'Found {len(photo_files)} photos in students folder')
        
        # Get all students without photos
        students = Student.objects.filter(photo__isnull=True) | Student.objects.filter(photo='')
        
        if not students.exists():
            self.stdout.write(self.style.SUCCESS('All students already have photos assigned'))
            return
        
        self.stdout.write(f'Found {students.count()} students without photos')
        
        # Create media directory if it doesn't exist
        media_student_photos = os.path.join(settings.MEDIA_ROOT, 'student_photos')
        os.makedirs(media_student_photos, exist_ok=True)
        
        assigned_count = 0
        
        for student in students:
            # Pick a random photo
            random_photo = random.choice(photo_files)
            source_path = os.path.join(source_folder, random_photo)
            
            # Create unique filename for the student
            file_extension = os.path.splitext(random_photo)[1]
            new_filename = f"student_{student.reg_number}_{random.randint(1000, 9999)}{file_extension}"
            destination_path = os.path.join(media_student_photos, new_filename)
            
            try:
                # Copy the photo to media folder
                shutil.copy2(source_path, destination_path)
                
                # Update student record
                student.photo = f'student_photos/{new_filename}'
                student.save()
                
                assigned_count += 1
                self.stdout.write(f'Assigned {random_photo} to {student.name} (Reg: {student.reg_number})')
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error assigning photo to {student.name}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully assigned photos to {assigned_count} students'))