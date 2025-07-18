from django.urls import path
from . import views

app_name = 'xtransport'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Vendor Management
    path('vendors/', views.vendor_list, name='vendor_list'),
    path('vendors/create/', views.vendor_create, name='vendor_create'),
    path('vendors/<int:pk>/', views.vendor_detail, name='vendor_detail'),
    path('vendors/<int:pk>/edit/', views.vendor_edit, name='vendor_edit'),
    path('vendors/<int:pk>/delete/', views.vendor_delete, name='vendor_delete'),
    
    # Vendor Requests & Approval
    path('vendor-requests/', views.vendor_request_list, name='vendor_request_list'),
    path('vendor-requests/create/', views.vendor_request_create, name='vendor_request_create'),
    path('vendor-requests/<int:pk>/', views.vendor_request_detail, name='vendor_request_detail'),
    path('vendor-requests/<int:pk>/approve/', views.vendor_request_approve, name='vendor_request_approve'),
    path('vendor-requests/<int:pk>/reject/', views.vendor_request_reject, name='vendor_request_reject'),
    
    # Student Transport Assignments
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/create/', views.assignment_create, name='assignment_create'),
    path('assignments/<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('assignments/<int:pk>/edit/', views.assignment_edit, name='assignment_edit'),
    path('assignments/<int:pk>/delete/', views.assignment_delete, name='assignment_delete'),
    
    # Vendor Payments
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/create/', views.payment_create, name='payment_create'),
    path('payments/<int:pk>/', views.payment_detail, name='payment_detail'),
    path('payments/<int:pk>/edit/', views.payment_edit, name='payment_edit'),
    path('payments/<int:pk>/approve/', views.payment_approve, name='payment_approve'),
    
    # Monthly Payment Generation
    path('payment-generation/', views.payment_generation_list, name='payment_generation_list'),
    path('payment-generation/create/', views.payment_generation_create, name='payment_generation_create'),
    path('payment-generation/<int:pk>/', views.payment_generation_detail, name='payment_generation_detail'),
    path('payment-generation/<int:pk>/generate/', views.payment_generation_generate, name='payment_generation_generate'),
    
    # Vendor Ratings
    path('ratings/', views.rating_list, name='rating_list'),
    path('ratings/create/', views.rating_create, name='rating_create'),
    path('vendors/<int:vendor_id>/rate/', views.vendor_rate, name='vendor_rate'),
    
    # Reports
    path('reports/', views.reports_dashboard, name='reports_dashboard'),
    path('reports/vendor-payments/', views.vendor_payments_report, name='vendor_payments_report'),
    path('reports/student-transport/', views.student_transport_report, name='student_transport_report'),
    
    # AJAX endpoints
    path('api/vendor/<int:vendor_id>/assignments/', views.api_vendor_assignments, name='api_vendor_assignments'),
    path('api/student/<int:student_id>/transport-history/', views.api_student_transport_history, name='api_student_transport_history'),
] 