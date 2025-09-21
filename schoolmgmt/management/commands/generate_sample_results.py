from django.core.management.base import BaseCommand
from schoolmgmt.models import Student, Subject, Exam, Marksheet
import random

class Command(BaseCommand):
    help = 'Generate sample result data for students'

    def handle(self, *args, **options):
        # Get first 10 students for demo
        students = Student.objects.all()[:10]
        
        if not students:
            self.stdout.write(self.style.ERROR('No students found. Please add students first.'))
            return
        
        created_count = 0
        
        for student in students:
            # Get subjects for this student's class
            subjects = Subject.objects.filter(class_name=student.student_class)
            
            if not subjects:
                self.stdout.write(f'No subjects found for class {student.student_class}')
                continue
            
            # Get exams for this student's class
            exams = Exam.objects.filter(class_name=student.student_class)
            
            if not exams:
                self.stdout.write(f'No exams found for class {student.student_class}')
                continue
            
            # Generate marks for each exam and subject
            for exam in exams:
                for subject in subjects:
                    # Check if marksheet already exists
                    if not Marksheet.objects.filter(student=student, exam=exam, subject=subject).exists():
                        # Generate random marks (60-95% of max marks for good results)
                        min_marks = int(subject.max_marks * 0.6)
                        max_marks = int(subject.max_marks * 0.95)
                        marks = random.randint(min_marks, max_marks)
                        
                        # Occasionally add some lower marks for variety
                        if random.random() < 0.1:  # 10% chance of lower marks
                            marks = random.randint(subject.pass_marks, min_marks)
                        
                        Marksheet.objects.create(
                            student=student,
                            exam=exam,
                            subject=subject,
                            marks_obtained=marks,
                            remarks=random.choice(['Excellent', 'Good', 'Satisfactory', 'Needs Improvement', ''])
                        )
                        created_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} marksheet entries')
        )