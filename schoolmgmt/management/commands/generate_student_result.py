from django.core.management.base import BaseCommand
from django.db import models
from schoolmgmt.models import Student, Subject, Exam, Marksheet
import random

class Command(BaseCommand):
    help = 'Generate result for a student with all subjects'

    def add_arguments(self, parser):
        parser.add_argument('--student-id', type=int, help='Student ID to generate result for')
        parser.add_argument('--exam-name', type=str, default='First Term', help='Exam name')
        parser.add_argument('--exam-type', type=str, default='First Term', help='Exam type')

    def handle(self, *args, **options):
        student_id = options.get('student_id')
        exam_name = options.get('exam_name')
        exam_type = options.get('exam_type')

        if student_id:
            try:
                student = Student.objects.get(id=student_id)
            except Student.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Student with ID {student_id} not found'))
                return
        else:
            # Get first student if no ID provided
            student = Student.objects.first()
            if not student:
                self.stdout.write(self.style.ERROR('No students found in database'))
                return

        # Get or create exam for student's class
        exam, created = Exam.objects.get_or_create(
            name=exam_name,
            class_name=student.student_class,
            defaults={
                'exam_type': exam_type,
                'exam_date': '2024-12-01',
                'session': '2024-25'
            }
        )

        if created:
            self.stdout.write(f'Created exam: {exam.name} for class {exam.class_name}')

        # Get all subjects for student's class
        subjects = Subject.objects.filter(class_name=student.student_class)
        
        if not subjects.exists():
            self.stdout.write(self.style.ERROR(f'No subjects found for class {student.student_class}'))
            return

        created_count = 0
        updated_count = 0

        for subject in subjects:
            # Generate random marks (70-95% of max marks for good results)
            min_marks = int(subject.max_marks * 0.70)
            max_marks = int(subject.max_marks * 0.95)
            marks = random.randint(min_marks, max_marks)

            # Create or update marksheet
            marksheet, created = Marksheet.objects.update_or_create(
                student=student,
                exam=exam,
                subject=subject,
                defaults={
                    'marks_obtained': marks,
                    'remarks': 'Good performance' if marks >= subject.pass_marks else 'Needs improvement'
                }
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

            self.stdout.write(f'{subject.name}: {marks}/{subject.max_marks} - {marksheet.grade} ({marksheet.status})')

        # Calculate overall result
        marksheets = Marksheet.objects.filter(student=student, exam=exam)
        total_marks = sum(m.subject.max_marks for m in marksheets)
        obtained_marks = sum(m.marks_obtained for m in marksheets)
        percentage = (obtained_marks / total_marks * 100) if total_marks > 0 else 0
        
        failed_subjects = marksheets.filter(marks_obtained__lt=models.F('subject__pass_marks')).count()
        overall_status = 'Pass' if failed_subjects == 0 else 'Fail'

        self.stdout.write(self.style.SUCCESS(f'\nResult generated for {student.name} (Class: {student.student_class})'))
        self.stdout.write(f'Exam: {exam.name}')
        self.stdout.write(f'Total Marks: {obtained_marks}/{total_marks}')
        self.stdout.write(f'Percentage: {percentage:.2f}%')
        self.stdout.write(f'Overall Status: {overall_status}')
        self.stdout.write(f'Created: {created_count} marksheets, Updated: {updated_count} marksheets')