from django.core.management.base import BaseCommand
from django.core.files import File
from schoolmgmt.models import Student
import os
import random
import shutil
from django.conf import settings

class Command(BaseCommand):
    help = 'Assign random photos to all students from static/img/students folder'

    def handle(self, *args, **options):
        # Get all students
        students = Student.objects.all()
        
        # Get available photos
        static_photos_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'students')
        media_photos_path = os.path.join(settings.MEDIA_ROOT, 'student_photos')
        
        # Create media directory if it doesn't exist
        os.makedirs(media_photos_path, exist_ok=True)
        
        if not os.path.exists(static_photos_path):
            self.stdout.write(self.style.ERROR('Static photos folder not found'))
            return
        
        # Get all image files
        image_files = [f for f in os.listdir(static_photos_path) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        
        if not image_files:
            self.stdout.write(self.style.ERROR('No image files found'))
            return
        
        updated_count = 0
        
        for student in students:
            # Pick random image
            random_image = random.choice(image_files)
            source_path = os.path.join(static_photos_path, random_image)
            
            # Create unique filename for student
            file_extension = os.path.splitext(random_image)[1]
            new_filename = f"student_{student.id}_{random.randint(1000, 9999)}{file_extension}"
            dest_path = os.path.join(media_photos_path, new_filename)
            
            # Copy file to media folder
            shutil.copy2(source_path, dest_path)
            
            # Update student photo field
            student.photo.name = f'student_photos/{new_filename}'
            student.save(update_fields=['photo'])
            
            updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully assigned photos to {updated_count} students')
        )