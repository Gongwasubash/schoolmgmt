from django.db import models
from datetime import datetime, date
from .nepali_calendar import NepaliCalendar
import os
import random
from django.conf import settings

class SchoolDetail(models.Model):
    school_name = models.CharField(max_length=200, default="Everest Academy")
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)
    principal_signature = models.ImageField(upload_to='signatures/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "School Detail"
        verbose_name_plural = "School Details"
    
    def __str__(self):
        return self.school_name
    
    @classmethod
    def get_current_school(cls):
        school, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'school_name': 'Everest Academy',
                'address': 'Kathmandu, Nepal',
                'phone': '+977-1-4444444',
                'email': 'info@everestacademy.edu.np'
            }
        )
        return school

class Student(models.Model):
    GENDER_CHOICES = [
        ('Boy', 'Boy'),
        ('Girl', 'Girl'),
    ]
    
    RELIGION_CHOICES = [
        ('Hindu', 'Hindu'),
        ('Muslim', 'Muslim'),
        ('Christian', 'Christian'),
        ('Sikh', 'Sikh'),
        ('Other', 'Other'),
    ]
    
    CLASS_CHOICES = [
        ('Nursery', 'Nursery'),
        ('LKG', 'LKG'),
        ('UKG', 'UKG'),
        ('One', 'One'),
        ('Two', 'Two'),
        ('Three', 'Three'),
        ('Four', 'Four'),
        ('Five', 'Five'),
        ('Six', 'Six'),
        ('Seven', 'Seven'),
        ('Eight', 'Eight'),
        ('Nine', 'Nine'),
        ('Ten', 'Ten'),
        ('Eleven', 'Eleven'),
        ('Twelve', 'Twelve'),
    ]
    
    SECTION_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]
    
    # Personal Information
    name = models.CharField(max_length=100)
    student_class = models.CharField(max_length=10, choices=CLASS_CHOICES)
    section = models.CharField(max_length=1, choices=SECTION_CHOICES)
    transport = models.CharField(max_length=100)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(default='subashgongwanepal@gmail.com')
    gender = models.CharField(max_length=4, choices=GENDER_CHOICES)
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES)
    dob = models.DateField()
    dob_nepali = models.CharField(max_length=20, blank=True, help_text='Format: YYYY/MM/DD')
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    
    # Admission Details
    admission_date = models.DateField()
    admission_date_nepali = models.CharField(max_length=50, blank=True, help_text="Nepali date format")
    admission_date_nepali_short = models.CharField(max_length=20, blank=True, help_text="Short Nepali date (YYYY/MM/DD)")
    reg_number = models.CharField(max_length=50, unique=True)
    session = models.CharField(max_length=10)
    session_nepali = models.CharField(max_length=15, blank=True, help_text="Nepali session (e.g., 2082-83)")
    
    # Documents
    character_cert = models.BooleanField(default=False)
    report_card = models.BooleanField(default=False)
    dob_cert = models.BooleanField(default=False)
    
    # Academic History
    last_school = models.CharField(max_length=200, blank=True)
    marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    exam_result = models.CharField(max_length=100, blank=True)
    
    # Father's Details
    father_name = models.CharField(max_length=100)
    father_mobile = models.CharField(max_length=10)
    father_email = models.EmailField(blank=True)
    father_occupation = models.CharField(max_length=100, blank=True)
    father_qualification = models.CharField(max_length=100, blank=True)
    father_dob = models.DateField(blank=True, null=True)
    father_dob_nepali = models.CharField(max_length=20, blank=True, help_text='Format: YYYY/MM/DD')
    father_citizen = models.CharField(max_length=50, blank=True)
    
    # Mother's Details
    mother_name = models.CharField(max_length=100)
    mother_mobile = models.CharField(max_length=10, blank=True)
    mother_occupation = models.CharField(max_length=100, blank=True)
    mother_qualification = models.CharField(max_length=100, blank=True)
    mother_dob = models.DateField(blank=True, null=True)
    mother_dob_nepali = models.CharField(max_length=20, blank=True, help_text='Format: YYYY/MM/DD')
    mother_citizen = models.CharField(max_length=50, blank=True)
    
    # Other Information
    old_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    admission_paid = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Auto-populate Nepali dates if not provided
        if self.admission_date:
            if not self.admission_date_nepali:
                nepali_date = NepaliCalendar.english_to_nepali_date(self.admission_date)
                self.admission_date_nepali = NepaliCalendar.format_nepali_date(nepali_date, 'full_en')
                self.admission_date_nepali_short = NepaliCalendar.format_nepali_date(nepali_date, 'short')
            
            # Auto-populate Nepali session if not provided
            if not self.session_nepali:
                self.session_nepali = NepaliCalendar.get_nepali_session_from_date(self.admission_date)
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.reg_number}"
    
    def get_nepali_dob(self):
        """Convert AD DOB to Nepali date"""
        if self.dob_nepali:
            return self.dob_nepali
        try:
            from nepali_datetime import date as nepali_date
            nepali_dob = nepali_date.from_datetime_date(self.dob)
            return f'{nepali_dob.year}/{nepali_dob.month:02d}/{nepali_dob.day:02d}'
        except:
            return f'{self.dob.year + 57}/{self.dob.month:02d}/{self.dob.day:02d}'
    
    def get_random_photo_url(self):
        """Get a random photo from static/img/students folder"""
        try:
            students_folder = os.path.join(settings.BASE_DIR, 'static', 'img', 'students')
            if os.path.exists(students_folder):
                image_files = [f for f in os.listdir(students_folder) 
                             if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
                if image_files:
                    random_image = random.choice(image_files)
                    return f'/static/img/students/{random_image}'
            return '/static/img/default-student.png'  # Fallback
        except:
            return '/static/img/default-student.png'  # Fallback
    
    class Meta:
        ordering = ['-created_at']


class FeeStructure(models.Model):
    CLASS_CHOICES = [
        ('Nursery', 'Nursery'),
        ('LKG', 'LKG'),
        ('UKG', 'UKG'),
        ('One', 'One'),
        ('Two', 'Two'),
        ('Three', 'Three'),
        ('Four', 'Four'),
        ('Five', 'Five'),
        ('Six', 'Six'),
        ('Seven', 'Seven'),
        ('Eight', 'Eight'),
        ('Nine', 'Nine'),
        ('Ten', 'Ten'),
        ('Eleven', 'Eleven'),
        ('Twelve', 'Twelve'),
    ]
    
    class_name = models.CharField(max_length=10, choices=CLASS_CHOICES, unique=True)
    class_order = models.IntegerField(default=0, help_text="Order for sorting classes")
    admission_fee = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)
    examination_fee = models.DecimalField(max_digits=10, decimal_places=2)
    library_fee = models.DecimalField(max_digits=10, decimal_places=2)
    sports_fee = models.DecimalField(max_digits=10, decimal_places=2)
    laboratory_fee = models.DecimalField(max_digits=10, decimal_places=2)
    computer_fee = models.DecimalField(max_digits=10, decimal_places=2)
    transportation_fee = models.DecimalField(max_digits=10, decimal_places=2)

    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.class_name}"
    
    class Meta:
        ordering = ['class_order']


