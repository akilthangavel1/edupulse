from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_dashboard, name='student_dashboard'),
    path('students/', views.student_list, name='student_list'),
    path('students/drafts/', views.student_draft_list, name='student_drafts'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_update, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('students/export/', views.student_export, name='student_export'),
    path('old-students/', views.old_student_list, name='old_student_list'),
    path('old-students/create/', views.old_student_create, name='old_student_create'),
    path('old-students/<int:pk>/', views.old_student_detail, name='old_student_detail'),
    path('old-students/<int:pk>/edit/', views.old_student_update, name='old_student_edit'),
    path('old-students/<int:pk>/delete/', views.old_student_delete, name='old_student_delete'),
    
    # Attendance URLs
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/dashboard/', views.attendance_dashboard, name='attendance_dashboard'),
    path('attendance/create/', views.attendance_create, name='attendance_create'),
    path('attendance/bulk/', views.attendance_bulk_create, name='attendance_bulk_create'),
    path('attendance/<int:pk>/', views.attendance_detail, name='attendance_detail'),
    path('attendance/<int:pk>/edit/', views.attendance_update, name='attendance_edit'),
    path('attendance/<int:pk>/delete/', views.attendance_delete, name='attendance_delete'),
    path('attendance/report/', views.attendance_report, name='attendance_report'),
]