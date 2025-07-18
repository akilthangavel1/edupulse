from django.urls import path
from . import views

app_name = 'xadmin'

urlpatterns = [
    # System Dashboard
    path('', views.system_dashboard, name='dashboard'),
    
    # User and Role Management
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:pk>/activate/', views.user_activate, name='user_activate'),
    path('users/<int:pk>/deactivate/', views.user_deactivate, name='user_deactivate'),
    
    # System Roles
    path('roles/', views.role_list, name='role_list'),
    path('roles/create/', views.role_create, name='role_create'),
    path('roles/<int:pk>/', views.role_detail, name='role_detail'),
    path('roles/<int:pk>/edit/', views.role_edit, name='role_edit'),
    
    # User Profiles
    path('profiles/', views.profile_list, name='profile_list'),
    path('profiles/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('profiles/<int:pk>/edit/', views.profile_edit, name='profile_edit'),
    
    # Audit Logs
    path('audit/', views.audit_log_list, name='audit_log_list'),
    path('audit/<int:pk>/', views.audit_log_detail, name='audit_log_detail'),
    path('audit/export/', views.audit_log_export, name='audit_log_export'),
    
    # Security Logs
    path('security/', views.security_log_list, name='security_log_list'),
    path('security/<int:pk>/', views.security_log_detail, name='security_log_detail'),
    path('security/<int:pk>/investigate/', views.security_log_investigate, name='security_log_investigate'),
    path('security/<int:pk>/resolve/', views.security_log_resolve, name='security_log_resolve'),
    
    # System Configuration
    path('config/', views.config_list, name='config_list'),
    path('config/<str:config_type>/', views.config_by_type, name='config_by_type'),
    path('config/<int:pk>/edit/', views.config_edit, name='config_edit'),
    
    # Backup Management
    path('backup/', views.backup_dashboard, name='backup_dashboard'),
    path('backup/list/', views.backup_list, name='backup_list'),
    path('backup/create/', views.backup_create, name='backup_create'),
    path('backup/<int:pk>/', views.backup_detail, name='backup_detail'),
    path('backup/<int:pk>/download/', views.backup_download, name='backup_download'),
    path('backup/<int:pk>/delete/', views.backup_delete, name='backup_delete'),
    
    # Restore Management
    path('restore/', views.restore_dashboard, name='restore_dashboard'),
    path('restore/list/', views.restore_list, name='restore_list'),
    path('restore/create/', views.restore_create, name='restore_create'),
    path('restore/<int:pk>/', views.restore_detail, name='restore_detail'),
    path('restore/<int:pk>/approve/', views.restore_approve, name='restore_approve'),
    
    # System Monitoring
    path('monitoring/', views.monitoring_dashboard, name='monitoring_dashboard'),
    path('monitoring/performance/', views.performance_monitoring, name='performance_monitoring'),
    path('monitoring/errors/', views.error_monitoring, name='error_monitoring'),
    
    # Navigation & UI
    path('navigation/', views.navigation_management, name='navigation_management'),
    path('ui/', views.ui_settings, name='ui_settings'),
    
    # Role Testing
    path('testing/', views.role_testing_dashboard, name='role_testing_dashboard'),
    path('testing/admin/', views.test_admin_access, name='test_admin_access'),
    path('testing/staff/', views.test_staff_access, name='test_staff_access'),
    
    # Security Testing
    path('security-testing/', views.security_testing_dashboard, name='security_testing_dashboard'),
    path('security-testing/penetration/', views.penetration_testing, name='penetration_testing'),
    path('security-testing/vulnerability/', views.vulnerability_scan, name='vulnerability_scan'),
    
    # System Health
    path('health/', views.system_health, name='system_health'),
    path('health/database/', views.database_health, name='database_health'),
    path('health/storage/', views.storage_health, name='storage_health'),
    
    # AJAX endpoints
    path('api/system/status/', views.api_system_status, name='api_system_status'),
    path('api/user/<int:user_id>/permissions/', views.api_user_permissions, name='api_user_permissions'),
    path('api/backup/progress/<int:backup_id>/', views.api_backup_progress, name='api_backup_progress'),
    path('api/restore/progress/<int:restore_id>/', views.api_restore_progress, name='api_restore_progress'),
] 