class FeePayment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque'),
        ('Bank Transfer', 'Bank Transfer'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    payment_date_nepali = models.CharField(max_length=50, blank=True, help_text="Nepali payment date")
    payment_date_nepali_short = models.CharField(max_length=20, blank=True, help_text="Short Nepali payment date")
    selected_months = models.TextField()  # JSON string of selected months
    fee_types = models.TextField()  # JSON string of fee types and amounts
    custom_fees = models.TextField(blank=True)  # JSON string of custom fees
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    bank_name = models.CharField(max_length=100, blank=True)
    cheque_dd_no = models.CharField(max_length=50, blank=True)
    cheque_date = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True)
    sms_sent = models.BooleanField(default=False)
    whatsapp_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Auto-populate Nepali payment date if not provided
        if self.payment_date and not self.payment_date_nepali:
            nepali_date = NepaliCalendar.english_to_nepali_date(self.payment_date)
            self.payment_date_nepali = NepaliCalendar.format_nepali_date(nepali_date, 'full_en')
            self.payment_date_nepali_short = NepaliCalendar.format_nepali_date(nepali_date, 'short')
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student.name} - Rs.{self.payment_amount} - {self.payment_date}"
    
    class Meta:
        ordering = ['-created_at']


class Subject(models.Model):
    SPECIALIZATION_CHOICES = [
        ('Mathematics', 'Mathematics'),
        ('Science', 'Science'),
        ('English', 'English'),
        ('Social Studies', 'Social Studies'),
        ('Computer Science', 'Computer Science'),
        ('Arts', 'Arts'),
        ('Physical Education', 'Physical Education'),
        ('Other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    class_name = models.CharField(max_length=10, choices=Student.CLASS_CHOICES)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES, blank=True, null=True)
    max_marks = models.IntegerField(default=100)
    pass_marks = models.IntegerField(default=35)
    
    def __str__(self):
        return f"{self.name} - {self.class_name}"
    
    class Meta:
        ordering = ['class_name', 'name']


class Exam(models.Model):
    EXAM_TYPE_CHOICES = [
        ('First Term', 'First Term'),
        ('Mid Term', 'Mid Term'),
        ('Final Term', 'Final Term'),
        ('Unit Test', 'Unit Test'),
        ('Annual', 'Annual'),
    ]
    
    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES)
    class_name = models.CharField(max_length=10, choices=Student.CLASS_CHOICES)
    exam_date = models.DateField()
    exam_date_nepali = models.CharField(max_length=50, blank=True, help_text="Nepali date format")
    exam_date_nepali_short = models.CharField(max_length=20, blank=True, help_text="Short Nepali date (YYYY/MM/DD)")
    session = models.CharField(max_length=10)
    session_nepali = models.CharField(max_length=15, blank=True, help_text="Nepali session (e.g., 2082-83)")
    
    def save(self, *args, **kwargs):
        # Auto-populate Nepali dates if not provided
        if self.exam_date:
            if not self.exam_date_nepali:
                nepali_date = NepaliCalendar.english_to_nepali_date(self.exam_date)
                self.exam_date_nepali = NepaliCalendar.format_nepali_date(nepali_date, 'full_en')
                self.exam_date_nepali_short = NepaliCalendar.format_nepali_date(nepali_date, 'short')
            
            # Auto-populate Nepali session if not provided
            if not self.session_nepali:
                self.session_nepali = NepaliCalendar.get_nepali_session_from_date(self.exam_date)
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.class_name}"
    
    class Meta:
        ordering = ['-exam_date']


