from django.core.management.base import BaseCommand
from schoolmgmt.models import Teacher, AdminLogin

class Command(BaseCommand):
    help = 'Map existing AdminLogin records to their corresponding Teacher records'

    def handle(self, *args, **options):
        mapped_count = 0
        unmapped_count = 0
        
        # Get all AdminLogin records without teacher mapping
        admin_logins = AdminLogin.objects.filter(teacher__isnull=True)
        
        for admin_login in admin_logins:
            # Generate expected username from teacher names
            teachers = Teacher.objects.all()
            
            for teacher in teachers:
                expected_username = teacher.name.lower().replace(' ', '').replace('.', '')
                
                if admin_login.username == expected_username:
                    # Map the login to the teacher
                    admin_login.teacher = teacher
                    admin_login.save()
                    mapped_count += 1
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'Mapped login "{admin_login.username}" to teacher "{teacher.name}"')
                    )
                    break
            else:
                # No matching teacher found
                unmapped_count += 1
                self.stdout.write(
                    self.style.WARNING(f'No matching teacher found for login: {admin_login.username}')
                )
        
        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('MAPPING SUMMARY'))
        self.stdout.write('='*50)
        self.stdout.write(f'Successfully mapped: {mapped_count} logins')
        self.stdout.write(f'Unmapped logins: {unmapped_count}')
        
        # Show all mapped logins
        mapped_logins = AdminLogin.objects.filter(teacher__isnull=False)
        self.stdout.write(f'\nTotal mapped logins: {mapped_logins.count()}')
        
        self.stdout.write('\nMAPPED LOGINS:')
        self.stdout.write('-' * 60)
        for login in mapped_logins:
            self.stdout.write(f'{login.teacher.name:<25} -> {login.username}')
        
        self.stdout.write('='*50)