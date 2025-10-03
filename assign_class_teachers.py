#!/usr/bin/env python
import os
import sys
import django
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolmgmt.settings')
django.setup()

from schoolmgmt.models import Teacher, TeacherClassSubject

def assign_class_teachers():
    classes = ['Nursery', 'LKG', 'UKG', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve']
    
    for class_name in classes:
        # Get teachers who teach in this class
        teachers_in_class = Teacher.objects.filter(
            class_subjects__class_name=class_name,
            class_subjects__is_active=True,
            is_active=True
        ).distinct()
        
        if teachers_in_class.exists():
            # Check if any teacher is already assigned as class teacher for this class
            current_class_teacher = Teacher.objects.filter(class_teacher_for=class_name).first()
            
            if not current_class_teacher:
                # Assign a random teacher from those who teach in this class
                selected_teacher = random.choice(teachers_in_class)
                selected_teacher.class_teacher_for = class_name
                selected_teacher.save()
                print(f"Assigned {selected_teacher.name} as class teacher for {class_name}")
            else:
                print(f"{current_class_teacher.name} is already class teacher for {class_name}")
        else:
            print(f"No teachers found for class {class_name}")

if __name__ == "__main__":
    assign_class_teachers()