class Marksheet(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField()
    remarks = models.CharField(max_length=200, blank=True)
    session = models.CharField(max_length=10, default='2024-25')
    
    def __str__(self):
        return f"{self.student.name} - {self.exam.name} - {self.subject.name}"
    
    @property
    def percentage(self):
        return (int(self.marks_obtained) / int(self.subject.max_marks)) * 100
    
    @property
    def grade(self):
        percentage = self.percentage
        if percentage >= 90:
            return 'A+'
        elif percentage >= 80:
            return 'A'
        elif percentage >= 70:
            return 'B+'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C+'
        elif percentage >= 40:
            return 'C'
        elif percentage >= 30:
            return 'D+'
        elif percentage >= 20:
            return 'D'
        else:
            return 'E'
    
    @property
    def grade_point(self):
        percentage = self.percentage
        if percentage >= 90:
            return 4.0
        elif percentage >= 80:
            return 3.6
        elif percentage >= 70:
            return 3.2
        elif percentage >= 60:
            return 2.8
        elif percentage >= 50:
            return 2.4
        elif percentage >= 40:
            return 2.0
        elif percentage >= 30:
            return 1.6
        elif percentage >= 20:
            return 1.2
        else:
            return 0.8
    
    @property
    def grade_remarks(self):
        percentage = self.percentage
        if percentage >= 90:
            return 'Outstanding'
        elif percentage >= 80:
            return 'Excellent'
        elif percentage >= 70:
            return 'Very Good'
        elif percentage >= 60:
            return 'Good'
        elif percentage >= 50:
            return 'Satisfactory'
        elif percentage >= 40:
            return 'Acceptable'
        elif percentage >= 30:
            return 'Partially Accept.'
        elif percentage >= 20:
            return 'Weak'
        else:
            return 'Very Poor / Fail'
    
    @property
    def status(self):
        return 'Pass' if int(self.marks_obtained) >= int(self.subject.pass_marks) else 'Fail'
    
    class Meta:
        unique_together = ['student', 'exam', 'subject']
        ordering = ['exam', 'student', 'subject']


class Session(models.Model):
    name = models.CharField(max_length=20, unique=True)  # e.g., "2024-25", "2025-26"
    name_nepali = models.CharField(max_length=25, blank=True, help_text="Nepali session name (e.g., 2082-83)")
    start_date = models.DateField()
    end_date = models.DateField()
    start_date_nepali = models.CharField(max_length=50, blank=True, help_text="Nepali start date")
    end_date_nepali = models.CharField(max_length=50, blank=True, help_text="Nepali end date")
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Auto-populate Nepali session data if not provided
        if not self.name_nepali and self.start_date:
            nepali_start_date = NepaliCalendar.english_to_nepali_date(self.start_date)
            start_year = nepali_start_date['year']
            self.name_nepali = f"{start_year}-{str(start_year+1)[-2:]}"
        
        if self.start_date and not self.start_date_nepali:
            nepali_date = NepaliCalendar.english_to_nepali_date(self.start_date)
            self.start_date_nepali = NepaliCalendar.format_nepali_date(nepali_date, 'full_en')
        
        if self.end_date and not self.end_date_nepali:
            nepali_date = NepaliCalendar.english_to_nepali_date(self.end_date)
            self.end_date_nepali = NepaliCalendar.format_nepali_date(nepali_date, 'full_en')
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.name_nepali})" if self.name_nepali else self.name
    
    @classmethod
    def get_current_session(cls):
        return cls.objects.filter(is_active=True).first()
    
    @classmethod
    def get_current_nepali_session(cls):
        current = cls.get_current_session()
        return current.name_nepali if current and current.name_nepali else NepaliCalendar.get_nepali_session_from_date()
    
    class Meta:
        ordering = ['-start_date']


