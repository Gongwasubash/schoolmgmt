from django.core.management.base import BaseCommand
from schoolmgmt.models import AdminLogin
import hashlib

class Command(BaseCommand):
    help = 'Fix admin login by creating default admin users'

    def handle(self, *args, **options):
        # Create default admin users
        admin_users = [
            {
                'username': 'superadmin',
                'password': 'admin123',
                'is_super_admin': True,
            },
            {
                'username': 'subashgongwa',
                'password': 'saMA@123',
                'is_super_admin': True,
            },
            {
                'username': 'supereme',
                'password': 'saMA@123',
                'is_super_admin': True,
            },
            {
                'username': 'basicuser',
                'password': 'basic123',
                'is_super_admin': False,
            }
        ]
        
        for user_data in admin_users:
            username = user_data['username']
            password = user_data['password']
            is_super_admin = user_data['is_super_admin']
            
            hashed_password = hashlib.md5(password.encode()).hexdigest()
            
            admin, created = AdminLogin.objects.get_or_create(
                username=username,
                defaults={
                    'password': hashed_password,
                    'is_active': True,
                    'is_super_admin': is_super_admin,
                    'can_create_users': is_super_admin,
                    'can_delete_users': is_super_admin,
                    'can_view_dashboard': True,
                    'can_view_charts': True,
                    'can_view_stats': True,
                    'can_view_students': True,
                    'can_view_teachers': True,
                    'can_view_reports': True,
                    'can_view_marksheet': True,
                    'can_view_fees': True,
                    'can_view_receipts': True,
                    'can_view_expenses': True,
                    'can_view_settings': is_super_admin,
                }
            )
            
            if not created:
                # Update existing user
                admin.password = hashed_password
                admin.is_active = True
                admin.is_super_admin = is_super_admin
                admin.can_create_users = is_super_admin
                admin.can_delete_users = is_super_admin
                admin.can_view_settings = is_super_admin
                admin.save()
            
            action = 'Created' if created else 'Updated'
            role = 'Super Admin' if is_super_admin else 'Basic User'
            self.stdout.write(f'{action} {role}: {username}')
        
        self.stdout.write(self.style.SUCCESS('Admin login fix completed!'))