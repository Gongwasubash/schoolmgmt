from django.core.management.base import BaseCommand
from schoolmgmt.models import Teacher

class Command(BaseCommand):
    help = 'Update teachers with class and subject assignments'

    def handle(self, *args, **options):
        teacher_assignments = {
            'Ram Bahadur Shrestha': {
                'assigned_class': 'All Classes',
                'subject_specialization': 'Administration',
                'subjects': 'Administration, Management, Leadership'
            },
            'Sita Devi Poudel': {
                'assigned_class': 'Eleven',
                'subject_specialization': 'English',
                'subjects': 'English, Literature, Communication Skills'
            },
            'Hari Prasad Sharma': {
                'assigned_class': 'Ten',
                'subject_specialization': 'Mathematics',
                'subjects': 'Mathematics, Statistics, Optional Mathematics'
            },
            'Kamala Kumari Thapa': {
                'assigned_class': 'Nine',
                'subject_specialization': 'Nepali',
                'subjects': 'Nepali, Social Studies, History'
            },
            'Bishnu Kumar Gurung': {
                'assigned_class': 'Twelve',
                'subject_specialization': 'Physics',
                'subjects': 'Physics, Chemistry, Science'
            },
            'Mohan Bahadur Rai': {
                'assigned_class': 'Eleven',
                'subject_specialization': 'Biology',
                'subjects': 'Biology, Environmental Science, Health Education'
            },
            'Krishna Prasad Oli': {
                'assigned_class': 'Ten',
                'subject_specialization': 'Chemistry',
                'subjects': 'Chemistry, Mathematics, Science'
            },
            'Narayan Prasad Bhattarai': {
                'assigned_class': 'Eight',
                'subject_specialization': 'Computer Science',
                'subjects': 'Computer Science, ICT, Computer'
            },
            'Rajesh Kumar Limbu': {
                'assigned_class': 'Twelve',
                'subject_specialization': 'Economics',
                'subjects': 'Economics, Business Studies, Account'
            },
            'Gita Rani Adhikari': {
                'assigned_class': 'Seven',
                'subject_specialization': 'History',
                'subjects': 'History, Geography, Social Studies'
            },
            'Gopal Prasad Regmi': {
                'assigned_class': 'Six',
                'subject_specialization': 'Moral Education',
                'subjects': 'Political Science, Current Affairs, Moral Education'
            },
            'Laxmi Devi Pandey': {
                'assigned_class': 'Five',
                'subject_specialization': 'Nepali',
                'subjects': 'Sanskrit, Nepali, Literature'
            },
            'Durga Devi Khadka': {
                'assigned_class': 'All Classes',
                'subject_specialization': 'Physical Education',
                'subjects': 'Health & Physical Education, First Aid, Sports'
            },
            'Tek Bahadur Thakuri': {
                'assigned_class': 'All Classes',
                'subject_specialization': 'Sports',
                'subjects': 'Physical Education, Sports, Health & Physical Education'
            },
            'Parvati Kumari Chaudhary': {
                'assigned_class': 'Four',
                'subject_specialization': 'Science',
                'subjects': 'Agriculture, Environmental Science, Science'
            },
            'Deepak Bahadur Magar': {
                'assigned_class': 'Three',
                'subject_specialization': 'Social Studies',
                'subjects': 'Social Studies, Civics, Geography'
            },
            'Sunita Devi Karki': {
                'assigned_class': 'Two',
                'subject_specialization': 'English',
                'subjects': 'English, Computer, Communication'
            },
            'Saraswati Devi Joshi': {
                'assigned_class': 'One',
                'subject_specialization': 'Art & Craft',
                'subjects': 'Art & Craft, Music, Drawing'
            },
            'Mina Kumari Sherpa': {
                'assigned_class': 'UKG',
                'subject_specialization': 'Music',
                'subjects': 'Music, Dance, Cultural Studies, Rhymes'
            },
            'Radha Kumari Tamang': {
                'assigned_class': 'LKG',
                'subject_specialization': 'Mathematics',
                'subjects': 'Math, Mathematics, Primary Education'
            },
            'Binod Kumar Acharya': {
                'assigned_class': 'Eleven',
                'subject_specialization': 'Marketing',
                'subjects': 'Marketing, Business Studies, Economics'
            },
            'Anita Kumari Maharjan': {
                'assigned_class': 'Twelve',
                'subject_specialization': 'Hotel Management',
                'subjects': 'Hotel Management, Tourism, Business Studies'
            },
            'Prakash Bahadur Karki': {
                'assigned_class': 'Nursery',
                'subject_specialization': 'Primary Education',
                'subjects': 'Primary Education, Math, English, Nepali'
            }
        }
        
        updated_count = 0
        for teacher_name, assignments in teacher_assignments.items():
            try:
                teacher = Teacher.objects.get(name=teacher_name)
                teacher.assigned_class = assignments['assigned_class']
                teacher.subject_specialization = assignments['subject_specialization']
                teacher.subjects = assignments['subjects']
                teacher.save()
                updated_count += 1
                self.stdout.write(f"Updated {teacher_name}: Class {assignments['assigned_class']}, Subject: {assignments['subject_specialization']}")
            except Teacher.DoesNotExist:
                self.stdout.write(f"Teacher {teacher_name} not found")
        
        self.stdout.write(f"\nSuccessfully updated {updated_count} teachers with class and subject assignments")