from django.contrib import admin
from .models import Student, FeeStructure, FeePayment, Session, Subject, Exam, Marksheet, StudentMarks, MarksheetData, StudentDailyExpense, SchoolDetail, AdminLogin, StudentRegistration, ContactEnquiry, HeroSlider, Blog, StudentAttendance

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

@admin.register(StudentDailyExpense)
class StudentDailyExpenseAdmin(admin.ModelAdmin):
    list_display = ['student', 'description', 'amount', 'expense_date', 'created_at']
    list_filter = ['expense_date', 'student__student_class']
    search_fields = ['student__name', 'description']
    ordering = ['-created_at']

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_nepali', 'start_date', 'end_date', 'is_active', 'created_at']
    list_filter = ['is_active', 'start_date']
    search_fields = ['name', 'name_nepali']
    ordering = ['-start_date']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'class_name', 'max_marks', 'pass_marks']
    list_filter = ['class_name', 'max_marks', 'pass_marks']
    search_fields = ['name', 'code', 'class_name']
    ordering = ['class_name', 'name']

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'exam_type', 'class_name', 'exam_date', 'session', 'session_nepali']
    list_filter = ['exam_type', 'class_name', 'session', 'exam_date']
    search_fields = ['name', 'class_name', 'session']
    ordering = ['-exam_date']

@admin.register(Marksheet)
class MarksheetAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'subject', 'marks_obtained', 'percentage', 'grade', 'status', 'session']
    list_filter = ['exam__exam_type', 'subject__class_name', 'session', 'exam__exam_date']
    search_fields = ['student__name', 'exam__name', 'subject__name']
    ordering = ['-exam__exam_date', 'student__name']

@admin.register(SchoolDetail)
class SchoolDetailAdmin(admin.ModelAdmin):
    list_display = ['school_name', 'phone', 'email', 'updated_at']
    fields = ['school_name', 'logo', 'principal_signature', 'address', 'phone', 'email']

@admin.register(AdminLogin)
class AdminLoginAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['username']
    fields = ['username', 'password', 'is_active']

@admin.register(StudentRegistration)
class StudentRegistrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'application_number', 'student_class', 'father_name', 'mobile', 'status', 'registration_date']
    list_filter = ['status', 'student_class', 'gender', 'religion', 'registration_date']
    search_fields = ['name', 'application_number', 'father_name', 'mother_name', 'mobile']
    readonly_fields = ['application_number', 'registration_date']
    ordering = ['-registration_date']
    
    fieldsets = (
        ('Student Information', {
            'fields': ('name', 'student_class', 'section', 'gender', 'dob', 'religion')
        }),
        ('Parent Information', {
            'fields': ('father_name', 'mother_name', 'mobile')
        }),
        ('Address Information', {
            'fields': ('address', 'city')
        }),
        ('Registration Details', {
            'fields': ('application_number', 'registration_date', 'status', 'remarks')
        }),
    )

@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

@admin.register(HeroSlider)
class HeroSliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title']
    ordering = ['order', '-created_at']

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['heading', 'created_at']
    list_filter = ['created_at']
    search_fields = ['heading', 'description']
    ordering = ['-created_at']

@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status', 'marked_by', 'created_at']
    list_filter = ['status', 'date', 'student__student_class', 'student__section']
    search_fields = ['student__name', 'student__reg_number']
    date_hierarchy = 'date'
    ordering = ['-date', 'student__name']
    
    fieldsets = (
        ('Attendance Information', {
            'fields': ('student', 'date', 'status', 'remarks')
        }),
        ('Additional Details', {
            'fields': ('marked_by', 'date_nepali')
        }),
    )