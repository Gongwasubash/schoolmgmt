from django.core.management.base import BaseCommand
from schoolmgmt.models import Teacher, Subject
from collections import defaultdict

class Command(BaseCommand):
    help = 'Show detailed teacher-subject coverage for all classes'

    def handle(self, *args, **options):
        # Get all subjects by class
        subjects_by_class = defaultdict(list)
        for subject in Subject.objects.all().order_by('class_name', 'name'):
            subjects_by_class[subject.class_name].append(subject.name)
        
        # Get teachers by class
        teachers_by_class = defaultdict(list)
        for teacher in Teacher.objects.filter(is_active=True).order_by('assigned_class', 'name'):
            if teacher.assigned_class and teacher.assigned_class != 'All Classes':
                teachers_by_class[teacher.assigned_class].append(teacher)
        
        self.stdout.write("COMPLETE TEACHER-SUBJECT COVERAGE REPORT")
        self.stdout.write("=" * 80)
        
        total_classes = len(subjects_by_class)
        total_subjects = sum(len(subjects) for subjects in subjects_by_class.values())
        
        for class_name in sorted(subjects_by_class.keys()):
            required_subjects = set(subjects_by_class[class_name])
            class_teachers = teachers_by_class[class_name]
            
            self.stdout.write(f"\nCLASS: {class_name}")
            self.stdout.write("-" * 40)
            self.stdout.write(f"Required Subjects ({len(required_subjects)}): {', '.join(sorted(required_subjects))}")
            
            if class_teachers:
                self.stdout.write(f"\nTeachers ({len(class_teachers)}):")
                covered_subjects = set()
                
                for teacher in class_teachers:
                    teacher_subjects = []
                    if teacher.subjects:
                        teacher_subjects = [s.strip() for s in teacher.subjects.split(',') if s.strip()]
                        covered_subjects.update(teacher_subjects)
                    
                    self.stdout.write(f"  * {teacher.name} ({teacher.designation})")
                    self.stdout.write(f"    Subjects: {', '.join(sorted(teacher_subjects)) if teacher_subjects else 'None'}")
                
                # Check coverage
                missing_subjects = required_subjects - covered_subjects
                coverage_percent = ((len(required_subjects) - len(missing_subjects)) / len(required_subjects)) * 100
                
                self.stdout.write(f"\nCoverage: {coverage_percent:.1f}% ({len(required_subjects) - len(missing_subjects)}/{len(required_subjects)} subjects)")
                
                if missing_subjects:
                    self.stdout.write(f"Missing: {', '.join(sorted(missing_subjects))}")
                else:
                    self.stdout.write("Status: COMPLETE COVERAGE")
            else:
                self.stdout.write("Teachers: None assigned")
                self.stdout.write("Status: NO COVERAGE")
        
        # Summary
        self.stdout.write(f"\n{'=' * 80}")
        self.stdout.write("SUMMARY:")
        self.stdout.write(f"Total Classes: {total_classes}")
        self.stdout.write(f"Total Subjects: {total_subjects}")
        self.stdout.write(f"Total Active Teachers: {Teacher.objects.filter(is_active=True).count()}")
        
        # Calculate overall coverage
        total_covered = 0
        for class_name in subjects_by_class.keys():
            required_subjects = set(subjects_by_class[class_name])
            class_teachers = teachers_by_class[class_name]
            covered_subjects = set()
            
            for teacher in class_teachers:
                if teacher.subjects:
                    teacher_subjects = [s.strip() for s in teacher.subjects.split(',') if s.strip()]
                    covered_subjects.update(teacher_subjects)
            
            total_covered += len(required_subjects & covered_subjects)
        
        overall_coverage = (total_covered / total_subjects) * 100
        self.stdout.write(f"Overall Coverage: {overall_coverage:.1f}% ({total_covered}/{total_subjects} subjects)")
        
        if overall_coverage == 100:
            self.stdout.write(self.style.SUCCESS("STATUS: ALL SUBJECTS COVERED!"))
        else:
            self.stdout.write(self.style.WARNING(f"STATUS: {total_subjects - total_covered} subjects still need coverage"))