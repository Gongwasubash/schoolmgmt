from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum
from decimal import Decimal
import json
from .models import Student, FeeStructure, FeePayment, StudentDailyExpense

def student_detail_with_filters(request, student_id):
    """Student detail page with fee history based on filters"""
    student = get_object_or_404(Student, id=student_id)
    
    # Get filter parameters
    selected_months = [m.strip() for m in request.GET.get('months', '').split(',') if m.strip()]
    selected_fee_types = [f.strip() for f in request.GET.get('fee_types', '').split(',') if f.strip()]
    
    # Get fee structure for student's class
    try:
        fee_structure = FeeStructure.objects.get(class_name=student.student_class)
    except FeeStructure.DoesNotExist:
        fee_structure = None
    
    # Calculate fee totals based on filters
    total_fee = Decimal('0')
    paid_amount = Decimal('0')
    
    if fee_structure:
        # Apply fee type filters or show all if none selected
        fee_types_to_show = selected_fee_types if selected_fee_types else [
            'admission_fee', 'monthly_fee', 'tuition_fee', 'transportation_fee',
            'examination_fee', 'library_fee', 'sports_fee', 'laboratory_fee', 'computer_fee'
        ]
        
        # Apply month filters for monthly fees
        months_count = len(selected_months) if selected_months else 12
        
        # Calculate total fee based on filters
        for fee_type in fee_types_to_show:
            fee_amount = getattr(fee_structure, fee_type, 0)
            if fee_type in ['monthly_fee', 'tuition_fee', 'transportation_fee']:
                total_fee += fee_amount * months_count
            else:
                total_fee += fee_amount
    
    # Get payments and calculate paid amount
    payments = FeePayment.objects.filter(student=student).order_by('-payment_date')
    for payment in payments:
        paid_amount += payment.payment_amount
    
    # Get all daily expenses (both paid and unpaid)
    daily_expenses = StudentDailyExpense.objects.filter(student=student).order_by('-expense_date')
    daily_expenses_total = daily_expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0')
    daily_expenses_paid = daily_expenses.filter(is_paid=True).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    # Add unpaid daily expenses to total fee, paid expenses are already covered in payments
    total_fee += daily_expenses_total
    paid_amount += daily_expenses_paid
    pending_amount = max(Decimal('0'), total_fee - paid_amount)
    
    # Create fee history based on filters
    fee_history = []
    nepali_months = ['Baisakh', 'Jestha', 'Ashadh', 'Shrawan', 'Bhadra', 'Ashwin',
                    'Kartik', 'Mangsir', 'Poush', 'Magh', 'Falgun', 'Chaitra']
    
    # Get paid months from payments
    paid_months = set()
    paid_fee_types = set()
    
    for payment in payments:
        if payment.selected_months:
            try:
                months = json.loads(payment.selected_months)
                paid_months.update(months)
            except json.JSONDecodeError:
                pass
        
        if payment.fee_types:
            try:
                fee_types = json.loads(payment.fee_types)
                for fee_data in fee_types:
                    paid_fee_types.add(fee_data.get('type'))
            except json.JSONDecodeError:
                pass
    
    # Create fee history records based on filters
    if selected_months:
        for month in selected_months:
            if month in nepali_months:
                status = 'Paid' if month in paid_months else 'Pending'
                amount = 0
                
                if fee_structure:
                    if 'monthly_fee' in selected_fee_types or not selected_fee_types:
                        amount += fee_structure.monthly_fee
                    if 'tuition_fee' in selected_fee_types or not selected_fee_types:
                        amount += fee_structure.tuition_fee
                    if 'transportation_fee' in selected_fee_types or not selected_fee_types:
                        amount += fee_structure.transportation_fee
                
                fee_history.append({
                    'month': month,
                    'fee_type': 'Monthly Fees',
                    'amount': amount,
                    'status': status,
                    'payment_date': None,
                    'payment_method': None
                })
    
    # Add one-time fees if selected
    if selected_fee_types:
        one_time_fees = {
            'admission_fee': 'Admission Fee',
            'examination_fee': 'Examination Fee',
            'library_fee': 'Library Fee',
            'sports_fee': 'Sports Fee',
            'laboratory_fee': 'Laboratory Fee',
            'computer_fee': 'Computer Fee'
        }
        
        for fee_type, fee_name in one_time_fees.items():
            if fee_type in selected_fee_types and fee_structure:
                status = 'Paid' if fee_type in paid_fee_types else 'Pending'
                amount = getattr(fee_structure, fee_type, 0)
                
                fee_history.append({
                    'month': 'One-time',
                    'fee_type': fee_name,
                    'amount': amount,
                    'status': status,
                    'payment_date': None,
                    'payment_method': None
                })
    
    # Always show daily expenses regardless of filters
    elif not selected_months and not selected_fee_types:
        # Show all daily expenses when no filters are applied
        pass
    

    
    context = {
        'student': student,
        'total_fee': float(total_fee),
        'paid_amount': float(paid_amount),
        'pending_amount': float(pending_amount),
        'fee_history': fee_history,
        'daily_expenses': daily_expenses,
        'daily_expenses_total': float(daily_expenses_total),
        'selected_months': selected_months,
        'selected_fee_types': selected_fee_types
    }
    
    return render(request, 'student_detail.html', context)

def student_fee_history_api(request, student_id):
    """API to get student fee history"""
    try:
        student = get_object_or_404(Student, id=student_id)
        payments = FeePayment.objects.filter(student=student).order_by('-payment_date')
        
        payments_data = []
        for payment in payments:
            # Parse fee types and months
            fee_types = []
            months = []
            
            if payment.fee_types:
                try:
                    fee_types = json.loads(payment.fee_types)
                except json.JSONDecodeError:
                    pass
            
            if payment.selected_months:
                try:
                    months = json.loads(payment.selected_months)
                except json.JSONDecodeError:
                    pass
            
            payments_data.append({
                'date': payment.payment_date.strftime('%Y-%m-%d'),
                'amount': float(payment.payment_amount),
                'fee_type': ', '.join([ft.get('type', '').replace('_', ' ').title() for ft in fee_types]) if fee_types else 'N/A',
                'months': ', '.join(months) if months else 'N/A',
                'method': payment.payment_method
            })
        
        return JsonResponse({
            'success': True,
            'payments': payments_data
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})