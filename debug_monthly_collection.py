#!/usr/bin/env python
"""
Debug script to check Monthly Collection Details data
Run this script to see what data exists in the database
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from datetime import date
from django.db.models import Sum, Count
from schoolmgmt.models import FeePayment, StudentDailyExpense

def debug_monthly_collection():
    today = date.today()
    start_date = today.replace(day=1)
    end_date = today
    
    print(f"=== Monthly Collection Debug ===")
    print(f"Date range: {start_date} to {end_date}")
    print(f"Current month: {today.strftime('%B %Y')}")
    print()
    
    # Check FeePayment records
    payments = FeePayment.objects.filter(
        payment_date__range=[start_date, end_date]
    )
    print(f"FeePayment records in current month: {payments.count()}")
    
    if payments.exists():
        fee_total = payments.aggregate(total=Sum('payment_amount'))['total'] or 0
        print(f"Total fee collection: Rs. {fee_total}")
        print("Recent payments:")
        for payment in payments[:5]:
            print(f"  - {payment.student.name}: Rs. {payment.payment_amount} on {payment.payment_date}")
    else:
        print("No fee payments found for current month")
    
    print()
    
    # Check StudentDailyExpense records
    expenses = StudentDailyExpense.objects.filter(
        expense_date__range=[start_date, end_date]
    )
    print(f"StudentDailyExpense records in current month: {expenses.count()}")
    
    if expenses.exists():
        expense_total = expenses.aggregate(total=Sum('amount'))['total'] or 0
        print(f"Total daily expenses: Rs. {expense_total}")
        print("Recent expenses:")
        for expense in expenses[:5]:
            print(f"  - {expense.student.name}: {expense.description} - Rs. {expense.amount} on {expense.expense_date}")
    else:
        print("No daily expenses found for current month")
    
    print()
    
    # Check all-time data
    all_payments = FeePayment.objects.all()
    all_expenses = StudentDailyExpense.objects.all()
    
    print(f"Total FeePayment records (all time): {all_payments.count()}")
    print(f"Total StudentDailyExpense records (all time): {all_expenses.count()}")
    
    if all_payments.exists():
        print("Latest payment dates:")
        for payment in all_payments.order_by('-payment_date')[:5]:
            print(f"  - {payment.payment_date}")
    
    if all_expenses.exists():
        print("Latest expense dates:")
        for expense in all_expenses.order_by('-expense_date')[:5]:
            print(f"  - {expense.expense_date}")

if __name__ == "__main__":
    debug_monthly_collection()