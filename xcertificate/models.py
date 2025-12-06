from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
import hashlib
import uuid
from xstudent.models import NewStudent
from xcoursefee.models import Course


class CertificateTemplate(models.Model):
    """Templates for different types of certificates"""
    
    TEMPLATE_TYPE_CHOICES = [
        ('completion', 'Course Completion'),
        ('achievement', 'Achievement Certificate'),
        ('participation', 'Participation Certificate'),
        ('excellence', 'Certificate of Excellence'),
        ('merit', 'Certificate of Merit'),
        ('attendance', 'Perfect Attendance'),
        ('custom', 'Custom Certificate'),
    ]
    
    ORIENTATION_CHOICES = [
        ('portrait', 'Portrait'),
        ('landscape', 'Landscape'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200, verbose_name="Template Name")
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPE_CHOICES, verbose_name="Template Type")
    code = models.CharField(max_length=20, unique=True, verbose_name="Template Code")
    description = models.TextField(blank=True, verbose_name="Description")
    
    # Design Settings
    orientation = models.CharField(max_length=20, choices=ORIENTATION_CHOICES, default='landscape')
    border_style = models.CharField(max_length=100, blank=True, verbose_name="Border Style")
    background_image = models.ImageField(upload_to='certificate_templates/', blank=True, verbose_name="Background Image")
    
    # Content Settings
    header_text = models.CharField(max_length=200, default="Certificate of Completion", verbose_name="Header Text")
    subheader_text = models.CharField(max_length=200, blank=True, verbose_name="Subheader Text")
    body_text_template = models.TextField(
        verbose_name="Body Text Template",
        help_text="Use {student_name}, {course_name}, {completion_date}, {grade} as placeholders"
    )
    footer_text = models.TextField(blank=True, verbose_name="Footer Text")
    
    # Institution Information
    institution_name = models.CharField(max_length=200, default="Brillianz Institute", verbose_name="Institution Name")
    institution_logo = models.ImageField(upload_to='certificate_templates/', blank=True, verbose_name="Institution Logo")
    institution_seal = models.ImageField(upload_to='certificate_templates/', blank=True, verbose_name="Institution Seal")
    
    # Signature Fields
    show_signature_line = models.BooleanField(default=True, verbose_name="Show Signature Line")
    signature_count = models.PositiveIntegerField(default=2, verbose_name="Number of Signatures")
    
    # QR Code Settings
    include_qr_code = models.BooleanField(default=True, verbose_name="Include QR Code")
    qr_code_position = models.CharField(
        max_length=20,
        choices=[
            ('bottom_left', 'Bottom Left'),
            ('bottom_right', 'Bottom Right'),
            ('top_right', 'Top Right'),
        ],
        default='bottom_right',
        verbose_name="QR Code Position"
    )
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Active Template")
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_certificate_templates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['template_type', 'name']
        verbose_name = 'Certificate Template'
        verbose_name_plural = 'Certificate Templates'
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def get_certificates_count(self):
        """Get count of certificates using this template"""
        return self.certificates.count()


class CertificateSignatory(models.Model):
    """Authorized signatories for certificates"""
    
    POSITION_CHOICES = [
        ('director', 'Director'),
        ('principal', 'Principal'),
        ('coordinator', 'Academic Coordinator'),
        ('hod', 'Head of Department'),
        ('ceo', 'CEO'),
        ('manager', 'Manager'),
        ('other', 'Other'),
    ]
    
    # Signatory Information
    name = models.CharField(max_length=100, verbose_name="Full Name")
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, verbose_name="Position")
    custom_position = models.CharField(max_length=100, blank=True, verbose_name="Custom Position Title")
    
    # Signature
    signature_image = models.ImageField(upload_to='certificate_signatures/', verbose_name="Signature Image")
    
    # Contact Information
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone")
    
    # Display Settings
    display_order = models.PositiveIntegerField(default=1, verbose_name="Display Order")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Certificate Signatory'
        verbose_name_plural = 'Certificate Signatories'
    
    def __str__(self):
        position = self.custom_position if self.custom_position else self.get_position_display()
        return f"{self.name} - {position}"
    
    def get_position_title(self):
        """Get the position title to display"""
        return self.custom_position if self.custom_position else self.get_position_display()


