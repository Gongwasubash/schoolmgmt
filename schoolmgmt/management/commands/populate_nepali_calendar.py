from django.core.management.base import BaseCommand
from schoolmgmt.models import CalendarEvent, SchoolDetail
from schoolmgmt.nepali_calendar import NepaliCalendar

class Command(BaseCommand):
    help = 'Populate Nepali calendar events from Baishakh 1 to Chaitra 30'

    def add_arguments(self, parser):
        parser.add_argument(
            '--year',
            type=int,
            help='Nepali year (default: current year)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing events before populating',
        )

    def handle(self, *args, **options):
        year = options['year'] or NepaliCalendar.get_current_nepali_date()['year']
        
        self.stdout.write(f'Populating Nepali calendar for year {year}...')
        
        if options['clear']:
            CalendarEvent.objects.all().delete()
            self.stdout.write('Cleared existing events.')
        
        # Accurate Festival data based on traditional Nepali calendar
        festivals = {
            1: {1: "Nepali New Year", 15: "Buddha Jayanti (Baisakh Purnima)"},
            2: {15: "Jestha Purnima"},
            3: {15: "Guru Purnima (Ashadh Purnima)"},
            4: {1: "Shrawan Sankranti", 15: "Janai Purnima (Raksha Bandhan)", 16: "Gai Jatra", 23: "Krishna Janmashtami"},
            5: {3: "Haritalika Teej", 5: "Rishi Panchami", 15: "Bhadra Purnima"},
            6: {1: "Ghatasthapana (Dashain Begins)", 7: "Phulpati", 8: "Maha Ashtami", 9: "Maha Navami", 10: "Vijaya Dashami", 15: "Kojagrat Purnima"},
            7: {2: "Bhai Tika", 6: "Chhath Parva", 13: "Kag Tihar (Crow Day)", 14: "Kukur Tihar (Dog Day)", 15: "Gai Tihar/Laxmi Puja", 30: "Goru Tihar/Govardhan Puja"},
            8: {15: "Yomari Punhi (Mangsir Purnima)"},
            9: {1: "Poush Sankranti", 15: "Poush Purnima"},
            10: {1: "Maghe Sankranti", 5: "Shree Panchami (Saraswati Puja)", 15: "Magh Purnima", 29: "Maha Shivaratri"},
            11: {15: "Holi (Fagu Purnima)"},
            12: {8: "Chaitra Ashtami", 9: "Ram Navami (Chaitra Navami)", 15: "Chaitra Purnima", 30: "Chaitra Dashain"}
        }
        
        school_events = {
            1: {10: "New Session Begins", 20: "Parent Meeting"},
            2: {15: "Sports Competition", 25: "Cultural Program"},
            3: {10: "Annual Examination", 25: "Exam Results"},
            4: {5: "Teacher's Day", 20: "Science Fair"},
            5: {15: "Cleanliness Campaign", 25: "Tree Plantation"},
            6: {10: "Dashain Holiday Begins", 25: "Dashain Holiday Ends"},
            7: {10: "Tihar Holiday Begins", 20: "Tihar Holiday Ends"},
            8: {15: "Winter Holiday", 30: "Annual Celebration"},
            9: {10: "Winter Sports", 25: "Community Service"},
            10: {15: "Art Exhibition", 25: "Final Exam Preparation"},
            11: {10: "Holi Celebration", 25: "Graduation Ceremony"},
            12: {15: "Annual Review", 29: "Session End"}
        }
        
        school = SchoolDetail.get_current_school()
        total_events = 0
        
        # Add festivals
        for month, events in festivals.items():
            for day, name in events.items():
                try:
                    english_date = NepaliCalendar.nepali_date_to_english_approximate(year, month, day)
                    CalendarEvent.objects.create(
                        title=name,
                        description=f"Traditional Nepali festival on {day} {NepaliCalendar.NEPALI_MONTHS_EN[month-1]}",
                        event_date=english_date,
                        event_type='festival',
                        school=school,
                        created_by='Management Command'
                    )
                    total_events += 1
                except Exception as e:
                    self.stdout.write(f'Error creating {name}: {e}')
        
        # Add school events
        for month, events in school_events.items():
            for day, name in events.items():
                try:
                    english_date = NepaliCalendar.nepali_date_to_english_approximate(year, month, day)
                    CalendarEvent.objects.create(
                        title=name,
                        description=f"School event on {day} {NepaliCalendar.NEPALI_MONTHS_EN[month-1]}",
                        event_date=english_date,
                        event_type='event',
                        school=school,
                        created_by='Management Command'
                    )
                    total_events += 1
                except Exception as e:
                    self.stdout.write(f'Error creating {name}: {e}')
        
        # Add Saturday holidays
        saturday_count = 0
        for month in range(1, 13):
            days_in_month = NepaliCalendar.NEPALI_DAYS.get(year, [31]*12)[month-1]
            for day in range(1, days_in_month + 1):
                try:
                    english_date = NepaliCalendar.nepali_date_to_english_approximate(year, month, day)
                    if english_date.weekday() == 5:  # Saturday
                        CalendarEvent.objects.create(
                            title="Saturday Holiday",
                            description="Weekly holiday",
                            event_date=english_date,
                            event_type='holiday',
                            school=school,
                            created_by='Management Command'
                        )
                        saturday_count += 1
                except Exception:
                    continue
        
        total_events += saturday_count
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated {total_events} events for Nepali year {year}\n'
                f'Festivals: {sum(len(events) for events in festivals.values())}\n'
                f'School Events: {sum(len(events) for events in school_events.values())}\n'
                f'Saturday Holidays: {saturday_count}'
            )
        )