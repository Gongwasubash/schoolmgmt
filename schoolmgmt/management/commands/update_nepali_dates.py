from django.core.management.base import BaseCommand
from schoolmgmt.models import Student, FeePayment, Exam, Session
from schoolmgmt.nepali_calendar import NepaliCalendar


class Command(BaseCommand):
    help = 'Update all Nepali date fields to use English format instead of Devanagari'

    def handle(self, *args, **options):
        self.stdout.write('Starting to update Nepali date fields to English format...')
        
        # Update Student records
        students_updated = 0
        for student in Student.objects.all():
            updated = False
            
            # Update admission date nepali fields
            if student.admission_date:
                nepali_date = NepaliCalendar.english_to_nepali_date(student.admission_date)
                new_admission_date_nepali = NepaliCalendar.format_nepali_date(nepali_date, 'full_en')
                new_admission_date_nepali_short = NepaliCalendar.format_nepali_date(nepali_date, 'short')
                
                if student.admission_date_nepali != new_admission_date_nepali:
                    student.admission_date_nepali = new_admission_date_nepali
                    updated = True
                
                if student.admission_date_nepali_short != new_admission_date_nepali_short:
                    student.admission_date_nepali_short = new_admission_date_nepali_short
                    updated = True
            
            # Update DOB nepali field
            if student.dob:
                nepali_date = NepaliCalendar.english_to_nepali_date(student.dob)
                new_dob_nepali = NepaliCalendar.format_nepali_date(nepali_date, 'short')
                
                if student.dob_nepali != new_dob_nepali:
                    student.dob_nepali = new_dob_nepali
                    updated = True
            
            # Update session nepali field
            if student.admission_date:
                new_session_nepali = NepaliCalendar.get_nepali_session_from_date(student.admission_date)
                if student.session_nepali != new_session_nepali:
                    student.session_nepali = new_session_nepali
                    updated = True
            
            if updated:
                student.save()
                students_updated += 1
        
        self.stdout.write(f'Updated {students_updated} student records')
        
        # Update FeePayment records
        payments_updated = 0
        for payment in FeePayment.objects.all():
            updated = False
            
            if payment.payment_date:
                nepali_date = NepaliCalendar.english_to_nepali_date(payment.payment_date)
                new_payment_date_nepali = NepaliCalendar.format_nepali_date(nepali_date, 'full_en')
                new_payment_date_nepali_short = NepaliCalendar.format_nepali_date(nepali_date, 'short')
                
                if payment.payment_date_nepali != new_payment_date_nepali:
                    payment.payment_date_nepali = new_payment_date_nepali
                    updated = True
                
                if payment.payment_date_nepali_short != new_payment_date_nepali_short:
                    payment.payment_date_nepali_short = new_payment_date_nepali_short
                    updated = True
            
            if updated:
                payment.save()
                payments_updated += 1
        
        self.stdout.write(f'Updated {payments_updated} fee payment records')
        
        # Update Exam records
        exams_updated = 0
        for exam in Exam.objects.all():
            updated = False
            
            if exam.exam_date:
                nepali_date = NepaliCalendar.english_to_nepali_date(exam.exam_date)
                new_exam_date_nepali = NepaliCalendar.format_nepali_date(nepali_date, 'full_en')
                new_exam_date_nepali_short = NepaliCalendar.format_nepali_date(nepali_date, 'short')
                
                if exam.exam_date_nepali != new_exam_date_nepali:
                    exam.exam_date_nepali = new_exam_date_nepali
                    updated = True
                
                if exam.exam_date_nepali_short != new_exam_date_nepali_short:
                    exam.exam_date_nepali_short = new_exam_date_nepali_short
                    updated = True
                
                # Update session nepali field
                new_session_nepali = NepaliCalendar.get_nepali_session_from_date(exam.exam_date)
                if exam.session_nepali != new_session_nepali:
                    exam.session_nepali = new_session_nepali
                    updated = True
            
            if updated:
                exam.save()
                exams_updated += 1
        
        self.stdout.write(f'Updated {exams_updated} exam records')
        
        # Update Session records
        sessions_updated = 0
        for session in Session.objects.all():
            updated = False
            
            if session.start_date:
                nepali_start_date = NepaliCalendar.english_to_nepali_date(session.start_date)
                start_year = nepali_start_date['year']
                new_name_nepali = f"{start_year}-{str(start_year+1)[-2:]}"
                
                if session.name_nepali != new_name_nepali:
                    session.name_nepali = new_name_nepali
                    updated = True
                
                new_start_date_nepali = NepaliCalendar.format_nepali_date(nepali_start_date, 'full_en')
                if session.start_date_nepali != new_start_date_nepali:
                    session.start_date_nepali = new_start_date_nepali
                    updated = True
            
            if session.end_date:
                nepali_end_date = NepaliCalendar.english_to_nepali_date(session.end_date)
                new_end_date_nepali = NepaliCalendar.format_nepali_date(nepali_end_date, 'full_en')
                if session.end_date_nepali != new_end_date_nepali:
                    session.end_date_nepali = new_end_date_nepali
                    updated = True
            
            if updated:
                session.save()
                sessions_updated += 1
        
        self.stdout.write(f'Updated {sessions_updated} session records')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated all Nepali date fields to English format!\n'
                f'Total records updated: {students_updated + payments_updated + exams_updated + sessions_updated}'
            )
        )