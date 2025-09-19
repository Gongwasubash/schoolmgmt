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
    path('search-student/', views.search_student_page, name='search_student'),
    path('pay-student/<int:student_id>/', views.pay_student, name='pay_student'),
    path('api/search-student/', views.search_student_api, name='search_student_api'),
    path('events/', views.events, name='events'),
    path('edit-student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('download-csv/', views.download_csv, name='download_csv'),
    path('download-template/', views.download_template, name='download_template'),
    path('upload-csv/', views.upload_csv, name='upload_csv'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('bulk-delete-students/', views.bulk_delete_students, name='bulk_delete_students'),
    path('api/fee-structure/<str:class_name>/', views.get_fee_structure, name='get_fee_structure'),
    path('submit-payment/', views.submit_payment, name='submit_payment'),
    path('fee-receipt-book/', views.fee_receipt_book, name='fee_receipt_book'),
    path('api/fee-receipt-book/', views.fee_receipt_book_api, name='fee_receipt_book_api'),
    path('admission-fee-table/', views.admission_fee_table, name='admission_fee_table'),
    path('api/student-payments/<int:student_id>/', views.student_payments_api, name='student_payments_api'),
    path('student-payments/<int:student_id>/', views.student_payments, name='student_payments'),
    path('fee-receipt/<int:payment_id>/', views.fee_receipt, name='fee_receipt'),
    path('receipt-pdf/<int:payment_id>/', views.generate_receipt_pdf, name='generate_receipt_pdf'),
    path('credit-slip/<int:student_id>/', views.credit_slip, name='credit_slip'),
    path('bulk-print-receipts/', views.bulk_print_receipts, name='bulk_print_receipts'),
    path('admin/', admin.site.urls),
]
