from django.core.management.base import BaseCommand
from schoolmgmt.models import FeeStructure

class Command(BaseCommand):
    help = 'Populate fee structure with default data for all classes'

    def handle(self, *args, **options):
        FeeStructure.objects.all().delete()
        
        fee_data = [
            {'class_name': 'Nursery', 'class_order': 1, 'admission_fee': 5000, 'monthly_fee': 2500, 'tuition_fee': 2000, 'examination_fee': 500, 'library_fee': 200, 'sports_fee': 300, 'laboratory_fee': 0, 'computer_fee': 0, 'transportation_fee': 1200},
            {'class_name': 'LKG', 'class_order': 2, 'admission_fee': 5200, 'monthly_fee': 2700, 'tuition_fee': 2200, 'examination_fee': 500, 'library_fee': 200, 'sports_fee': 300, 'laboratory_fee': 0, 'computer_fee': 0, 'transportation_fee': 1200},
            {'class_name': 'UKG', 'class_order': 3, 'admission_fee': 5400, 'monthly_fee': 2900, 'tuition_fee': 2400, 'examination_fee': 500, 'library_fee': 200, 'sports_fee': 300, 'laboratory_fee': 0, 'computer_fee': 200, 'transportation_fee': 1200},
            {'class_name': 'One', 'class_order': 4, 'admission_fee': 5600, 'monthly_fee': 3100, 'tuition_fee': 2600, 'examination_fee': 600, 'library_fee': 250, 'sports_fee': 350, 'laboratory_fee': 200, 'computer_fee': 300, 'transportation_fee': 1200},
            {'class_name': 'Two', 'class_order': 5, 'admission_fee': 5800, 'monthly_fee': 3300, 'tuition_fee': 2800, 'examination_fee': 600, 'library_fee': 250, 'sports_fee': 350, 'laboratory_fee': 200, 'computer_fee': 300, 'transportation_fee': 1200},
            {'class_name': 'Three', 'class_order': 6, 'admission_fee': 6000, 'monthly_fee': 3500, 'tuition_fee': 3000, 'examination_fee': 700, 'library_fee': 300, 'sports_fee': 400, 'laboratory_fee': 300, 'computer_fee': 400, 'transportation_fee': 1200},
            {'class_name': 'Four', 'class_order': 7, 'admission_fee': 6200, 'monthly_fee': 3700, 'tuition_fee': 3200, 'examination_fee': 700, 'library_fee': 300, 'sports_fee': 400, 'laboratory_fee': 300, 'computer_fee': 400, 'transportation_fee': 1200},
            {'class_name': 'Five', 'class_order': 8, 'admission_fee': 6400, 'monthly_fee': 3900, 'tuition_fee': 3400, 'examination_fee': 800, 'library_fee': 350, 'sports_fee': 450, 'laboratory_fee': 400, 'computer_fee': 500, 'transportation_fee': 1200},
            {'class_name': 'Six', 'class_order': 9, 'admission_fee': 6600, 'monthly_fee': 4100, 'tuition_fee': 3600, 'examination_fee': 800, 'library_fee': 350, 'sports_fee': 450, 'laboratory_fee': 500, 'computer_fee': 500, 'transportation_fee': 1200},
            {'class_name': 'Seven', 'class_order': 10, 'admission_fee': 6800, 'monthly_fee': 4300, 'tuition_fee': 3800, 'examination_fee': 900, 'library_fee': 400, 'sports_fee': 500, 'laboratory_fee': 600, 'computer_fee': 600, 'transportation_fee': 1200},
            {'class_name': 'Eight', 'class_order': 11, 'admission_fee': 7000, 'monthly_fee': 4500, 'tuition_fee': 4000, 'examination_fee': 900, 'library_fee': 400, 'sports_fee': 500, 'laboratory_fee': 600, 'computer_fee': 600, 'transportation_fee': 1200},
            {'class_name': 'Nine', 'class_order': 12, 'admission_fee': 7200, 'monthly_fee': 4700, 'tuition_fee': 4200, 'examination_fee': 1000, 'library_fee': 450, 'sports_fee': 550, 'laboratory_fee': 700, 'computer_fee': 700, 'transportation_fee': 1200},
            {'class_name': 'Ten', 'class_order': 13, 'admission_fee': 7500, 'monthly_fee': 5000, 'tuition_fee': 4500, 'examination_fee': 1200, 'library_fee': 500, 'sports_fee': 600, 'laboratory_fee': 800, 'computer_fee': 800, 'transportation_fee': 1200},
            {'class_name': 'Eleven', 'class_order': 14, 'admission_fee': 8000, 'monthly_fee': 5500, 'tuition_fee': 5000, 'examination_fee': 1500, 'library_fee': 600, 'sports_fee': 700, 'laboratory_fee': 1000, 'computer_fee': 1000, 'transportation_fee': 1200},
            {'class_name': 'Twelve', 'class_order': 15, 'admission_fee': 8500, 'monthly_fee': 6000, 'tuition_fee': 5500, 'examination_fee': 1800, 'library_fee': 700, 'sports_fee': 800, 'laboratory_fee': 1200, 'computer_fee': 1200, 'transportation_fee': 1200},
        ]
        
        for data in fee_data:
            FeeStructure.objects.create(**data)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(fee_data)} fee structure records for all classes'))