class StudentMarks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=100)
    marks_obtained = models.IntegerField()
    max_marks = models.IntegerField(default=100)
    session = models.CharField(max_length=20)
    exam_type = models.CharField(max_length=50, default='Regular')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.subject_name} - {self.marks_obtained}/{self.max_marks}"
    
    @property
    def percentage(self):
        return (self.marks_obtained / self.max_marks) * 100 if self.max_marks > 0 else 0
    
    @property
    def grade(self):
        percentage = self.percentage
        if percentage >= 90: return 'A+'
        elif percentage >= 80: return 'A'
        elif percentage >= 70: return 'B+'
        elif percentage >= 60: return 'B'
        elif percentage >= 50: return 'C+'
        elif percentage >= 40: return 'C'
        elif percentage >= 30: return 'D+'
        elif percentage >= 20: return 'D'
        else: return 'E'
    
    @property
    def grade_point(self):
        percentage = self.percentage
        if percentage >= 90: return 4.0
        elif percentage >= 80: return 3.6
        elif percentage >= 70: return 3.2
        elif percentage >= 60: return 2.8
        elif percentage >= 50: return 2.4
        elif percentage >= 40: return 2.0
        elif percentage >= 30: return 1.6
        elif percentage >= 20: return 1.2
        else: return 0.8
    
    @property
    def grade_remarks(self):
        percentage = self.percentage
        if percentage >= 90: return 'Outstanding'
        elif percentage >= 80: return 'Excellent'
        elif percentage >= 70: return 'Very Good'
        elif percentage >= 60: return 'Good'
        elif percentage >= 50: return 'Satisfactory'
        elif percentage >= 40: return 'Acceptable'
        elif percentage >= 30: return 'Partially Accept.'
        elif percentage >= 20: return 'Weak'
        else: return 'Very Poor / Fail'
    
    class Meta:
        unique_together = ['student', 'subject_name', 'session', 'exam_type']
        ordering = ['-created_at']


class GradingScale(models.Model):
    min_marks = models.IntegerField()
    max_marks = models.IntegerField()
    grade = models.CharField(max_length=5)
    performance = models.CharField(max_length=20)
    grade_point = models.DecimalField(max_digits=3, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.min_marks}-{self.max_marks}: {self.grade} ({self.grade_point})"
    
    class Meta:
        ordering = ['-min_marks']


