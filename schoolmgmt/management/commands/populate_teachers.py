from django.core.management.base import BaseCommand
from schoolmgmt.models import Teacher
from datetime import date, timedelta
import random
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate 20 teachers with Nepali context data'

    def handle(self, *args, **options):
        # Clear existing teachers
        Teacher.objects.all().delete()
        
        # Nepali teacher names and data
        teachers_data = [
            {
                'name': 'Ram Bahadur Shrestha',
                'gender': 'Male',
                'designation': 'Principal',
                'address': 'Kathmandu-15, Thamel',
                'phone_number': '9841234567',
                'email': 'ram.shrestha@everestacademy.edu.np',
                'qualification': 'M.Ed in Educational Leadership',
                'subjects': 'Administration, Management',
                'salary': 85000.00
            },
            {
                'name': 'Sita Devi Poudel',
                'gender': 'Female',
                'designation': 'Vice Principal',
                'address': 'Lalitpur-8, Patan Dhoka',
                'phone_number': '9851234568',
                'email': 'sita.poudel@everestacademy.edu.np',
                'qualification': 'M.A in English Literature',
                'subjects': 'English, Literature',
                'salary': 75000.00
            },
            {
                'name': 'Hari Prasad Sharma',
                'gender': 'Male',
                'designation': 'Head Teacher',
                'address': 'Bhaktapur-12, Durbar Square',
                'phone_number': '9861234569',
                'email': 'hari.sharma@everestacademy.edu.np',
                'qualification': 'M.Sc in Mathematics',
                'subjects': 'Mathematics, Statistics',
                'salary': 65000.00
            },
            {
                'name': 'Kamala Kumari Thapa',
                'gender': 'Female',
                'designation': 'Senior Teacher',
                'address': 'Kathmandu-32, New Baneshwor',
                'phone_number': '9871234570',
                'email': 'kamala.thapa@everestacademy.edu.np',
                'qualification': 'M.A in Nepali Literature',
                'subjects': 'Nepali, Social Studies',
                'salary': 55000.00
            },
            {
                'name': 'Bishnu Kumar Gurung',
                'gender': 'Male',
                'designation': 'Teacher',
                'address': 'Pokhara-17, Lakeside',
                'phone_number': '9881234571',
                'email': 'bishnu.gurung@everestacademy.edu.np',
                'qualification': 'B.Sc in Physics',
                'subjects': 'Physics, Chemistry',
                'salary': 45000.00
            },
            {
                'name': 'Gita Rani Adhikari',
                'gender': 'Female',
                'designation': 'Teacher',
                'address': 'Chitwan-5, Bharatpur',
                'phone_number': '9891234572',
                'email': 'gita.adhikari@everestacademy.edu.np',
                'qualification': 'M.A in History',
                'subjects': 'History, Geography',
                'salary': 45000.00
            },
            {
                'name': 'Mohan Bahadur Rai',
                'gender': 'Male',
                'designation': 'Teacher',
                'address': 'Dharan-15, Bhanuchowk',
                'phone_number': '9801234573',
                'email': 'mohan.rai@everestacademy.edu.np',
                'qualification': 'B.Ed in Science',
                'subjects': 'Biology, Environmental Science',
                'salary': 42000.00
            },
            {
                'name': 'Sunita Devi Karki',
                'gender': 'Female',
                'designation': 'Assistant Teacher',
                'address': 'Butwal-11, Traffic Chowk',
                'phone_number': '9811234574',
                'email': 'sunita.karki@everestacademy.edu.np',
                'qualification': 'B.A in English',
                'subjects': 'English, Computer',
                'salary': 38000.00
            },
            {
                'name': 'Krishna Prasad Oli',
                'gender': 'Male',
                'designation': 'Teacher',
                'address': 'Biratnagar-12, Rani Mills',
                'phone_number': '9821234575',
                'email': 'krishna.oli@everestacademy.edu.np',
                'qualification': 'M.Sc in Chemistry',
                'subjects': 'Chemistry, Mathematics',
                'salary': 48000.00
            },
            {
                'name': 'Radha Kumari Tamang',
                'gender': 'Female',
                'designation': 'Teacher',
                'address': 'Hetauda-10, Makwanpur',
                'phone_number': '9831234576',
                'email': 'radha.tamang@everestacademy.edu.np',
                'qualification': 'B.Ed in Primary Education',
                'subjects': 'Primary Mathematics, Science',
                'salary': 40000.00
            },
            {
                'name': 'Deepak Bahadur Magar',
                'gender': 'Male',
                'designation': 'Subject Teacher',
                'address': 'Nepalgunj-8, Tribhuvan Chowk',
                'phone_number': '9841234577',
                'email': 'deepak.magar@everestacademy.edu.np',
                'qualification': 'B.A in Social Work',
                'subjects': 'Social Studies, Civics',
                'salary': 35000.00
            },
            {
                'name': 'Laxmi Devi Pandey',
                'gender': 'Female',
                'designation': 'Teacher',
                'address': 'Janakpur-5, Ram Mandir',
                'phone_number': '9851234578',
                'email': 'laxmi.pandey@everestacademy.edu.np',
                'qualification': 'M.A in Sanskrit',
                'subjects': 'Sanskrit, Nepali',
                'salary': 43000.00
            },
            {
                'name': 'Narayan Prasad Bhattarai',
                'gender': 'Male',
                'designation': 'Teacher',
                'address': 'Mahendranagar-7, Bhimdatta',
                'phone_number': '9861234579',
                'email': 'narayan.bhattarai@everestacademy.edu.np',
                'qualification': 'B.Sc in Computer Science',
                'subjects': 'Computer Science, ICT',
                'salary': 46000.00
            },
            {
                'name': 'Saraswati Devi Joshi',
                'gender': 'Female',
                'designation': 'Assistant Teacher',
                'address': 'Dhangadhi-3, Attariya Road',
                'phone_number': '9871234580',
                'email': 'saraswati.joshi@everestacademy.edu.np',
                'qualification': 'B.Ed in Arts',
                'subjects': 'Art, Craft, Music',
                'salary': 36000.00
            },
            {
                'name': 'Rajesh Kumar Limbu',
                'gender': 'Male',
                'designation': 'Teacher',
                'address': 'Ilam-9, Mai Pokhari',
                'phone_number': '9881234581',
                'email': 'rajesh.limbu@everestacademy.edu.np',
                'qualification': 'M.A in Economics',
                'subjects': 'Economics, Business Studies',
                'salary': 44000.00
            },
            {
                'name': 'Parvati Kumari Chaudhary',
                'gender': 'Female',
                'designation': 'Teacher',
                'address': 'Birgunj-14, Ghantaghar',
                'phone_number': '9891234582',
                'email': 'parvati.chaudhary@everestacademy.edu.np',
                'qualification': 'B.Sc in Agriculture',
                'subjects': 'Agriculture, Environmental Science',
                'salary': 41000.00
            },
            {
                'name': 'Tek Bahadur Thakuri',
                'gender': 'Male',
                'designation': 'Subject Teacher',
                'address': 'Dadeldhura-2, Amargadhi',
                'phone_number': '9801234583',
                'email': 'tek.thakuri@everestacademy.edu.np',
                'qualification': 'B.P.Ed in Physical Education',
                'subjects': 'Physical Education, Sports',
                'salary': 37000.00
            },
            {
                'name': 'Mina Kumari Sherpa',
                'gender': 'Female',
                'designation': 'Assistant Teacher',
                'address': 'Solukhumbu-1, Namche Bazaar',
                'phone_number': '9811234584',
                'email': 'mina.sherpa@everestacademy.edu.np',
                'qualification': 'B.A in Music',
                'subjects': 'Music, Dance, Cultural Studies',
                'salary': 34000.00
            },
            {
                'name': 'Gopal Prasad Regmi',
                'gender': 'Male',
                'designation': 'Teacher',
                'address': 'Gorkha-8, Palungtar',
                'phone_number': '9821234585',
                'email': 'gopal.regmi@everestacademy.edu.np',
                'qualification': 'M.A in Political Science',
                'subjects': 'Political Science, Current Affairs',
                'salary': 47000.00
            },
            {
                'name': 'Durga Devi Khadka',
                'gender': 'Female',
                'designation': 'Teacher',
                'address': 'Surkhet-5, Birendranagar',
                'phone_number': '9831234586',
                'email': 'durga.khadka@everestacademy.edu.np',
                'qualification': 'B.Sc in Nursing',
                'subjects': 'Health Education, First Aid',
                'salary': 39000.00
            }
        ]
        
        # Get teacher images from static folder
        teacher_images_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'teacher')
        teacher_images = []
        
        if os.path.exists(teacher_images_path):
            teacher_images = [f for f in os.listdir(teacher_images_path) 
                            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        
        created_count = 0
        
        for teacher_data in teachers_data:
            # Random joining date between 2015-2024
            start_date = date(2015, 1, 1)
            end_date = date(2024, 12, 31)
            random_days = random.randint(0, (end_date - start_date).days)
            joining_date = start_date + timedelta(days=random_days)
            
            # Random date of birth (25-55 years old)
            birth_year = random.randint(1969, 1999)
            birth_month = random.randint(1, 12)
            birth_day = random.randint(1, 28)
            date_of_birth = date(birth_year, birth_month, birth_day)
            
            # Random photo assignment
            photo_path = None
            if teacher_images:
                random_image = random.choice(teacher_images)
                photo_path = f'teacher_photos/{random_image}'
            
            teacher = Teacher.objects.create(
                name=teacher_data['name'],
                address=teacher_data['address'],
                designation=teacher_data['designation'],
                phone_number=teacher_data['phone_number'],
                email=teacher_data['email'],
                gender=teacher_data['gender'],
                date_of_birth=date_of_birth,
                joining_date=joining_date,
                qualification=teacher_data['qualification'],
                subjects=teacher_data['subjects'],
                salary=teacher_data['salary'],
                is_active=True,
                photo=photo_path if photo_path else None
            )
            
            created_count += 1
            self.stdout.write(f"Created teacher: {teacher.name}")
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} teachers with Nepali context data')
        )