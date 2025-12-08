from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.forms import formset_factory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from datetime import datetime, date

from .models import Subject, AssessmentType, StudentMark, GradeScale, StudentGradeSummary
from .forms import (
    SubjectForm, AssessmentTypeForm, StudentMarkForm, BulkMarkEntryForm,
    GradeScaleForm, MarkSearchForm, StudentReportForm, SubjectSearchForm
)
from xstudent.models import NewStudent
from xcoursefee.models import Course, StudentEnrollment
from .email_notifications import send_marks_published_notification, send_marks_updated_notification


# Dashboard View
@login_required
def marks_dashboard(request):
    """Main dashboard for marks module"""
    
    # Statistics
    total_subjects = Subject.objects.filter(is_active=True).count()
    total_students = NewStudent.objects.filter(status='active').count()
    total_marks = StudentMark.objects.filter(is_active=True).count()
    pending_marks = StudentMark.objects.filter(status='draft', is_active=True).count()
    
    # Recent marks
    recent_marks = StudentMark.objects.select_related(
        'student', 'subject', 'assessment_type'
    ).filter(is_active=True).order_by('-created_at')[:10]
    
    # Assessment type statistics
    assessment_stats = AssessmentType.objects.annotate(
        mark_count=Count('marks', filter=Q(marks__is_active=True))
    ).filter(is_active=True)
    
    # Grade distribution
    grade_distribution = StudentMark.objects.filter(
        is_active=True, 
        status='published'
    ).values('grade').annotate(count=Count('id')).order_by('grade')
    
    context = {
        'total_subjects': total_subjects,
        'total_students': total_students,
        'total_marks': total_marks,
        'pending_marks': pending_marks,
        'recent_marks': recent_marks,
        'assessment_stats': assessment_stats,
        'grade_distribution': grade_distribution,
    }
    
    return render(request, 'xmark/dashboard.html', context)


# Subject Views
@login_required
def subject_list(request):
    """List all subjects with search functionality"""
    form = SubjectSearchForm(request.GET)
    subjects = Subject.objects.select_related('course').all()
    
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        course = form.cleaned_data.get('course')
        is_active = form.cleaned_data.get('is_active')
        
        if search_query:
            subjects = subjects.filter(
                Q(name__icontains=search_query) | 
                Q(code__icontains=search_query) |
                Q(instructor__icontains=search_query)
            )
        
        if course:
            subjects = subjects.filter(course=course)
        
        if is_active == 'true':
            subjects = subjects.filter(is_active=True)
        elif is_active == 'false':
            subjects = subjects.filter(is_active=False)
    
    # Pagination
    paginator = Paginator(subjects, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'subjects': page_obj,
    }
    
    return render(request, 'xmark/subject_list.html', context)


@login_required
def subject_create(request):
    """Create new subject"""
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save()
            messages.success(request, f'Subject "{subject.name}" created successfully!')
            return redirect('subject_list')
    else:
        form = SubjectForm()
    
    return render(request, 'xmark/subject_form.html', {
        'form': form,
        'title': 'Create Subject'
    })


@login_required
def subject_edit(request, pk):
    """Edit existing subject"""
    subject = get_object_or_404(Subject, pk=pk)
    
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            subject = form.save()
            messages.success(request, f'Subject "{subject.name}" updated successfully!')
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)
    
    return render(request, 'xmark/subject_form.html', {
        'form': form,
        'subject': subject,
        'title': 'Edit Subject'
    })


@login_required
def subject_detail(request, pk):
    """Subject detail view with related marks"""
    subject = get_object_or_404(Subject, pk=pk)
    
    # Get marks for this subject
    marks = StudentMark.objects.select_related(
        'student', 'assessment_type'
    ).filter(subject=subject, is_active=True).order_by('-assessment_date')
    
    # Statistics
    total_marks = marks.count()
    average_marks = marks.aggregate(avg=Avg('percentage'))['avg'] or 0
    grade_dist = marks.values('grade').annotate(count=Count('id')).order_by('grade')
    
    # Recent marks
    recent_marks = marks[:10]
    
    context = {
        'subject': subject,
        'total_marks': total_marks,
        'average_marks': round(average_marks, 2),
        'grade_distribution': grade_dist,
        'recent_marks': recent_marks,
    }
    
    return render(request, 'xmark/subject_detail.html', context)


