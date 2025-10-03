from django.core.management.base import BaseCommand
from schoolmgmt.models import AdminLogin
import hashlib

class Command(BaseCommand):
    help = 'Create a super admin with user management permissions'

    def handle(self, *args, **options):
        # Super admin credentials
        username = 'superadmin'
        password = 'admin123'
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        
        # Create or update super admin
        super_admin, created = AdminLogin.objects.get_or_create(
            username=username,
            defaults={
                'password': hashed_password,
                'is_active': True,
                'is_super_admin': True,
                'can_create_users': True,
                'can_delete_users': True
            }
        )
        
        if not created:
            # Update existing admin to super admin
            super_admin.is_super_admin = True
            super_admin.can_create_users = True
            super_admin.can_delete_users = True
            super_admin.is_active = True
            super_admin.save()
            
        action = 'Created' if created else 'Updated'
        self.stdout.write(
            self.style.SUCCESS(f'{action} super admin account:')
        )
        self.stdout.write(f'Username: {username}')
        self.stdout.write(f'Password: {password}')
        self.stdout.write('Permissions: Create Users, Delete Users, Super Admin')
        
        # Show summary of all admin permissions
        self.stdout.write('\n' + '='*50)
        self.stdout.write('ADMIN PERMISSIONS SUMMARY')
        self.stdout.write('='*50)
        
        super_admins = AdminLogin.objects.filter(is_super_admin=True)
        user_managers = AdminLogin.objects.filter(can_create_users=True, can_delete_users=True, is_super_admin=False)
        
        self.stdout.write(f'Super Admins: {super_admins.count()}')
        for admin in super_admins:
            self.stdout.write(f'  - {admin.username}')
        
        self.stdout.write(f'User Managers: {user_managers.count()}')
        for admin in user_managers:
            self.stdout.write(f'  - {admin.username}')
        
        self.stdout.write(f'Total Active Logins: {AdminLogin.objects.filter(is_active=True).count()}')