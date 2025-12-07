from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum, Avg
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from datetime import date, datetime, timedelta
from decimal import Decimal
import csv
import json

from .models import (
    Faculty, FacultyOnboarding, FacultyLeaveRequest, BackupSchedule,
    FacultyAttendance, FacultyPayment, ExamRequest, NotificationLog
)
from .forms import (
    FacultyForm, FacultyOnboardingForm, FacultyLeaveRequestForm, BackupScheduleForm,
    FacultyAttendanceForm, FacultyPaymentForm, ExamRequestForm, 
    FacultySearchForm, AttendanceReportForm
)
from xcoursefee.models import Course, StudentEnrollment
from xstudent.models import NewStudent


@login_required
def faculty_dashboard(request):
    """Dashboard view for faculty management"""
    today = date.today()
    current_month = today.replace(day=1)
    
    # Basic statistics
    stats = {
        'total_faculty': Faculty.objects.filter(status='active').count(),
        'pending_onboarding': FacultyOnboarding.objects.filter(status='pending').count(),
        'pending_leave_requests': FacultyLeaveRequest.objects.filter(status='pending').count(),
        'pending_exam_requests': ExamRequest.objects.filter(status='pending').count(),
    }
    
    # Faculty statistics by employment type
    employment_stats = Faculty.objects.filter(status='active').values('employment_type').annotate(
        count=Count('id')
    ).order_by('employment_type')
    
    # Recent activities
    recent_onboarding = FacultyOnboarding.objects.order_by('-application_date')[:5]
    recent_leave_requests = FacultyLeaveRequest.objects.select_related('faculty').order_by('-request_date')[:5]
    recent_payments = FacultyPayment.objects.select_related('faculty').order_by('-created_at')[:5]
    
    # Upcoming backup schedules
    upcoming_backups = BackupSchedule.objects.filter(
        date__gte=today,
        status__in=['scheduled', 'confirmed']
    ).select_related('backup_faculty', 'original_faculty', 'course').order_by('date', 'start_time')[:5]
    
    # Monthly payment statistics
    monthly_payment_stats = FacultyPayment.objects.filter(
        period_end__gte=current_month,
        status='paid'
    ).aggregate(
        total_amount=Sum('net_amount'),
        total_hours=Sum('total_hours'),
        payment_count=Count('id')
    )
    
    context = {
        'stats': stats,
        'employment_stats': employment_stats,
        'recent_onboarding': recent_onboarding,
        'recent_leave_requests': recent_leave_requests,
        'recent_payments': recent_payments,
        'upcoming_backups': upcoming_backups,
        'monthly_payment_stats': monthly_payment_stats,
    }
    return render(request, 'xtrainer/dashboard.html', context)


# Faculty Management Views
@login_required
def faculty_list(request):
    """List view for faculty with search and pagination"""
    queryset = Faculty.objects.all()
    form = FacultySearchForm(request.GET)
    
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        status = form.cleaned_data.get('status')
        employment_type = form.cleaned_data.get('employment_type')
        qualification = form.cleaned_data.get('qualification')
        can_teach_course = form.cleaned_data.get('can_teach_course')
        
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(faculty_id__icontains=search_query) |
                Q(specialization__icontains=search_query)
            )
        
        if status:
            queryset = queryset.filter(status=status)
        
        if employment_type:
            queryset = queryset.filter(employment_type=employment_type)
            
        if qualification:
            queryset = queryset.filter(qualification=qualification)
            
        if can_teach_course:
            queryset = queryset.filter(can_teach_courses=can_teach_course)
    
    queryset = queryset.order_by('first_name', 'last_name')
    
    # Pagination
    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    faculty_stats = {
        'total_faculty': Faculty.objects.count(),
        'active_faculty': Faculty.objects.filter(status='active').count(),
        'inactive_faculty': Faculty.objects.filter(status='inactive').count(),
        'pending_faculty': Faculty.objects.filter(status='pending').count(),
    }
    
    context = {
        'faculty': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'filter_form': form,
        'faculty_stats': faculty_stats,
    }
    return render(request, 'xtrainer/faculty_list.html', context)


