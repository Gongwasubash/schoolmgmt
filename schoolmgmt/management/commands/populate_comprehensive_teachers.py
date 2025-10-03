from django.core.management.base import BaseCommand
from schoolmgmt.models import Teacher, Subject
from datetime import date
import random

class Command(BaseCommand):
    help = 'Populate teachers to cover all subjects comprehensively'

    def handle(self, *args, **options):
        # Clear existing teachers
        Teacher.objects.all().delete()
        
        # Comprehensive teacher data covering all subjects
        teachers_data = [
            # Administration
            {
                'name': 'Ram Bahadur Shrestha',
                'address': 'Kathmandu-10, Baneshwor',
                'designation': 'Principal',
                'phone_number': '+977-9841234567',
                'email': 'principal@everestacademy.edu.np',
                'gender': 'Male',
                'date_of_birth': date(1975, 5, 15),
                'joining_date': date(2015, 4, 1),
                'qualification': 'M.Ed in Educational Administration, B.Ed',
                'assigned_class': 'All Classes',
                'subject_specialization': 'Administration',
                'subjects': 'Administration, Management, Leadership',
                'salary': 85000.00
            },
            {
                'name': 'Sita Devi Poudel',
                'address': 'Lalitpur-5, Jawalakhel',
                'designation': 'Vice Principal',
                'phone_number': '+977-9851234568',
                'email': 'vp@everestacademy.edu.np',
                'gender': 'Female',
                'date_of_birth': date(1978, 8, 22),
                'joining_date': date(2016, 7, 15),
                'qualification': 'M.A in English Literature, B.Ed',
                'assigned_class': 'Eleven',
                'subject_specialization': 'English',
                'subjects': 'English, Literature',
                'salary': 75000.00
            },
            
            # Mathematics Teachers
            {
                'name': 'Hari Prasad Sharma',
                'address': 'Bhaktapur-12, Thimi',
                'designation': 'Head Teacher',
                'phone_number': '+977-9861234569',
                'email': 'hari.sharma@everestacademy.edu.np',
                'gender': 'Male',
                'date_of_birth': date(1980, 3, 10),
                'joining_date': date(2018, 1, 10),
                'qualification': 'M.Sc Mathematics, B.Ed',
                'assigned_class': 'Ten',
                'subject_specialization': 'Mathematics',
                'subjects': 'Mathematics, Optional Mathematics',
                'salary': 65000.00
            },
            {
                'name': 'Radha Kumari Tamang',
                'address': 'Kathmandu-32, Gokarneshwor',
                'designation': 'Teacher',
                'phone_number': '+977-9871234570',
                'email': 'radha.tamang@everestacademy.edu.np',
                'gender': 'Female',
                'date_of_birth': date(1985, 11, 5),
                'joining_date': date(2019, 3, 15),
                'qualification': 'B.Sc Mathematics, B.Ed',
                'assigned_class': 'Eight',
                'subject_specialization': 'Mathematics',
                'subjects': 'Mathematics, Optional Mathematics',
                'salary': 50000.00
            },
            {
                'name': 'Prakash Bahadur Karki',
                'address': 'Kathmandu-16, Balkhu',
                'designation': 'Assistant Teacher',
                'phone_number': '+977-9881234571',
                'email': 'prakash.karki@everestacademy.edu.np',
                'gender': 'Male',
                'date_of_birth': date(1990, 7, 18),
                'joining_date': date(2020, 8, 1),
                'qualification': 'B.Ed in Primary Education',
                'assigned_class': 'Five',
                'subject_specialization': 'Math',
                'subjects': 'Math, Mathematics',
                'salary': 35000.00
            },
            
            # Science Teachers
            {
                'name': 'Bishnu Kumar Gurung',
                'address': 'Kathmandu-25, Tokha',
                'designation': 'Senior Teacher',
                'phone_number': '+977-9891234572',
                'email': 'bishnu.gurung@everestacademy.edu.np',
                'gender': 'Male',
                'date_of_birth': date(1982, 12, 8),
                'joining_date': date(2017, 6, 20),
                'qualification': 'M.Sc Physics, B.Ed',
                'assigned_class': 'Twelve',
                'subject_specialization': 'Physics',
                'subjects': 'Physics, Science',
                'salary': 60000.00
            },
            {
                'name': 'Mohan Bahadur Rai',
                'address': 'Lalitpur-8, Imadol',
                'designation': 'Teacher',
                'phone_number': '+977-9801234573',
                'email': 'mohan.rai@everestacademy.edu.np',
                'gender': 'Male',
                'date_of_birth': date(1983, 9, 25),
                'joining_date': date(2018, 4, 10),
                'qualification': 'M.Sc Biology, B.Ed',
                'assigned_class': 'Eleven',
                'subject_specialization': 'Biology',
                'subjects': 'Biology, Science',
                'salary': 55000.00
            },
            {
                'name': 'Krishna Prasad Oli',
                'address': 'Kathmandu-6, Nagarjun',
                'designation': 'Teacher',
                'phone_number': '+977-9811234574',
                'email': 'krishna.oli@everestacademy.edu.np',
                'gender': 'Male',
                'date_of_birth': date(1984, 6, 12),
                'joining_date': date(2019, 1, 5),
                'qualification': 'M.Sc Chemistry, B.Ed',
                'assigned_class': 'Twelve',
                'subject_specialization': 'Chemistry',
                'subjects': 'Chemistry, Science',
                'salary': 55000.00
            },
            {
                'name': 'Parvati Kumari Chaudhary',
                'address': 'Bhaktapur-4, Suryabinayak',
                'designation': 'Teacher',
                'phone_number': '+977-9821234575',
                'email': 'parvati.chaudhary@everestacademy.edu.np',
                'gender': 'Female',
                'date_of_birth': date(1987, 4, 30),
                'joining_date': date(2020, 2, 12),
                'qualification': 'B.Sc Environmental Science, B.Ed',
                'assigned_class': 'Nine',
                'subject_specialization': 'Science',
                'subjects': 'Science, Environmental Science',
                'salary': 48000.00
            },
            
            # English Teachers
            {
                'name': 'Sunita Devi Karki',
                'address': 'Kathmandu-44, Chandragiri',
                'designation': 'Teacher',
                'phone_number': '+977-9831234576',
                'email': 'sunita.karki@everestacademy.edu.np',
                'gender': 'Female',
                'date_of_birth': date(1986, 1, 14),
                'joining_date': date(2019, 7, 8),
                'qualification': 'M.A English, B.Ed',
                'assigned_class': 'Ten',
                'subject_specialization': 'English',
                'subjects': 'English, Literature',
                'salary': 52000.00
            },
            {
                'name': 'Maya Kumari Shrestha',
                'address': 'Lalitpur-15, Godawari',
                'designation': 'Teacher',
                'phone_number': '+977-9841234577',
                'email': 'maya.shrestha@everestacademy.edu.np',
                'gender': 'Female',
                'date_of_birth': date(1988, 10, 3),
                'joining_date': date(2020, 5, 18),
                'qualification': 'B.A English, B.Ed',
                'assigned_class': 'Eight',
                'subject_specialization': 'English',
                'subjects': 'English',
                'salary': 45000.00
            },
            
            # Nepali Teachers
            {
                'name': 'Kamala Kumari Thapa',
                'address': 'Kathmandu-35, Budhanilkantha',
                'designation': 'Senior Teacher',
                'phone_number': '+977-9851234578',
                'email': 'kamala.thapa@everestacademy.edu.np',
                'gender': 'Female',
                'date_of_birth': date(1981, 7, 20),
                'joining_date': date(2017, 3, 25),
                'qualification': 'M.A Nepali Literature, B.Ed',
                'assigned_class': 'Nine',
                'subject_specialization': 'Nepali',
                'subjects': 'Nepali, Literature',
                'salary': 58000.00
            },
            {
                'name': 'Laxmi Devi Pandey',
                'address': 'Bhaktapur-9, Changunarayan',
                'designation': 'Teacher',
                'phone_number': '+977-9861234579',
                'email': 'laxmi.pandey@everestacademy.edu.np',
                'gender': 'Female',
                'date_of_birth': date(1985, 2, 28),
                'joining_date': date(2018, 9, 12),
                'qualification': 'M.A Sanskrit, B.Ed',
                'assigned_class': 'Seven',
                'subject_specialization': 'Nepali',
                'subjects': 'Nepali, Sanskrit',
                'salary': 50000.00
            },
            
            # Social Studies & History Teachers
            {
                'name': 'Gita Rani Adhikari',
                'address': 'Lalitpur-20, Mahalaxmi',
                'designation': 'Teacher',
                'phone_number': '+977-9871234580',
                'email': 'gita.adhikari@everestacademy.edu.np',
                'gender': 'Female',
                'date_of_birth': date(1983, 5, 16),
                'joining_date': date(2018, 6, 30),
                'qualification': 'M.A History, B.Ed',
                'assigned_class': 'Eight',
                'subject_specialization': 'Social Studies',
                'subjects': 'Social Studies, History, Geography',
                'salary': 50000.00
            },
            {
                'name': 'Deepak Bahadur Magar',
                'address': 'Kathmandu-11, Kirtipur',
                'designation': 'Teacher',
                'phone_number': '+977-9881234581',
                'email': 'deepak.magar@everestacademy.edu.np',
                'gender': 'Male',
                'date_of_birth': date(1986, 8, 7),
                'joining_date': date(2019, 11, 20),
                'qualification': 'M.A Geography, B.Ed',
                'assigned_class': 'Six',
                'subject_specialization': 'Social Studies',
                'subjects': 'Social Studies, Geography, Civics',
                'salary': 48000.00
            },
            
            # Computer Science Teachers
            {
                'name': 'Narayan Prasad Bhattarai',
                'address': 'Kathmandu-4, Kageshwori Manohara',
                'designation': 'Subject Teacher',
                'phone_number': '+977-9891234582',
                'email': 'narayan.bhattarai@everestacademy.edu.np',
                'gender': 'Male',
                'date_of_birth': date(1985, 11, 11),
                'joining_date': date(2019, 2, 14),
                'qualification': 'B.Sc Computer Science, Diploma in IT',
                'assigned_class': 'Ten',
                'subject_specialization': 'Computer Science',
                'subjects': 'Computer Science, Computer, ICT',
                'salary': 52000.00
            },
            
            # Business & Economics Teachers
            {
                'name': 'Rajesh Kumar Limbu',
                'address': 'Lalitpur-25, Lubhu',
                'designation': 'Teacher',
                'phone_number': '+977-9801234583',
                'email': 'rajesh.limbu@everestacademy.edu.np',
                'gender': 'Male',
                'date_of_birth': date(1984, 3, 19),
                'joining_date': date(2018, 8, 5),
                'qualification': 'MBA, BBS',
                'assigned_class': 'Eleven',
                'subject_specialization': 'Economics',
                'subjects': 'Economics, Business Studies, Account',
                'salary': 55000.00
            },
            {
                'name': 'Binod Kumar Acharya',
                'address': 'Bhaktapur-8, Madhyapur Thimi',
                'designation': 'Subject Teacher',
                'phone_number': '+977-9811234584',
                'email': 'binod.acharya@everestacademy.edu.np',
                'gender': 'Male',
                'date_of_birth': date(1987, 12, 25),
                'joining_date': date(2020, 1, 8),
                'qualification': 'MBA Marketing, BBS',
                'assigned_class': 'Twelve',
                'subject_specialization': 'Marketing',
                'subjects': 'Marketing, Business Studies',
                'salary': 50000.00
            },
            {
                'name': 'Anita Kumari Maharjan',
                'address': 'Lalitpur-12, Pulchowk',
                'designation': 'Subject Teacher',
                'phone_number': '+977-9821234585',
                'email': 'anita.maharjan@everestacademy.edu.np',
                'gender': 'Female',
                'date_of_birth': date(1989, 4, 8),
                'joining_date': date(2021, 3, 22),
                'qualification': 'Bachelor in Hotel Management',
                'assigned_class': 'Eleven',
                'subject_specialization': 'Hotel Management',
                'subjects': 'Hotel Management, Tourism',
                'salary': 48000.00
            },
            
            # Physical Education & Sports
            {
                'name': 'Tek Bahadur Thakuri',
                'address': 'Kathmandu-29, Tarakeshwor',
                'designation': 'Subject Teacher',
                'phone_number': '+977-9831234586',
                'email': 'tek.thakuri@everestacademy.edu.np',
                'gender': 'Male',
                'date_of_birth': date(1982, 6, 30),
                'joining_date': date(2017, 5, 10),
                'qualification': 'B.P.Ed, Diploma in Sports',
                'assigned_class': 'All Classes',
                'subject_specialization': 'Health & Physical Education',
                'subjects': 'Health & Physical Education, Sports',
                'salary': 45000.00
            },
            
            # Moral Education
            {
                'name': 'Gopal Prasad Regmi',
                'address': 'Bhaktapur-6, Bhaktapur Municipality',
                'designation': 'Teacher',
                'phone_number': '+977-9841234587',
                'email': 'gopal.regmi@everestacademy.edu.np',
                'gender': 'Male',
                'date_of_birth': date(1980, 9, 14),
                'joining_date': date(2016, 12, 1),
                'qualification': 'M.A Political Science, B.Ed',
                'assigned_class': 'Seven',
                'subject_specialization': 'Moral Education',
                'subjects': 'Moral Education, Political Science',
                'salary': 48000.00
            },
            
            # Art & Craft Teachers
            {
                'name': 'Saraswati Devi Joshi',
                'address': 'Kathmandu-17, Dakshinkali',
                'designation': 'Assistant Teacher',
                'phone_number': '+977-9851234588',
                'email': 'saraswati.joshi@everestacademy.edu.np',
                'gender': 'Female',
                'date_of_birth': date(1988, 1, 22),
                'joining_date': date(2019, 4, 15),
                'qualification': 'Bachelor in Fine Arts, Diploma in Art Education',
                'assigned_class': 'Five',
                'subject_specialization': 'Art & Craft',
                'subjects': 'Art & Craft, Drawing',
                'salary': 40000.00
            },
            
            # Music & Cultural Studies
            {
                'name': 'Mina Kumari Sherpa',
                'address': 'Lalitpur-19, Mahalaxmi',
                'designation': 'Assistant Teacher',
                'phone_number': '+977-9861234589',
                'email': 'mina.sherpa@everestacademy.edu.np',
                'gender': 'Female',
                'date_of_birth': date(1990, 3, 5),
                'joining_date': date(2020, 6, 8),
                'qualification': 'Bachelor in Music, Diploma in Cultural Studies',
                'assigned_class': 'UKG',
                'subject_specialization': 'Music',
                'subjects': 'Music, Dance, Rhymes',
                'salary': 38000.00
            },
            
            # Primary Education Teachers
            {
                'name': 'Durga Devi Khadka',
                'address': 'Kathmandu-14, Shankharapur',
                'designation': 'Assistant Teacher',
                'phone_number': '+977-9871234590',
                'email': 'durga.khadka@everestacademy.edu.np',
                'gender': 'Female',
                'date_of_birth': date(1987, 7, 12),
                'joining_date': date(2019, 8, 20),
                'qualification': 'B.Ed Primary Education',
                'assigned_class': 'Four',
                'subject_specialization': 'Primary Education',
                'subjects': 'English, Math, Nepali, Science',
                'salary': 42000.00
            },
            {
                'name': 'Shanti Devi Tamang',
                'address': 'Bhaktapur-11, Suryabinayak',
                'designation': 'Assistant Teacher',
                'phone_number': '+977-9881234591',
                'email': 'shanti.tamang@everestacademy.edu.np',
                'gender': 'Female',
                'date_of_birth': date(1989, 12, 18),
                'joining_date': date(2020, 9, 10),
                'qualification': 'B.Ed Primary Education',
                'assigned_class': 'Three',
                'subject_specialization': 'Primary Education',
                'subjects': 'English, Math, Nepali, Science',
                'salary': 40000.00
            },
            {
                'name': 'Kiran Bahadur Thapa',
                'address': 'Kathmandu-31, Dakshinkali',
                'designation': 'Assistant Teacher',
                'phone_number': '+977-9891234592',
                'email': 'kiran.thapa@everestacademy.edu.np',
                'gender': 'Male',
                'date_of_birth': date(1991, 5, 8),
                'joining_date': date(2021, 1, 15),
                'qualification': 'B.Ed Primary Education',
                'assigned_class': 'Two',
                'subject_specialization': 'Primary Education',
                'subjects': 'English, Math, Nepali, Science',
                'salary': 38000.00
            },
            {
                'name': 'Sushila Kumari Rai',
                'address': 'Lalitpur-22, Godawari',
                'designation': 'Assistant Teacher',
                'phone_number': '+977-9801234593',
                'email': 'sushila.rai@everestacademy.edu.np',
                'gender': 'Female',
                'date_of_birth': date(1992, 8, 15),
                'joining_date': date(2021, 4, 5),
                'qualification': 'B.Ed Primary Education',
                'assigned_class': 'One',
                'subject_specialization': 'Primary Education',
                'subjects': 'English, Math, Nepali, Science',
                'salary': 36000.00
            },
            {
                'name': 'Ravi Kumar Maharjan',
                'address': 'Lalitpur-3, Patan',
                'designation': 'Assistant Teacher',
                'phone_number': '+977-9811234594',
                'email': 'ravi.maharjan@everestacademy.edu.np',
                'gender': 'Male',
                'date_of_birth': date(1993, 2, 20),
                'joining_date': date(2021, 7, 12),
                'qualification': 'B.Ed Early Childhood Education',
                'assigned_class': 'LKG',
                'subject_specialization': 'Early Childhood Education',
                'subjects': 'English, Math, Nepali, Drawing, Rhymes',
                'salary': 35000.00
            },
            {
                'name': 'Nirmala Devi Shakya',
                'address': 'Bhaktapur-2, Bhaktapur Municipality',
                'designation': 'Assistant Teacher',
                'phone_number': '+977-9821234595',
                'email': 'nirmala.shakya@everestacademy.edu.np',
                'gender': 'Female',
                'date_of_birth': date(1994, 11, 10),
                'joining_date': date(2021, 9, 8),
                'qualification': 'B.Ed Early Childhood Education',
                'assigned_class': 'Nursery',
                'subject_specialization': 'Early Childhood Education',
                'subjects': 'English, Math, Nepali, Drawing, Rhymes',
                'salary': 34000.00
            }
        ]
        
        created_count = 0
        for teacher_data in teachers_data:
            teacher = Teacher.objects.create(**teacher_data)
            created_count += 1
            self.stdout.write(f"Created: {teacher.name} - {teacher.assigned_class} - {teacher.subject_specialization}")
        
        self.stdout.write(f"\nSuccessfully created {created_count} teachers")
        
        # Verify subject coverage
        self.stdout.write("\n=== SUBJECT COVERAGE VERIFICATION ===")
        all_subjects = set(Subject.objects.values_list('name', flat=True).distinct())
        covered_subjects = set()
        
        for teacher in Teacher.objects.all():
            if teacher.subjects:
                for subject in teacher.subjects.split(', '):
                    covered_subjects.add(subject.strip())
        
        uncovered = all_subjects - covered_subjects
        if uncovered:
            self.stdout.write(f"Uncovered subjects: {list(uncovered)}")
        else:
            self.stdout.write("All subjects are covered!")
        
        self.stdout.write(f"Total subjects in system: {len(all_subjects)}")
        self.stdout.write(f"Subjects covered by teachers: {len(covered_subjects)}")