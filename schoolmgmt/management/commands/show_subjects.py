from django.core.management.base import BaseCommand
from schoolmgmt.models import Subject
from collections import defaultdict

class Command(BaseCommand):
    help = 'Show all subjects grouped by class'

    def handle(self, *args, **options):
        subjects_by_class = defaultdict(list)
        
        for subject in Subject.objects.all().order_by('class_name', 'name'):
            subjects_by_class[subject.class_name].append(subject.name)
        
        self.stdout.write("=== ALL SUBJECTS BY CLASS ===")
        for class_name, subjects in subjects_by_class.items():
            self.stdout.write(f"\n{class_name}:")
            for subject in subjects:
                self.stdout.write(f"  - {subject}")
        
        total_subjects = Subject.objects.count()
        unique_subjects = Subject.objects.values('name').distinct().count()
        self.stdout.write(f"\nTotal subject entries: {total_subjects}")
        self.stdout.write(f"Unique subjects: {unique_subjects}")