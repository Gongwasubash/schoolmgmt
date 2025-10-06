from django.contrib import admin
from .models import StudentAttendance

@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ['date', 'student', 'status', 'marked_by']
    list_filter = ['date', 'status', 'student__student_class']
    search_fields = ['student__name', 'date']
    ordering = ['-date', 'student__name']
    date_hierarchy = 'date'
    
    def changelist_view(self, request, extra_context=None):
        # Group by date in the admin interface
        extra_context = extra_context or {}
        return super().changelist_view(request, extra_context=extra_context)