from django.core.management.base import BaseCommand
from schoolmgmt.models import Student, Session
from django.db import models
from datetime import date

class Command(BaseCommand):
    help = 'Update all students to have session names assigned'

    def handle(self, *args, **options):
        # Get or create current active session
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

        # Update students without sessions or with empty sessions
        students_without_session = Student.objects.filter(
            models.Q(session__isnull=True) | models.Q(session='')
        )
        count = students_without_session.count()
        
        if count > 0:
            students_without_session.update(session=current_session.name)
            self.stdout.write(
                self.style.SUCCESS(f'Updated {count} students with session "{current_session.name}"')
            )
        
        # Show statistics
        total_students = Student.objects.count()
        students_with_sessions = Student.objects.exclude(
            models.Q(session__isnull=True) | models.Q(session='')
        ).count()
        
        self.stdout.write(
            self.style.SUCCESS(f'Total students: {total_students}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Students with sessions: {students_with_sessions}')
        )
        
        if total_students == students_with_sessions:
            self.stdout.write(
                self.style.SUCCESS('All students now have session names assigned!')
            )