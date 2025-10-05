from django.contrib import admin
from .models import Student, FeeStructure, FeePayment, Session, Subject, Exam, Marksheet, StudentMarks, MarksheetData, StudentDailyExpense, SchoolDetail, AdminLogin, StudentRegistration, ContactEnquiry, HeroSlider, Blog, SchoolAttendance, Teacher, TeacherClassSubject, CalendarEvent

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
    list_display = ['name', 'code', 'class_name', 'specialization', 'max_marks', 'pass_marks']
    list_filter = ['class_name', 'specialization', 'max_marks', 'pass_marks']
    search_fields = ['name', 'code', 'class_name']
    ordering = ['class_name', 'name']
    
    fieldsets = (
        ('Subject Information', {
            'fields': ('name', 'code', 'class_name', 'specialization')
        }),
        ('Grading', {
            'fields': ('max_marks', 'pass_marks')
        }),
    )

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
    list_display = ['username', 'get_teacher_name', 'get_teacher_designation', 'get_permissions', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_super_admin', 'can_create_users', 'can_delete_users', 'teacher__designation', 'created_at']
    search_fields = ['username', 'teacher__name', 'teacher__designation']
    
    fieldsets = (
        ('Login Information', {
            'fields': ('username', 'password', 'teacher', 'is_active')
        }),
        ('User Management Permissions', {
            'fields': ('is_super_admin', 'can_create_users', 'can_delete_users')
        }),
        ('Sidebar Menu Permissions', {
            'fields': ('can_view_dashboard', 'can_view_students', 'can_view_teachers', 'can_view_reports', 'can_view_marksheet', 'can_view_fee_structure', 'can_view_fee_receipt', 'can_view_daily_expenses', 'can_view_school_settings', 'can_view_website_settings', 'can_view_user_management', 'can_view_attendance')
        }),
        ('Additional Permissions', {
            'fields': ('can_view_charts', 'can_view_stats', 'can_view_fees', 'can_view_receipts', 'can_view_expenses', 'can_view_settings'),
            'classes': ('collapse',)
        }),
    )
    
    def get_teacher_name(self, obj):
        return obj.teacher.name if obj.teacher else 'System Admin'
    get_teacher_name.short_description = 'Name'
    
    def get_teacher_designation(self, obj):
        return obj.teacher.designation if obj.teacher else 'System'
    get_teacher_designation.short_description = 'Designation'
    
    def get_permissions(self, obj):
        perms = []
        if obj.is_super_admin:
            perms.append('Super Admin')
        if obj.can_create_users:
            perms.append('Create Users')
        if obj.can_delete_users:
            perms.append('Delete Users')
        return ', '.join(perms) if perms else 'Basic'
    get_permissions.short_description = 'Permissions'

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

@admin.register(SchoolAttendance)
class SchoolAttendanceAdmin(admin.ModelAdmin):
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

class TeacherClassSubjectInline(admin.TabularInline):
    model = TeacherClassSubject
    extra = 1
    fields = ['class_name', 'subject', 'is_active']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject":
            # Filter subjects based on selected class
            kwargs["queryset"] = Subject.objects.all().order_by('class_name', 'name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'phone_number', 'get_assigned_classes_display', 'is_active']
    list_filter = ['designation', 'is_active', 'gender', 'joining_date']
    search_fields = ['name', 'phone_number', 'email', 'qualification']
    ordering = ['name']
    inlines = [TeacherClassSubjectInline]
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'gender', 'date_of_birth', 'phone_number', 'email', 'address', 'photo')
        }),
        ('Professional Information', {
            'fields': ('designation', 'joining_date', 'qualification', 'salary')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def get_assigned_classes_display(self, obj):
        """Display assigned classes in admin list"""
        classes = obj.get_assigned_classes()
        return ', '.join(classes) if classes else 'No assignments'
    get_assigned_classes_display.short_description = 'Assigned Classes'

@admin.register(TeacherClassSubject)
class TeacherClassSubjectAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'class_name', 'subject', 'is_active', 'created_at']
    list_filter = ['class_name', 'is_active', 'subject__specialization', 'created_at']
    search_fields = ['teacher__name', 'subject__name', 'class_name']
    ordering = ['teacher__name', 'class_name', 'subject__name']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Assignment Details', {
            'fields': ('teacher', 'class_name', 'subject', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('teacher', 'subject')

@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'event_type', 'is_active', 'created_by', 'created_at']
    list_filter = ['event_type', 'is_active', 'event_date', 'created_at']
    search_fields = ['title', 'description', 'created_by']
    date_hierarchy = 'event_date'
    ordering = ['-event_date']
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'event_date', 'event_type')
        }),
        ('Status', {
            'fields': ('is_active', 'created_by')
        }),
    )