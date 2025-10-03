from django.core.management.base import BaseCommand
from schoolmgmt.models import Teacher
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Populate office staff and other non-teaching personnel'

    def handle(self, *args, **options):
        # Office staff data
        office_staff_data = [
            # Accountants
            {'name': 'Rajesh Sharma', 'designation': 'Accountant', 'phone': '9841234567', 'email': 'rajesh.sharma@school.edu.np', 'gender': 'Male', 'qualification': 'BBS, CA'},
            {'name': 'Sunita Thapa', 'designation': 'Office Assistant', 'phone': '9841234568', 'email': 'sunita.thapa@school.edu.np', 'gender': 'Female', 'qualification': 'BBA'},
            
            # Office Assistants
            {'name': 'Mohan Karki', 'designation': 'Office Assistant', 'phone': '9841234569', 'email': 'mohan.karki@school.edu.np', 'gender': 'Male', 'qualification': '+2 Management'},
            {'name': 'Kamala Devi', 'designation': 'Office Assistant', 'phone': '9841234570', 'email': 'kamala.devi@school.edu.np', 'gender': 'Female', 'qualification': '+2 Science'},
            
            # Librarian
            {'name': 'Bishnu Prasad Poudel', 'designation': 'Librarian', 'phone': '9841234571', 'email': 'bishnu.poudel@school.edu.np', 'gender': 'Male', 'qualification': 'MA English, Library Science'},
            
            # Lab Assistants
            {'name': 'Ravi Kumar Joshi', 'designation': 'Lab Assistant', 'phone': '9841234572', 'email': 'ravi.joshi@school.edu.np', 'gender': 'Male', 'qualification': 'BSc Physics'},
            {'name': 'Sita Kumari', 'designation': 'Lab Assistant', 'phone': '9841234573', 'email': 'sita.kumari@school.edu.np', 'gender': 'Female', 'qualification': 'BSc Chemistry'},
            
            # Computer Operator
            {'name': 'Prakash Adhikari', 'designation': 'Computer Operator', 'phone': '9841234574', 'email': 'prakash.adhikari@school.edu.np', 'gender': 'Male', 'qualification': 'Diploma in Computer Science'},
            
            # Security Guards
            {'name': 'Ram Bahadur Gurung', 'designation': 'Security Guard', 'phone': '9841234575', 'email': 'ram.gurung@school.edu.np', 'gender': 'Male', 'qualification': 'SLC'},
            {'name': 'Tek Bahadur Magar', 'designation': 'Security Guard', 'phone': '9841234576', 'email': 'tek.magar@school.edu.np', 'gender': 'Male', 'qualification': 'SLC'},
            
            # Kitchen Staff
            {'name': 'Maya Tamang', 'designation': 'Kitchen Staff', 'phone': '9841234577', 'email': 'maya.tamang@school.edu.np', 'gender': 'Female', 'qualification': 'Class 8'},
            {'name': 'Dil Maya Sherpa', 'designation': 'Kitchen Staff', 'phone': '9841234578', 'email': 'dilmaya.sherpa@school.edu.np', 'gender': 'Female', 'qualification': 'Class 10'},
            
            # Cleaners
            {'name': 'Sanu Kanchha', 'designation': 'Cleaner', 'phone': '9841234579', 'email': 'sanu.kanchha@school.edu.np', 'gender': 'Male', 'qualification': 'Class 5'},
            {'name': 'Parbati Devi', 'designation': 'Cleaner', 'phone': '9841234580', 'email': 'parbati.devi@school.edu.np', 'gender': 'Female', 'qualification': 'Class 8'},
            
            # Driver
            {'name': 'Gopal Shrestha', 'designation': 'Driver', 'phone': '9841234581', 'email': 'gopal.shrestha@school.edu.np', 'gender': 'Male', 'qualification': '+2, Driving License'},
            
            # Maintenance Staff
            {'name': 'Hari Bahadur Thapa', 'designation': 'Maintenance Staff', 'phone': '9841234582', 'email': 'hari.thapa@school.edu.np', 'gender': 'Male', 'qualification': 'Technical Training'},
            
            # Nurse
            {'name': 'Gita Sharma', 'designation': 'Nurse', 'phone': '9841234583', 'email': 'gita.sharma@school.edu.np', 'gender': 'Female', 'qualification': 'Nursing Diploma'},
            
            # Counselor
            {'name': 'Dr. Anita Regmi', 'designation': 'Counselor', 'phone': '9841234584', 'email': 'anita.regmi@school.edu.np', 'gender': 'Female', 'qualification': 'MA Psychology'},
            
            # Sports Instructor
            {'name': 'Bikash Tamang', 'designation': 'Sports Instructor', 'phone': '9841234585', 'email': 'bikash.tamang@school.edu.np', 'gender': 'Male', 'qualification': 'Bachelor in Physical Education'},
        ]
        
        created_count = 0
        
        for staff_data in office_staff_data:
            # Check if staff already exists
            if not Teacher.objects.filter(phone_number=staff_data['phone']).exists():
                # Generate random joining date (within last 5 years)
                joining_date = date.today() - timedelta(days=random.randint(30, 1825))
                
                # Generate random date of birth (25-55 years old)
                birth_date = date.today() - timedelta(days=random.randint(9125, 20075))
                
                # Generate random salary based on designation
                salary_ranges = {
                    'Accountant': (35000, 50000),
                    'Office Assistant': (20000, 30000),
                    'Librarian': (30000, 40000),
                    'Lab Assistant': (25000, 35000),
                    'Computer Operator': (25000, 35000),
                    'Security Guard': (18000, 25000),
                    'Kitchen Staff': (15000, 22000),
                    'Cleaner': (12000, 18000),
                    'Driver': (20000, 28000),
                    'Maintenance Staff': (18000, 25000),
                    'Nurse': (30000, 45000),
                    'Counselor': (40000, 60000),
                    'Sports Instructor': (25000, 35000),
                }
                
                salary_range = salary_ranges.get(staff_data['designation'], (15000, 25000))
                salary = random.randint(salary_range[0], salary_range[1])
                
                # Generate address
                addresses = [
                    'Kathmandu-10, Nepal',
                    'Lalitpur-5, Nepal', 
                    'Bhaktapur-8, Nepal',
                    'Kathmandu-16, Nepal',
                    'Lalitpur-12, Nepal',
                    'Kathmandu-32, Nepal',
                    'Bhaktapur-4, Nepal',
                    'Kathmandu-25, Nepal'
                ]
                
                Teacher.objects.create(
                    name=staff_data['name'],
                    designation=staff_data['designation'],
                    phone_number=staff_data['phone'],
                    email=staff_data['email'],
                    gender=staff_data['gender'],
                    date_of_birth=birth_date,
                    joining_date=joining_date,
                    qualification=staff_data['qualification'],
                    salary=salary,
                    address=random.choice(addresses),
                    is_active=True
                )
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created {staff_data["designation"]}: {staff_data["name"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Staff already exists: {staff_data["name"]}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} office staff members')
        )