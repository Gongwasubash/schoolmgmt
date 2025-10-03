from django import forms
from .models import Teacher, Subject, TeacherClassSubject

class TeacherAssignmentForm(forms.Form):
    """Form for assigning multiple classes and subjects to a teacher"""
    
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
    
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        
        # Create dynamic fields for each class
        for class_name, class_display in self.CLASS_CHOICES:
            # Get subjects for this class
            subjects = Subject.objects.filter(class_name=class_name)
            if subjects.exists():
                field_name = f'class_{class_name.lower()}_subjects'
                self.fields[field_name] = forms.ModelMultipleChoiceField(
                    queryset=subjects,
                    widget=forms.CheckboxSelectMultiple,
                    required=False,
                    label=f'{class_display} - Subjects'
                )
        
        # Pre-populate with existing assignments if teacher is provided
        if teacher:
            existing_assignments = TeacherClassSubject.objects.filter(
                teacher=teacher, is_active=True
            ).select_related('subject')
            
            for assignment in existing_assignments:
                field_name = f'class_{assignment.class_name.lower()}_subjects'
                if field_name in self.fields:
                    current_values = self.fields[field_name].initial or []
                    if isinstance(current_values, list):
                        current_values.append(assignment.subject)
                    else:
                        current_values = [assignment.subject]
                    self.fields[field_name].initial = current_values
    
    def get_assignments_data(self):
        """Convert form data to assignments format"""
        assignments_data = []
        
        for class_name, class_display in self.CLASS_CHOICES:
            field_name = f'class_{class_name.lower()}_subjects'
            if field_name in self.cleaned_data:
                subjects = self.cleaned_data[field_name]
                if subjects:
                    subject_ids = [subject.id for subject in subjects]
                    assignments_data.append({
                        'class_name': class_name,
                        'subject_ids': subject_ids
                    })
        
        return assignments_data