from django.core.management.base import BaseCommand
from schoolmgmt.models import Session
from datetime import date

class Command(BaseCommand):
    help = 'Create default academic sessions'

    def handle(self, *args, **options):
        sessions_data = [
            {
                'name': '2023-24',
                'start_date': date(2023, 4, 1),
                'end_date': date(2024, 3, 31),
                'is_active': False
            },
            {
                'name': '2024-25',
                'start_date': date(2024, 4, 1),
                'end_date': date(2025, 3, 31),
                'is_active': True
            },
            {
                'name': '2025-26',
                'start_date': date(2025, 4, 1),
                'end_date': date(2026, 3, 31),
                'is_active': False
            }
        ]

        for session_data in sessions_data:
            session, created = Session.objects.get_or_create(
                name=session_data['name'],
                defaults=session_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created session: {session.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Session already exists: {session.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully processed all sessions')
        )