# Student Mark Views
@login_required
def mark_list(request):
    """List all marks with search and filtering"""
    form = MarkSearchForm(request.GET)
    marks = StudentMark.objects.select_related(
        'student', 'subject', 'assessment_type'
    ).filter(is_active=True)
    
    if form.is_valid():
        student = form.cleaned_data.get('student')
        subject = form.cleaned_data.get('subject')
        assessment_type = form.cleaned_data.get('assessment_type')
        status = form.cleaned_data.get('status')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        grade = form.cleaned_data.get('grade')
        
        if student:
            marks = marks.filter(student=student)
        if subject:
            marks = marks.filter(subject=subject)
        if assessment_type:
            marks = marks.filter(assessment_type=assessment_type)
        if status:
            marks = marks.filter(status=status)
        if date_from:
            marks = marks.filter(assessment_date__gte=date_from)
        if date_to:
            marks = marks.filter(assessment_date__lte=date_to)
        if grade:
            marks = marks.filter(grade__icontains=grade)
    
    marks = marks.order_by('-assessment_date', '-created_at')
    
    # Pagination
    paginator = Paginator(marks, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'marks': page_obj,
    }
    
    return render(request, 'xmark/mark_list.html', context)


@login_required
def mark_create(request):
    """Create new mark entry"""
    course_id = request.GET.get('course_id')
    
    if request.method == 'POST':
        form = StudentMarkForm(request.POST, course_id=course_id)
        if form.is_valid():
            mark = form.save(commit=False)
            mark.entered_by = request.user
            mark.save()
            
            # Send email notification if mark is published
            send_email = request.POST.get('send_email', 'on') == 'on'
            if send_email and mark.status == 'published':
                if send_marks_published_notification(mark):
                    messages.success(request, 'Mark entry created and published successfully! Email notification sent to parents.')
                else:
                    messages.success(request, 'Mark entry created successfully! However, email notification could not be sent.')
            else:
                messages.success(request, 'Mark entry created successfully!')
            
            return redirect('mark_list')
    else:
        form = StudentMarkForm(course_id=course_id)
    
    return render(request, 'xmark/mark_form.html', {
        'form': form,
        'title': 'Create Mark Entry'
    })


@login_required
def mark_edit(request, pk):
    """Edit existing mark"""
    mark = get_object_or_404(StudentMark, pk=pk)
    original_status = mark.status
    
    if request.method == 'POST':
        form = StudentMarkForm(request.POST, instance=mark)
        if form.is_valid():
            mark = form.save()
            
            # Send email notification if mark is newly published or updated while published
            send_email = request.POST.get('send_email', 'on') == 'on'
            if send_email and mark.status == 'published':
                if original_status != 'published':
                    # Newly published
                    if send_marks_published_notification(mark):
                        messages.success(request, 'Mark updated and published successfully! Email notification sent to parents.')
                    else:
                        messages.success(request, 'Mark updated successfully! However, email notification could not be sent.')
                else:
                    # Updated while published
                    if send_marks_updated_notification(mark):
                        messages.success(request, 'Mark updated successfully! Update notification sent to parents.')
                    else:
                        messages.success(request, 'Mark updated successfully! However, email notification could not be sent.')
            else:
                messages.success(request, 'Mark updated successfully!')
            
            return redirect('mark_list')
    else:
        form = StudentMarkForm(instance=mark)
    
    return render(request, 'xmark/mark_form.html', {
        'form': form,
        'mark': mark,
        'title': 'Edit Mark Entry'
    })


@login_required
def mark_detail(request, pk):
    """Mark detail view"""
    mark = get_object_or_404(StudentMark, pk=pk)
    
    # Get other marks for same student and subject
    related_marks = StudentMark.objects.filter(
        student=mark.student,
        subject=mark.subject,
        is_active=True
    ).exclude(pk=pk).order_by('-assessment_date')
    
    context = {
        'mark': mark,
        'related_marks': related_marks,
    }
    
    return render(request, 'xmark/mark_detail.html', context)


@login_required
def mark_resend_email(request, pk):
    """Resend email notification for a published mark"""
    mark = get_object_or_404(StudentMark, pk=pk)
    
    if mark.status != 'published':
        messages.warning(request, 'Email notifications are only sent for published marks.')
        return redirect('mark_detail', pk=pk)
    
    if send_marks_published_notification(mark):
        messages.success(request, f'Email notification resent successfully to parents of {mark.student.student_name}!')
    else:
        messages.error(request, 'Failed to send email notification. Please check parent email addresses.')
    
    return redirect('mark_detail', pk=pk)


