from django.core.management.base import BaseCommand
from schoolmgmt.models import Student, FeeStructure, FeePayment
import json
from datetime import date, datetime
import random

class Command(BaseCommand):
    help = 'Populate sample fee data for testing'

    def handle(self, *args, **options):
        # Create fee structures for all classes if they don't exist
        classes = ['Nursery', 'LKG', 'UKG', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th']
        
        for class_name in classes:
            fee_structure, created = FeeStructure.objects.get_or_create(
                class_name=class_name,
                defaults={
                    'admission_fee': 5000,
                    'monthly_fee': 2500,
                    'tuition_fee': 2000,
                    'examination_fee': 1000,
                    'library_fee': 500,
                    'sports_fee': 800,
                    'laboratory_fee': 1200,
                    'computer_fee': 1500,
                    'transportation_fee': 1500,
                }
            )
            if created:
                self.stdout.write(f'Created fee structure for {class_name}')

        # Create sample payments for existing students
        students = Student.objects.all()[:10]  # Limit to first 10 students
        
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        
        for student in students:
            # Create 1-3 random payments per student
            num_payments = random.randint(1, 3)
            
            for i in range(num_payments):
                # Random months paid
                paid_months = random.sample(months, random.randint(1, 3))
                
                # Random fee types
                fee_types = [
                    {'type': 'monthly_fee', 'amount': 2500, 'months': len(paid_months)},
                    {'type': 'tuition_fee', 'amount': 2000, 'months': len(paid_months)}
                ]
                
                if i == 0:  # First payment includes admission fee
                    fee_types.append({'type': 'admission_fee', 'amount': 5000, 'months': 1})
                
                total_amount = sum(fee['amount'] * fee['months'] for fee in fee_types)
                
                payment = FeePayment.objects.create(
                    student=student,
                    selected_months=json.dumps(paid_months),
                    fee_types=json.dumps(fee_types),
                    total_fee=total_amount,
                    payment_amount=total_amount,
                    balance=0,
                    payment_method=random.choice(['Cash', 'Cheque', 'Bank Transfer']),
                    remarks=f'Payment for {", ".join(paid_months)}'
                )
                
                self.stdout.write(f'Created payment for {student.name}: ₹{total_amount}')

        self.stdout.write(self.style.SUCCESS('Successfully populated fee data'))