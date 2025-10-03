from django.core.management.base import BaseCommand
from schoolmgmt.models import AdminLogin

class Command(BaseCommand):
    help = 'Enable all sidebar menu permissions for basic users (non-super admin)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Enable permissions for specific username only',
        )

    def handle(self, *args, **options):
        username = options.get('username')
        
        if username:
            try:
                user = AdminLogin.objects.get(username=username, is_active=True)
                if user.is_super_admin:
                    self.stdout.write(
                        self.style.WARNING(f'User {username} is already a super admin with all permissions')
                    )
                    return
                
                user.enable_all_permissions()
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully enabled all permissions for user: {username}')
                )
            except AdminLogin.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'User {username} not found or inactive')
                )
        else:
            # Enable for all basic users
            basic_users = AdminLogin.objects.filter(is_super_admin=False, is_active=True)
            count = basic_users.count()
            
            self.stdout.write(f'Found {count} basic users')
            
            for user in basic_users:
                user.enable_all_permissions()
                self.stdout.write(f'Enabled all permissions for: {user.username}')
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully enabled all permissions for {count} basic users!')
            )