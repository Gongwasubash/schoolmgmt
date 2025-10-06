#!/usr/bin/env python
"""
Script to fix daily expenses data inconsistencies.
This script will help identify and fix any paid daily expenses that should be marked as paid.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import StudentDailyExpense, FeePayment
from django.db.models import Q
import json

def fix_daily_expenses():
    """
    Fix daily expenses that should be marked as paid based on FeePayment records.
    """
    print("Checking for daily expenses that should be marked as paid...")
    
    # Find all FeePayment records that contain daily expenses in custom_fees
    fee_payments_with_expenses = FeePayment.objects.exclude(custom_fees='[]').exclude(custom_fees='')
    
    fixed_count = 0
    
    for payment in fee_payments_with_expenses:
        try:
            custom_fees = json.loads(payment.custom_fees)
            
            for custom_fee in custom_fees:
                # Look for daily expenses that match this payment
                expense_name = custom_fee.get('name', '')
                expense_amount = custom_fee.get('amount', 0)
                
                # Find matching unpaid daily expenses
                matching_expenses = StudentDailyExpense.objects.filter(
                    student=payment.student,
                    description=expense_name,
                    amount=expense_amount,
                    is_paid=False
                )
                
                if matching_expenses.exists():
                    # Mark these expenses as paid
                    updated_count = matching_expenses.update(
                        is_paid=True,
                        payment_date=payment.payment_date
                    )
                    fixed_count += updated_count
                    print(f"Marked {updated_count} daily expense(s) as paid for student {payment.student.name}")
                    
        except json.JSONDecodeError:
            continue
    
    print(f"\nFixed {fixed_count} daily expense records.")
    
    # Show summary of current state
    total_expenses = StudentDailyExpense.objects.count()
    paid_expenses = StudentDailyExpense.objects.filter(is_paid=True).count()
    unpaid_expenses = StudentDailyExpense.objects.filter(is_paid=False).count()
    
    print(f"\nCurrent state:")
    print(f"Total daily expenses: {total_expenses}")
    print(f"Paid daily expenses: {paid_expenses}")
    print(f"Unpaid daily expenses: {unpaid_expenses}")

if __name__ == '__main__':
    fix_daily_expenses()