class MarksheetData(models.Model):
    student_name = models.CharField(max_length=100)
    subject_name = models.CharField(max_length=100)
    marks_obtained = models.IntegerField()
    max_marks = models.IntegerField(default=100)
    session = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student_name} - {self.subject_name} - {self.marks_obtained}/{self.max_marks} ({self.session})"
    
    @property
    def percentage(self):
        return (self.marks_obtained / self.max_marks) * 100 if self.max_marks > 0 else 0
    
    @property
    def grade(self):
        percentage = self.percentage
        if percentage >= 90: return 'A+'
        elif percentage >= 80: return 'A'
        elif percentage >= 70: return 'B+'
        elif percentage >= 60: return 'B'
        elif percentage >= 50: return 'C+'
        elif percentage >= 40: return 'C'
        elif percentage >= 30: return 'D+'
        elif percentage >= 20: return 'D'
        else: return 'E'
    
    @property
    def grade_point(self):
        percentage = self.percentage
        if percentage >= 90: return 4.0
        elif percentage >= 80: return 3.6
        elif percentage >= 70: return 3.2
        elif percentage >= 60: return 2.8
        elif percentage >= 50: return 2.4
        elif percentage >= 40: return 2.0
        elif percentage >= 30: return 1.6
        elif percentage >= 20: return 1.2
        else: return 0.8
    
    @property
    def grade_remarks(self):
        percentage = self.percentage
        if percentage >= 90: return 'Outstanding'
        elif percentage >= 80: return 'Excellent'
        elif percentage >= 70: return 'Very Good'
        elif percentage >= 60: return 'Good'
        elif percentage >= 50: return 'Satisfactory'
        elif percentage >= 40: return 'Acceptable'
        elif percentage >= 30: return 'Partially Accept.'
        elif percentage >= 20: return 'Weak'
        else: return 'Very Poor / Fail'
    
    class Meta:
        ordering = ['-created_at']


class StudentDailyExpense(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    expense_date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.description} - Rs.{self.amount}"
    
    class Meta:
        ordering = ['-created_at']


class AdminLogin(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100, help_text="Plain text password (no hashing)")
    teacher = models.OneToOneField('Teacher', on_delete=models.CASCADE, blank=True, null=True, related_name='login')
    is_active = models.BooleanField(default=True)
    is_super_admin = models.BooleanField(default=False, help_text="Can create and delete users")
    can_create_users = models.BooleanField(default=False)
    can_delete_users = models.BooleanField(default=False)
    
    # Sidebar Menu Permissions
    can_view_dashboard = models.BooleanField(default=False, verbose_name="Dashboard", help_text="Can view dashboard")
    can_view_students = models.BooleanField(default=True, verbose_name="Students", help_text="Can view students menu")
    can_view_teachers = models.BooleanField(default=True, verbose_name="Teachers", help_text="Can view teachers menu")
    can_view_reports = models.BooleanField(default=False, verbose_name="Reports", help_text="Can view reports menu")
    can_view_marksheet = models.BooleanField(default=False, verbose_name="Marksheet", help_text="Can view marksheet menu")
    can_view_fee_structure = models.BooleanField(default=False, verbose_name="Fee Structure", help_text="Can view fee structure menu")
    can_view_fee_receipt = models.BooleanField(default=False, verbose_name="Fee Receipt", help_text="Can view fee receipt menu")
    can_view_daily_expenses = models.BooleanField(default=False, verbose_name="Daily Expenses", help_text="Can view daily expenses menu")
    can_view_school_settings = models.BooleanField(default=False, verbose_name="School Settings", help_text="Can view school settings menu")
    can_view_website_settings = models.BooleanField(default=False, verbose_name="Website Settings", help_text="Can view website settings menu")
    can_view_user_management = models.BooleanField(default=False, verbose_name="User Management", help_text="Can view user management menu")
    can_view_attendance = models.BooleanField(default=False, verbose_name="Student Attendance", help_text="Can view student attendance menu")
    can_edit_own_class_marksheet = models.BooleanField(default=True, verbose_name="Edit Own Class Marksheet", help_text="Can edit marksheet data for assigned classes/subjects")
    
    # Additional permissions for compatibility
    can_view_charts = models.BooleanField(default=False, verbose_name="Charts", help_text="Can view charts and graphs")
    can_view_stats = models.BooleanField(default=False, verbose_name="Statistics", help_text="Can view statistics")
    can_view_fees = models.BooleanField(default=False, verbose_name="Fees", help_text="Can view fees menu")
    can_view_receipts = models.BooleanField(default=False, verbose_name="Receipts", help_text="Can view receipts menu")
    can_view_expenses = models.BooleanField(default=False, verbose_name="Expenses", help_text="Can view expenses menu")
    can_view_settings = models.BooleanField(default=False, verbose_name="Settings", help_text="Can view settings menu")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.teacher:
            return f"{self.username} ({self.teacher.name})"
        return self.username
    
    def save(self, *args, **kwargs):
        # Store password as plain text (no hashing)
        super().save(*args, **kwargs)
    
    def has_user_management_permission(self):
        return self.is_super_admin or self.can_view_user_management
    
    def enable_all_permissions(self):
        """Enable all sidebar menu permissions for basic users"""
        self.can_view_dashboard = True
        self.can_view_students = True
        self.can_view_teachers = True
        self.can_view_reports = True
        self.can_view_marksheet = True
        self.can_view_fee_structure = True
        self.can_view_fee_receipt = True
        self.can_view_daily_expenses = True
        self.can_view_school_settings = True
        self.can_view_website_settings = True
        self.can_view_user_management = True
        self.can_view_charts = True
        self.can_view_stats = True
        self.can_view_fees = True
        self.can_view_receipts = True
        self.can_view_expenses = True
        self.can_view_settings = True
        self.can_view_attendance = True
        self.save()
    
    class Meta:
        verbose_name = "Admin Login"
        verbose_name_plural = "Admin Logins"


