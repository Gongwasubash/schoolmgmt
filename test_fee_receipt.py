#!/usr/bin/env python
"""
Test script for Fee Receipt Book functionality
Run this after setting up the database and creating some students
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import Student, FeeStructure, FeePayment
import json
from datetime import date

def test_fee_receipt_book():
    print("Testing Fee Receipt Book functionality...")
    
    # Check if we have students
    student_count = Student.objects.count()
    print(f"Total students in database: {student_count}")
    
    if student_count == 0:
        print("No students found. Please add some students first.")
        return
    
    # Check fee structures
    fee_structures = FeeStructure.objects.count()
    print(f"Fee structures configured: {fee_structures}")
    
    # Check payments
    payments = FeePayment.objects.count()
    print(f"Total payments recorded: {payments}")
    
    # Test fee calculation for first student
    first_student = Student.objects.first()
    if first_student:
        print(f"\nTesting fee calculation for: {first_student.name}")
        
        try:
            fee_structure = FeeStructure.objects.get(class_name=first_student.student_class)
            total_annual_fee = (
                float(fee_structure.admission_fee) +
                float(fee_structure.monthly_fee) * 12 +
                float(fee_structure.tuition_fee) * 12 +
                float(fee_structure.examination_fee) +
                float(fee_structure.library_fee) +
                float(fee_structure.sports_fee) +
                float(fee_structure.laboratory_fee) +
                float(fee_structure.computer_fee) +
                float(fee_structure.transportation_fee) * 12
            )
            print(f"Total annual fee: ₹{total_annual_fee:,.2f}")
            
            # Check payments for this student
            student_payments = FeePayment.objects.filter(student=first_student)
            total_paid = sum(payment.payment_amount for payment in student_payments)
            print(f"Total paid: ₹{total_paid:,.2f}")
            print(f"Balance: ₹{total_annual_fee - total_paid:,.2f}")
            
        except FeeStructure.DoesNotExist:
            print(f"No fee structure found for class: {first_student.student_class}")
    
    print("\nFee Receipt Book is ready to use!")
    print("Access it at: http://localhost:8000/fee-receipt-book/")

if __name__ == "__main__":
    test_fee_receipt_book()