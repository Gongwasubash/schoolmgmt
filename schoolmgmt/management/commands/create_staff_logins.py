from django.core.management.base import BaseCommand
from schoolmgmt.models import Teacher, AdminLogin
import hashlib

class Command(BaseCommand):
    help = 'Create login credentials for all staff members'

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0
        
        # Get all teachers
        teachers = Teacher.objects.all()
        
        for teacher in teachers:
            # Generate username from name (lowercase, no spaces)
            username = teacher.name.lower().replace(' ', '').replace('.', '')
            
            # Generate simple password (first name + last 4 digits of phone)
            name_parts = teacher.name.split()
            first_name = name_parts[0].lower()
            phone_suffix = teacher.phone_number[-4:] if len(teacher.phone_number) >= 4 else '1234'
            password = f"{first_name}{phone_suffix}"
            
            # Hash the password (simple MD5 for demo - use proper hashing in production)
            hashed_password = hashlib.md5(password.encode()).hexdigest()
            
            # Check if login already exists
            admin_login, created = AdminLogin.objects.get_or_create(
                username=username,
                defaults={
                    'password': hashed_password,
                    'is_active': True
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created login for {teacher.name}:')
                )
                self.stdout.write(f'  Username: {username}')
                self.stdout.write(f'  Password: {password}')
                self.stdout.write(f'  Designation: {teacher.designation}')
                self.stdout.write('---')
            else:
                # Update existing login if needed
                if not admin_login.is_active:
                    admin_login.is_active = True
                    admin_login.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'Activated existing login for {teacher.name}: {username}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Login already exists for {teacher.name}: {username}')
                    )
        
        # Create summary report
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('STAFF LOGIN CREDENTIALS SUMMARY'))
        self.stdout.write('='*50)
        
        # Display all credentials in a formatted table
        all_logins = AdminLogin.objects.filter(username__in=[
            teacher.name.lower().replace(' ', '').replace('.', '') 
            for teacher in teachers
        ])
        
        self.stdout.write(f"{'Name':<25} {'Username':<20} {'Password':<15} {'Designation':<20}")
        self.stdout.write('-' * 80)
        
        for teacher in teachers:
            username = teacher.name.lower().replace(' ', '').replace('.', '')
            name_parts = teacher.name.split()
            first_name = name_parts[0].lower()
            phone_suffix = teacher.phone_number[-4:] if len(teacher.phone_number) >= 4 else '1234'
            password = f"{first_name}{phone_suffix}"
            
            self.stdout.write(f"{teacher.name:<25} {username:<20} {password:<15} {teacher.designation:<20}")
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(
            self.style.SUCCESS(f'Summary: {created_count} new logins created, {updated_count} existing logins updated')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total active staff logins: {AdminLogin.objects.filter(is_active=True).count()}')
        )