class StudentCertificate(models.Model):
    """Student certificates - manually issued"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('issued', 'Issued'),
        ('printed', 'Printed'),
        ('collected', 'Collected by Student'),
        ('revoked', 'Revoked'),
        ('expired', 'Expired'),
    ]
    
    GRADE_CHOICES = [
        ('distinction', 'Distinction'),
        ('first_class', 'First Class'),
        ('second_class', 'Second Class'),
        ('pass', 'Pass'),
        ('completed', 'Completed'),
        ('', 'Not Applicable'),
    ]
    
    # Certificate Identification
    certificate_number = models.CharField(max_length=50, unique=True, verbose_name="Certificate Number")
    verification_code = models.CharField(max_length=64, unique=True, verbose_name="Verification Code")
    qr_code_data = models.TextField(blank=True, verbose_name="QR Code Data")
    
    # Student and Course Information
    student = models.ForeignKey(NewStudent, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    template = models.ForeignKey(CertificateTemplate, on_delete=models.SET_NULL, null=True, related_name='certificates')
    
    # Certificate Details
    issue_date = models.DateField(verbose_name="Issue Date")
    completion_date = models.DateField(verbose_name="Course Completion Date")
    valid_from = models.DateField(null=True, blank=True, verbose_name="Valid From")
    valid_until = models.DateField(null=True, blank=True, verbose_name="Valid Until")
    
    # Performance Details
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES, blank=True, verbose_name="Grade/Result")
    percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Percentage"
    )
    duration_hours = models.PositiveIntegerField(null=True, blank=True, verbose_name="Course Duration (Hours)")
    
    # Status and Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Issuance Information
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='issued_certificates')
    issued_at = models.DateTimeField(null=True, blank=True, verbose_name="Issued At")
    
    # Signatories
    signatories = models.ManyToManyField(CertificateSignatory, blank=True, verbose_name="Signatories")
    
    # Collection Tracking
    printed_date = models.DateField(null=True, blank=True, verbose_name="Printed Date")
    collected_date = models.DateField(null=True, blank=True, verbose_name="Collection Date")
    collected_by = models.CharField(max_length=100, blank=True, verbose_name="Collected By")
    collection_remarks = models.TextField(blank=True, verbose_name="Collection Remarks")
    
    # Revocation
    revoked_date = models.DateField(null=True, blank=True, verbose_name="Revoked Date")
    revoked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='revoked_certificates')
    revocation_reason = models.TextField(blank=True, verbose_name="Revocation Reason")
    
    # Additional Information
    remarks = models.TextField(blank=True, verbose_name="Internal Remarks")
    custom_text = models.TextField(blank=True, verbose_name="Custom Text (Optional)")
    
    # File Storage
    certificate_pdf = models.FileField(upload_to='certificates/pdfs/', blank=True, verbose_name="Certificate PDF")
    certificate_image = models.ImageField(upload_to='certificates/images/', blank=True, verbose_name="Certificate Image")
    
    # Verification Statistics
    verification_count = models.PositiveIntegerField(default=0, verbose_name="Times Verified")
    last_verified = models.DateTimeField(null=True, blank=True, verbose_name="Last Verified")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-issue_date', '-created_at']
        unique_together = ['student', 'course', 'issue_date']
        verbose_name = 'Student Certificate'
        verbose_name_plural = 'Student Certificates'
    
    def __str__(self):
        return f"{self.certificate_number} - {self.student.student_name} - {self.course.name}"
    
    def save(self, *args, **kwargs):
        # Generate certificate number if not exists
        if not self.certificate_number:
            year = timezone.now().year
            # Get the last certificate for this year
            last_cert = StudentCertificate.objects.filter(
                certificate_number__startswith=f'CERT/{year}/'
            ).order_by('-certificate_number').first()
            
            if last_cert:
                # Extract number and increment
                last_num = int(last_cert.certificate_number.split('/')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            
            self.certificate_number = f'CERT/{year}/{new_num:04d}'
        
        # Generate verification code if not exists
        if not self.verification_code:
            unique_string = f"{self.certificate_number}{self.student.id}{timezone.now().timestamp()}"
            self.verification_code = hashlib.sha256(unique_string.encode()).hexdigest()
        
        # Set issued_at when status changes to issued
        if self.status == 'issued' and not self.issued_at:
            self.issued_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('certificate_detail', kwargs={'pk': self.pk})
    
    def get_verification_url(self):
        """Get public verification URL"""
        return f"/verify-certificate/{self.verification_code}/"
    
    def is_valid(self):
        """Check if certificate is currently valid"""
        if self.status == 'revoked':
            return False
        
        if self.valid_until:
            return timezone.now().date() <= self.valid_until
        
        return self.status == 'issued'
    
    def is_expired(self):
        """Check if certificate has expired"""
        if self.valid_until:
            return timezone.now().date() > self.valid_until
        return False
    
    def get_status_color(self):
        """Get Bootstrap color class for status"""
        colors = {
            'draft': 'secondary',
            'issued': 'success',
            'printed': 'info',
            'collected': 'primary',
            'revoked': 'danger',
            'expired': 'warning'
        }
        return colors.get(self.status, 'secondary')
    
    def increment_verification_count(self):
        """Increment verification counter"""
        self.verification_count += 1
        self.last_verified = timezone.now()
        self.save(update_fields=['verification_count', 'last_verified'])


class CertificateVerification(models.Model):
    """Log of certificate verification attempts"""
    
    VERIFICATION_METHOD_CHOICES = [
        ('number', 'Certificate Number'),
        ('qr_code', 'QR Code'),
        ('verification_code', 'Verification Code'),
        ('student_search', 'Student Search'),
    ]
    
    VERIFICATION_RESULT_CHOICES = [
        ('valid', 'Valid Certificate'),
        ('invalid', 'Invalid/Not Found'),
        ('revoked', 'Revoked'),
        ('expired', 'Expired'),
    ]
    
    # Certificate Information
    certificate = models.ForeignKey(
        StudentCertificate, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='verification_logs'
    )
    
    # Verification Details
    verification_method = models.CharField(max_length=20, choices=VERIFICATION_METHOD_CHOICES)
    search_query = models.CharField(max_length=200, verbose_name="Search Query")
    verification_result = models.CharField(max_length=20, choices=VERIFICATION_RESULT_CHOICES)
    
    # Requester Information
    ip_address = models.GenericIPAddressField(verbose_name="IP Address")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    country = models.CharField(max_length=100, blank=True, verbose_name="Country")
    city = models.CharField(max_length=100, blank=True, verbose_name="City")
    
    # Additional Information
    verified_by_name = models.CharField(max_length=100, blank=True, verbose_name="Verified By (Name)")
    organization = models.CharField(max_length=200, blank=True, verbose_name="Organization")
    purpose = models.TextField(blank=True, verbose_name="Verification Purpose")
    
    # Response Information
    response_time_ms = models.PositiveIntegerField(null=True, blank=True, verbose_name="Response Time (ms)")
    
    # Metadata
    verified_at = models.DateTimeField(auto_now_add=True, verbose_name="Verified At")
    
    class Meta:
        ordering = ['-verified_at']
        verbose_name = 'Certificate Verification'
        verbose_name_plural = 'Certificate Verifications'
        indexes = [
            models.Index(fields=['certificate', 'verified_at']),
            models.Index(fields=['verification_result', 'verified_at']),
            models.Index(fields=['ip_address']),
        ]
    
    def __str__(self):
        cert_num = self.certificate.certificate_number if self.certificate else self.search_query
        return f"{cert_num} - {self.get_verification_result_display()} - {self.verified_at.strftime('%Y-%m-%d %H:%M')}"
    
    def is_successful(self):
        """Check if verification was successful"""
        return self.verification_result == 'valid'


class CertificateBatch(models.Model):
    """Batch processing of certificates for bulk issuance"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    # Batch Information
    batch_id = models.CharField(max_length=20, unique=True, verbose_name="Batch ID")
    batch_name = models.CharField(max_length=200, verbose_name="Batch Name")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificate_batches')
    template = models.ForeignKey(CertificateTemplate, on_delete=models.SET_NULL, null=True)
    
    # Batch Details
    total_students = models.PositiveIntegerField(default=0, verbose_name="Total Students")
    processed_count = models.PositiveIntegerField(default=0, verbose_name="Processed Count")
    success_count = models.PositiveIntegerField(default=0, verbose_name="Success Count")
    failed_count = models.PositiveIntegerField(default=0, verbose_name="Failed Count")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Processing Information
    started_at = models.DateTimeField(null=True, blank=True, verbose_name="Started At")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Completed At")
    error_log = models.TextField(blank=True, verbose_name="Error Log")
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Certificate Batch'
        verbose_name_plural = 'Certificate Batches'
    
    def __str__(self):
        return f"{self.batch_id} - {self.batch_name} - {self.get_status_display()}"
    
    def get_progress_percentage(self):
        """Calculate batch processing progress"""
        if self.total_students > 0:
            return (self.processed_count / self.total_students) * 100
        return 0
