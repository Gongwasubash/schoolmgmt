from django.core.management.base import BaseCommand
from schoolmgmt.models import Teacher, Subject

class Command(BaseCommand):
    help = 'Update teachers to cover all subjects in the school'

    def handle(self, *args, **options):
        # Get all unique subjects
        all_subjects = Subject.objects.values_list('name', flat=True).distinct()
        
        # Define comprehensive subject mapping for teachers
        teacher_subject_mapping = {
            'Ram Bahadur Shrestha': 'Administration, Management, Leadership',
            'Sita Devi Poudel': 'English, Literature, Communication Skills',
            'Hari Prasad Sharma': 'Mathematics, Statistics, Optional Mathematics',
            'Kamala Kumari Thapa': 'Nepali, Social Studies, History',
            'Bishnu Kumar Gurung': 'Physics, Chemistry, Science',
            'Mohan Bahadur Rai': 'Biology, Environmental Science, Health Education',
            'Krishna Prasad Oli': 'Chemistry, Mathematics, Science',
            'Narayan Prasad Bhattarai': 'Computer Science, ICT, Computer',
            'Rajesh Kumar Limbu': 'Economics, Business Studies, Account',
            'Gita Rani Adhikari': 'History, Geography, Social Studies',
            'Gopal Prasad Regmi': 'Political Science, Current Affairs, Moral Education',
            'Laxmi Devi Pandey': 'Sanskrit, Nepali, Literature',
            'Durga Devi Khadka': 'Health & Physical Education, First Aid, Sports',
            'Tek Bahadur Thakuri': 'Physical Education, Sports, Health & Physical Education',
            'Parvati Kumari Chaudhary': 'Agriculture, Environmental Science, Science',
            'Deepak Bahadur Magar': 'Social Studies, Civics, Geography',
            'Sunita Devi Karki': 'English, Computer, Communication',
            'Saraswati Devi Joshi': 'Art & Craft, Music, Drawing',
            'Mina Kumari Sherpa': 'Music, Dance, Cultural Studies, Rhymes',
            'Radha Kumari Tamang': 'Math, Mathematics, Primary Education'
        }
        
        # Update teachers with their subjects
        updated_count = 0
        for teacher_name, subjects in teacher_subject_mapping.items():
            try:
                teacher = Teacher.objects.get(name=teacher_name)
                teacher.subjects = subjects
                teacher.save()
                updated_count += 1
                self.stdout.write(f"Updated {teacher_name}: {subjects}")
            except Teacher.DoesNotExist:
                self.stdout.write(f"Teacher {teacher_name} not found")
        
        # Check coverage
        self.stdout.write(f"\n=== SUBJECT COVERAGE ANALYSIS ===")
        covered_subjects = set()
        for subjects_str in teacher_subject_mapping.values():
            for subject in subjects_str.split(', '):
                covered_subjects.add(subject.strip())
        
        # Find uncovered subjects
        uncovered = []
        for subject in all_subjects:
            found = False
            for covered in covered_subjects:
                if subject.lower() in covered.lower() or covered.lower() in subject.lower():
                    found = True
                    break
            if not found:
                uncovered.append(subject)
        
        if uncovered:
            self.stdout.write(f"\nUncovered subjects: {uncovered}")
        else:
            self.stdout.write(f"\nAll subjects are covered by teachers!")
        
        self.stdout.write(f"\nSuccessfully updated {updated_count} teachers with subject assignments")