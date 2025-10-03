from django.core.management.base import BaseCommand
from schoolmgmt.models import Teacher, Subject
from collections import defaultdict

class Command(BaseCommand):
    help = 'Ensure all subjects in all classes are covered by teachers'

    def handle(self, *args, **options):
        # Get all subjects grouped by class
        all_subjects = Subject.objects.all().order_by('class_name', 'name')
        subjects_by_class = defaultdict(list)
        
        for subject in all_subjects:
            subjects_by_class[subject.class_name].append(subject.name)
        
        # Get current teacher coverage
        teachers = Teacher.objects.all()
        current_coverage = defaultdict(set)
        
        for teacher in teachers:
            if teacher.assigned_class and teacher.subjects:
                class_name = teacher.assigned_class
                if class_name != 'All Classes':
                    teacher_subjects = [s.strip() for s in teacher.subjects.split(',') if s.strip()]
                    current_coverage[class_name].update(teacher_subjects)
        
        # Find gaps and update existing teachers or create new ones
        gaps_filled = 0
        teachers_updated = 0
        
        for class_name, required_subjects in subjects_by_class.items():
            covered_subjects = current_coverage[class_name]
            missing_subjects = set(required_subjects) - covered_subjects
            
            if missing_subjects:
                self.stdout.write(f"\nClass {class_name} missing subjects: {', '.join(missing_subjects)}")
                
                # Try to find an existing teacher for this class to add missing subjects
                class_teacher = Teacher.objects.filter(assigned_class=class_name).first()
                
                if class_teacher:
                    # Add missing subjects to existing teacher
                    current_subjects = [s.strip() for s in class_teacher.subjects.split(',') if s.strip()] if class_teacher.subjects else []
                    all_subjects_for_teacher = list(set(current_subjects + list(missing_subjects)))
                    class_teacher.subjects = ', '.join(sorted(all_subjects_for_teacher))
                    class_teacher.save()
                    self.stdout.write(f"  > Updated {class_teacher.name} to cover all subjects")
                    teachers_updated += 1
                    gaps_filled += len(missing_subjects)
                else:
                    # Create new teacher for this class
                    new_teacher = self.create_teacher_for_class(class_name, required_subjects)
                    self.stdout.write(f"  > Created {new_teacher.name} to cover all subjects")
                    gaps_filled += len(missing_subjects)
            else:
                self.stdout.write(f"Class {class_name}: All subjects covered")
        
        # Verify complete coverage
        self.stdout.write(f"\n{'='*50}")
        self.stdout.write("COVERAGE VERIFICATION:")
        self.stdout.write(f"{'='*50}")
        
        total_subjects = 0
        covered_subjects = 0
        
        for class_name, required_subjects in subjects_by_class.items():
            total_subjects += len(required_subjects)
            
            # Recheck coverage after updates
            class_teachers = Teacher.objects.filter(assigned_class=class_name)
            class_coverage = set()
            
            for teacher in class_teachers:
                if teacher.subjects:
                    teacher_subjects = [s.strip() for s in teacher.subjects.split(',') if s.strip()]
                    class_coverage.update(teacher_subjects)
            
            covered_in_class = len(set(required_subjects) & class_coverage)
            covered_subjects += covered_in_class
            
            coverage_percent = (covered_in_class / len(required_subjects)) * 100
            status = "COMPLETE" if coverage_percent == 100 else f"INCOMPLETE {coverage_percent:.1f}%"
            
            self.stdout.write(f"{class_name:12} | {covered_in_class:2}/{len(required_subjects):2} subjects | {status}")
        
        overall_coverage = (covered_subjects / total_subjects) * 100
        
        self.stdout.write(f"\n{'='*50}")
        self.stdout.write(f"OVERALL COVERAGE: {covered_subjects}/{total_subjects} subjects ({overall_coverage:.1f}%)")
        self.stdout.write(f"Teachers Updated: {teachers_updated}")
        self.stdout.write(f"Subject Gaps Filled: {gaps_filled}")
        self.stdout.write(f"{'='*50}")
        
        if overall_coverage == 100:
            self.stdout.write(self.style.SUCCESS("SUCCESS: ALL SUBJECTS IN ALL CLASSES ARE NOW COVERED!"))
        else:
            self.stdout.write(self.style.WARNING(f"WARNING: Still need to cover {total_subjects - covered_subjects} subjects"))

    def create_teacher_for_class(self, class_name, subjects):
        """Create a new teacher for a specific class with all required subjects"""
        
        # Teacher names for different classes
        teacher_names = {
            'Nursery': ('Sunita Kumari Poudel', 'Female', 'Teacher'),
            'LKG': ('Kamala Devi Sharma', 'Female', 'Teacher'), 
            'UKG': ('Ganga Kumari Thapa', 'Female', 'Teacher'),
            'One': ('Bishnu Kumari Rai', 'Female', 'Teacher'),
            'Two': ('Sarita Devi Gurung', 'Female', 'Teacher'),
            'Three': ('Manju Kumari Magar', 'Female', 'Teacher'),
            'Four': ('Purnima Devi Tamang', 'Female', 'Teacher'),
            'Five': ('Sabita Kumari Limbu', 'Female', 'Teacher'),
            'Six': ('Indira Devi Sherpa', 'Female', 'Senior Teacher'),
            'Seven': ('Kopila Kumari Chhetri', 'Female', 'Senior Teacher'),
            'Eight': ('Sarmila Devi Bhattarai', 'Female', 'Senior Teacher'),
            'Nine': ('Renu Kumari Khadka', 'Female', 'Senior Teacher'),
            'Ten': ('Bimala Devi Acharya', 'Female', 'Senior Teacher'),
            'Eleven': ('Sangita Kumari Pandey', 'Female', 'Senior Teacher'),
            'Twelve': ('Urmila Devi Joshi', 'Female', 'Head Teacher'),
        }
        
        name, gender, designation = teacher_names.get(class_name, ('New Teacher', 'Female', 'Teacher'))
        
        # Nepali addresses
        addresses = [
            "Bhaktapur-4, Madhyapur Thimi",
            "Lalitpur-8, Patan Dhoka", 
            "Kathmandu-16, Bouddha",
            "Bhaktapur-12, Suryabinayak",
            "Kathmandu-32, Tokha"
        ]
        
        import random
        from datetime import date, timedelta
        
        teacher = Teacher.objects.create(
            name=name,
            address=random.choice(addresses),
            designation=designation,
            phone_number=f"98{random.randint(10000000, 99999999)}",
            email=f"{name.lower().replace(' ', '.')}@everestacademy.edu.np",
            gender=gender,
            joining_date=date.today() - timedelta(days=random.randint(365, 1825)),
            qualification="Bachelor's Degree in Education",
            assigned_class=class_name,
            subject_specialization=subjects[0] if subjects else "General",
            subjects=', '.join(sorted(subjects)),
            salary=random.randint(25000, 45000),
            is_active=True
        )
        
        return teacher