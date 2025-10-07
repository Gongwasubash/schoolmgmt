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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views, views_admin, views_user, student_views
from . import registration_views, festival_views, festival_api, attendance_views, school_attendance_views, student_attendance_views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('students/', views.students, name='students'),
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),
    path('student-detail/<int:student_id>/', student_views.student_detail_with_filters, name='student_detail_with_filters'),
    path('student-admission/', views.student_admission, name='student_admission'),
    path('studentlist/', views.studentlist, name='studentlist'),
    path('teachers/', views.teachers, name='teachers'),
    path('teacher/<int:teacher_id>/view/', views.teacher_view, name='teacher_view'),
    path('teacher/<int:teacher_id>/edit/', views.teacher_edit, name='teacher_edit'),
    path('teacher/<int:teacher_id>/assign/', views.teacher_assignment, name='teacher_assignment'),
    path('teacher/<int:teacher_id>/delete/', views.teacher_delete, name='teacher_delete'),
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
    path('fee-pending-report/', views.fee_pending_report, name='fee_pending_report'),
    path('create-exam/', views.create_exam, name='create_exam'),
    path('create-subject/', views.create_subject, name='create_subject'),
    path('edit-subject/', views.edit_subject, name='edit_subject'),
    path('delete-subject/', views.delete_subject, name='delete_subject'),
    path('enter-marks/', views.enter_marks, name='enter_marks'),
    path('update-subject-class/', views.update_subject_class, name='update_subject_class'),
    path('delete-exam/', views.delete_exam, name='delete_exam'),
    path('generate-results/', views.generate_results, name='generate_results'),
    path('bulk-edit-subjects/', views.bulk_edit_subjects, name='bulk_edit_subjects'),
    path('student-marksheet/<int:student_id>/<int:exam_id>/', views.student_marksheet, name='student_marksheet'),
    path('marksheet-system/', views.marksheet_system, name='marksheet_system'),
    path('marksheet-new/', views.marksheet_new, name='marksheet_new'),
    path('marksheet-advanced/', views.marksheet_advanced, name='marksheet_advanced'),
    path('api/subjects-by-class/<str:class_name>/', views.subjects_by_class_api, name='subjects_by_class_api'),
    path('api/subjects-by-class/<str:class_name>/', views.api_subjects_by_class, name='api_subjects_by_class'),
    path('api/marksheet-data/<int:exam_id>/<int:subject_id>/', views.marksheet_data_api, name='marksheet_data_api'),
    path('api/save-marksheet/', views.save_marksheet_api, name='save_marksheet_api'),
    path('api/populate-all-marksheet-data/', views.populate_all_marksheet_data, name='populate_all_marksheet_data'),
    path('api/auto-populate-exam-marks/<int:exam_id>/', views.auto_populate_exam_marks, name='auto_populate_exam_marks'),
    path('api/student-marksheet-data/<int:student_id>/', views.get_student_marksheet_data, name='get_student_marksheet_data'),
    path('generate-class-marksheets/<int:exam_id>/', views.generate_class_marksheets, name='generate_class_marksheets'),
    path('generate-class-marksheets-print/<int:exam_id>/', views.generate_class_marksheets_new_tab, name='generate_class_marksheets_print'),
    path('generate-class-marksheets-see-style/<int:exam_id>/', views.generate_class_marksheets_see_style, name='generate_class_marksheets_see_style'),
    path('generate-class-marksheets-print-see-style/<int:exam_id>/', views.generate_class_marksheets_print_see_style, name='generate_class_marksheets_print_see_style'),
    path('generate-sarathi-pathshala-marksheets/<int:exam_id>/', views.generate_sarathi_pathshala_marksheets, name='generate_sarathi_pathshala_marksheets'),
    path('generate-sarathi-pathshala-see-marksheets/<int:exam_id>/', views.generate_sarathi_pathshala_see_marksheets, name='generate_sarathi_pathshala_see_marksheets'),
    path('student-result/<int:student_id>/', views.generate_student_result, name='student_result'),
    path('create-session/', views.create_session, name='create_session'),
    path('set-active-session/', views.set_active_session, name='set_active_session'),
    path('api/sessions/', views.get_sessions_api, name='get_sessions_api'),
    path('api/students-by-session/<str:session_name>/', views.students_by_session_api, name='students_by_session_api'),
    path('assign-sessions/', views.assign_sessions_to_students, name='assign_sessions'),
    path('api/save-student-marks/', views.save_student_marks, name='save_student_marks'),
    path('grade-sheet-certificate/', views.grade_sheet_certificate, name='grade_sheet_certificate'),
    path('grade-sheet-certificate-populated/', views.populate_grade_sheet_certificate, name='grade_sheet_certificate_populated'),
    path('student-marksheet-finder/', views.student_marksheet_finder, name='student_marksheet_finder'),
    path('student_attendance_dashboard/', views.student_attendance_dashboard, name='student_attendance_dashboard'),
    path('student-attendance-detail/<int:student_id>/', student_attendance_views.student_attendance_detail, name='student_attendance_detail'),
    path('api/save-attendance/', views.save_attendance, name='save_attendance'),
    path('api/bulk-save-attendance/', views.bulk_save_attendance, name='bulk_save_attendance'),
    path('api/delete-attendance/', views.delete_attendance, name='delete_attendance'),
    path('api/load-attendance/', views.load_attendance, name='load_attendance'),
    path('api/get-attendance/', views.get_attendance_api, name='get_attendance_api'),
    path('api/attendance-summary/<int:student_id>/', views.get_attendance_summary, name='get_attendance_summary'),
    path('attendance-report/', views.attendance_report, name='attendance_report'),
    # Nepali Date API endpoints
    path('api/nepali-date/', views.get_nepali_date_api, name='get_nepali_date_api'),
    path('api/convert-date/', views.convert_date_api, name='convert_date_api'),
    path('api/nepali-sessions/', views.get_nepali_sessions_api, name='get_nepali_sessions_api'),
    path('print-bill/', views.print_bill, name='print_bill'),
    path('student-daily-exp/', views.student_daily_exp, name='student_daily_exp'),
    path('api/add-student-expense/', views.add_student_expense, name='add_student_expense'),
    path('api/delete-student-expense/', views.delete_student_expense, name='delete_student_expense'),
    path('api/student-expenses/<int:student_id>/', views.get_student_expenses_api, name='get_student_expenses_api'),
    path('api/class-expenses/<str:class_name>/', views.get_class_expenses_api, name='get_class_expenses_api'),
    path('api/todays-all-expenses/', views.get_todays_all_expenses_api, name='get_todays_all_expenses_api'),
    path('collection-dashboard/', views.collection_dashboard, name='collection_dashboard'),
    path('collection-details/<str:period>/', views.collection_details, name='collection_details'),
    path('weekly-collection-details/', views.weekly_collection_details, name='weekly_collection_details'),
    path('monthly-collection-details/', views.monthly_collection_details, name='monthly_collection_details'),
    path('yearly-collection-details/', views.yearly_collection_details, name='yearly_collection_details'),
    path('school-settings/', views.school_settings, name='school_settings'),
    path('website-settings/', views.website_settings, name='website_settings'),
    path('school-settings-test/', views.school_settings_test, name='school_settings_test'),
    path('id-creation/', views.id_creation, name='id_creation'),
    path('photo-management/', views.photo_management, name='photo_management'),
    path('photo-gallery/', views.photo_gallery, name='photo_gallery'),
    path('api/assign-photo/', views.assign_photo, name='assign_photo'),
    path('api/remove-photo/', views.remove_photo, name='remove_photo'),
    path('generate-id/', views.generate_id, name='generate_id'),
    path('print-id-cards/', views.print_id_cards, name='print_id_cards'),
    path('whatsapp-balance/', views.whatsapp_balance, name='whatsapp_balance'),
    path('send-fee-email/', views.send_fee_email, name='send_fee_email'),
    path('api/student-fee-history/<int:student_id>/', student_views.student_fee_history_api, name='student_fee_history_api'),
    path('fee-payment-report-dashboard/', views.fee_payment_report_dashboard, name='fee_payment_report_dashboard'),
    path('api/update-enquiry-status/', views.update_enquiry_status_api, name='update_enquiry_status_api'),
    path('api/update-registration-status/', views.update_registration_status_api, name='update_registration_status_api'),
    path('api/delete-registration/', views.delete_registration_api, name='delete_registration_api'),
    path('api/filter-enquiries/', views.filter_enquiries_api, name='filter_enquiries_api'),
    path('public-registration/', registration_views.public_registration, name='public_registration'),
    path('application-status/<int:registration_id>/', registration_views.application_status, name='application_status'),
    path('api/approve-registration/', registration_views.approve_registration, name='approve_registration'),
    path('api/register-student/', views.register_student_api, name='register_student_api'),
    path('login/', views_admin.admin_login_view, name='admin_login'),
    path('logout/', views_admin.admin_logout, name='admin_logout'),
    path('contact/', views.contact, name='contact'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('pending-enquiry/', views.pending_enquiry, name='pending_enquiry'),
    path('blog/', views.blog_list, name='blog_redirect'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('test-enquiry-status/', views.test_enquiry_status, name='test_enquiry_status'),
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path('auth/logout/', views_user.student_logout, name='auth_logout_redirect'),
    
    # Admin Login URLs
    path('admin-login/', views_admin.admin_login_view, name='admin_login_view'),
    path('admin-dashboard/', views_admin.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views_admin.admin_logout, name='admin_logout_view'),
    path('user-management/', views_admin.user_management, name='user_management'),
    path('create-user/', views_admin.create_user, name='create_user'),
    path('admin/delete-user/<int:user_id>/', views_admin.delete_user, name='delete_user'),
    path('admin/enable-all-permissions/<int:user_id>/', views_admin.enable_all_permissions, name='enable_all_permissions'),
    path('edit-user/<int:user_id>/', views_admin.edit_user, name='edit_user'),
    
    # User Dashboard URLs
    path('user-login/', views_user.user_login_view, name='user_login'),
    path('user-dashboard/', views_user.user_dashboard, name='user_dashboard'),
    path('user-logout/', views_user.user_logout, name='user_logout'),
    
    # Student Login URLs
    path('student-login/', views_user.student_login_view, name='student_login'),
    path('student-dashboard/', views_user.student_dashboard, name='student_dashboard'),
    path('student-logout/', views_user.student_logout, name='student_logout'),
    path('google-login/', views_user.google_oauth_redirect, name='google_login'),
    path('user-profile/', views_user.user_profile, name='user_profile'),
    path('student-performance/<int:student_id>/', views_user.student_performance, name='student_performance'),
    path('student-attendance/<int:student_id>/', views_user.student_attendance, name='student_attendance'),
    path('student-fees/<int:student_id>/', views_user.student_fees, name='student_fees'),
    path('school-calendar/', views.school_calendar, name='school_calendar'),
    path('public-school-calendar/', views.public_school_calendar, name='public_school_calendar'),
    path('get-calendar-data/', views.get_calendar_data_api, name='get_calendar_data_api'),
    path('api/add-holiday/', views.add_holiday_api, name='add_holiday_api'),
    path('api/edit-holiday/', views.edit_holiday_api, name='edit_holiday_api'),
    path('api/delete-holiday/', views.delete_holiday_api, name='delete_holiday_api'),
    path('api/nepali-calendar-events/', views.get_nepali_calendar_events_api, name='get_nepali_calendar_events_api'),
    path('api/send-whatsapp-attendance/', views.send_whatsapp_attendance, name='send_whatsapp_attendance'),
    
    # Festival API endpoints
    path('api/festivals/', festival_views.festivals_view, name='festivals_api'),
    path('api/populate-festivals/', festival_views.populate_festivals_from_api, name='populate_festivals_api'),
    path('api/festivals/2082/', festival_api.festivals_2082_api, name='festivals_2082_api'),
    
    # Attendance URLs
    path('school-attendance-calendar/', attendance_views.school_attendance_calendar, name='school_attendance_calendar'),
    path('attendance/date/<str:date_str>/', attendance_views.attendance_by_date, name='attendance_by_date'),
    path('api/mark-attendance/', attendance_views.mark_attendance_api, name='mark_attendance_api'),
    
    # School Attendance Model URLs
    path('school-attendance-dates/', school_attendance_views.school_attendance_dates, name='school_attendance_dates'),
    path('school-attendance/records/<str:date_str>/', school_attendance_views.school_attendance_records, name='school_attendance_records'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
