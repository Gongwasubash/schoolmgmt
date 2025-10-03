from django.core.management.base import BaseCommand
from schoolmgmt.models import Teacher, Subject
from datetime import date

class Command(BaseCommand):
    help = 'Populate teachers to cover all subjects for each class'

    def handle(self, *args, **options):
        Teacher.objects.all().delete()
        
        # Get subjects by class
        subjects_by_class = {}
        for subject in Subject.objects.all():
            if subject.class_name not in subjects_by_class:
                subjects_by_class[subject.class_name] = []
            subjects_by_class[subject.class_name].append(subject.name)
        
        teachers_data = [
            # Nursery Teachers
            {'name': 'Nirmala Devi Shakya', 'class': 'Nursery', 'subjects': ['Drawing', 'English', 'Math', 'Nepali', 'Rhymes'], 'designation': 'Assistant Teacher', 'specialization': 'Early Childhood Education'},
            
            # LKG Teachers  
            {'name': 'Ravi Kumar Maharjan', 'class': 'LKG', 'subjects': ['Drawing', 'English', 'Math', 'Nepali', 'Rhymes'], 'designation': 'Assistant Teacher', 'specialization': 'Early Childhood Education'},
            
            # UKG Teachers
            {'name': 'Mina Kumari Sherpa', 'class': 'UKG', 'subjects': ['Drawing', 'English', 'Math', 'Nepali', 'Rhymes'], 'designation': 'Assistant Teacher', 'specialization': 'Early Childhood Education'},
            
            # One Teachers
            {'name': 'Sushila Kumari Rai', 'class': 'One', 'subjects': ['Art & Craft', 'Computer', 'English', 'Health & Physical Education', 'Mathematics', 'Nepali', 'Science', 'Social Studies'], 'designation': 'Assistant Teacher', 'specialization': 'Primary Education'},
            
            # Two Teachers
            {'name': 'Kiran Bahadur Thapa', 'class': 'Two', 'subjects': ['Art & Craft', 'Computer', 'English', 'Health & Physical Education', 'Mathematics', 'Nepali', 'Science', 'Social Studies'], 'designation': 'Assistant Teacher', 'specialization': 'Primary Education'},
            
            # Three Teachers
            {'name': 'Shanti Devi Tamang', 'class': 'Three', 'subjects': ['Art & Craft', 'Computer', 'English', 'Health & Physical Education', 'Mathematics', 'Nepali', 'Science', 'Social Studies'], 'designation': 'Assistant Teacher', 'specialization': 'Primary Education'},
            
            # Four Teachers
            {'name': 'Durga Devi Khadka', 'class': 'Four', 'subjects': ['Art & Craft', 'Computer', 'English', 'Health & Physical Education', 'Mathematics', 'Nepali', 'Science', 'Social Studies'], 'designation': 'Teacher', 'specialization': 'Primary Education'},
            
            # Five Teachers
            {'name': 'Saraswati Devi Joshi', 'class': 'Five', 'subjects': ['Art & Craft', 'Computer', 'English', 'Health & Physical Education', 'Mathematics', 'Nepali', 'Science', 'Social Studies'], 'designation': 'Teacher', 'specialization': 'Primary Education'},
            {'name': 'Prakash Bahadur Karki', 'class': 'Five', 'subjects': ['Mathematics', 'Science'], 'designation': 'Assistant Teacher', 'specialization': 'Mathematics'},
            
            # Six Teachers
            {'name': 'Deepak Bahadur Magar', 'class': 'Six', 'subjects': ['Computer Science', 'English', 'Health & Physical Education', 'Mathematics', 'Moral Education', 'Nepali', 'Optional Mathematics', 'Science', 'Social Studies'], 'designation': 'Teacher', 'specialization': 'Social Studies'},
            {'name': 'Gopal Prasad Regmi', 'class': 'Six', 'subjects': ['Moral Education', 'Social Studies'], 'designation': 'Teacher', 'specialization': 'Moral Education'},
            
            # Seven Teachers
            {'name': 'Laxmi Devi Pandey', 'class': 'Seven', 'subjects': ['Computer Science', 'English', 'Health & Physical Education', 'Mathematics', 'Moral Education', 'Nepali', 'Optional Mathematics', 'Science', 'Social Studies'], 'designation': 'Teacher', 'specialization': 'Nepali'},
            {'name': 'Gita Rani Adhikari', 'class': 'Seven', 'subjects': ['Social Studies', 'History'], 'designation': 'Teacher', 'specialization': 'History'},
            
            # Eight Teachers
            {'name': 'Radha Kumari Tamang', 'class': 'Eight', 'subjects': ['Computer Science', 'English', 'Health & Physical Education', 'Mathematics', 'Moral Education', 'Nepali', 'Optional Mathematics', 'Science', 'Social Studies'], 'designation': 'Teacher', 'specialization': 'Mathematics'},
            {'name': 'Maya Kumari Shrestha', 'class': 'Eight', 'subjects': ['English', 'Computer Science'], 'designation': 'Teacher', 'specialization': 'English'},
            {'name': 'Narayan Prasad Bhattarai', 'class': 'Eight', 'subjects': ['Computer Science', 'Science'], 'designation': 'Subject Teacher', 'specialization': 'Computer Science'},
            
            # Nine Teachers
            {'name': 'Kamala Kumari Thapa', 'class': 'Nine', 'subjects': ['Account', 'Computer Science', 'Economics', 'English', 'Health & Physical Education', 'Mathematics', 'Nepali', 'Optional Mathematics', 'Science', 'Social Studies'], 'designation': 'Senior Teacher', 'specialization': 'Nepali'},
            {'name': 'Parvati Kumari Chaudhary', 'class': 'Nine', 'subjects': ['Science', 'Health & Physical Education'], 'designation': 'Teacher', 'specialization': 'Science'},
            
            # Ten Teachers
            {'name': 'Hari Prasad Sharma', 'class': 'Ten', 'subjects': ['Account', 'Computer Science', 'Economics', 'English', 'Health & Physical Education', 'Mathematics', 'Nepali', 'Optional Mathematics', 'Science', 'Social Studies'], 'designation': 'Head Teacher', 'specialization': 'Mathematics'},
            {'name': 'Sunita Devi Karki', 'class': 'Ten', 'subjects': ['English', 'Computer Science'], 'designation': 'Teacher', 'specialization': 'English'},
            
            # Eleven Teachers
            {'name': 'Sita Devi Poudel', 'class': 'Eleven', 'subjects': ['Account', 'Biology', 'Business Studies', 'Chemistry', 'Computer Science', 'Economics', 'English', 'Hotel Management', 'Marketing', 'Mathematics', 'Nepali', 'Physics'], 'designation': 'Vice Principal', 'specialization': 'English'},
            {'name': 'Mohan Bahadur Rai', 'class': 'Eleven', 'subjects': ['Biology', 'Chemistry'], 'designation': 'Teacher', 'specialization': 'Biology'},
            {'name': 'Rajesh Kumar Limbu', 'class': 'Eleven', 'subjects': ['Economics', 'Business Studies', 'Account'], 'designation': 'Teacher', 'specialization': 'Economics'},
            {'name': 'Anita Kumari Maharjan', 'class': 'Eleven', 'subjects': ['Hotel Management', 'Marketing'], 'designation': 'Subject Teacher', 'specialization': 'Hotel Management'},
            
            # Twelve Teachers
            {'name': 'Bishnu Kumar Gurung', 'class': 'Twelve', 'subjects': ['Account', 'Biology', 'Business Studies', 'Chemistry', 'Computer Science', 'Economics', 'English', 'Hotel Management', 'Marketing', 'Mathematics', 'Nepali', 'Physics'], 'designation': 'Senior Teacher', 'specialization': 'Physics'},
            {'name': 'Krishna Prasad Oli', 'class': 'Twelve', 'subjects': ['Chemistry', 'Physics'], 'designation': 'Teacher', 'specialization': 'Chemistry'},
            {'name': 'Binod Kumar Acharya', 'class': 'Twelve', 'subjects': ['Marketing', 'Business Studies'], 'designation': 'Subject Teacher', 'specialization': 'Marketing'},
            
            # All Classes Teachers
            {'name': 'Ram Bahadur Shrestha', 'class': 'All Classes', 'subjects': ['Administration', 'Management'], 'designation': 'Principal', 'specialization': 'Administration'},
            {'name': 'Tek Bahadur Thakuri', 'class': 'All Classes', 'subjects': ['Health & Physical Education', 'Sports'], 'designation': 'Subject Teacher', 'specialization': 'Physical Education'},
        ]
        
        created_count = 0
        for teacher_data in teachers_data:
            teacher = Teacher.objects.create(
                name=teacher_data['name'],
                address=f"Kathmandu-{created_count+1}, Nepal",
                designation=teacher_data['designation'],
                phone_number=f"+977-98{10000000 + created_count:08d}",
                email=f"{teacher_data['name'].lower().replace(' ', '.')}@everestacademy.edu.np",
                gender='Male' if 'Bahadur' in teacher_data['name'] or teacher_data['name'].split()[0] in ['Ram', 'Hari', 'Gopal', 'Krishna', 'Mohan', 'Narayan', 'Rajesh', 'Bishnu', 'Deepak', 'Prakash', 'Kiran', 'Ravi', 'Binod', 'Tek'] else 'Female',
                date_of_birth=date(1980 + (created_count % 15), 1 + (created_count % 12), 1 + (created_count % 28)),
                joining_date=date(2015 + (created_count % 8), 1 + (created_count % 12), 1 + (created_count % 28)),
                qualification=f"M.Ed in {teacher_data['specialization']}, B.Ed",
                assigned_class=teacher_data['class'],
                subject_specialization=teacher_data['specialization'],
                subjects=', '.join(teacher_data['subjects']),
                salary=35000 + (created_count * 2000),
                is_active=True
            )
            created_count += 1
            self.stdout.write(f"Created: {teacher.name} - {teacher.assigned_class} - {teacher.subject_specialization}")
        
        # Verify coverage
        self.stdout.write("\n=== COVERAGE VERIFICATION ===")
        for class_name, subjects in subjects_by_class.items():
            teachers_for_class = Teacher.objects.filter(assigned_class=class_name)
            covered_subjects = set()
            for teacher in teachers_for_class:
                if teacher.subjects:
                    covered_subjects.update([s.strip() for s in teacher.subjects.split(',')])
            
            missing = set(subjects) - covered_subjects
            if missing:
                self.stdout.write(f"{class_name}: Missing {missing}")
            else:
                self.stdout.write(f"{class_name}: All {len(subjects)} subjects covered")
        
        self.stdout.write(f"\nCreated {created_count} teachers covering all classes and subjects")