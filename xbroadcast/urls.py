from django.urls import path
from . import views

app_name = 'xbroadcast'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Broadcast Templates
    path('templates/', views.template_list, name='template_list'),
    path('templates/create/', views.template_create, name='template_create'),
    path('templates/<int:pk>/', views.template_detail, name='template_detail'),
    path('templates/<int:pk>/edit/', views.template_edit, name='template_edit'),
    path('templates/<int:pk>/delete/', views.template_delete, name='template_delete'),
    
    # Broadcasts
    path('broadcasts/', views.broadcast_list, name='broadcast_list'),
    path('broadcasts/create/', views.broadcast_create, name='broadcast_create'),
    path('broadcasts/<int:pk>/', views.broadcast_detail, name='broadcast_detail'),
    path('broadcasts/<int:pk>/edit/', views.broadcast_edit, name='broadcast_edit'),
    path('broadcasts/<int:pk>/send/', views.broadcast_send, name='broadcast_send'),
    path('broadcasts/<int:pk>/cancel/', views.broadcast_cancel, name='broadcast_cancel'),
    
    # General Broadcasts
    path('general/', views.general_broadcast, name='general_broadcast'),
    path('general/new-batch/', views.new_batch_broadcast, name='new_batch_broadcast'),
    path('general/holiday/', views.holiday_broadcast, name='holiday_broadcast'),
    
    # Specific Broadcasts
    path('specific/', views.specific_broadcast, name='specific_broadcast'),
    path('specific/batch/', views.batch_broadcast, name='batch_broadcast'),
    path('specific/course/', views.course_broadcast, name='course_broadcast'),
    path('specific/fee-reminder/', views.fee_reminder_broadcast, name='fee_reminder_broadcast'),
    
    # Lead Management
    path('leads/', views.lead_list, name='lead_list'),
    path('leads/create/', views.lead_create, name='lead_create'),
    path('leads/<int:pk>/', views.lead_detail, name='lead_detail'),
    path('leads/<int:pk>/edit/', views.lead_edit, name='lead_edit'),
    path('leads/<int:pk>/delete/', views.lead_delete, name='lead_delete'),
    
    # Lead Activities
    path('leads/<int:lead_id>/activities/', views.lead_activities, name='lead_activities'),
    path('leads/<int:lead_id>/activities/add/', views.add_lead_activity, name='add_lead_activity'),
    path('activities/<int:pk>/edit/', views.edit_lead_activity, name='edit_lead_activity'),
    
    # Lead Scoring
    path('leads/<int:lead_id>/score/', views.lead_score, name='lead_score'),
    path('leads/<int:lead_id>/score/calculate/', views.calculate_lead_score, name='calculate_lead_score'),
    
    # Communication Logs
    path('communications/', views.communication_log_list, name='communication_log_list'),
    path('communications/<int:pk>/', views.communication_log_detail, name='communication_log_detail'),
    
    # Reports and Analytics
    path('reports/', views.reports_dashboard, name='reports_dashboard'),
    path('reports/broadcast-performance/', views.broadcast_performance_report, name='broadcast_performance_report'),
    path('reports/lead-conversion/', views.lead_conversion_report, name='lead_conversion_report'),
    path('reports/communication-costs/', views.communication_costs_report, name='communication_costs_report'),
    
    # AJAX endpoints
    path('api/leads/search/', views.api_lead_search, name='api_lead_search'),
    path('api/broadcast/<int:broadcast_id>/recipients/', views.api_broadcast_recipients, name='api_broadcast_recipients'),
    path('api/templates/<int:template_id>/content/', views.api_template_content, name='api_template_content'),
    path('api/leads/<int:lead_id>/quick-update/', views.api_lead_quick_update, name='api_lead_quick_update'),
] 