@login_required
def faculty_detail(request, pk):
    """Detail view for faculty"""
    faculty = get_object_or_404(Faculty, pk=pk)
    
    # Get related data
    active_courses = faculty.can_teach_courses.filter(status='active')
    recent_attendance = faculty.attendance_records.order_by('-date')[:10]
    recent_payments = faculty.payments.order_by('-created_at')[:5]
    leave_requests = faculty.leave_requests.order_by('-request_date')[:5]
    backup_schedules = faculty.backup_schedules.filter(date__gte=date.today()).order_by('date', 'start_time')[:5]
    
    # Calculate statistics
    this_month = date.today().replace(day=1)
    monthly_stats = {
        'hours_this_month': faculty.attendance_records.filter(
            date__gte=this_month,
            status='present'
        ).aggregate(total=Sum('attendance_records__hours'))['total'] or 0,
        'payment_this_month': faculty.payments.filter(
            period_end__gte=this_month,
            status='paid'
        ).aggregate(total=Sum('net_amount'))['total'] or Decimal('0.000'),
    }
    
    context = {
        'faculty': faculty,
        'active_courses': active_courses,
        'recent_attendance': recent_attendance,
        'recent_payments': recent_payments,
        'leave_requests': leave_requests,
        'backup_schedules': backup_schedules,
        'monthly_stats': monthly_stats,
    }
    return render(request, 'xtrainer/faculty_detail.html', context)


