from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.marks_dashboard, name='marks_dashboard'),
    
    # Subject URLs
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/create/', views.subject_create, name='subject_create'),
    path('subjects/<int:pk>/', views.subject_detail, name='subject_detail'),
    path('subjects/<int:pk>/edit/', views.subject_edit, name='subject_edit'),
    
    # Mark URLs
    path('marks/', views.mark_list, name='mark_list'),
    path('marks/create/', views.mark_create, name='mark_create'),
    path('marks/<int:pk>/', views.mark_detail, name='mark_detail'),
    path('marks/<int:pk>/edit/', views.mark_edit, name='mark_edit'),
    path('marks/<int:pk>/resend-email/', views.mark_resend_email, name='mark_resend_email'),
    path('marks/bulk-entry/', views.bulk_mark_entry, name='bulk_mark_entry'),
    
    # Assessment Type URLs
    path('assessment-types/', views.assessment_type_list, name='assessment_type_list'),
    path('assessment-types/create/', views.assessment_type_create, name='assessment_type_create'),
    path('assessment-types/<int:pk>/edit/', views.assessment_type_edit, name='assessment_type_edit'),
    
    # Grade Scale URLs
    path('grade-scales/', views.grade_scale_list, name='grade_scale_list'),
    path('grade-scales/create/', views.grade_scale_create, name='grade_scale_create'),
    path('grade-scales/<int:pk>/edit/', views.grade_scale_edit, name='grade_scale_edit'),
    
    # Reports
    path('reports/student/', views.student_report, name='student_report'),
    
    # AJAX URLs
    path('ajax/subjects-by-course/', views.get_subjects_by_course, name='get_subjects_by_course'),
    path('ajax/students-by-course/', views.get_students_by_course, name='get_students_by_course'),
    path('ajax/marks/<int:pk>/status/', views.mark_status_update, name='mark_status_update'),
    
    # Utility URLs
    path('utilities/calculate-summaries/', views.calculate_grade_summaries, name='calculate_grade_summaries'),
] 