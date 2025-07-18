from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import NewStudent, OldStudent, Attendance, AttendanceSummary
from .forms import (
    StudentForm, StudentSearchForm, OldStudentForm, OldStudentSearchForm,
    AttendanceForm, BulkAttendanceForm, AttendanceFilterForm, AttendanceReportForm
)
from datetime import date, datetime, timedelta
import csv


def student_list(request):
    """List view for students with search and pagination"""
    queryset = NewStudent.objects.all()
    form = StudentSearchForm(request.GET)
    
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        status = form.cleaned_data.get('status')
        gender = form.cleaned_data.get('gender')
        grade = form.cleaned_data.get('grade')
        program = form.cleaned_data.get('program')
        
        if search_query:
            queryset = queryset.filter(
                Q(student_name__icontains=search_query) |
                Q(email_id__icontains=search_query) |
                Q(grade__icontains=search_query) |
                Q(program__icontains=search_query)
            )
        
        if status:
            queryset = queryset.filter(status=status)
        
        if gender:
            queryset = queryset.filter(gender=gender)
            
        if grade:
            queryset = queryset.filter(grade__icontains=grade)
            
        if program:
            queryset = queryset.filter(program__icontains=program)
    
    queryset = queryset.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'students': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'search_form': StudentSearchForm(request.GET),
        'total_students': NewStudent.objects.count(),
        'active_students': NewStudent.objects.filter(status='active').count(),
        'draft_students': NewStudent.objects.filter(status='draft').count(),
    }
    return render(request, 'xstudent/student_list.html', context)


def student_draft_list(request):
    """List view for draft students with pagination"""
    queryset = NewStudent.objects.filter(status='draft').order_by('-created_at')
    
    # Pagination
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'students': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'total_drafts': NewStudent.objects.filter(status='draft').count(),
    }
    return render(request, 'xstudent/student_draft_list.html', context)


def student_create(request):
    """Create view for new students"""
    if request.method == 'POST':
        action = request.POST.get('action')
        is_draft = action == 'save_draft'
        form = StudentForm(request.POST, request.FILES, is_draft=is_draft)
        
        if form.is_valid():
            student = form.save(commit=False)
            
            if action == 'save_draft':
                student.status = 'draft'
                messages.success(request, f'Student {student.student_name or "draft"} has been saved as draft!')
            else:
                student.status = 'active'
                messages.success(request, f'Student {student.student_name} has been registered successfully!')
            
            student.save()
            return redirect('student_list')
        else:
            # Debug: Show specific form errors
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        error_messages.append(f"Form error: {error}")
                    else:
                        field_label = form.fields[field].label or field.replace('_', ' ').title()
                        error_messages.append(f"{field_label}: {error}")
            
            if action == 'save_draft':
                messages.error(request, f'Cannot save draft. Errors: {"; ".join(error_messages)}')
            else:
                messages.error(request, f'Please correct the errors: {"; ".join(error_messages)}')
    else:
        form = StudentForm()
    
    return render(request, 'xstudent/student_form.html', {'form': form})


def student_detail(request, pk):
    """Detail view for a student"""
    student = get_object_or_404(NewStudent, pk=pk)
    return render(request, 'xstudent/student_detail.html', {'student': student})


def student_update(request, pk):
    """Update view for a student"""
    student = get_object_or_404(NewStudent, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        is_draft = action == 'save_draft'
        form = StudentForm(request.POST, request.FILES, instance=student, is_draft=is_draft)
        
        if form.is_valid():
            student = form.save(commit=False)
            
            if action == 'save_draft':
                student.status = 'draft'
                messages.success(request, f'Student {student.student_name or "draft"} has been saved as draft!')
            elif action == 'activate':
                student.status = 'active'
                messages.success(request, f'Student {student.student_name} has been activated successfully!')
            else:
                messages.success(request, f'Student {student.student_name} has been updated successfully!')
            
            student.save()
            return redirect('student_detail', pk=student.pk)
        else:
            # Debug: Show specific form errors
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        error_messages.append(f"Form error: {error}")
                    else:
                        field_label = form.fields[field].label or field.replace('_', ' ').title()
                        error_messages.append(f"{field_label}: {error}")
            
            if action == 'save_draft':
                messages.error(request, f'Cannot save draft. Errors: {"; ".join(error_messages)}')
            else:
                messages.error(request, f'Please correct the errors: {"; ".join(error_messages)}')
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'xstudent/student_form.html', {'form': form, 'student': student})


