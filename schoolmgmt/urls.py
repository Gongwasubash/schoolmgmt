"""
URL configuration for schoolmgmt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.students, name='students'),
    path('studentlist/', views.studentlist, name='studentlist'),
    path('teachers/', views.teachers, name='teachers'),
    path('classes/', views.classes, name='classes'),
    path('reports/', views.reports, name='reports'),
    path('fees/', views.fees, name='fees'),
    path('pay/', views.pay, name='pay'),
    path('pay-new/', views.pay_new, name='pay_new'),
    path('pay/<int:student_id>/', views.pay_student, name='pay_student'),
    path('events/', views.events, name='events'),
    path('edit-student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('download-csv/', views.download_csv, name='download_csv'),
    path('download-template/', views.download_template, name='download_template'),
    path('upload-csv/', views.upload_csv, name='upload_csv'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('bulk-delete-students/', views.bulk_delete_students, name='bulk_delete_students'),
    path('api/fee-structure/<str:class_name>/', views.get_fee_structure, name='get_fee_structure'),
    path('submit-payment/', views.submit_payment, name='submit_payment'),
    path('admin/', admin.site.urls),
]
