from django.core.management.base import BaseCommand
from schoolmgmt.models import AdminLogin
import hashlib

class Command(BaseCommand):
    help = 'Debug admin login credentials'

    def handle(self, *args, **options):
        # Check all admin logins
        admins = AdminLogin.objects.all()
        
        self.stdout.write('ALL ADMIN LOGINS:')
        self.stdout.write('-' * 50)
        
        for admin in admins:
            self.stdout.write(f'Username: {admin.username}')
            self.stdout.write(f'Password Hash: {admin.password}')
            self.stdout.write(f'Is Active: {admin.is_active}')
            self.stdout.write(f'Is Super Admin: {admin.is_super_admin}')
            self.stdout.write('-' * 30)
        
        # Test superadmin credentials
        test_username = 'superadmin'
        test_password = 'admin123'
        test_hash = hashlib.md5(test_password.encode()).hexdigest()
        
        self.stdout.write(f'Testing credentials:')
        self.stdout.write(f'Username: {test_username}')
        self.stdout.write(f'Password: {test_password}')
        self.stdout.write(f'Expected Hash: {test_hash}')
        
        # Check if superadmin exists with correct hash
        try:
            admin = AdminLogin.objects.get(username=test_username, password=test_hash, is_active=True)
            self.stdout.write(self.style.SUCCESS('✓ Superadmin login should work'))
        except AdminLogin.DoesNotExist:
            self.stdout.write(self.style.ERROR('✗ Superadmin login will fail'))
            
            # Check if username exists but password is wrong
            try:
                admin = AdminLogin.objects.get(username=test_username)
                self.stdout.write(f'Found username but password hash mismatch:')
                self.stdout.write(f'Stored: {admin.password}')
                self.stdout.write(f'Expected: {test_hash}')
            except AdminLogin.DoesNotExist:
                self.stdout.write('Username does not exist')