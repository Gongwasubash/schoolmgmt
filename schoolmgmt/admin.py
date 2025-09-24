from django.contrib import admin
from .models import Student, FeeStructure, FeePayment, Session, Subject, Exam, Marksheet, StudentMarks, MarksheetData

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'reg_number', 'student_class', 'section', 'father_name', 'mobile', 'session']
    list_filter = ['student_class', 'section', 'gender', 'session']
    search_fields = ['name', 'reg_number', 'father_name', 'mobile', 'session']
    ordering = ['-created_at']

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

@admin.register(StudentMarks)
class StudentMarksAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject_name', 'marks_obtained', 'max_marks', 'percentage', 'grade', 'session', 'exam_type', 'created_at']
    list_filter = ['session', 'exam_type', 'subject_name', 'created_at']
    search_fields = ['student__name', 'subject_name']
    ordering = ['-created_at']

@admin.register(MarksheetData)
class MarksheetDataAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'subject_name', 'marks_obtained', 'max_marks', 'percentage', 'grade', 'session', 'created_at']
    list_filter = ['session', 'subject_name', 'created_at']
    search_fields = ['student_name', 'subject_name']
    ordering = ['-created_at']