@login_required
def bulk_mark_entry(request):
    """Bulk mark entry for multiple students"""
    course_id = request.GET.get('course_id')
    
    if request.method == 'POST':
        form = BulkMarkEntryForm(request.POST, course_id=course_id)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            assessment_type = form.cleaned_data['assessment_type']
            total_marks = form.cleaned_data['total_marks']
            assessment_date = form.cleaned_data['assessment_date']
            
            # Get students enrolled in the course
            enrolled_students = NewStudent.objects.filter(
                course_enrollments__course=subject.course,
                course_enrollments__status='active',
                status='active'
            ).distinct()
            
            # Process individual mark entries
            created_count = 0
            for student in enrolled_students:
                student_marks = request.POST.get(f'marks_{student.id}')
                if student_marks:
                    try:
                        marks_obtained = float(student_marks)
                        
                        # Check if mark already exists
                        existing_mark = StudentMark.objects.filter(
                            student=student,
                            subject=subject,
                            assessment_type=assessment_type,
                            assessment_date=assessment_date
                        ).first()
                        
                        if not existing_mark:
                            StudentMark.objects.create(
                                student=student,
                                subject=subject,
                                assessment_type=assessment_type,
                                marks_obtained=marks_obtained,
                                total_marks=total_marks,
                                assessment_date=assessment_date,
                                entered_by=request.user,
                                status='draft'
                            )
                            created_count += 1
                    except ValueError:
                        continue
            
            messages.success(request, f'Successfully created {created_count} mark entries!')
            return redirect('mark_list')
    else:
        form = BulkMarkEntryForm(course_id=course_id)
    
    # Get students for bulk entry
    students = []
    if course_id:
        students = NewStudent.objects.filter(
            course_enrollments__course_id=course_id,
            course_enrollments__status='active',
            status='active'
        ).distinct().order_by('student_name')
    
    context = {
        'form': form,
        'students': students,
        'title': 'Bulk Mark Entry'
    }
    
    return render(request, 'xmark/bulk_mark_entry.html', context)


# Assessment Type Views
@login_required
def assessment_type_list(request):
    """List all assessment types"""
    assessment_types = AssessmentType.objects.all().order_by('category', 'weight_percentage')
    
    context = {
        'assessment_types': assessment_types,
    }
    
    return render(request, 'xmark/assessment_type_list.html', context)


@login_required
def assessment_type_create(request):
    """Create new assessment type"""
    if request.method == 'POST':
        form = AssessmentTypeForm(request.POST)
        if form.is_valid():
            assessment_type = form.save()
            messages.success(request, f'Assessment type "{assessment_type.name}" created successfully!')
            return redirect('assessment_type_list')
    else:
        form = AssessmentTypeForm()
    
    return render(request, 'xmark/assessment_type_form.html', {
        'form': form,
        'title': 'Create Assessment Type'
    })


@login_required
def assessment_type_edit(request, pk):
    """Edit existing assessment type"""
    assessment_type = get_object_or_404(AssessmentType, pk=pk)
    
    if request.method == 'POST':
        form = AssessmentTypeForm(request.POST, instance=assessment_type)
        if form.is_valid():
            assessment_type = form.save()
            messages.success(request, f'Assessment type "{assessment_type.name}" updated successfully!')
            return redirect('assessment_type_list')
    else:
        form = AssessmentTypeForm(instance=assessment_type)
    
    return render(request, 'xmark/assessment_type_form.html', {
        'form': form,
        'assessment_type': assessment_type,
        'title': 'Edit Assessment Type'
    })


# Grade Scale Views
@login_required
def grade_scale_list(request):
    """List all grade scales"""
    grade_scales = GradeScale.objects.filter(is_active=True).order_by('-min_percentage')
    
    context = {
        'grade_scales': grade_scales,
    }
    
    return render(request, 'xmark/grade_scale_list.html', context)


@login_required
def grade_scale_create(request):
    """Create new grade scale"""
    if request.method == 'POST':
        form = GradeScaleForm(request.POST)
        if form.is_valid():
            grade_scale = form.save()
            messages.success(request, f'Grade scale "{grade_scale.grade}" created successfully!')
            return redirect('grade_scale_list')
    else:
        form = GradeScaleForm()
    
    return render(request, 'xmark/grade_scale_form.html', {
        'form': form,
        'title': 'Create Grade Scale'
    })