def student_delete(request, pk):
    """Delete view for a student"""
    student = get_object_or_404(NewStudent, pk=pk)
    
    if request.method == 'POST':
        student_name = student.student_name
        student.delete()
        messages.success(request, f'Student {student_name} has been deleted successfully!')
        return redirect('student_list')
    
    return render(request, 'xstudent/student_confirm_delete.html', {'student': student})


def student_dashboard(request):
    """Dashboard with student statistics"""
    # Get grade statistics
    grades = NewStudent.objects.values_list('grade', flat=True).distinct()
    students_by_grade = {
        grade: NewStudent.objects.filter(grade=grade).count()
        for grade in grades if grade
    }
    
    # Get program statistics
    programs = NewStudent.objects.values_list('program', flat=True).distinct()
    students_by_program = {
        program: NewStudent.objects.filter(program=program).count()
        for program in programs if program
    }
    
    context = {
        'total_students': NewStudent.objects.count(),
        'recent_students': NewStudent.objects.order_by('-created_at')[:5],
        'students_by_grade': students_by_grade,
        'students_by_program': students_by_program,
        'students_by_gender': {
            choice[1]: NewStudent.objects.filter(gender=choice[0]).count()
            for choice in NewStudent.GENDER_CHOICES
        }
    }
    return render(request, 'xstudent/dashboard.html', context)


def student_export(request):
    """Export students data to CSV"""
    import csv
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Student Name', 'Email ID', 'Grade', 'Program', 'Gender',
        'Date of Birth', 'School Name', 'Father Name', 'Father Mobile',
        'Father Email', 'Mother Name', 'Mother Mobile', 'Mother Email',
        'Address Line 1', 'Area', 'City', 'State/Province', 'Country',
        'Postal Code', 'Created Date'
    ])
    
    for student in NewStudent.objects.all():
        writer.writerow([
            student.student_name, student.email_id, student.grade,
            student.program, student.get_gender_display(),
            student.date_of_birth, student.school_name,
            student.father_name, student.father_mobile_no, student.father_email_id,
            student.mother_name, student.mother_mobile_no, student.mother_email_id,
            student.address_line_1, student.area, student.city,
            student.state_emirates_province, student.country,
            student.postal_code, student.created_at
        ])
    
    return response


