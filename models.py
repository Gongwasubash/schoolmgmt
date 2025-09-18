from django.db import models

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
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.reg_number}"
    
    class Meta:
        ordering = ['-created_at']

class FeeStructure(models.Model):
    class_name = models.CharField(max_length=20)
    admission_fee = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)
    examination_fee = models.DecimalField(max_digits=10, decimal_places=2)
    library_fee = models.DecimalField(max_digits=10, decimal_places=2)
    sports_fee = models.DecimalField(max_digits=10, decimal_places=2)
    laboratory_fee = models.DecimalField(max_digits=10, decimal_places=2)
    computer_fee = models.DecimalField(max_digits=10, decimal_places=2)
    transportation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.class_name} - ₹{self.total_fee}"