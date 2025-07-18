from django.urls import path
from . import views

app_name = 'xkit'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Material Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    
    # Suppliers
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/create/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/', views.supplier_detail, name='supplier_detail'),
    path('suppliers/<int:pk>/edit/', views.supplier_edit, name='supplier_edit'),
    
    # Materials
    path('materials/', views.material_list, name='material_list'),
    path('materials/create/', views.material_create, name='material_create'),
    path('materials/<int:pk>/', views.material_detail, name='material_detail'),
    path('materials/<int:pk>/edit/', views.material_edit, name='material_edit'),
    path('materials/<int:pk>/delete/', views.material_delete, name='material_delete'),
    
    # Material Kits
    path('kits/', views.kit_list, name='kit_list'),
    path('kits/create/', views.kit_create, name='kit_create'),
    path('kits/<int:pk>/', views.kit_detail, name='kit_detail'),
    path('kits/<int:pk>/edit/', views.kit_edit, name='kit_edit'),
    path('kits/<int:pk>/delete/', views.kit_delete, name='kit_delete'),
    
    # Kit Materials (adding materials to kits)
    path('kits/<int:kit_id>/materials/', views.kit_materials, name='kit_materials'),
    path('kits/<int:kit_id>/materials/add/', views.add_material_to_kit, name='add_material_to_kit'),
    path('kits/<int:kit_id>/materials/<int:material_id>/remove/', views.remove_material_from_kit, name='remove_material_from_kit'),
    
    # Stock Management
    path('stock/', views.stock_dashboard, name='stock_dashboard'),
    path('stock/movements/', views.stock_movement_list, name='stock_movement_list'),
    path('stock/movements/create/', views.stock_movement_create, name='stock_movement_create'),
    path('materials/<int:material_id>/adjust-stock/', views.adjust_material_stock, name='adjust_material_stock'),
    
    # Kit Assembly
    path('assembly/', views.assembly_dashboard, name='assembly_dashboard'),
    path('assembly/logs/', views.assembly_log_list, name='assembly_log_list'),
    path('assembly/create/', views.assembly_create, name='assembly_create'),
    path('assembly/<int:pk>/', views.assembly_detail, name='assembly_detail'),
    path('kits/<int:kit_id>/assemble/', views.assemble_kit, name='assemble_kit'),
    
    # Reports
    path('reports/', views.reports_dashboard, name='reports_dashboard'),
    path('reports/inventory/', views.inventory_report, name='inventory_report'),
    path('reports/low-stock/', views.low_stock_report, name='low_stock_report'),
    path('reports/kit-costs/', views.kit_costs_report, name='kit_costs_report'),
    
    # Integration with Course Fee Kit
    path('sync/', views.sync_dashboard, name='sync_dashboard'),
    path('kits/<int:kit_id>/sync-coursefee/', views.sync_with_coursefee, name='sync_with_coursefee'),
    
    # AJAX endpoints
    path('api/materials/search/', views.api_material_search, name='api_material_search'),
    path('api/kit/<int:kit_id>/can-assemble/', views.api_kit_can_assemble, name='api_kit_can_assemble'),
    path('api/materials/low-stock/', views.api_low_stock_materials, name='api_low_stock_materials'),
] 