# Old Student Views
def old_student_list(request):
    """List view for old students with search and pagination"""
    queryset = OldStudent.objects.all()
    form = OldStudentSearchForm(request.GET)
    
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        completion_year = form.cleaned_data.get('completion_year')
        
        if search_query:
            queryset = queryset.filter(
                Q(student_name__icontains=search_query) |
                Q(student_code__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        
        if completion_year:
            queryset = queryset.filter(tenth_level_completed_date__year=completion_year)
    
    queryset = queryset.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'old_students': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'search_form': OldStudentSearchForm(request.GET),
        'total_old_students': OldStudent.objects.count(),
    }
    return render(request, 'xstudent/old_student_list.html', context)


def old_student_create(request):
    """Create view for old students"""
    if request.method == 'POST':
        form = OldStudentForm(request.POST)
        
        if form.is_valid():
            old_student = form.save()
            messages.success(request, f'Old student {old_student.student_name} has been added successfully!')
            return redirect('old_student_list')
        else:
            # Show specific form errors
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        error_messages.append(f"Form error: {error}")
                    else:
                        field_label = form.fields[field].label or field.replace('_', ' ').title()
                        error_messages.append(f"{field_label}: {error}")
            
            messages.error(request, f'Please correct the errors: {"; ".join(error_messages)}')
    else:
        form = OldStudentForm()
    
    return render(request, 'xstudent/old_student_form.html', {'form': form})


def old_student_detail(request, pk):
    """Detail view for an old student"""
    old_student = get_object_or_404(OldStudent, pk=pk)
    return render(request, 'xstudent/old_student_detail.html', {'old_student': old_student})


def old_student_update(request, pk):
    """Update view for an old student"""
    old_student = get_object_or_404(OldStudent, pk=pk)
    
    if request.method == 'POST':
        form = OldStudentForm(request.POST, instance=old_student)
        
        if form.is_valid():
            old_student = form.save()
            messages.success(request, f'Old student {old_student.student_name} has been updated successfully!')
            return redirect('old_student_detail', pk=old_student.pk)
        else:
            # Show specific form errors
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        error_messages.append(f"Form error: {error}")
                    else:
                        field_label = form.fields[field].label or field.replace('_', ' ').title()
                        error_messages.append(f"{field_label}: {error}")
            
            messages.error(request, f'Please correct the errors: {"; ".join(error_messages)}')
    else:
        form = OldStudentForm(instance=old_student)
    
    return render(request, 'xstudent/old_student_form.html', {'form': form, 'old_student': old_student})


def old_student_delete(request, pk):
    """Delete view for an old student"""
    old_student = get_object_or_404(OldStudent, pk=pk)
    
    if request.method == 'POST':
        student_name = old_student.student_name
        old_student.delete()
        messages.success(request, f'Old student {student_name} has been deleted successfully!')
        return redirect('old_student_list')
    
    return render(request, 'xstudent/old_student_confirm_delete.html', {'old_student': old_student})


# Attendance Views
@login_required
def attendance_list(request):
    """List view for attendance records with filtering"""
    queryset = Attendance.objects.select_related('student').all()
    form = AttendanceFilterForm(request.GET)
    
    if form.is_valid():
        student = form.cleaned_data.get('student')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        status = form.cleaned_data.get('status')
        grade = form.cleaned_data.get('grade')
        program = form.cleaned_data.get('program')
        
        if student:
            queryset = queryset.filter(student=student)
        
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
            
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        
        if status:
            queryset = queryset.filter(status=status)
            
        if grade:
            queryset = queryset.filter(student__grade__icontains=grade)
            
        if program:
            queryset = queryset.filter(student__program__icontains=program)
    
    queryset = queryset.order_by('-date', '-created_at')
    
    # Pagination
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    stats = {
        'total_records': Attendance.objects.count(),
        'present_today': Attendance.objects.filter(date=date.today(), status='present').count(),
        'absent_today': Attendance.objects.filter(date=date.today(), status='absent').count(),
        'late_today': Attendance.objects.filter(date=date.today(), status='late').count(),
    }
    
    context = {
        'attendances': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'filter_form': form,
        'stats': stats,
    }
    return render(request, 'xstudent/attendance_list.html', context)


@login_required
def attendance_create(request):
    """Create view for individual attendance record"""
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.recorded_by = request.user
            attendance.save()
            messages.success(request, f'Attendance recorded for {attendance.student.student_name} on {attendance.date}')
            return redirect('attendance_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = AttendanceForm()
    
    return render(request, 'xstudent/attendance_form.html', {'form': form})


@login_required
def attendance_bulk_create(request):
    """Bulk attendance recording view"""
    if request.method == 'POST':
        form = BulkAttendanceForm(request.POST)
        if form.is_valid():
            attendance_date = form.cleaned_data['date']
            grade = form.cleaned_data.get('grade')
            program = form.cleaned_data.get('program')
            default_status = form.cleaned_data['default_status']
            default_time_in = form.cleaned_data.get('default_time_in')
            
            # Get students based on filters
            students = NewStudent.objects.filter(status='active')
            if grade:
                students = students.filter(grade__icontains=grade)
            if program:
                students = students.filter(program__icontains=program)
            
            # Process individual attendance records from form
            created_count = 0
            updated_count = 0
            
            for student in students:
                student_status = request.POST.get(f'status_{student.id}', default_status)
                student_time_in = request.POST.get(f'time_in_{student.id}') or default_time_in
                student_notes = request.POST.get(f'notes_{student.id}', '')
                
                # Check if attendance already exists
                attendance, created = Attendance.objects.get_or_create(
                    student=student,
                    date=attendance_date,
                    defaults={
                        'status': student_status,
                        'time_in': student_time_in,
                        'notes': student_notes,
                        'recorded_by': request.user
                    }
                )
                
                if created:
                    created_count += 1
                else:
                    # Update existing record
                    attendance.status = student_status
                    attendance.time_in = student_time_in
                    attendance.notes = student_notes
                    attendance.recorded_by = request.user
                    attendance.save()
                    updated_count += 1
            
            messages.success(request, f'Bulk attendance completed: {created_count} created, {updated_count} updated')
            return redirect('attendance_list')
    else:
        form = BulkAttendanceForm()
    
    # Get students for display
    students = NewStudent.objects.filter(status='active').order_by('student_name')
    
    # Apply filters if form is bound
    if request.GET:
        grade = request.GET.get('grade')
        program = request.GET.get('program')
        if grade:
            students = students.filter(grade__icontains=grade)
        if program:
            students = students.filter(program__icontains=program)
    
    context = {
        'form': form,
        'students': students,
    }
    return render(request, 'xstudent/attendance_bulk_form.html', context)


@login_required
def attendance_detail(request, pk):
    """Detail view for attendance record"""
    attendance = get_object_or_404(Attendance, pk=pk)
    return render(request, 'xstudent/attendance_detail.html', {'attendance': attendance})


@login_required
def attendance_update(request, pk):
    """Update view for attendance record"""
    attendance = get_object_or_404(Attendance, pk=pk)
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.recorded_by = request.user
            attendance.save()
            messages.success(request, f'Attendance updated for {attendance.student.student_name}')
            return redirect('attendance_detail', pk=attendance.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = AttendanceForm(instance=attendance)
    
    return render(request, 'xstudent/attendance_form.html', {'form': form, 'attendance': attendance})


@login_required
def attendance_delete(request, pk):
    """Delete view for attendance record"""
    attendance = get_object_or_404(Attendance, pk=pk)
    
    if request.method == 'POST':
        student_name = attendance.student.student_name
        attendance_date = attendance.date
        attendance.delete()
        messages.success(request, f'Attendance record for {student_name} on {attendance_date} has been deleted')
        return redirect('attendance_list')
    
    return render(request, 'xstudent/attendance_confirm_delete.html', {'attendance': attendance})


@login_required
def attendance_dashboard(request):
    """Attendance dashboard with statistics"""
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    
    # Today's statistics
    today_stats = {
        'total': NewStudent.objects.filter(status='active').count(),
        'present': Attendance.objects.filter(date=today, status='present').count(),
        'absent': Attendance.objects.filter(date=today, status='absent').count(),
        'late': Attendance.objects.filter(date=today, status='late').count(),
        'excused': Attendance.objects.filter(date=today, status='excused').count(),
    }
    today_stats['not_marked'] = today_stats['total'] - (
        today_stats['present'] + today_stats['absent'] + 
        today_stats['late'] + today_stats['excused']
    )
    
    # This week's statistics
    week_attendance = Attendance.objects.filter(date__gte=week_start, date__lte=today)
    week_stats = {
        'total_records': week_attendance.count(),
        'present': week_attendance.filter(status='present').count(),
        'absent': week_attendance.filter(status='absent').count(),
        'late': week_attendance.filter(status='late').count(),
        'excused': week_attendance.filter(status='excused').count(),
    }
    
    # This month's statistics
    month_attendance = Attendance.objects.filter(date__gte=month_start, date__lte=today)
    month_stats = {
        'total_records': month_attendance.count(),
        'present': month_attendance.filter(status='present').count(),
        'absent': month_attendance.filter(status='absent').count(),
        'late': month_attendance.filter(status='late').count(),
        'excused': month_attendance.filter(status='excused').count(),
    }
    
    # Recent attendance records
    recent_attendance = Attendance.objects.select_related('student').order_by('-created_at')[:10]
    
    # Students with perfect attendance this month
    perfect_attendance = []
    for student in NewStudent.objects.filter(status='active'):
        student_month_attendance = month_attendance.filter(student=student)
        total_days = student_month_attendance.count()
        present_days = student_month_attendance.filter(status='present').count()
        if total_days > 0 and present_days == total_days:
            perfect_attendance.append(student)
    
    # Students with concerning attendance (less than 80% this month)
    concerning_attendance = []
    for student in NewStudent.objects.filter(status='active'):
        student_month_attendance = month_attendance.filter(student=student)
        total_days = student_month_attendance.count()
        present_days = student_month_attendance.filter(status='present').count()
        if total_days > 0:
            attendance_rate = (present_days / total_days) * 100
            if attendance_rate < 80:
                concerning_attendance.append({
                    'student': student,
                    'rate': round(attendance_rate, 1),
                    'present_days': present_days,
                    'total_days': total_days
                })
    
    context = {
        'today_stats': today_stats,
        'week_stats': week_stats,
        'month_stats': month_stats,
        'recent_attendance': recent_attendance,
        'perfect_attendance': perfect_attendance[:5],  # Top 5
        'concerning_attendance': concerning_attendance[:5],  # Top 5
        'today': today,
    }
    return render(request, 'xstudent/attendance_dashboard.html', context)


@login_required
def attendance_report(request):
    """Generate attendance reports"""
    if request.method == 'POST':
        form = AttendanceReportForm(request.POST)
        if form.is_valid():
            report_type = form.cleaned_data['report_type']
            date_from = form.cleaned_data.get('date_from')
            date_to = form.cleaned_data.get('date_to')
            students = form.cleaned_data.get('students')
            include_summary = form.cleaned_data.get('include_summary', False)
            
            # Calculate date range based on report type
            today = date.today()
            if report_type == 'daily':
                date_from = date_to = today
            elif report_type == 'weekly':
                date_from = today - timedelta(days=today.weekday())
                date_to = today
            elif report_type == 'monthly':
                date_from = today.replace(day=1)
                date_to = today
            
            # Get attendance data
            attendance_qs = Attendance.objects.filter(date__gte=date_from, date__lte=date_to)
            if students:
                attendance_qs = attendance_qs.filter(student__in=students)
            
            attendance_data = attendance_qs.select_related('student').order_by('date', 'student__student_name')
            
            # Generate CSV report
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="attendance_report_{date_from}_{date_to}.csv"'
            
            writer = csv.writer(response)
            
            # Header
            writer.writerow([
                'Date', 'Student Name', 'Grade', 'Program', 'Status', 
                'Time In', 'Time Out', 'Notes', 'Recorded By'
            ])
            
            # Data rows
            for attendance in attendance_data:
                writer.writerow([
                    attendance.date,
                    attendance.student.student_name,
                    attendance.student.grade,
                    attendance.student.program,
                    attendance.get_status_display(),
                    attendance.time_in or '',
                    attendance.time_out or '',
                    attendance.notes,
                    attendance.recorded_by.username if attendance.recorded_by else ''
                ])
            
            # Summary if requested
            if include_summary:
                writer.writerow([])  # Empty row
                writer.writerow(['SUMMARY STATISTICS'])
                writer.writerow(['Status', 'Count', 'Percentage'])
                
                total_records = attendance_data.count()
                if total_records > 0:
                    for status, display in Attendance.ATTENDANCE_STATUS_CHOICES:
                        count = attendance_data.filter(status=status).count()
                        percentage = (count / total_records) * 100
                        writer.writerow([display, count, f'{percentage:.1f}%'])
            
            return response
    else:
        form = AttendanceReportForm()
    
    return render(request, 'xstudent/attendance_report.html', {'form': form})
