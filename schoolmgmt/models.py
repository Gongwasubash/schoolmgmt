from django.db import models
from datetime import datetime

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
        ('1st', '1st'),
        ('2nd', '2nd'),
        ('3rd', '3rd'),
        ('4th', '4th'),
        ('5th', '5th'),
        ('6th', '6th'),
        ('7th', '7th'),
        ('8th', '8th'),
        ('9th', '9th'),
        ('10th', '10th'),
        ('11th', '11th'),
        ('12th', '12th'),
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
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    
    # Admission Details
    admission_date = models.DateField()
    reg_number = models.CharField(max_length=50, unique=True)
    session = models.CharField(max_length=10)
    
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
    father_citizen = models.CharField(max_length=50, blank=True)
    
    # Mother's Details
    mother_name = models.CharField(max_length=100)
    mother_mobile = models.CharField(max_length=10, blank=True)
    mother_occupation = models.CharField(max_length=100, blank=True)
    mother_qualification = models.CharField(max_length=100, blank=True)
    mother_dob = models.DateField(blank=True, null=True)
    mother_citizen = models.CharField(max_length=50, blank=True)
    
    # Other Information
    old_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    admission_paid = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.reg_number}"
    
    class Meta:
        ordering = ['-created_at']


class FeeStructure(models.Model):
    CLASS_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
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
    session = models.CharField(max_length=10)
    
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
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    @classmethod
    def get_current_session(cls):
        return cls.objects.filter(is_active=True).first()
    
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