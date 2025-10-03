from django.core.management.base import BaseCommand
from schoolmgmt.models import Teacher
from django.core.files import File
from django.conf import settings
import os
import random
import shutil

class Command(BaseCommand):
    help = 'Populate random photos for all staff members'

    def handle(self, *args, **options):
        # Create teacher photos directory if it doesn't exist
        teacher_photos_dir = os.path.join(settings.MEDIA_ROOT, 'teacher_photos')
        os.makedirs(teacher_photos_dir, exist_ok=True)
        
        # Source photos directory
        source_photos_dir = os.path.join(settings.BASE_DIR, 'static', 'img', 'teachers')
        
        # Check if source directory exists
        if not os.path.exists(source_photos_dir):
            self.stdout.write(
                self.style.WARNING(f'Source photos directory not found: {source_photos_dir}')
            )
            self.stdout.write(
                self.style.WARNING('Creating sample teacher photos...')
            )
            # Create the directory and add some sample photos
            os.makedirs(source_photos_dir, exist_ok=True)
            
            # Create placeholder images (you can replace these with actual photos)
            sample_photos = [
                'teacher1.jpg', 'teacher2.jpg', 'teacher3.jpg', 'teacher4.jpg',
                'teacher5.jpg', 'teacher6.jpg', 'teacher7.jpg', 'teacher8.jpg',
                'teacher9.jpg', 'teacher10.jpg', 'teacher11.jpg', 'teacher12.jpg',
                'teacher13.jpg', 'teacher14.jpg', 'teacher15.jpg', 'teacher16.jpg',
                'teacher17.jpg', 'teacher18.jpg', 'teacher19.jpg', 'teacher20.jpg'
            ]
            
            for photo_name in sample_photos:
                placeholder_path = os.path.join(source_photos_dir, photo_name)
                # Create a simple placeholder file (you should replace with actual photos)
                with open(placeholder_path, 'w') as f:
                    f.write('placeholder')
            
            self.stdout.write(
                self.style.SUCCESS(f'Created {len(sample_photos)} placeholder photos in {source_photos_dir}')
            )
            self.stdout.write(
                self.style.WARNING('Please replace placeholder files with actual teacher photos')
            )
            return
        
        # Get available photo files
        available_photos = [f for f in os.listdir(source_photos_dir) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        
        if not available_photos:
            self.stdout.write(
                self.style.ERROR('No photo files found in the source directory')
            )
            return
        
        # Get all teachers without photos
        teachers_without_photos = Teacher.objects.filter(photo__isnull=True) | Teacher.objects.filter(photo='')
        
        updated_count = 0
        
        for teacher in teachers_without_photos:
            try:
                # Select a random photo
                random_photo = random.choice(available_photos)
                source_path = os.path.join(source_photos_dir, random_photo)
                
                # Generate unique filename for this teacher
                file_extension = os.path.splitext(random_photo)[1]
                new_filename = f"teacher_{teacher.id}_{teacher.name.replace(' ', '_').lower()}{file_extension}"
                destination_path = os.path.join(teacher_photos_dir, new_filename)
                
                # Copy the photo to media directory
                shutil.copy2(source_path, destination_path)
                
                # Update teacher record
                teacher.photo = f'teacher_photos/{new_filename}'
                teacher.save()
                
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Updated photo for {teacher.name} ({teacher.designation})')
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error updating photo for {teacher.name}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated photos for {updated_count} staff members')
        )
        
        # Show summary
        total_teachers = Teacher.objects.count()
        teachers_with_photos = Teacher.objects.exclude(photo__isnull=True).exclude(photo='').count()
        
        self.stdout.write(
            self.style.SUCCESS(f'Summary: {teachers_with_photos}/{total_teachers} teachers now have photos')
        )