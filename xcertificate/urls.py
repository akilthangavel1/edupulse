from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.certificate_dashboard, name='certificate_dashboard'),
    
    # Certificate CRUD
    path('list/', views.certificate_list, name='certificate_list'),
    path('create/', views.certificate_create, name='certificate_create'),
    path('<int:pk>/', views.certificate_detail, name='certificate_detail'),
    path('<int:pk>/edit/', views.certificate_edit, name='certificate_edit'),
    path('<int:pk>/delete/', views.certificate_delete, name='certificate_delete'),
    
    # Bulk Recording
    path('bulk-create/', views.bulk_certificate_create, name='bulk_certificate_create'),
]
