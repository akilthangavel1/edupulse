from django.urls import path
from . import views

app_name = 'xbatch'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Batch Management
    path('batches/', views.batch_list, name='batch_list'),
    path('batches/create/', views.batch_create, name='batch_create'),
    path('batches/<int:pk>/', views.batch_detail, name='batch_detail'),
    path('batches/<int:pk>/edit/', views.batch_edit, name='batch_edit'),
    path('batches/<int:pk>/delete/', views.batch_delete, name='batch_delete'),
    
    # Student Management in Batches
    path('batches/<int:batch_id>/students/', views.batch_students, name='batch_students'),
    path('batches/<int:batch_id>/students/add/', views.add_student_to_batch, name='add_student_to_batch'),
    path('batches/<int:batch_id>/students/<int:student_id>/remove/', views.remove_student_from_batch, name='remove_student_from_batch'),
    
    # Batch Transfer
    path('transfers/', views.transfer_list, name='transfer_list'),
    path('transfers/create/', views.transfer_create, name='transfer_create'),
    path('transfers/<int:pk>/', views.transfer_detail, name='transfer_detail'),
    path('transfers/<int:pk>/approve/', views.transfer_approve, name='transfer_approve'),
    path('transfers/<int:pk>/reject/', views.transfer_reject, name='transfer_reject'),
    
    # Faculty Changes
    path('faculty-changes/', views.faculty_change_list, name='faculty_change_list'),
    path('faculty-changes/create/', views.faculty_change_create, name='faculty_change_create'),
    path('faculty-changes/<int:pk>/', views.faculty_change_detail, name='faculty_change_detail'),
    path('faculty-changes/<int:pk>/approve/', views.faculty_change_approve, name='faculty_change_approve'),
    
    # WhatsApp Group Management
    path('whatsapp-groups/', views.whatsapp_group_list, name='whatsapp_group_list'),
    path('whatsapp-groups/create/', views.whatsapp_group_create, name='whatsapp_group_create'),
    path('whatsapp-groups/<int:pk>/', views.whatsapp_group_detail, name='whatsapp_group_detail'),
    path('whatsapp-groups/<int:pk>/sync/', views.whatsapp_group_sync, name='whatsapp_group_sync'),
    
    # AJAX endpoints
    path('api/batch/<int:batch_id>/students/', views.api_batch_students, name='api_batch_students'),
    path('api/transfer/validate/', views.api_validate_transfer, name='api_validate_transfer'),
] 