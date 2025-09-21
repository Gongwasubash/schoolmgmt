from django.core.management.base import BaseCommand
from schoolmgmt.models import Student, Subject, Exam, Marksheet
import random
from datetime import date

class Command(BaseCommand):
    help = 'Add demo marks for all students with all subjects'

    def handle(self, *args, **options):
        # Create demo exams if they don't exist
        exam_types = [
            {'name': 'First Term Exam 2024', 'exam_type': 'First Term', 'session': '2024'},
            {'name': 'Mid Term Exam 2024', 'exam_type': 'Mid Term', 'session': '2024'},
            {'name': 'Final Term Exam 2024', 'exam_type': 'Final Term', 'session': '2024'},
        ]
        
        created_exams = 0
        created_marksheets = 0
        
        # Get all students
        students = Student.objects.all()
        if not students.exists():
            self.stdout.write(self.style.WARNING('No students found. Please add students first.'))
            return
        
        # Create exams for each class
        for student in students:
            class_name = student.student_class
            
            for exam_data in exam_types:
                exam, created = Exam.objects.get_or_create(
                    name=exam_data['name'],
                    class_name=class_name,
                    defaults={
                        'exam_type': exam_data['exam_type'],
                        'exam_date': date.today(),
                        'session': exam_data['session']
                    }
                )
                if created:
                    created_exams += 1
                    self.stdout.write(f"Created exam: {exam.name} for {class_name}")
        
        # Get all subjects and create marksheets
        for student in students:
            subjects = Subject.objects.filter(class_name=student.student_class)
            exams = Exam.objects.filter(class_name=student.student_class)
            
            for exam in exams:
                for subject in subjects:
                    # Check if marksheet already exists
                    if not Marksheet.objects.filter(student=student, exam=exam, subject=subject).exists():
                        # Generate random marks (60-95% of max marks for demo)
                        min_marks = int(subject.max_marks * 0.6)  # 60% minimum
                        max_marks = int(subject.max_marks * 0.95)  # 95% maximum
                        demo_marks = random.randint(min_marks, max_marks)
                        
                        # Create marksheet
                        marksheet = Marksheet.objects.create(
                            student=student,
                            exam=exam,
                            subject=subject,
                            marks_obtained=demo_marks,
                            remarks='Demo marks'
                        )
                        created_marksheets += 1
                        
                        if created_marksheets % 50 == 0:  # Progress indicator
                            self.stdout.write(f"Created {created_marksheets} marksheets...")
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_exams} exams and {created_marksheets} marksheets with demo marks'
            )
        )
        
        # Summary
        total_students = students.count()
        self.stdout.write(f"Total students: {total_students}")
        self.stdout.write(f"Demo marks added for all students across all their subjects")