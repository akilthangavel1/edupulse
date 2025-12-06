from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def dashboard(request):
    return render(request, 'base_placeholder.html', {'title': 'Kit Management', 'message': 'Kit management module under development'})

# All placeholder views point to dashboard for now
category_list = category_create = category_detail = category_edit = dashboard
supplier_list = supplier_create = supplier_detail = supplier_edit = dashboard  
material_list = material_create = material_detail = material_edit = material_delete = dashboard
kit_list = kit_create = kit_detail = kit_edit = kit_delete = dashboard
kit_materials = add_material_to_kit = remove_material_from_kit = dashboard
stock_dashboard = stock_movement_list = stock_movement_create = adjust_material_stock = dashboard
assembly_dashboard = assembly_log_list = assembly_create = assembly_detail = assemble_kit = dashboard
reports_dashboard = inventory_report = low_stock_report = kit_costs_report = dashboard
sync_dashboard = sync_with_coursefee = dashboard

@login_required
def api_material_search(request):
    return JsonResponse({'success': True, 'data': []})

@login_required  
def api_kit_can_assemble(request, kit_id):
    return JsonResponse({'success': True, 'can_assemble': 0})

@login_required
def api_low_stock_materials(request):
    return JsonResponse({'success': True, 'data': []})



def dummy():
    pass