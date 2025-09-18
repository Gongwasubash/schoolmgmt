from django.contrib import admin
from .models import Student, FeeStructure, FeePayment

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'reg_number', 'student_class', 'section', 'father_name', 'mobile', 'admission_date']
    list_filter = ['student_class', 'section', 'gender', 'admission_date']
    search_fields = ['name', 'reg_number', 'father_name', 'mobile']
    ordering = ['-admission_date']

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ['class_name', 'admission_fee', 'monthly_fee', 'updated_at']
    list_filter = ['class_name']
    ordering = ['class_name']

@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'total_fee', 'payment_amount', 'balance', 'payment_method', 'created_at']
    list_filter = ['payment_method', 'created_at']
    search_fields = ['student__name']
    ordering = ['-created_at']