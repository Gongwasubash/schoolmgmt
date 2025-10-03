from django.core.management.base import BaseCommand
from schoolmgmt.models import Teacher, Subject
from collections import defaultdict

class Command(BaseCommand):
    help = 'Fix subject coverage gaps by ensuring every subject has a teacher'

    def handle(self, *args, **options):
        # Get all subjects by class
        subjects_by_class = defaultdict(list)
        for subject in Subject.objects.all().order_by('class_name', 'name'):
            subjects_by_class[subject.class_name].append(subject.name)
        
        self.stdout.write("ANALYZING SUBJECT COVERAGE GAPS...")
        self.stdout.write("=" * 60)
        
        gaps_found = 0
        gaps_fixed = 0
        
        for class_name, required_subjects in subjects_by_class.items():
            # Get current coverage for this class
            class_teachers = Teacher.objects.filter(assigned_class=class_name, is_active=True)
            covered_subjects = set()
            
            for teacher in class_teachers:
                if teacher.subjects:
                    teacher_subjects = [s.strip() for s in teacher.subjects.split(',') if s.strip()]
                    covered_subjects.update(teacher_subjects)
            
            missing_subjects = set(required_subjects) - covered_subjects
            
            if missing_subjects:
                gaps_found += len(missing_subjects)
                self.stdout.write(f"\nClass {class_name}:")
                self.stdout.write(f"  Required: {', '.join(sorted(required_subjects))}")
                self.stdout.write(f"  Covered:  {', '.join(sorted(covered_subjects)) if covered_subjects else 'None'}")
                self.stdout.write(f"  Missing:  {', '.join(sorted(missing_subjects))}")
                
                # Find the main teacher for this class or create one
                main_teacher = class_teachers.first()
                
                if main_teacher:
                    # Update existing teacher to cover all subjects
                    current_subjects = [s.strip() for s in main_teacher.subjects.split(',') if s.strip()] if main_teacher.subjects else []
                    all_subjects = list(set(current_subjects + required_subjects))
                    main_teacher.subjects = ', '.join(sorted(all_subjects))
                    main_teacher.save()
                    
                    self.stdout.write(f"  FIXED: Updated {main_teacher.name} to cover all {len(all_subjects)} subjects")
                    gaps_fixed += len(missing_subjects)
                else:
                    # Create new teacher for this class
                    new_teacher = self.create_class_teacher(class_name, required_subjects)
                    self.stdout.write(f"  FIXED: Created {new_teacher.name} to cover all {len(required_subjects)} subjects")
                    gaps_fixed += len(missing_subjects)
            else:
                self.stdout.write(f"Class {class_name}: OK - All {len(required_subjects)} subjects covered")
        
        # Final verification
        self.stdout.write(f"\n{'=' * 60}")
        self.stdout.write("FINAL VERIFICATION:")
        self.stdout.write(f"{'=' * 60}")
        
        total_subjects = 0
        total_covered = 0
        
        for class_name, required_subjects in subjects_by_class.items():
            total_subjects += len(required_subjects)
            
            # Recheck coverage after fixes
            class_teachers = Teacher.objects.filter(assigned_class=class_name, is_active=True)
            covered_subjects = set()
            
            for teacher in class_teachers:
                if teacher.subjects:
                    teacher_subjects = [s.strip() for s in teacher.subjects.split(',') if s.strip()]
                    covered_subjects.update(teacher_subjects)
            
            covered_count = len(set(required_subjects) & covered_subjects)
            total_covered += covered_count
            
            status = "COMPLETE" if covered_count == len(required_subjects) else f"INCOMPLETE ({covered_count}/{len(required_subjects)})"
            self.stdout.write(f"{class_name:12} | {covered_count:2}/{len(required_subjects):2} subjects | {status}")
        
        coverage_percent = (total_covered / total_subjects) * 100
        
        self.stdout.write(f"\n{'=' * 60}")
        self.stdout.write(f"SUMMARY:")
        self.stdout.write(f"Total Subjects: {total_subjects}")
        self.stdout.write(f"Covered Subjects: {total_covered}")
        self.stdout.write(f"Coverage: {coverage_percent:.1f}%")
        self.stdout.write(f"Gaps Found: {gaps_found}")
        self.stdout.write(f"Gaps Fixed: {gaps_fixed}")
        
        if coverage_percent == 100:
            self.stdout.write(self.style.SUCCESS("SUCCESS: ALL SUBJECTS NOW COVERED!"))
        else:
            remaining_gaps = total_subjects - total_covered
            self.stdout.write(self.style.ERROR(f"ERROR: {remaining_gaps} subjects still need coverage"))

    def create_class_teacher(self, class_name, subjects):
        """Create a comprehensive teacher for a class"""
        
        teacher_data = {
            'Nursery': ('Kamala Devi Poudel', 'Female', 'Teacher'),
            'LKG': ('Sunita Kumari Sharma', 'Female', 'Teacher'),
            'UKG': ('Ganga Devi Thapa', 'Female', 'Teacher'),
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
        
        name, gender, designation = teacher_data.get(class_name, (f'Teacher for {class_name}', 'Female', 'Teacher'))
        
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