@login_required
def grade_scale_edit(request, pk):
    """Edit existing grade scale"""
    grade_scale = get_object_or_404(GradeScale, pk=pk)
    
    if request.method == 'POST':
        form = GradeScaleForm(request.POST, instance=grade_scale)
        if form.is_valid():
            grade_scale = form.save()
            messages.success(request, f'Grade scale "{grade_scale.grade}" updated successfully!')
            return redirect('grade_scale_list')
    else:
        form = GradeScaleForm(instance=grade_scale)
    
    return render(request, 'xmark/grade_scale_form.html', {
        'form': form,
        'grade_scale': grade_scale,
        'title': 'Edit Grade Scale'
    })


# Student Report Views
@login_required
def student_report(request):
    """Generate individual student report"""
    form = StudentReportForm(request.GET)
    report_data = None
    
    if form.is_valid():
        student = form.cleaned_data['student']
        semester = form.cleaned_data.get('semester')
        academic_year = form.cleaned_data.get('academic_year')
        include_drafts = form.cleaned_data.get('include_drafts', False)
        
        # Build query
        marks_query = Q(student=student, is_active=True)
        if not include_drafts:
            marks_query &= Q(status='published')
        
        marks = StudentMark.objects.select_related(
            'subject', 'assessment_type'
        ).filter(marks_query).order_by('subject', '-assessment_date')
        
        # Group by subject
        subjects_data = {}
        for mark in marks:
            subject_key = mark.subject.id
            if subject_key not in subjects_data:
                subjects_data[subject_key] = {
                    'subject': mark.subject,
                    'marks': [],
                    'total_obtained': 0,
                    'total_possible': 0,
                }
            subjects_data[subject_key]['marks'].append(mark)
            subjects_data[subject_key]['total_obtained'] += mark.marks_obtained
            subjects_data[subject_key]['total_possible'] += mark.total_marks
        
        # Calculate averages
        for subject_id, data in subjects_data.items():
            if data['total_possible'] > 0:
                data['percentage'] = round((data['total_obtained'] / data['total_possible']) * 100, 2)
            else:
                data['percentage'] = 0
        
        report_data = {
            'student': student,
            'subjects_data': subjects_data,
            'semester': semester,
            'academic_year': academic_year,
            'generated_at': datetime.now()
        }
    
    context = {
        'form': form,
        'report_data': report_data,
    }
    
    return render(request, 'xmark/student_report.html', context)


# AJAX Views
@login_required
@require_http_methods(["GET"])
def get_subjects_by_course(request):
    """AJAX view to get subjects by course"""
    course_id = request.GET.get('course_id')
    subjects = Subject.objects.filter(course_id=course_id, is_active=True).values('id', 'name', 'code')
    return JsonResponse({'subjects': list(subjects)})


@login_required
@require_http_methods(["GET"])
def get_students_by_course(request):
    """AJAX view to get students enrolled in a course"""
    course_id = request.GET.get('course_id')
    students = NewStudent.objects.filter(
        course_enrollments__course_id=course_id,
        course_enrollments__status='active',
        status='active'
    ).distinct().values('id', 'student_name')
    return JsonResponse({'students': list(students)})


@login_required
@require_http_methods(["POST"])
def mark_status_update(request, pk):
    """AJAX view to update mark status"""
    mark = get_object_or_404(StudentMark, pk=pk)
    new_status = request.POST.get('status')
    
    if new_status in dict(StudentMark.STATUS_CHOICES):
        mark.status = new_status
        if new_status == 'published' and not mark.verified_by:
            mark.verified_by = request.user
        mark.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Mark status updated to {mark.get_status_display()}',
            'new_status': mark.status,
            'status_display': mark.get_status_display()
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid status'})


# Utility Views
@login_required
def calculate_grade_summaries(request):
    """Recalculate all grade summaries"""
    if request.method == 'POST':
        # Get all unique student-subject combinations
        combinations = StudentMark.objects.filter(
            status='published', 
            is_active=True
        ).values('student', 'subject').distinct()
        
        updated_count = 0
        for combo in combinations:
            summary, created = StudentGradeSummary.objects.get_or_create(
                student_id=combo['student'],
                subject_id=combo['subject'],
                defaults={
                    'calculated_by': request.user,
                    'semester': 'Current',
                    'academic_year': str(date.today().year)
                }
            )
            
            summary.calculate_weighted_grade()
            updated_count += 1
        
        messages.success(request, f'Updated {updated_count} grade summaries!')
        return redirect('marks_dashboard')
    
    return render(request, 'xmark/calculate_summaries.html')
