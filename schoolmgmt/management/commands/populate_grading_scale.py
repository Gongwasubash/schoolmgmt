from django.core.management.base import BaseCommand
from schoolmgmt.models import GradingScale

class Command(BaseCommand):
    help = 'Populate grading scale data'

    def handle(self, *args, **options):
        grading_data = [
            {'min_marks': 90, 'max_marks': 100, 'grade': 'A+', 'performance': 'Outstanding', 'grade_point': 4.0},
            {'min_marks': 80, 'max_marks': 89, 'grade': 'A', 'performance': 'Excellent', 'grade_point': 3.6},
            {'min_marks': 70, 'max_marks': 79, 'grade': 'B+', 'performance': 'Very Good', 'grade_point': 3.2},
            {'min_marks': 60, 'max_marks': 69, 'grade': 'B', 'performance': 'Good', 'grade_point': 2.8},
            {'min_marks': 50, 'max_marks': 59, 'grade': 'C+', 'performance': 'Satisfactory', 'grade_point': 2.4},
            {'min_marks': 40, 'max_marks': 49, 'grade': 'C', 'performance': 'Acceptable', 'grade_point': 2.0},
            {'min_marks': 30, 'max_marks': 39, 'grade': 'D', 'performance': 'Basic', 'grade_point': 1.6},
            {'min_marks': 0, 'max_marks': 29, 'grade': 'NG', 'performance': 'Not Graded', 'grade_point': 0.0},
        ]
        
        GradingScale.objects.all().delete()
        
        for data in grading_data:
            GradingScale.objects.create(**data)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated grading scale data'))