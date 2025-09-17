from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def students(request):
    return render(request, 'students.html')

def teachers(request):
    return render(request, 'teachers.html')

def classes(request):
    return render(request, 'classes.html')

def reports(request):
    return render(request, 'reports.html')

def fees(request):
    return render(request, 'fees.html')

def events(request):
    return render(request, 'events.html')