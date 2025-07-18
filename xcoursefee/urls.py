from django.urls import path
from . import views
from . import receipt_views

urlpatterns = [
    # Test URL
    path('test/', views.test_template, name='test_template'),
    
    # Dashboard
    path('', views.coursefee_dashboard, name='coursefee_dashboard'),
    
    # Course URLs
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/<int:pk>/edit/', views.course_update, name='course_edit'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),
    
    # Enrollment URLs
    path('enrollments/', views.enrollment_list, name='enrollment_list'),
    path('enrollments/create/', views.enrollment_create, name='enrollment_create'),
    path('enrollments/<int:pk>/', views.enrollment_detail, name='enrollment_detail'),
    
    # Payment URLs
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/create/', views.payment_create, name='payment_create'),
    path('payments/<int:pk>/', views.payment_detail, name='payment_detail'),
    
    # Invoice URLs
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/create/', views.invoice_create, name='invoice_create'),
    path('invoices/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    
    # Discount URLs
    path('discounts/', views.discount_list, name='discount_list'),
    path('discounts/create/', views.discount_create, name='discount_create'),
    
    # Report URLs
    path('reports/financial/', views.financial_report, name='financial_report'),
    
    # Kit URLs
    path('kits/', views.kit_list, name='kit_list'),
    path('kits/create/', views.kit_create, name='kit_create'),
    path('kits/<int:pk>/', views.kit_detail, name='kit_detail'),
    path('kits/<int:pk>/edit/', views.kit_update, name='kit_edit'),
    path('kits/<int:pk>/delete/', views.kit_delete, name='kit_delete'),
    
    # Course Kit URLs
    path('course-kits/', views.course_kit_list, name='course_kit_list'),
    path('course-kits/create/', views.course_kit_create, name='course_kit_create'),
    path('course-kits/<int:pk>/', views.course_kit_detail, name='course_kit_detail'),
    path('course-kits/<int:pk>/edit/', views.course_kit_update, name='course_kit_edit'),
    path('course-kits/<int:pk>/delete/', views.course_kit_delete, name='course_kit_delete'),
    
    # Kit Fee URLs
    path('kit-fees/', views.kit_fee_list, name='kit_fee_list'),
    path('kit-fees/create/', views.kit_fee_create, name='kit_fee_create'),
    path('kit-fees/<int:pk>/', views.kit_fee_detail, name='kit_fee_detail'),
    path('kit-fees/<int:pk>/edit/', views.kit_fee_update, name='kit_fee_edit'),
    path('kit-fees/<int:pk>/delete/', views.kit_fee_delete, name='kit_fee_delete'),

    
    # AJAX URLs
    path('ajax/course-fees/<int:course_id>/', views.get_course_fees, name='get_course_fees'),
    path('ajax/payment/<int:payment_id>/complete/', views.mark_payment_completed, name='mark_payment_completed'),
    path('ajax/course-kits/<int:course_id>/', views.get_course_kits, name='get_course_kits'),
    path('ajax/kit-fee/<int:kit_fee_id>/mark-paid/', views.mark_kit_fee_paid, name='mark_kit_fee_paid'),
    path('ajax/kit-fee/<int:kit_fee_id>/mark-delivered/', views.mark_kit_delivered, name='mark_kit_delivered'),
    
    # Receipt URLs
    path('receipts/enrollment/<int:enrollment_id>/print/', receipt_views.enrollment_receipt_print, name='enrollment_receipt_print'),
    path('receipts/enrollment/<int:enrollment_id>/pdf/', receipt_views.enrollment_receipt_pdf, name='enrollment_receipt_pdf'),
    path('receipts/enrollment/<int:enrollment_id>/excel/', receipt_views.enrollment_receipt_excel, name='enrollment_receipt_excel'),
    path('receipts/payment/<int:payment_id>/print/', receipt_views.payment_receipt_print, name='payment_receipt_print'),
    path('receipts/payment/<int:payment_id>/pdf/', receipt_views.payment_receipt_pdf, name='payment_receipt_pdf'),
] 