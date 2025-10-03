from django.core.management.base import BaseCommand
from schoolmgmt.models import Teacher, Subject, TeacherClassSubject
import random

class Command(BaseCommand):
    help = 'Populate class and subject assignments for all teachers'

    def handle(self, *args, **options):
        teachers = Teacher.objects.all()
        subjects = Subject.objects.all()
        
        if not teachers.exists():
            self.stdout.write(self.style.ERROR('No teachers found'))
            return
            
        if not subjects.exists():
            self.stdout.write(self.style.ERROR('No subjects found'))
            return

        # Clear existing assignments
        TeacherClassSubject.objects.all().delete()
        
        for teacher in teachers:
            # Get random classes (1-3 classes per teacher)
            classes = ['Nursery', 'LKG', 'UKG', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten']
            assigned_classes = random.sample(classes, random.randint(1, 3))
            
            for class_name in assigned_classes:
                # Get subjects for this class
                class_subjects = subjects.filter(class_name=class_name)
                if class_subjects.exists():
                    # Assign 1-3 subjects per class
                    num_subjects = min(random.randint(1, 3), class_subjects.count())
                    selected_subjects = random.sample(list(class_subjects), num_subjects)
                    
                    for subject in selected_subjects:
                        TeacherClassSubject.objects.create(
                            teacher=teacher,
                            class_name=class_name,
                            subject=subject,
                            is_active=True
                        )
        
        total_assignments = TeacherClassSubject.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {total_assignments} teacher assignments')
        )