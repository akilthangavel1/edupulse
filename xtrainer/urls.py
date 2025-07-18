from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.faculty_dashboard, name='faculty_dashboard'),
    
    # Faculty Management URLs
    path('faculty/', views.faculty_list, name='faculty_list'),
    path('faculty/create/', views.faculty_create, name='faculty_create'),
    path('faculty/<int:pk>/', views.faculty_detail, name='faculty_detail'),
    path('faculty/<int:pk>/edit/', views.faculty_edit, name='faculty_edit'),
    
    # Faculty Onboarding URLs
    path('onboarding/', views.faculty_onboarding_list, name='faculty_onboarding_list'),
    path('onboarding/create/', views.faculty_onboarding_create, name='faculty_onboarding_create'),
    path('onboarding/<int:pk>/', views.faculty_onboarding_detail, name='faculty_onboarding_detail'),
    path('onboarding/<int:pk>/approve/', views.faculty_onboarding_approve, name='faculty_onboarding_approve'),
    path('onboarding/<int:pk>/reject/', views.faculty_onboarding_reject, name='faculty_onboarding_reject'),
    
    # Faculty Leave Request URLs
    path('leave-requests/', views.faculty_leave_request_list, name='faculty_leave_request_list'),
    path('leave-requests/create/', views.faculty_leave_request_create, name='faculty_leave_request_create'),
    path('leave-requests/<int:pk>/', views.faculty_leave_request_detail, name='faculty_leave_request_detail'),
    path('leave-requests/<int:pk>/approve/', views.faculty_leave_request_approve, name='faculty_leave_request_approve'),
    path('leave-requests/<int:pk>/reject/', views.faculty_leave_request_reject, name='faculty_leave_request_reject'),
    
    # Backup Schedule URLs
    path('backup-schedules/', views.backup_schedule_list, name='backup_schedule_list'),
    path('backup-schedules/create/', views.backup_schedule_create, name='backup_schedule_create'),
    path('backup-schedules/<int:pk>/', views.backup_schedule_detail, name='backup_schedule_detail'),
    
    # Faculty Payment URLs
    path('payments/', views.faculty_payment_list, name='faculty_payment_list'),
    path('payments/create/', views.faculty_payment_create, name='faculty_payment_create'),
    path('payments/<int:pk>/', views.faculty_payment_detail, name='faculty_payment_detail'),
    
    # Exam Request URLs
    path('exam-requests/', views.exam_request_list, name='exam_request_list'),
    path('exam-requests/create/', views.exam_request_create, name='exam_request_create'),
    path('exam-requests/<int:pk>/', views.exam_request_detail, name='exam_request_detail'),
    path('exam-requests/<int:pk>/approve/', views.exam_request_approve, name='exam_request_approve'),
    
    # Attendance Report URLs
    path('attendance-report/', views.faculty_attendance_report, name='faculty_attendance_report'),
    
    # AJAX URLs
    path('ajax/faculty/<int:faculty_id>/courses/', views.get_faculty_courses, name='get_faculty_courses'),
    path('ajax/course/<int:course_id>/students/', views.get_course_students, name='get_course_students'),
] 