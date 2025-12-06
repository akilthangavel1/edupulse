from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'xtransport'

urlpatterns = [
    path('', lambda request: redirect('xtransport:transport_fee_list'), name='transport_home'),
    # Transport Fees Management
    path('fees/', views.transport_fee_list, name='transport_fee_list'),
    path('fees/create/', views.transport_fee_create, name='transport_fee_create'),
    path('fees/<int:pk>/edit/', views.transport_fee_edit, name='transport_fee_edit'),
]