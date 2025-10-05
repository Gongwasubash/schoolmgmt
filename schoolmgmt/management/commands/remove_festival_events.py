from django.core.management.base import BaseCommand
from schoolmgmt.models import CalendarEvent

class Command(BaseCommand):
    help = 'Remove all festival events from the school calendar'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Skip confirmation prompt and delete immediately',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING('School Calendar Festival Event Removal Tool')
        )
        self.stdout.write('=' * 50)
        
        try:
            # Get all festival events
            festival_events = CalendarEvent.objects.filter(event_type='festival')
            count = festival_events.count()
            
            if count == 0:
                self.stdout.write(
                    self.style.SUCCESS('No festival events found in the calendar.')
                )
                return
            
            self.stdout.write(f"Found {count} festival events:")
            for event in festival_events:
                self.stdout.write(f"- {event.title} ({event.event_date})")
            
            # Check for confirmation
            if not options['confirm']:
                confirm = input(f"\nAre you sure you want to delete all {count} festival events? (y/N): ")
                if confirm.lower() not in ['y', 'yes']:
                    self.stdout.write(
                        self.style.WARNING('Operation cancelled.')
                    )
                    return
            
            # Delete all festival events
            deleted_count = festival_events.delete()[0]
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully deleted {deleted_count} festival events from the calendar.'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )