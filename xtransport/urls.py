from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'xtransport'

urlpatterns = [
    path('', lambda request: redirect('xtransport:transport_fee_list'), name='dashboard'),
    # Transport Fees Management
    path('fees/', views.transport_fee_list, name='transport_fee_list'),
    path('fees/create/', views.transport_fee_create, name='transport_fee_create'),
    path('fees/<int:pk>/edit/', views.transport_fee_edit, name='transport_fee_edit'),
    path('fees/<int:pk>/resend-email/', views.transport_fee_resend_email, name='transport_fee_resend_email'),
    path('fees/<int:pk>/receipt/', views.transport_fee_receipt, name='transport_fee_receipt'),
    path('fees/export/', views.transport_fee_export, name='transport_fee_export'),
]