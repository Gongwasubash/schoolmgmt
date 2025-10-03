from django.core.management.base import BaseCommand
from schoolmgmt.models import Teacher
from django.core.files import File
import os
import random
import shutil
from django.conf import settings

class Command(BaseCommand):
    help = 'Assign random teacher photos to teachers'

    def handle(self, *args, **options):
        # Source and destination paths
        source_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'teacher')
        media_path = os.path.join(settings.MEDIA_ROOT, 'teacher_photos')
        
        # Create media directory if it doesn't exist
        os.makedirs(media_path, exist_ok=True)
        
        # Get all teacher images
        if os.path.exists(source_path):
            teacher_images = [f for f in os.listdir(source_path) 
                            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        else:
            self.stdout.write(self.style.ERROR('Teacher images folder not found'))
            return
        
        if not teacher_images:
            self.stdout.write(self.style.ERROR('No teacher images found'))
            return
        
        # Get all teachers
        teachers = Teacher.objects.all()
        
        if not teachers:
            self.stdout.write(self.style.ERROR('No teachers found'))
            return
        
        updated_count = 0
        
        for teacher in teachers:
            # Select random image
            random_image = random.choice(teacher_images)
            source_file = os.path.join(source_path, random_image)
            
            # Create unique filename
            name_parts = teacher.name.lower().replace(' ', '_')
            file_extension = os.path.splitext(random_image)[1]
            new_filename = f"{name_parts}_{teacher.id}{file_extension}"
            
            # Copy file to media directory
            destination_file = os.path.join(media_path, new_filename)
            shutil.copy2(source_file, destination_file)
            
            # Update teacher photo field
            teacher.photo = f'teacher_photos/{new_filename}'
            teacher.save()
            
            updated_count += 1
            self.stdout.write(f"Assigned photo to: {teacher.name}")
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully assigned photos to {updated_count} teachers')
        )