class StudentRegistration(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    GENDER_CHOICES = [
        ('Boy', 'Boy'),
        ('Girl', 'Girl'),
    ]
    
    RELIGION_CHOICES = [
        ('Hindu', 'Hindu'),
        ('Muslim', 'Muslim'),
        ('Christian', 'Christian'),
        ('Other', 'Other'),
    ]
    
    CLASS_CHOICES = [
        ('Nursery', 'Nursery'),
        ('LKG', 'LKG'),
        ('UKG', 'UKG'),
        ('One', 'One'),
        ('Two', 'Two'),
        ('Three', 'Three'),
        ('Four', 'Four'),
        ('Five', 'Five'),
        ('Six', 'Six'),
        ('Seven', 'Seven'),
        ('Eight', 'Eight'),
        ('Nine', 'Nine'),
        ('Ten', 'Ten'),
        ('Eleven', 'Eleven'),
        ('Twelve', 'Twelve'),
    ]
    
    SECTION_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]
    
    # Student Information
    name = models.CharField(max_length=100)
    student_class = models.CharField(max_length=10, choices=CLASS_CHOICES)
    section = models.CharField(max_length=1, choices=SECTION_CHOICES, default='A')
    gender = models.CharField(max_length=4, choices=GENDER_CHOICES)
    dob = models.DateField()
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES, default='Hindu')
    
    # Parent Information
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    
    # Address Information
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    
    # Registration Details
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    remarks = models.TextField(blank=True)
    
    # Auto-generated fields
    application_number = models.CharField(max_length=20, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.application_number:
            from datetime import datetime
            self.application_number = f"APP{datetime.now().year}{StudentRegistration.objects.count() + 1:04d}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.application_number} ({self.status})"
    
    class Meta:
        ordering = ['-registration_date']
        verbose_name = "Student Registration"
        verbose_name_plural = "Student Registrations"

class ContactEnquiry(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=200)
    enquiry = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Enquiry"
        verbose_name_plural = "Contact Enquiries"

class HeroSlider(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='hero_images/')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['order', '-created_at']

class Blog(models.Model):
    heading = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.ImageField(upload_to='blog_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.heading
    
    class Meta:
        ordering = ['-created_at']

class WelcomeSection(models.Model):
    title = models.CharField(max_length=200, default="Welcome to Our School")
    content = models.TextField()
    image = models.ImageField(upload_to='welcome_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    @classmethod
    def get_active_welcome(cls):
        return cls.objects.filter(is_active=True).first()
    
    class Meta:
        ordering = ['-created_at']


class Teacher(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    
    CLASS_CHOICES = [
        ('Nursery', 'Nursery'),
        ('LKG', 'LKG'),
        ('UKG', 'UKG'),
        ('One', 'One'),
        ('Two', 'Two'),
        ('Three', 'Three'),
        ('Four', 'Four'),
        ('Five', 'Five'),
        ('Six', 'Six'),
        ('Seven', 'Seven'),
        ('Eight', 'Eight'),
        ('Nine', 'Nine'),
        ('Ten', 'Ten'),
        ('Eleven', 'Eleven'),
        ('Twelve', 'Twelve'),
    ]
    
    DESIGNATION_CHOICES = [
        ('Principal', 'Principal'),
        ('Vice Principal', 'Vice Principal'),
        ('Head Teacher', 'Head Teacher'),
        ('Senior Teacher', 'Senior Teacher'),
        ('Teacher', 'Teacher'),
        ('Assistant Teacher', 'Assistant Teacher'),
        ('Subject Teacher', 'Subject Teacher'),
        ('Accountant', 'Accountant'),
        ('Office Assistant', 'Office Assistant'),
        ('Librarian', 'Librarian'),
        ('Lab Assistant', 'Lab Assistant'),
        ('Computer Operator', 'Computer Operator'),
        ('Security Guard', 'Security Guard'),
        ('Kitchen Staff', 'Kitchen Staff'),
        ('Cleaner', 'Cleaner'),
        ('Driver', 'Driver'),
        ('Maintenance Staff', 'Maintenance Staff'),
        ('Nurse', 'Nurse'),
        ('Counselor', 'Counselor'),
        ('Sports Instructor', 'Sports Instructor'),
    ]
    
    name = models.CharField(max_length=100)
    address = models.TextField()
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    joining_date = models.DateField()
    qualification = models.CharField(max_length=200, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    class_teacher_for = models.CharField(max_length=15, choices=CLASS_CHOICES, blank=True, null=True, help_text="Class for which this teacher is the class teacher")
    photo = models.ImageField(upload_to='teacher_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.designation}"
    
    def get_assigned_classes(self):
        """Get all active classes assigned to this teacher"""
        return TeacherClassSubject.objects.filter(teacher=self, is_active=True).values_list('class_name', flat=True).distinct()
    
    def get_subjects_for_class(self, class_name):
        """Get all active subjects this teacher teaches for a specific class"""
        return TeacherClassSubject.objects.filter(teacher=self, class_name=class_name, is_active=True).select_related('subject')
    
    def get_all_assignments(self):
        """Get all active class-subject assignments grouped by class"""
        return TeacherClassSubject.get_teacher_assignments(self)
    
    def assign_classes_subjects(self, assignments_data):
        """Assign multiple classes and subjects to this teacher"""
        TeacherClassSubject.assign_multiple_classes_subjects(self, assignments_data)
    
    def get_random_photo_url(self):
        """Get a random photo from static/img/teachers folder"""
        try:
            teachers_folder = os.path.join(settings.BASE_DIR, 'static', 'img', 'teachers')
            if os.path.exists(teachers_folder):
                image_files = [f for f in os.listdir(teachers_folder) 
                             if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
                if image_files:
                    random_image = random.choice(image_files)
                    return f'/static/img/teachers/{random_image}'
            return '/static/img/default-teacher.png'
        except:
            return '/static/img/default-teacher.png'
    
    class Meta:
        ordering = ['name']


class TeacherClassSubject(models.Model):
    """Model to handle teacher assignments to multiple classes and subjects"""
    CLASS_CHOICES = [
        ('Nursery', 'Nursery'),
        ('LKG', 'LKG'),
        ('UKG', 'UKG'),
        ('One', 'One'),
        ('Two', 'Two'),
        ('Three', 'Three'),
        ('Four', 'Four'),
        ('Five', 'Five'),
        ('Six', 'Six'),
        ('Seven', 'Seven'),
        ('Eight', 'Eight'),
        ('Nine', 'Nine'),
        ('Ten', 'Ten'),
        ('Eleven', 'Eleven'),
        ('Twelve', 'Twelve'),
    ]
    
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='class_subjects')
    class_name = models.CharField(max_length=15, choices=CLASS_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, help_text="Is this assignment currently active?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.teacher.name} - {self.class_name} - {self.subject.name}"
    
    @classmethod
    def get_teacher_assignments(cls, teacher):
        """Get all active assignments for a teacher grouped by class"""
        assignments = cls.objects.filter(teacher=teacher, is_active=True).select_related('subject')
        grouped = {}
        for assignment in assignments:
            if assignment.class_name not in grouped:
                grouped[assignment.class_name] = []
            grouped[assignment.class_name].append(assignment.subject)
        return grouped
    
    @classmethod
    def assign_multiple_classes_subjects(cls, teacher, assignments_data):
        """Assign multiple classes and subjects to a teacher
        assignments_data format: [{'class_name': 'One', 'subject_ids': [1, 2, 3]}, ...]
        """
        # Deactivate existing assignments
        cls.objects.filter(teacher=teacher).update(is_active=False)
        
        # Create new assignments
        for assignment in assignments_data:
            class_name = assignment['class_name']
            subject_ids = assignment['subject_ids']
            
            for subject_id in subject_ids:
                try:
                    subject = Subject.objects.get(id=subject_id, class_name=class_name)
                    cls.objects.update_or_create(
                        teacher=teacher,
                        class_name=class_name,
                        subject=subject,
                        defaults={'is_active': True}
                    )
                except Subject.DoesNotExist:
                    continue
    
    class Meta:
        unique_together = ['teacher', 'class_name', 'subject']
        ordering = ['teacher__name', 'class_name', 'subject__name']


class SchoolAttendance(models.Model):
    ATTENDANCE_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    date_nepali = models.CharField(max_length=50, blank=True, help_text="Nepali date format")
    status = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES, default='present')
    remarks = models.CharField(max_length=200, blank=True)
    marked_by = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if self.date and not self.date_nepali:
            nepali_date = NepaliCalendar.english_to_nepali_date(self.date)
            self.date_nepali = NepaliCalendar.format_nepali_date(nepali_date, 'full_en')
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"
    
    @classmethod
    def get_attendance_summary(cls, student, start_date=None, end_date=None):
        queryset = cls.objects.filter(student=student)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        total = queryset.count()
        present = queryset.filter(status='present').count()
        absent = queryset.filter(status='absent').count()
        late = queryset.filter(status='late').count()
        
        return {
            'total': total,
            'present': present,
            'absent': absent,
            'late': late,
            'attendance_percentage': (present / total * 100) if total > 0 else 0
        }
    
    class Meta:
        unique_together = ['student', 'date']
        ordering = ['-date', 'student__name']
        verbose_name = "School Attendance"
        verbose_name_plural = "School Attendance"


class CalendarEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ('holiday', 'Holiday'),
        ('festival', 'Festival'),
        ('exam', 'Exam'),
        ('meeting', 'Meeting'),
        ('event', 'School Event'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_date = models.DateField()
    event_date_nepali = models.CharField(max_length=50, blank=True, help_text="Nepali date format")
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='event')
    school = models.ForeignKey(SchoolDetail, on_delete=models.CASCADE, blank=True, null=True, help_text="School for this event")
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Auto-populate Nepali date if not provided
        if self.event_date and not self.event_date_nepali:
            nepali_date = NepaliCalendar.english_to_nepali_date(self.event_date)
            self.event_date_nepali = NepaliCalendar.format_nepali_date(nepali_date, 'full_en')
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} - {self.event_date}"
    
    @classmethod
    def get_events_for_month(cls, year, month):
        """Get all active events for a specific month"""
        return cls.objects.filter(
            event_date__year=year,
            event_date__month=month,
            is_active=True
        ).order_by('event_date')
    
    class Meta:
        ordering = ['-event_date']
        verbose_name = "Calendar Event"
        verbose_name_plural = "Calendar Events"


class StudentAttendance(models.Model):
    ATTENDANCE_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    date_nepali = models.CharField(max_length=50, blank=True, help_text="Nepali date format")
    status = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES, default='present')
    remarks = models.CharField(max_length=200, blank=True)
    marked_by = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Auto-populate Nepali date if not provided
        if self.date and not self.date_nepali:
            nepali_date = NepaliCalendar.english_to_nepali_date(self.date)
            self.date_nepali = NepaliCalendar.format_nepali_date(nepali_date, 'full_en')
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"
    
    @classmethod
    def get_attendance_for_date(cls, date, student_class=None, section=None):
        """Get attendance records for a specific date with optional class/section filter"""
        queryset = cls.objects.filter(date=date).select_related('student')
        if student_class:
            queryset = queryset.filter(student__student_class=student_class)
        if section:
            queryset = queryset.filter(student__section=section)
        return queryset
    
    @classmethod
    def get_student_attendance_summary(cls, student, start_date=None, end_date=None):
        """Get attendance summary for a student within date range"""
        queryset = cls.objects.filter(student=student)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        total = queryset.count()
        present = queryset.filter(status='present').count()
        absent = queryset.filter(status='absent').count()
        late = queryset.filter(status='late').count()
        
        return {
            'total': total,
            'present': present,
            'absent': absent,
            'late': late,
            'attendance_percentage': (present / total * 100) if total > 0 else 0
        }
    
    class Meta:
        unique_together = ['student', 'date']
        ordering = ['-date', 'student__name']
        verbose_name = "Student Attendance"
        verbose_name_plural = "Student Attendance"