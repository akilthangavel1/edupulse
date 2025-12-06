from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count
from .models import StudentCertificate
from .forms import StudentCertificateForm, CertificateSearchForm, BulkCertificateForm


def is_staff_user(user):
    """Check if user is staff"""
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_staff_user)
def certificate_dashboard(request):
    """Simple certificate dashboard"""
    total_certificates = StudentCertificate.objects.count()
    recent_certificates = StudentCertificate.objects.select_related(
        'student', 'course'
    ).order_by('-created_at')[:10]
    
    # Certificates by course
    by_course = StudentCertificate.objects.values(
        'course__name'
    ).annotate(count=Count('id')).order_by('-count')[:5]
    
    context = {
        'total_certificates': total_certificates,
        'recent_certificates': recent_certificates,
        'by_course': by_course,
    }
    return render(request, 'xcertificate/dashboard.html', context)


@login_required
@user_passes_test(is_staff_user)
def certificate_list(request):
    """List all certificates with filtering"""
    certificates = StudentCertificate.objects.select_related(
        'student', 'course', 'issued_by'
    ).all()
    
    # Search and filter
    search_form = CertificateSearchForm(request.GET)
    
    if search_form.is_valid():
        if search_form.cleaned_data.get('student_name'):
            certificates = certificates.filter(
                student__student_name__icontains=search_form.cleaned_data['student_name']
            )
        
        if search_form.cleaned_data.get('certificate_number'):
            certificates = certificates.filter(
                certificate_number__icontains=search_form.cleaned_data['certificate_number']
            )
        
        if search_form.cleaned_data.get('course'):
            certificates = certificates.filter(course=search_form.cleaned_data['course'])
        
        if search_form.cleaned_data.get('date_from'):
            certificates = certificates.filter(issue_date__gte=search_form.cleaned_data['date_from'])
        
        if search_form.cleaned_data.get('date_to'):
            certificates = certificates.filter(issue_date__lte=search_form.cleaned_data['date_to'])
    
    certificates = certificates.order_by('-issue_date', '-created_at')
    
    context = {
        'certificates': certificates,
        'search_form': search_form,
    }
    return render(request, 'xcertificate/certificate_list.html', context)


@login_required
@user_passes_test(is_staff_user)
def certificate_create(request):
    """Record a new certificate"""
    if request.method == 'POST':
        form = StudentCertificateForm(request.POST)
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.issued_by = request.user
            certificate.save()
            
            messages.success(
                request, 
                f'Certificate {certificate.certificate_number} recorded successfully!'
            )
            return redirect('certificate_list')
    else:
        form = StudentCertificateForm()
    
    context = {
        'form': form,
        'title': 'Record New Certificate',
    }
    return render(request, 'xcertificate/certificate_form.html', context)


@login_required
@user_passes_test(is_staff_user)
def certificate_detail(request, pk):
    """View certificate details"""
    certificate = get_object_or_404(
        StudentCertificate.objects.select_related(
            'student', 'course', 'issued_by'
        ),
        pk=pk
    )
    
    context = {
        'certificate': certificate,
    }
    return render(request, 'xcertificate/certificate_detail.html', context)


@login_required
@user_passes_test(is_staff_user)
def certificate_edit(request, pk):
    """Edit an existing certificate record"""
    certificate = get_object_or_404(StudentCertificate, pk=pk)
    
    if request.method == 'POST':
        form = StudentCertificateForm(request.POST, instance=certificate)
        if form.is_valid():
            certificate = form.save()
            messages.success(request, f'Certificate {certificate.certificate_number} updated successfully!')
            return redirect('certificate_detail', pk=certificate.pk)
    else:
        form = StudentCertificateForm(instance=certificate)
    
    context = {
        'form': form,
        'certificate': certificate,
        'title': f'Edit Certificate {certificate.certificate_number}',
    }
    return render(request, 'xcertificate/certificate_form.html', context)


@login_required
@user_passes_test(is_staff_user)
def certificate_delete(request, pk):
    """Delete a certificate record"""
    certificate = get_object_or_404(StudentCertificate, pk=pk)
    
    if request.method == 'POST':
        cert_num = certificate.certificate_number
        certificate.delete()
        messages.success(request, f'Certificate {cert_num} deleted successfully.')
        return redirect('certificate_list')
    
    context = {
        'certificate': certificate,
    }
    return render(request, 'xcertificate/certificate_delete.html', context)


@login_required
@user_passes_test(is_staff_user)
def bulk_certificate_create(request):
    """Bulk record certificates for multiple students"""
    if request.method == 'POST':
        form = BulkCertificateForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            issue_date = form.cleaned_data['issue_date']
            remarks = form.cleaned_data.get('remarks', '')
            students = form.cleaned_data['students']
            
            created_count = 0
            for student in students:
                # Check if certificate already exists for this student/course
                if not StudentCertificate.objects.filter(
                    student=student, 
                    course=course,
                    issue_date=issue_date
                ).exists():
                    StudentCertificate.objects.create(
                        student=student,
                        course=course,
                        issue_date=issue_date,
                        remarks=remarks,
                        issued_by=request.user
                    )
                    created_count += 1
            
            messages.success(request, f'Successfully recorded {created_count} certificates!')
            return redirect('certificate_list')
    else:
        form = BulkCertificateForm()
    
    context = {
        'form': form,
        'title': 'Bulk Record Certificates',
    }
    return render(request, 'xcertificate/bulk_certificate_form.html', context)
