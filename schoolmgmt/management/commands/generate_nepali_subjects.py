from django.core.management.base import BaseCommand
from schoolmgmt.models import Subject

class Command(BaseCommand):
    help = 'Generate subjects for all classes with Nepali subject names'

    def handle(self, *args, **options):
        # Subject data for different class levels
        subjects_data = {
            # Early Childhood (Nursery, LKG, UKG)
            'early': [
                ('Nepali', 'NEP'),
                ('English', 'ENG'),
                ('Math', 'MATH'),
                ('Drawing', 'DRAW'),
                ('Rhymes', 'RHYM'),
            ],
            
            # Primary Level (1-5)
            'primary': [
                ('Nepali', 'NEP'),
                ('English', 'ENG'),
                ('Mathematics', 'MATH'),
                ('Science', 'SCI'),
                ('Social Studies', 'SS'),
                ('Health & Physical Education', 'HPE'),
                ('Art & Craft', 'ART'),
                ('Computer', 'COMP'),
            ],
            
            # Lower Secondary (6-8)
            'lower_secondary': [
                ('Nepali', 'NEP'),
                ('English', 'ENG'),
                ('Mathematics', 'MATH'),
                ('Science', 'SCI'),
                ('Social Studies', 'SS'),
                ('Health & Physical Education', 'HPE'),
                ('Computer Science', 'CS'),
                ('Optional Mathematics', 'OMATH'),
                ('Moral Education', 'ME'),
            ],
            
            # Secondary (9-10)
            'secondary': [
                ('Nepali', 'NEP'),
                ('English', 'ENG'),
                ('Mathematics', 'MATH'),
                ('Science', 'SCI'),
                ('Social Studies', 'SS'),
                ('Health & Physical Education', 'HPE'),
                ('Computer Science', 'CS'),
                ('Optional Mathematics', 'OMATH'),
                ('Account', 'ACC'),
                ('Economics', 'ECO'),
            ],
            
            # Higher Secondary (11-12)
            'higher_secondary': [
                ('Nepali', 'NEP'),
                ('English', 'ENG'),
                ('Mathematics', 'MATH'),
                ('Physics', 'PHY'),
                ('Chemistry', 'CHEM'),
                ('Biology', 'BIO'),
                ('Computer Science', 'CS'),
                ('Account', 'ACC'),
                ('Economics', 'ECO'),
                ('Business Studies', 'BS'),
                ('Marketing', 'MKT'),
                ('Hotel Management', 'HM'),
            ],
        }

        # Class mappings
        class_mappings = {
            'early': ['Nursery', 'LKG', 'UKG'],
            'primary': ['One', 'Two', 'Three', 'Four', 'Five'],
            'lower_secondary': ['Six', 'Seven', 'Eight'],
            'secondary': ['Nine', 'Ten'],
            'higher_secondary': ['Eleven', 'Twelve'],
        }

        created_count = 0
        
        for level, classes in class_mappings.items():
            subjects = subjects_data[level]
            
            for class_name in classes:
                for subject_name, subject_code in subjects:
                    # Create unique code for each class
                    unique_code = f"{subject_code}_{class_name.upper()}"
                    
                    subject, created = Subject.objects.get_or_create(
                        code=unique_code,
                        defaults={
                            'name': subject_name,
                            'class_name': class_name,
                            'max_marks': 100,
                            'pass_marks': 35,
                        }
                    )
                    
                    if created:
                        created_count += 1
                        self.stdout.write(f"Created: {subject_name} for Class {class_name}")

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} subjects')
        )