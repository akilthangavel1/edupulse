from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Count
from .models import TransportFee
from .forms import TransportFeeForm
from xstudent.models import NewStudent
from .email_notifications import send_transport_fee_notification

@login_required
def transport_fee_list(request):
    fees = TransportFee.objects.select_related('student').all()
    
    # Get filter parameters
    student_id = request.GET.get('student')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')
    search = request.GET.get('search')
    
    # Apply filters
    if student_id:
        fees = fees.filter(student_id=student_id)
    
    if from_date:
        fees = fees.filter(payment_date__gte=from_date)
    
    if to_date:
        fees = fees.filter(payment_date__lte=to_date)
    
    if min_amount:
        fees = fees.filter(amount__gte=min_amount)
    
    if max_amount:
        fees = fees.filter(amount__lte=max_amount)
    
    if search:
        fees = fees.filter(
            Q(student__student_name__icontains=search) |
            Q(student__admission_number__icontains=search) |
            Q(notes__icontains=search)
        )
    
    # Calculate statistics
    stats = fees.aggregate(
        total_amount=Sum('amount'),
        total_count=Count('id')
    )
    
    # Get all students for filter dropdown
    students = NewStudent.objects.filter(status='active').order_by('student_name')
    
    context = {
        'fees': fees,
        'students': students,
        'stats': stats,
        'filters': {
            'student': student_id,
            'from_date': from_date,
            'to_date': to_date,
            'min_amount': min_amount,
            'max_amount': max_amount,
            'search': search,
        }
    }
    
    return render(request, 'xtransport/transport_fee_list.html', context)

@login_required
def transport_fee_create(request):
    if request.method == 'POST':
        form = TransportFeeForm(request.POST)
        if form.is_valid():
            transport_fee = form.save()
            
            # Send email notification
            send_email = request.POST.get('send_email', 'on') == 'on'
            email_status = ''
            if send_email:
                if send_transport_fee_notification(transport_fee, action='created'):
                    email_status = ' Email notification sent to parents.'
                else:
                    email_status = ' However, email notification could not be sent.'
            
            # Add success message with print receipt link
            from django.utils.html import format_html
            from django.urls import reverse
            receipt_url = reverse('xtransport:transport_fee_receipt', args=[transport_fee.pk])
            message = format_html(
                'Transport fee entry created successfully!{} <a href="{}" target="_blank" class="btn btn-sm btn-light ms-2"><i class="fas fa-print"></i> Print Receipt</a>',
                email_status,
                receipt_url
            )
            messages.success(request, message)
            
            return redirect('xtransport:transport_fee_list')
    else:
        form = TransportFeeForm()
    return render(request, 'xtransport/transport_fee_form.html', {'form': form})

@login_required
def transport_fee_edit(request, pk):
    fee = get_object_or_404(TransportFee, pk=pk)
    if request.method == 'POST':
        form = TransportFeeForm(request.POST, instance=fee)
        if form.is_valid():
            transport_fee = form.save()
            
            # Send email notification
            send_email = request.POST.get('send_email', 'on') == 'on'
            email_status = ''
            if send_email:
                if send_transport_fee_notification(transport_fee, action='updated'):
                    email_status = ' Email notification sent to parents.'
                else:
                    email_status = ' However, email notification could not be sent.'
            
            # Add success message with print receipt link
            from django.utils.html import format_html
            from django.urls import reverse
            receipt_url = reverse('xtransport:transport_fee_receipt', args=[transport_fee.pk])
            message = format_html(
                'Transport fee entry updated successfully!{} <a href="{}" target="_blank" class="btn btn-sm btn-light ms-2"><i class="fas fa-print"></i> Print Receipt</a>',
                email_status,
                receipt_url
            )
            messages.success(request, message)
            
            return redirect('xtransport:transport_fee_list')
    else:
        form = TransportFeeForm(instance=fee)
    return render(request, 'xtransport/transport_fee_form.html', {'form': form, 'fee': fee})

@login_required
def transport_fee_resend_email(request, pk):
    """Resend email notification for a specific transport fee"""
    fee = get_object_or_404(TransportFee, pk=pk)
    
    if send_transport_fee_notification(fee, action='created'):
        messages.success(request, f'Email notification resent successfully to parents of {fee.student.student_name}!')
    else:
        messages.error(request, 'Failed to send email notification. Please check parent email addresses.')
    
    return redirect('xtransport:transport_fee_list')

@login_required
def transport_fee_receipt(request, pk):
    """Generate printable receipt for transport fee"""
    from django.utils import timezone
    
    fee = get_object_or_404(TransportFee, pk=pk)
    
    context = {
        'fee': fee,
        'receipt_date': timezone.now(),
    }
    
    return render(request, 'xtransport/receipt_print.html', context)

@login_required
def transport_fee_export(request):
    """Export transport fees to CSV"""
    import csv
    from django.http import HttpResponse
    from datetime import datetime
    
    # Get the same filtered queryset
    fees = TransportFee.objects.select_related('student').all()
    
    # Apply the same filters as in list view
    student_id = request.GET.get('student')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')
    search = request.GET.get('search')
    
    if student_id:
        fees = fees.filter(student_id=student_id)
    if from_date:
        fees = fees.filter(payment_date__gte=from_date)
    if to_date:
        fees = fees.filter(payment_date__lte=to_date)
    if min_amount:
        fees = fees.filter(amount__gte=min_amount)
    if max_amount:
        fees = fees.filter(amount__lte=max_amount)
    if search:
        fees = fees.filter(
            Q(student__student_name__icontains=search) |
            Q(student__admission_number__icontains=search) |
            Q(notes__icontains=search)
        )
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    filename = f'transport_fees_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    writer.writerow(['Admission Number', 'Student Name', 'Amount (KWD)', 'Payment Date', 'Notes', 'Created At'])
    
    for fee in fees:
        writer.writerow([
            fee.student.admission_number,
            fee.student.student_name,
            f'{fee.amount:.3f}',
            fee.payment_date.strftime('%Y-%m-%d'),
            fee.notes,
            fee.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    return response