@login_required
def faculty_create(request):
    """Create view for new faculty"""
    if request.method == 'POST':
        form = FacultyForm(request.POST, request.FILES)
        if form.is_valid():
            faculty = form.save()
            messages.success(request, f'Faculty {faculty.get_full_name()} has been created successfully!')
            return redirect('faculty_detail', pk=faculty.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = FacultyForm()
    
    return render(request, 'xtrainer/faculty_form.html', {'form': form, 'action': 'Create'})


@login_required
def faculty_edit(request, pk):
    """Edit view for faculty"""
    faculty = get_object_or_404(Faculty, pk=pk)
    
    if request.method == 'POST':
        form = FacultyForm(request.POST, request.FILES, instance=faculty)
        if form.is_valid():
            faculty = form.save()
            messages.success(request, f'Faculty {faculty.get_full_name()} has been updated successfully!')
            return redirect('faculty_detail', pk=faculty.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = FacultyForm(instance=faculty)
    
    return render(request, 'xtrainer/faculty_form.html', {'form': form, 'faculty': faculty, 'action': 'Edit'})


# Faculty Onboarding Views
@login_required
def faculty_onboarding_list(request):
    """List view for faculty onboarding requests"""
    queryset = FacultyOnboarding.objects.all()
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    
    queryset = queryset.order_by('-application_date')
    
    # Pagination
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    onboarding_stats = {
        'total_requests': FacultyOnboarding.objects.count(),
        'pending_requests': FacultyOnboarding.objects.filter(status='pending').count(),
        'approved_requests': FacultyOnboarding.objects.filter(status='approved').count(),
        'rejected_requests': FacultyOnboarding.objects.filter(status='rejected').count(),
    }
    
    context = {
        'onboarding_requests': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'status_filter': status_filter,
        'onboarding_stats': onboarding_stats,
        'status_choices': FacultyOnboarding.STATUS_CHOICES,
    }
    return render(request, 'xtrainer/faculty_onboarding_list.html', context)


@login_required
def faculty_onboarding_detail(request, pk):
    """Detail view for faculty onboarding request"""
    onboarding = get_object_or_404(FacultyOnboarding, pk=pk)
    
    context = {
        'onboarding': onboarding,
        'can_approve': onboarding.can_approve(),
        'can_reject': onboarding.can_reject(),
    }
    return render(request, 'xtrainer/faculty_onboarding_detail.html', context)


@login_required
def faculty_onboarding_create(request):
    """Create view for faculty onboarding request"""
    if request.method == 'POST':
        form = FacultyOnboardingForm(request.POST, request.FILES)
        if form.is_valid():
            onboarding = form.save(commit=False)
            # Generate request ID
            today = date.today()
            prefix = f"ONB-{today.year}{today.month:02d}"
            last_request = FacultyOnboarding.objects.filter(
                request_id__startswith=prefix
            ).order_by('-request_id').first()
            
            if last_request:
                last_number = int(last_request.request_id.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            onboarding.request_id = f"{prefix}-{new_number:04d}"
            onboarding.save()
            form.save_m2m()  # Save many-to-many relationships
            
            messages.success(request, f'Onboarding request {onboarding.request_id} has been submitted successfully!')
            return redirect('faculty_onboarding_detail', pk=onboarding.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = FacultyOnboardingForm()
    
    return render(request, 'xtrainer/faculty_onboarding_form.html', {'form': form})


@login_required
@require_http_methods(["POST"])
def faculty_onboarding_approve(request, pk):
    """Approve faculty onboarding request"""
    onboarding = get_object_or_404(FacultyOnboarding, pk=pk)
    
    if not onboarding.can_approve():
        messages.error(request, 'This onboarding request cannot be approved at this time.')
        return redirect('faculty_onboarding_detail', pk=pk)
    
    # Create faculty profile
    faculty = Faculty.objects.create(
        faculty_id=f"FAC-{timezone.now().year}-{Faculty.objects.count() + 1:04d}",
        first_name=onboarding.first_name,
        last_name=onboarding.last_name,
        email=onboarding.email,
        phone=onboarding.phone,
        qualification=onboarding.qualification,
        specialization=onboarding.specialization,
        experience_years=onboarding.experience_years,
        employment_type=onboarding.preferred_employment_type,
        hourly_rate=onboarding.expected_hourly_rate,
        join_date=date.today(),
        status='active',
        # Default address fields - can be updated later
        address_line_1='To be updated',
        city='Kuwait City',
        state='Kuwait',
        country='Kuwait',
        postal_code='00000',
    )
    
    # Set preferred courses
    faculty.can_teach_courses.set(onboarding.preferred_courses.all())
    
    # Update onboarding status
    onboarding.status = 'approved'
    onboarding.approved_by = request.user
    onboarding.approval_date = timezone.now()
    onboarding.created_faculty = faculty
    onboarding.approval_notes = request.POST.get('approval_notes', '')
    onboarding.save()
    
    messages.success(request, f'Onboarding request approved! Faculty profile created for {faculty.get_full_name()}.')
    return redirect('faculty_detail', pk=faculty.pk)


@login_required
@require_http_methods(["POST"])
def faculty_onboarding_reject(request, pk):
    """Reject faculty onboarding request"""
    onboarding = get_object_or_404(FacultyOnboarding, pk=pk)
    
    if not onboarding.can_reject():
        messages.error(request, 'This onboarding request cannot be rejected at this time.')
        return redirect('faculty_onboarding_detail', pk=pk)
    
    onboarding.status = 'rejected'
    onboarding.reviewed_by = request.user
    onboarding.review_date = timezone.now()
    onboarding.review_notes = request.POST.get('rejection_notes', '')
    onboarding.save()
    
    messages.success(request, 'Onboarding request has been rejected.')
    return redirect('faculty_onboarding_detail', pk=pk)


# Faculty Leave Request Views
@login_required
def faculty_leave_request_list(request):
    """List view for faculty leave requests"""
    queryset = FacultyLeaveRequest.objects.select_related('faculty', 'suggested_backup')
    
    # Filters
    status_filter = request.GET.get('status')
    faculty_filter = request.GET.get('faculty')
    request_type_filter = request.GET.get('request_type')
    
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    if faculty_filter:
        queryset = queryset.filter(faculty_id=faculty_filter)
    if request_type_filter:
        queryset = queryset.filter(request_type=request_type_filter)
    
    queryset = queryset.order_by('-request_date')
    
    # Pagination
    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Filter options
    faculty_list = Faculty.objects.filter(status='active').order_by('first_name', 'last_name')
    
    context = {
        'leave_requests': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'status_filter': status_filter,
        'faculty_filter': faculty_filter,
        'request_type_filter': request_type_filter,
        'faculty_list': faculty_list,
        'status_choices': FacultyLeaveRequest.STATUS_CHOICES,
        'request_type_choices': FacultyLeaveRequest.REQUEST_TYPE_CHOICES,
    }
    return render(request, 'xtrainer/leave_request_list.html', context)


@login_required
def faculty_leave_request_create(request):
    """Create view for faculty leave request"""
    if request.method == 'POST':
        form = FacultyLeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            # Generate request ID
            today = date.today()
            prefix = f"LVR-{today.year}{today.month:02d}"
            last_request = FacultyLeaveRequest.objects.filter(
                request_id__startswith=prefix
            ).order_by('-request_id').first()
            
            if last_request:
                last_number = int(last_request.request_id.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            leave_request.request_id = f"{prefix}-{new_number:04d}"
            leave_request.save()
            form.save_m2m()  # Save many-to-many relationships
            
            messages.success(request, f'Leave request {leave_request.request_id} has been submitted successfully!')
            return redirect('faculty_leave_request_detail', pk=leave_request.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = FacultyLeaveRequestForm()
    
    return render(request, 'xtrainer/leave_request_form.html', {'form': form})


@login_required
def faculty_leave_request_detail(request, pk):
    """Detail view for faculty leave request"""
    leave_request = get_object_or_404(FacultyLeaveRequest, pk=pk)
    
    # Get related backup schedules
    backup_schedules = leave_request.backup_schedules.all().order_by('date', 'start_time')
    
    context = {
        'leave_request': leave_request,
        'backup_schedules': backup_schedules,
        'can_approve': leave_request.status == 'pending',
        'can_reject': leave_request.status == 'pending',
    }
    return render(request, 'xtrainer/leave_request_detail.html', context)


@login_required
@require_http_methods(["POST"])
def faculty_leave_request_approve(request, pk):
    """Approve faculty leave request"""
    leave_request = get_object_or_404(FacultyLeaveRequest, pk=pk)
    
    if leave_request.status != 'pending':
        messages.error(request, 'This leave request cannot be approved at this time.')
        return redirect('faculty_leave_request_detail', pk=pk)
    
    leave_request.status = 'approved'
    leave_request.reviewed_by = request.user
    leave_request.review_date = timezone.now()
    leave_request.approval_notes = request.POST.get('approval_notes', '')
    leave_request.save()
    
    messages.success(request, f'Leave request {leave_request.request_id} has been approved.')
    return redirect('faculty_leave_request_detail', pk=pk)


@login_required
@require_http_methods(["POST"])
def faculty_leave_request_reject(request, pk):
    """Reject faculty leave request"""
    leave_request = get_object_or_404(FacultyLeaveRequest, pk=pk)
    
    if leave_request.status != 'pending':
        messages.error(request, 'This leave request cannot be rejected at this time.')
        return redirect('faculty_leave_request_detail', pk=pk)
    
    leave_request.status = 'rejected'
    leave_request.reviewed_by = request.user
    leave_request.review_date = timezone.now()
    leave_request.approval_notes = request.POST.get('rejection_notes', '')
    leave_request.save()
    
    messages.success(request, f'Leave request {leave_request.request_id} has been rejected.')
    return redirect('faculty_leave_request_detail', pk=pk)


# Backup Schedule Views
@login_required
def backup_schedule_list(request):
    """List view for backup schedules"""
    queryset = BackupSchedule.objects.select_related(
        'original_faculty', 'backup_faculty', 'course', 'leave_request'
    )
    
    # Filters
    date_filter = request.GET.get('date')
    backup_faculty_filter = request.GET.get('backup_faculty')
    status_filter = request.GET.get('status')
    
    if date_filter:
        queryset = queryset.filter(date=date_filter)
    if backup_faculty_filter:
        queryset = queryset.filter(backup_faculty_id=backup_faculty_filter)
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    
    queryset = queryset.order_by('date', 'start_time')
    
    # Pagination
    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Filter options
    faculty_list = Faculty.objects.filter(status='active').order_by('first_name', 'last_name')
    
    context = {
        'backup_schedules': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'date_filter': date_filter,
        'backup_faculty_filter': backup_faculty_filter,
        'status_filter': status_filter,
        'faculty_list': faculty_list,
        'status_choices': BackupSchedule.STATUS_CHOICES,
    }
    return render(request, 'xtrainer/backup_schedule_list.html', context)


@login_required
def backup_schedule_create(request):
    """Create view for backup schedule"""
    if request.method == 'POST':
        form = BackupScheduleForm(request.POST)
        if form.is_valid():
            backup_schedule = form.save(commit=False)
            # Generate schedule ID
            today = date.today()
            prefix = f"BKP-{today.year}{today.month:02d}"
            last_schedule = BackupSchedule.objects.filter(
                schedule_id__startswith=prefix
            ).order_by('-schedule_id').first()
            
            if last_schedule:
                last_number = int(last_schedule.schedule_id.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            backup_schedule.schedule_id = f"{prefix}-{new_number:04d}"
            backup_schedule.created_by = request.user
            backup_schedule.save()
            
            messages.success(request, f'Backup schedule {backup_schedule.schedule_id} has been created successfully!')
            return redirect('backup_schedule_detail', pk=backup_schedule.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = BackupScheduleForm()
    
    return render(request, 'xtrainer/backup_schedule_form.html', {'form': form})


@login_required
def backup_schedule_detail(request, pk):
    """Detail view for backup schedule"""
    backup_schedule = get_object_or_404(BackupSchedule, pk=pk)
    
    context = {
        'backup_schedule': backup_schedule,
    }
    return render(request, 'xtrainer/backup_schedule_detail.html', context)


# Faculty Payment Views
@login_required
def faculty_payment_list(request):
    """List view for faculty payments"""
    queryset = FacultyPayment.objects.select_related('faculty')
    
    # Filters
    faculty_filter = request.GET.get('faculty')
    status_filter = request.GET.get('status')
    payment_type_filter = request.GET.get('payment_type')
    
    if faculty_filter:
        queryset = queryset.filter(faculty_id=faculty_filter)
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    if payment_type_filter:
        queryset = queryset.filter(payment_type=payment_type_filter)
    
    queryset = queryset.order_by('-period_end', '-created_at')
    
    # Pagination
    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Filter options and statistics
    faculty_list = Faculty.objects.filter(status='active').order_by('first_name', 'last_name')
    payment_stats = {
        'total_payments': FacultyPayment.objects.count(),
        'pending_payments': FacultyPayment.objects.filter(status='pending').count(),
        'paid_payments': FacultyPayment.objects.filter(status='paid').count(),
        'total_amount': FacultyPayment.objects.filter(status='paid').aggregate(
            total=Sum('net_amount'))['total'] or Decimal('0.000'),
    }
    
    context = {
        'payments': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'faculty_filter': faculty_filter,
        'status_filter': status_filter,
        'payment_type_filter': payment_type_filter,
        'faculty_list': faculty_list,
        'status_choices': FacultyPayment.STATUS_CHOICES,
        'payment_type_choices': FacultyPayment.PAYMENT_TYPE_CHOICES,
        'payment_stats': payment_stats,
    }
    return render(request, 'xtrainer/faculty_payment_list.html', context)


@login_required
def faculty_payment_create(request):
    """Create view for faculty payment"""
    if request.method == 'POST':
        form = FacultyPaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            # Generate payment ID
            today = date.today()
            prefix = f"PAY-{today.year}{today.month:02d}"
            last_payment = FacultyPayment.objects.filter(
                payment_id__startswith=prefix
            ).order_by('-payment_id').first()
            
            if last_payment:
                last_number = int(last_payment.payment_id.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            payment.payment_id = f"{prefix}-{new_number:04d}"
            payment.generated_by = request.user
            payment.save()
            
            messages.success(request, f'Faculty payment {payment.payment_id} has been created successfully!')
            return redirect('faculty_payment_detail', pk=payment.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = FacultyPaymentForm()
    
    return render(request, 'xtrainer/faculty_payment_form.html', {'form': form})


@login_required
def faculty_payment_detail(request, pk):
    """Detail view for faculty payment"""
    payment = get_object_or_404(FacultyPayment, pk=pk)
    
    context = {
        'payment': payment,
    }
    return render(request, 'xtrainer/faculty_payment_detail.html', context)


# Exam Request Views
@login_required
def exam_request_list(request):
    """List view for exam requests"""
    queryset = ExamRequest.objects.select_related('faculty', 'course')
    
    # Filters
    faculty_filter = request.GET.get('faculty')
    status_filter = request.GET.get('status')
    exam_type_filter = request.GET.get('exam_type')
    
    if faculty_filter:
        queryset = queryset.filter(faculty_id=faculty_filter)
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    if exam_type_filter:
        queryset = queryset.filter(exam_type=exam_type_filter)
    
    queryset = queryset.order_by('-request_date')
    
    # Pagination
    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    stats = {
        'total_requests': ExamRequest.objects.count(),
        'pending_requests': ExamRequest.objects.filter(status='pending').count(),
        'approved_requests': ExamRequest.objects.filter(status='approved').count(),
        'scheduled_requests': ExamRequest.objects.filter(status='scheduled').count(),
        'completed_requests': ExamRequest.objects.filter(status='completed').count(),
    }
    
    # Filter options
    faculty_list = Faculty.objects.filter(status='active').order_by('first_name', 'last_name')
    
    context = {
        'exam_requests': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'faculty_filter': faculty_filter,
        'status_filter': status_filter,
        'exam_type_filter': exam_type_filter,
        'faculty_list': faculty_list,
        'status_choices': ExamRequest.STATUS_CHOICES,
        'exam_type_choices': ExamRequest.EXAM_TYPE_CHOICES,
        'stats': stats,
    }
    return render(request, 'xtrainer/exam_request_list.html', context)


@login_required
def exam_request_create(request):
    """Create view for exam request"""
    if request.method == 'POST':
        form = ExamRequestForm(request.POST)
        if form.is_valid():
            exam_request = form.save(commit=False)
            # Generate request ID
            today = date.today()
            prefix = f"EXM-{today.year}{today.month:02d}"
            last_request = ExamRequest.objects.filter(
                request_id__startswith=prefix
            ).order_by('-request_id').first()
            
            if last_request:
                last_number = int(last_request.request_id.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            exam_request.request_id = f"{prefix}-{new_number:04d}"
            exam_request.save()
            form.save_m2m()  # Save many-to-many relationships
            
            messages.success(request, f'Exam request {exam_request.request_id} has been submitted successfully!')
            return redirect('exam_request_detail', pk=exam_request.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ExamRequestForm()
    
    return render(request, 'xtrainer/exam_request_form.html', {'form': form})


@login_required
def exam_request_detail(request, pk):
    """Detail view for exam request"""
    exam_request = get_object_or_404(ExamRequest, pk=pk)
    
    context = {
        'exam_request': exam_request,
        'can_approve': exam_request.can_approve(),
    }
    return render(request, 'xtrainer/exam_request_detail.html', context)


@login_required
@require_http_methods(["POST"])
def exam_request_approve(request, pk):
    """Approve exam request"""
    exam_request = get_object_or_404(ExamRequest, pk=pk)
    
    if not exam_request.can_approve():
        messages.error(request, 'This exam request cannot be approved at this time.')
        return redirect('exam_request_detail', pk=pk)
    
    exam_request.status = 'approved'
    exam_request.reviewed_by = request.user
    exam_request.review_date = timezone.now()
    exam_request.approval_notes = request.POST.get('approval_notes', '')
    
    # Set final schedule details
    exam_request.final_date = exam_request.proposed_date
    exam_request.final_start_time = exam_request.proposed_start_time
    exam_request.assigned_room = request.POST.get('assigned_room', '')
    
    exam_request.save()
    
    messages.success(request, f'Exam request {exam_request.request_id} has been approved.')
    return redirect('exam_request_detail', pk=pk)


# Attendance Report Views
@login_required
def faculty_attendance_report(request):
    """Faculty attendance report view"""
    form = AttendanceReportForm(request.GET)
    attendance_records = None
    
    if form.is_valid():
        queryset = FacultyAttendance.objects.select_related('faculty', 'course')
        
        faculty = form.cleaned_data.get('faculty')
        course = form.cleaned_data.get('course')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        status = form.cleaned_data.get('status')
        
        if faculty:
            queryset = queryset.filter(faculty=faculty)
        if course:
            queryset = queryset.filter(course=course)
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        if status:
            queryset = queryset.filter(status=status)
        
        attendance_records = queryset.order_by('-date', 'faculty__first_name')
    
    context = {
        'form': form,
        'attendance_records': attendance_records,
    }
    return render(request, 'xtrainer/attendance_report.html', context)


# AJAX Views for dynamic content
@login_required
@require_http_methods(["GET"])
def get_faculty_courses(request, faculty_id):
    """AJAX view to get courses for a faculty member"""
    try:
        faculty = Faculty.objects.get(pk=faculty_id)
        courses = faculty.can_teach_courses.filter(status='active').values('id', 'name', 'course_code')
        return JsonResponse({'courses': list(courses)})
    except Faculty.DoesNotExist:
        return JsonResponse({'error': 'Faculty not found'}, status=404)


@login_required
@require_http_methods(["GET"])
def get_course_students(request, course_id):
    """AJAX view to get enrolled students for a course"""
    try:
        enrollments = StudentEnrollment.objects.filter(
            course_id=course_id,
            status='active'
        ).select_related('student').values(
            'id', 'student__student_name', 'student__email_id'
        )
        return JsonResponse({'students': list(enrollments)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
