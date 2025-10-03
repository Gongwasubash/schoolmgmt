from django.core.management.base import BaseCommand
from schoolmgmt.models import Teacher
from datetime import date

class Command(BaseCommand):
    help = 'Add specialized teachers for uncovered subjects'

    def handle(self, *args, **options):
        specialized_teachers = [
            {
                'name': 'Binod Kumar Acharya',
                'address': 'Bhaktapur-8, Madhyapur Thimi',
                'designation': 'Subject Teacher',
                'phone_number': '+977-9841234567',
                'email': 'binod.acharya@everestacademy.edu.np',
                'gender': 'Male',
                'date_of_birth': date(1985, 8, 15),
                'joining_date': date(2020, 4, 1),
                'qualification': 'MBA in Marketing, BBS',
                'subjects': 'Marketing, Business Studies, Economics',
                'salary': 45000.00,
                'is_active': True
            },
            {
                'name': 'Anita Kumari Maharjan',
                'address': 'Lalitpur-12, Pulchowk',
                'designation': 'Subject Teacher',
                'phone_number': '+977-9851234568',
                'email': 'anita.maharjan@everestacademy.edu.np',
                'gender': 'Female',
                'date_of_birth': date(1988, 3, 22),
                'joining_date': date(2021, 7, 15),
                'qualification': 'Bachelor in Hotel Management, Diploma in Hospitality',
                'subjects': 'Hotel Management, Tourism, Business Studies',
                'salary': 42000.00,
                'is_active': True
            },
            {
                'name': 'Prakash Bahadur Karki',
                'address': 'Kathmandu-16, Balkhu',
                'designation': 'Assistant Teacher',
                'phone_number': '+977-9861234569',
                'email': 'prakash.karki@everestacademy.edu.np',
                'gender': 'Male',
                'date_of_birth': date(1990, 11, 8),
                'joining_date': date(2022, 1, 10),
                'qualification': 'B.Ed in Primary Education, Intermediate',
                'subjects': 'Primary Education, Math, English, Nepali',
                'salary': 35000.00,
                'is_active': True
            }
        ]
        
        created_count = 0
        for teacher_data in specialized_teachers:
            teacher, created = Teacher.objects.get_or_create(
                name=teacher_data['name'],
                defaults=teacher_data
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created teacher: {teacher.name} - {teacher.subjects}")
            else:
                # Update subjects if teacher exists
                teacher.subjects = teacher_data['subjects']
                teacher.save()
                self.stdout.write(f"Updated existing teacher: {teacher.name} - {teacher.subjects}")
        
        self.stdout.write(f"\nSuccessfully processed {len(specialized_teachers)} specialized teachers")
        self.stdout.write(f"New teachers created: {created_count}")
        
        # Show final teacher count and coverage
        total_teachers = Teacher.objects.count()
        self.stdout.write(f"Total teachers in system: {total_teachers}")