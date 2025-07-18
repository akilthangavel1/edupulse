from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count, Avg
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from decimal import Decimal
from datetime import date, datetime, timedelta
import csv
import io
from django.template.loader import get_template
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side

from .models import (
    Course, FeeStructure, StudentEnrollment, 
    Discount, Invoice, Payment, Kit, CourseKit, KitFee
)
from .forms import (
    CourseForm, FeeStructureForm, StudentEnrollmentForm,
    PaymentForm, DiscountForm, InvoiceForm,
    CourseSearchForm, PaymentSearchForm, KitForm, 
    CourseKitForm, KitFeeForm, KitSearchForm, KitFeeSearchForm
)
from xstudent.models import NewStudent


def test_template(request):
    """Simple test view"""
    return render(request, 'xcoursefee/test.html')


@login_required
def coursefee_dashboard(request):
    """Dashboard view for course fee management"""
    today = date.today()
    current_month = today.replace(day=1)
    
    # Basic statistics
    stats = {
        'total_courses': Course.objects.filter(status='active').count(),
        'total_enrollments': StudentEnrollment.objects.filter(status='active').count(),
        'total_students': NewStudent.objects.filter(status='active').count(),
        'available_spots': sum([course.get_available_spots() for course in Course.objects.filter(status='active')]),
    }
    
    # Financial statistics
    financial_stats = {
        'total_revenue': Payment.objects.filter(status='completed').aggregate(
            total=Sum('amount'))['total'] or Decimal('0.000'),
        'monthly_revenue': Payment.objects.filter(
            status='completed', 
            payment_date__gte=current_month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.000'),
        'pending_payments': Payment.objects.filter(status='pending').aggregate(
            total=Sum('amount'))['total'] or Decimal('0.000'),
        'outstanding_invoices': Invoice.objects.filter(status='sent').count(),
    }
    
    # Recent activities
    recent_enrollments = StudentEnrollment.objects.select_related(
        'student', 'course'
    ).order_by('-created_at')[:5]
    
    recent_payments = Payment.objects.select_related(
        'enrollment__student', 'enrollment__course'
    ).filter(status='completed').order_by('-payment_date')[:5]
    
    # Popular courses
    popular_courses = Course.objects.annotate(
        enrollment_count=Count('enrollments')
    ).filter(status='active').order_by('-enrollment_count')[:5]
    
    # Payment method statistics
    payment_methods = Payment.objects.filter(status='completed').values(
        'payment_method'
    ).annotate(count=Count('id'), total=Sum('amount')).order_by('-total')
    
    # Overdue invoices
    overdue_invoices = Invoice.objects.filter(
        status='sent',
        due_date__lt=today
    ).select_related('enrollment__student', 'enrollment__course')[:5]
    
    context = {
        'stats': stats,
        'financial_stats': financial_stats,
        'recent_enrollments': recent_enrollments,
        'recent_payments': recent_payments,
        'popular_courses': popular_courses,
        'payment_methods': payment_methods,
        'overdue_invoices': overdue_invoices,
        'today': today,
    }
    return render(request, 'xcoursefee/dashboard.html', context)


# Course Views
@login_required
def course_list(request):
    """List view for courses with search and pagination"""
    queryset = Course.objects.all()
    form = CourseSearchForm(request.GET)
    
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        course_type = form.cleaned_data.get('course_type')
        status = form.cleaned_data.get('status')
        min_duration = form.cleaned_data.get('min_duration')
        max_duration = form.cleaned_data.get('max_duration')
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(course_code__icontains=search_query) |
                Q(instructor_name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        if course_type:
            queryset = queryset.filter(course_type=course_type)
        
        if status:
            queryset = queryset.filter(status=status)
        
        if min_duration:
            queryset = queryset.filter(duration__gte=min_duration)
        
        if max_duration:
            queryset = queryset.filter(duration__lte=max_duration)
    
    queryset = queryset.annotate(
        enrollment_count=Count('enrollments')
    ).order_by('name')
    
    # Pagination
    paginator = Paginator(queryset, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'courses': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'search_form': form,
        'total_courses': Course.objects.count(),
        'active_courses': Course.objects.filter(status='active').count(),
    }
    return render(request, 'xcoursefee/course_list.html', context)


@login_required
def course_detail(request, pk):
    """Detail view for a course"""
    course = get_object_or_404(Course, pk=pk)
    enrollments = course.enrollments.select_related('student').order_by('-enrollment_date')
    fee_structures = course.fee_structures.all()
    
    # Calculate statistics
    total_revenue = Payment.objects.filter(
        enrollment__course=course,
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.000')
    
    context = {
        'course': course,
        'enrollments': enrollments,
        'fee_structures': fee_structures,
        'total_revenue': total_revenue,
        'enrollment_count': enrollments.count(),
        'available_spots': course.get_available_spots(),
    }
    return render(request, 'xcoursefee/course_detail.html', context)


@login_required
def course_create(request):
    """Create view for courses"""
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, f'Course "{course.name}" has been created successfully!')
            return redirect('course_detail', pk=course.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CourseForm()
    
    return render(request, 'xcoursefee/course_form.html', {'form': form})


@login_required
def course_update(request, pk):
    """Update view for a course"""
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            messages.success(request, f'Course "{course.name}" has been updated successfully!')
            return redirect('course_detail', pk=course.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'xcoursefee/course_form.html', {'form': form, 'course': course})


@login_required
def course_delete(request, pk):
    """Delete view for a course"""
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == 'POST':
        course_name = course.name
        course.delete()
        messages.success(request, f'Course "{course_name}" has been deleted successfully!')
        return redirect('course_list')
    
    return render(request, 'xcoursefee/course_confirm_delete.html', {'course': course})


# Enrollment Views
@login_required
def enrollment_list(request):
    """List view for student enrollments"""
    queryset = StudentEnrollment.objects.select_related('student', 'course').all()
    
    # Apply filters
    student_filter = request.GET.get('student')
    course_filter = request.GET.get('course')
    status_filter = request.GET.get('status')
    
    if student_filter:
        queryset = queryset.filter(student__id=student_filter)
    if course_filter:
        queryset = queryset.filter(course__id=course_filter)
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    
    queryset = queryset.order_by('-enrollment_date')
    
    # Pagination
    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Filter choices for dropdowns
    students = NewStudent.objects.filter(status='active').order_by('student_name')
    courses = Course.objects.filter(status='active').order_by('name')
    
    context = {
        'enrollments': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'students': students,
        'courses': courses,
        'status_choices': StudentEnrollment.STATUS_CHOICES,
        'selected_student': student_filter,
        'selected_course': course_filter,
        'selected_status': status_filter,
    }
    return render(request, 'xcoursefee/enrollment_list.html', context)


@login_required
def enrollment_create(request):
    """Create view for student enrollment"""
    if request.method == 'POST':
        form = StudentEnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save()
            messages.success(request, f'{enrollment.student.student_name} has been enrolled in {enrollment.course.name}!')
            return redirect('enrollment_detail', pk=enrollment.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = StudentEnrollmentForm()
    
    return render(request, 'xcoursefee/enrollment_form.html', {'form': form})


@login_required
def enrollment_detail(request, pk):
    """Detail view for enrollment"""
    enrollment = get_object_or_404(StudentEnrollment, pk=pk)
    payments = enrollment.payments.all().order_by('-payment_date')
    invoices = enrollment.invoices.all().order_by('-issue_date')
    
    context = {
        'enrollment': enrollment,
        'payments': payments,
        'invoices': invoices,
        'total_fees': enrollment.get_total_fees(),
        'total_paid': enrollment.get_total_paid(),
        'outstanding_balance': enrollment.get_outstanding_balance(),
    }
    return render(request, 'xcoursefee/enrollment_detail.html', context)


# Payment Views
@login_required
def payment_list(request):
    """List view for payments with filtering"""
    queryset = Payment.objects.select_related(
        'enrollment__student', 'enrollment__course'
    ).all()
    
    form = PaymentSearchForm(request.GET)
    
    if form.is_valid():
        student = form.cleaned_data.get('student')
        course = form.cleaned_data.get('course')
        payment_method = form.cleaned_data.get('payment_method')
        status = form.cleaned_data.get('status')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        
        if student:
            queryset = queryset.filter(enrollment__student=student)
        if course:
            queryset = queryset.filter(enrollment__course=course)
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)
        if status:
            queryset = queryset.filter(status=status)
        if date_from:
            queryset = queryset.filter(payment_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(payment_date__lte=date_to)
    
    queryset = queryset.order_by('-payment_date', '-created_at')
    
    # Pagination
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    stats = {
        'total_payments': Payment.objects.count(),
        'completed_payments': Payment.objects.filter(status='completed').count(),
        'pending_payments': Payment.objects.filter(status='pending').count(),
        'total_amount': Payment.objects.filter(status='completed').aggregate(
            total=Sum('amount'))['total'] or Decimal('0.000'),
    }
    
    context = {
        'payments': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'filter_form': form,
        'stats': stats,
    }
    return render(request, 'xcoursefee/payment_list.html', context)


@login_required
def payment_create(request):
    """Create view for payments"""
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.processed_by = request.user
            payment.save()
            messages.success(request, f'Payment of {payment.amount} KWD has been recorded!')
            return redirect('payment_detail', pk=payment.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PaymentForm()
    
    return render(request, 'xcoursefee/payment_form.html', {'form': form})


@login_required
def payment_detail(request, pk):
    """Detail view for payment"""
    payment = get_object_or_404(Payment, pk=pk)
    return render(request, 'xcoursefee/payment_detail.html', {'payment': payment})


# Invoice Views
@login_required
def invoice_list(request):
    """List view for invoices"""
    queryset = Invoice.objects.select_related(
        'enrollment__student', 'enrollment__course'
    ).all()
    
    # Apply filters
    status_filter = request.GET.get('status')
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    
    queryset = queryset.order_by('-issue_date')
    
    # Pagination
    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'invoices': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'status_choices': Invoice.STATUS_CHOICES,
        'selected_status': status_filter,
    }
    return render(request, 'xcoursefee/invoice_list.html', context)


@login_required
def invoice_create(request):
    """Create view for invoices"""
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()
            messages.success(request, f'Invoice {invoice.invoice_number} has been created!')
            return redirect('invoice_detail', pk=invoice.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = InvoiceForm()
    
    return render(request, 'xcoursefee/invoice_form.html', {'form': form})


@login_required
def invoice_detail(request, pk):
    """Detail view for invoice"""
    invoice = get_object_or_404(Invoice, pk=pk)
    payments = invoice.payments.all().order_by('-payment_date')
    
    context = {
        'invoice': invoice,
        'payments': payments,
        'total_paid': payments.filter(status='completed').aggregate(
            total=Sum('amount'))['total'] or Decimal('0.000'),
    }
    return render(request, 'xcoursefee/invoice_detail.html', context)


# Discount Views
@login_required
def discount_list(request):
    """List view for discounts"""
    queryset = Discount.objects.all().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'discounts': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'xcoursefee/discount_list.html', context)


@login_required
def discount_create(request):
    """Create view for discounts"""
    if request.method == 'POST':
        form = DiscountForm(request.POST)
        if form.is_valid():
            discount = form.save()
            messages.success(request, f'Discount "{discount.name}" has been created!')
            return redirect('discount_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = DiscountForm()
    
    return render(request, 'xcoursefee/discount_form.html', {'form': form})


# Report Views
@login_required
def financial_report(request):
    """Generate financial reports"""
    if request.method == 'POST':
        report_type = request.POST.get('report_type', 'monthly')
        
        today = date.today()
        if report_type == 'daily':
            start_date = end_date = today
        elif report_type == 'weekly':
            start_date = today - timedelta(days=today.weekday())
            end_date = today
        elif report_type == 'monthly':
            start_date = today.replace(day=1)
            end_date = today
        else:  # yearly
            start_date = today.replace(month=1, day=1)
            end_date = today
        
        # Generate CSV report
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="financial_report_{start_date}_{end_date}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Date', 'Student', 'Course', 'Payment Method', 'Amount (KWD)', 
            'Status', 'Reference Number', 'Receipt Number'
        ])
        
        payments = Payment.objects.filter(
            payment_date__gte=start_date,
            payment_date__lte=end_date
        ).select_related('enrollment__student', 'enrollment__course').order_by('payment_date')
        
        for payment in payments:
            writer.writerow([
                payment.payment_date,
                payment.enrollment.student.student_name,
                payment.enrollment.course.name,
                payment.get_payment_method_display(),
                payment.amount,
                payment.get_status_display(),
                payment.reference_number,
                payment.receipt_number,
            ])
        
        return response
    
    return render(request, 'xcoursefee/financial_report.html')


# AJAX Views
@login_required
def get_course_fees(request, course_id):
    """AJAX view to get course fee structure"""
    try:
        course = Course.objects.get(id=course_id)
        fee_structures = course.fee_structures.all()
        
        fees = []
        total = Decimal('0.000')
        
        for fee in fee_structures:
            fees.append({
                'type': fee.get_fee_type_display(),
                'amount': str(fee.amount),
                'frequency': fee.get_payment_frequency_display(),
                'mandatory': fee.is_mandatory,
            })
            total += fee.amount
        
        return JsonResponse({
            'success': True,
            'fees': fees,
            'total': str(total),
        })
    
    except Course.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Course not found'})


@login_required
@require_http_methods(["POST"])
def mark_payment_completed(request, payment_id):
    """AJAX view to mark payment as completed"""
    try:
        payment = Payment.objects.get(id=payment_id)
        payment.status = 'completed'
        payment.processed_by = request.user
        payment.save()
        
        messages.success(request, f'Payment of {payment.amount} KWD marked as completed')
        return JsonResponse({'success': True})
    
    except Payment.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Payment not found'})


# Kit Views
@login_required
def kit_list(request):
    """List view for kits with search and pagination"""
    queryset = Kit.objects.all()
    form = KitSearchForm(request.GET)
    
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        status = form.cleaned_data.get('status')
        is_mandatory = form.cleaned_data.get('is_mandatory')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        low_stock = form.cleaned_data.get('low_stock')
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(kit_code__icontains=search_query) |
                Q(supplier__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        if status:
            queryset = queryset.filter(status=status)
        
        if is_mandatory == 'true':
            queryset = queryset.filter(is_mandatory=True)
        elif is_mandatory == 'false':
            queryset = queryset.filter(is_mandatory=False)
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        if low_stock:
            queryset = queryset.extra(where=["stock_quantity <= minimum_stock"])
    
    queryset = queryset.order_by('name')
    
    # Pagination
    paginator = Paginator(queryset, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'kits': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'search_form': form,
        'total_kits': Kit.objects.count(),
        'available_kits': Kit.objects.filter(status='available').count(),
        'low_stock_kits': Kit.objects.extra(where=["stock_quantity <= minimum_stock"]).count(),
    }
    return render(request, 'xcoursefee/kit_list.html', context)


@login_required
def kit_detail(request, pk):
    """Detail view for a kit"""
    kit = get_object_or_404(Kit, pk=pk)
    course_kits = kit.course_kits.select_related('course').order_by('course__name')
    kit_fees = KitFee.objects.filter(course_kit__kit=kit).select_related(
        'enrollment__student', 'enrollment__course'
    ).order_by('-created_at')
    
    # Calculate statistics
    total_revenue = kit_fees.filter(payment_status='paid').aggregate(
        total=Sum('amount'))['total'] or Decimal('0.000')
    
    context = {
        'kit': kit,
        'course_kits': course_kits,
        'kit_fees': kit_fees[:10],  # Show latest 10
        'total_revenue': total_revenue,
        'total_fees': kit_fees.count(),
        'pending_fees': kit_fees.filter(payment_status='pending').count(),
        'is_low_stock': kit.is_low_stock(),
    }
    return render(request, 'xcoursefee/kit_detail.html', context)


@login_required
def kit_create(request):
    """Create view for kits"""
    if request.method == 'POST':
        form = KitForm(request.POST)
        if form.is_valid():
            kit = form.save()
            messages.success(request, f'Kit "{kit.name}" has been created successfully!')
            return redirect('kit_detail', pk=kit.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = KitForm()
    
    return render(request, 'xcoursefee/kit_form.html', {'form': form})


@login_required
def kit_update(request, pk):
    """Update view for a kit"""
    kit = get_object_or_404(Kit, pk=pk)
    
    if request.method == 'POST':
        form = KitForm(request.POST, instance=kit)
        if form.is_valid():
            kit = form.save()
            messages.success(request, f'Kit "{kit.name}" has been updated successfully!')
            return redirect('kit_detail', pk=kit.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = KitForm(instance=kit)
    
    return render(request, 'xcoursefee/kit_form.html', {'form': form, 'kit': kit})


@login_required
def kit_delete(request, pk):
    """Delete view for a kit"""
    kit = get_object_or_404(Kit, pk=pk)
    
    if request.method == 'POST':
        kit_name = kit.name
        kit.delete()
        messages.success(request, f'Kit "{kit_name}" has been deleted successfully!')
        return redirect('kit_list')
    
    return render(request, 'xcoursefee/kit_confirm_delete.html', {'kit': kit})


# Course Kit Views
@login_required
def course_kit_list(request):
    """List view for course-kit relationships"""
    queryset = CourseKit.objects.select_related('course', 'kit').all()
    
    # Apply filters
    course_filter = request.GET.get('course')
    kit_filter = request.GET.get('kit')
    is_required_filter = request.GET.get('is_required')
    
    if course_filter:
        queryset = queryset.filter(course__id=course_filter)
    if kit_filter:
        queryset = queryset.filter(kit__id=kit_filter)
    if is_required_filter == 'true':
        queryset = queryset.filter(is_required=True)
    elif is_required_filter == 'false':
        queryset = queryset.filter(is_required=False)
    
    queryset = queryset.order_by('course__name', 'kit__name')
    
    # Pagination
    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Filter choices
    courses = Course.objects.filter(status='active').order_by('name')
    kits = Kit.objects.filter(status='available').order_by('name')
    
    context = {
        'course_kits': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'courses': courses,
        'kits': kits,
        'selected_course': course_filter,
        'selected_kit': kit_filter,
        'selected_is_required': is_required_filter,
    }
    return render(request, 'xcoursefee/course_kit_list.html', context)


@login_required
def course_kit_create(request):
    """Create view for course-kit relationship"""
    if request.method == 'POST':
        form = CourseKitForm(request.POST)
        if form.is_valid():
            course_kit = form.save()
            messages.success(request, f'Kit "{course_kit.kit.name}" has been linked to course "{course_kit.course.name}"!')
            return redirect('course_kit_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CourseKitForm()
    
    return render(request, 'xcoursefee/course_kit_form.html', {'form': form})


@login_required
def course_kit_detail(request, pk):
    """Detail view for course-kit relationship"""
    course_kit = get_object_or_404(CourseKit, pk=pk)
    kit_fees = course_kit.kit_fees.select_related('enrollment__student').order_by('-created_at')
    
    context = {
        'course_kit': course_kit,
        'kit_fees': kit_fees,
        'total_fees': kit_fees.count(),
        'paid_fees': kit_fees.filter(payment_status='paid').count(),
        'pending_fees': kit_fees.filter(payment_status='pending').count(),
    }
    return render(request, 'xcoursefee/course_kit_detail.html', context)


@login_required
def course_kit_update(request, pk):
    """Update view for course-kit relationship"""
    course_kit = get_object_or_404(CourseKit, pk=pk)
    
    if request.method == 'POST':
        form = CourseKitForm(request.POST, instance=course_kit)
        if form.is_valid():
            course_kit = form.save()
            messages.success(request, f'Course-Kit relationship has been updated successfully!')
            return redirect('course_kit_detail', pk=course_kit.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CourseKitForm(instance=course_kit)
    
    return render(request, 'xcoursefee/course_kit_form.html', {'form': form, 'course_kit': course_kit})


@login_required
def course_kit_delete(request, pk):
    """Delete view for course-kit relationship"""
    course_kit = get_object_or_404(CourseKit, pk=pk)
    
    if request.method == 'POST':
        course_name = course_kit.course.name
        kit_name = course_kit.kit.name
        course_kit.delete()
        messages.success(request, f'Kit "{kit_name}" has been unlinked from course "{course_name}"!')
        return redirect('course_kit_list')
    
    return render(request, 'xcoursefee/course_kit_confirm_delete.html', {'course_kit': course_kit})


# Kit Fee Views
@login_required
def kit_fee_list(request):
    """List view for kit fees with filtering"""
    queryset = KitFee.objects.select_related(
        'enrollment__student', 'enrollment__course', 'course_kit__kit'
    ).all()
    
    form = KitFeeSearchForm(request.GET)
    
    if form.is_valid():
        student = form.cleaned_data.get('student')
        course = form.cleaned_data.get('course')
        kit = form.cleaned_data.get('kit')
        payment_status = form.cleaned_data.get('payment_status')
        delivery_status = form.cleaned_data.get('delivery_status')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        
        if student:
            queryset = queryset.filter(enrollment__student=student)
        if course:
            queryset = queryset.filter(enrollment__course=course)
        if kit:
            queryset = queryset.filter(course_kit__kit=kit)
        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)
        if delivery_status:
            queryset = queryset.filter(delivery_status=delivery_status)
        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)
    
    queryset = queryset.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    stats = {
        'total_kit_fees': KitFee.objects.count(),
        'paid_fees': KitFee.objects.filter(payment_status='paid').count(),
        'pending_fees': KitFee.objects.filter(payment_status='pending').count(),
        'total_revenue': KitFee.objects.filter(payment_status='paid').aggregate(
            total=Sum('amount'))['total'] or Decimal('0.000'),
        'pending_deliveries': KitFee.objects.filter(
            payment_status='paid', delivery_status='pending'
        ).count(),
    }
    
    context = {
        'kit_fees': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'filter_form': form,
        'stats': stats,
    }
    return render(request, 'xcoursefee/kit_fee_list.html', context)


@login_required
def kit_fee_create(request):
    """Create view for kit fees"""
    if request.method == 'POST':
        form = KitFeeForm(request.POST)
        if form.is_valid():
            kit_fee = form.save(commit=False)
            kit_fee.processed_by = request.user
            kit_fee.save()
            messages.success(request, f'Kit fee of {kit_fee.amount} KWD has been recorded!')
            return redirect('kit_fee_detail', pk=kit_fee.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = KitFeeForm()
    
    return render(request, 'xcoursefee/kit_fee_form.html', {'form': form})


@login_required
def kit_fee_detail(request, pk):
    """Detail view for kit fee"""
    kit_fee = get_object_or_404(KitFee, pk=pk)
    return render(request, 'xcoursefee/kit_fee_detail.html', {'kit_fee': kit_fee})


@login_required
def kit_fee_update(request, pk):
    """Update view for kit fee"""
    kit_fee = get_object_or_404(KitFee, pk=pk)
    
    if request.method == 'POST':
        form = KitFeeForm(request.POST, instance=kit_fee)
        if form.is_valid():
            kit_fee = form.save(commit=False)
            kit_fee.processed_by = request.user
            kit_fee.save()
            messages.success(request, f'Kit fee has been updated successfully!')
            return redirect('kit_fee_detail', pk=kit_fee.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = KitFeeForm(instance=kit_fee)
    
    return render(request, 'xcoursefee/kit_fee_form.html', {'form': form, 'kit_fee': kit_fee})


@login_required
def kit_fee_delete(request, pk):
    """Delete view for kit fee"""
    kit_fee = get_object_or_404(KitFee, pk=pk)
    
    if request.method == 'POST':
        student_name = kit_fee.enrollment.student.student_name
        kit_name = kit_fee.course_kit.kit.name
        kit_fee.delete()
        messages.success(request, f'Kit fee for {student_name} - {kit_name} has been deleted!')
        return redirect('kit_fee_list')
    
    return render(request, 'xcoursefee/kit_fee_confirm_delete.html', {'kit_fee': kit_fee})


# AJAX Views for Kit Management
@login_required
def get_course_kits(request, course_id):
    """AJAX view to get kits for a specific course"""
    try:
        course = Course.objects.get(id=course_id)
        course_kits = course.course_kits.select_related('kit').filter(kit__status='available')
        
        kits = []
        for course_kit in course_kits:
            kits.append({
                'id': course_kit.id,
                'kit_id': course_kit.kit.id,
                'kit_name': course_kit.kit.name,
                'kit_code': course_kit.kit.kit_code,
                'price': str(course_kit.kit.price),
                'is_required': course_kit.is_required,
                'is_available': course_kit.kit.is_available(),
                'stock_quantity': course_kit.kit.stock_quantity,
            })
        
        return JsonResponse({
            'success': True,
            'kits': kits,
        })
    
    except Course.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Course not found'})


@login_required
@require_http_methods(["POST"])
def mark_kit_delivered(request, kit_fee_id):
    """AJAX view to mark kit as delivered"""
    try:
        kit_fee = KitFee.objects.get(id=kit_fee_id)
        
        if kit_fee.payment_status != 'paid':
            return JsonResponse({'success': False, 'error': 'Payment must be completed before delivery'})
        
        kit_fee.delivery_status = 'delivered'
        kit_fee.delivery_date = timezone.now().date()
        kit_fee.save()
        
        # Update kit stock
        kit = kit_fee.course_kit.kit
        if kit.stock_quantity > 0:
            kit.stock_quantity -= 1
            kit.save()
        
        messages.success(request, f'Kit {kit_fee.course_kit.kit.name} marked as delivered')
        return JsonResponse({'success': True})
    
    except KitFee.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Kit fee not found'})


@login_required
@require_http_methods(["POST"]) 
def mark_kit_fee_paid(request, kit_fee_id):
    """AJAX view to mark kit fee as paid"""
    try:
        kit_fee = KitFee.objects.get(id=kit_fee_id)
        kit_fee.payment_status = 'paid'
        kit_fee.payment_date = timezone.now().date()
        kit_fee.processed_by = request.user
        kit_fee.save()
        
        messages.success(request, f'Kit fee of {kit_fee.amount} KWD marked as paid')
        return JsonResponse({'success': True})
    
    except KitFee.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Kit fee not found'})



