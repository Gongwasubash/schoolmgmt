from django.db import models
from datetime import datetime
from .nepali_calendar import NepaliCalendar

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
        ordering = ['class_name']


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
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    class_name = models.CharField(max_length=10, choices=Student.CLASS_CHOICES)
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