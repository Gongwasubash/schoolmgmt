def fee_receipt_book_api(request):
    try:
        selected_months = [m.strip() for m in request.GET.get('months', '').split(',') if m.strip()]
        
        students = Student.objects.annotate(
            total_paid=Sum('feepayment__payment_amount'),
            last_payment_date=Max('feepayment__payment_date')
        ).order_by('name')
        
        students_data = []
        total_collected = Decimal('0')
        total_pending = Decimal('0')
        
        for student in students:
            try:
                fee_structure = FeeStructure.objects.get(class_name=student.student_class)
            except FeeStructure.DoesNotExist:
                fee_structure = None
            
            # Calculate fee based on selected months
            if selected_months and fee_structure:
                monthly_fee = fee_structure.monthly_fee + fee_structure.tuition_fee
                student_total_fee = monthly_fee * len(selected_months)
                
                # Calculate paid amount for selected months
                payments = FeePayment.objects.filter(student=student)
                paid_months = set()
                for payment in payments:
                    if payment.selected_months:
                        try:
                            months = json.loads(payment.selected_months)
                            paid_months.update(months)
                        except json.JSONDecodeError:
                            pass
                
                paid_selected_months = len([m for m in selected_months if m in paid_months])
                student_paid = monthly_fee * paid_selected_months
            else:
                # Default calculation (all months)
                if fee_structure:
                    student_total_fee = (
                        fee_structure.admission_fee +
                        fee_structure.monthly_fee * 12 +
                        fee_structure.tuition_fee * 12 +
                        fee_structure.examination_fee +
                        fee_structure.library_fee +
                        fee_structure.sports_fee +
                        fee_structure.laboratory_fee +
                        fee_structure.computer_fee +
                        fee_structure.transportation_fee * 12
                    )
                else:
                    student_total_fee = Decimal('60000')
                
                student_paid = student.total_paid or Decimal('0')
            
            student_pending = max(Decimal('0'), student_total_fee - student_paid)
            payment_status = 'paid' if student_pending == 0 else 'pending'
            
            total_collected += student_paid
            total_pending += student_pending
            
            students_data.append({
                'id': student.id,
                'name': student.name,
                'class_name': student.student_class,
                'section': student.section,
                'roll_number': student.reg_number,
                'total_fee': float(student_total_fee),
                'paid_amount': float(student_paid),
                'pending_amount': float(student_pending),
                'payment_status': payment_status,
                'last_payment_date': student.last_payment_date.strftime('%Y-%m-%d') if student.last_payment_date else None
            })
        
        return JsonResponse({
            'success': True,
            'students': students_data,
            'total_students': len(students_data),
            'total_collected': float(total_collected),
            'total_pending': float(total_pending)
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})