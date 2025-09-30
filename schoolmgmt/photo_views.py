from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student
import json
import os
from django.conf import settings

def photo_management(request):
    students = Student.objects.all().order_by('name')
    return render(request, 'photo_management.html', {'students': students})

@csrf_exempt
def assign_photo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student = get_object_or_404(Student, id=data['student_id'])
            
            # For now, just store the photo URL reference
            # In production, you'd copy the file to student_photos
            photo_url = data['photo_url']
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@csrf_exempt
def remove_photo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student = get_object_or_404(Student, id=data['student_id'])
            
            if student.photo:
                student.photo.delete()
                student.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def photo_gallery(request):
    return render(request, 'photo_gallery.html')