from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def dashboard(request):
    return render(request, 'base_placeholder.html', {'title': 'Broadcast & Leads', 'message': 'Broadcast and lead management module under development'})

# All placeholder views point to dashboard for now  
template_list = template_create = template_detail = template_edit = template_delete = dashboard
broadcast_list = broadcast_create = broadcast_detail = broadcast_edit = broadcast_send = broadcast_cancel = dashboard
general_broadcast = new_batch_broadcast = holiday_broadcast = dashboard
specific_broadcast = batch_broadcast = course_broadcast = fee_reminder_broadcast = dashboard
lead_list = lead_create = lead_detail = lead_edit = lead_delete = dashboard
lead_activities = add_lead_activity = edit_lead_activity = dashboard
lead_score = calculate_lead_score = dashboard
communication_log_list = communication_log_detail = dashboard
reports_dashboard = broadcast_performance_report = lead_conversion_report = communication_costs_report = dashboard

@login_required
def api_lead_search(request):
    return JsonResponse({'success': True, 'data': []})

@login_required
def api_broadcast_recipients(request, broadcast_id):
    return JsonResponse({'success': True, 'data': []})

@login_required  
def api_template_content(request, template_id):
    return JsonResponse({'success': True, 'content': ''})

@login_required
def api_lead_quick_update(request, lead_id):
    return JsonResponse({'success': True, 'message': 'Updated'})
