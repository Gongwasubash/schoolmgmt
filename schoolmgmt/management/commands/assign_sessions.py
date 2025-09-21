from django.core.management.base import BaseCommand
from schoolmgmt.models import Student, Session
from datetime import date

class Command(BaseCommand):
    help = 'Assign sessions to students who don\'t have one'

    def handle(self, *args, **options):
        # Get or create default session
        current_session = Session.get_current_session()
        if not current_session:
            current_session, created = Session.objects.get_or_create(
                name='2024-25',
                defaults={
                    'start_date': date(2024, 4, 1),
                    'end_date': date(2025, 3, 31),
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created default session: {current_session.name}')
                )

        # Update students without sessions
        students_without_session = Student.objects.filter(session__isnull=True) | Student.objects.filter(session='')
        count = students_without_session.count()
        
        if count > 0:
            students_without_session.update(session=current_session.name)
            self.stdout.write(
                self.style.SUCCESS(f'Assigned session "{current_session.name}" to {count} students')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('All students already have sessions assigned')
            )