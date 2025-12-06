from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import (
    CertificateTemplate, CertificateSignatory, StudentCertificate,
    CertificateVerification, CertificateBatch
)


@admin.register(CertificateTemplate)
class CertificateTemplateAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'name', 'template_type', 'orientation',
        'include_qr_code', 'is_active', 'get_certificates_count', 'created_at'
    ]
    list_filter = ['template_type', 'orientation', 'is_active', 'created_at']
    search_fields = ['name', 'code', 'description', 'header_text']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['created_by']
    
    fieldsets = (
        ('Template Information', {
            'fields': (
                ('code', 'name'),
                ('template_type', 'is_active'),
                ('description',),
            )
        }),
        ('Design Settings', {
            'fields': (
                ('orientation', 'border_style'),
                ('background_image',),
            )
        }),
        ('Content', {
            'fields': (
                ('header_text',),
                ('subheader_text',),
                ('body_text_template',),
                ('footer_text',),
            )
        }),
        ('Institution', {
            'fields': (
                ('institution_name',),
                ('institution_logo', 'institution_seal'),
            )
        }),
        ('Signature Settings', {
            'fields': (
                ('show_signature_line', 'signature_count'),
            )
        }),
        ('QR Code Settings', {
            'fields': (
                ('include_qr_code', 'qr_code_position'),
            )
        }),
        ('Metadata', {
            'fields': (
                ('created_by',),
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['template_type', 'name']
    
    # Custom actions
    actions = ['activate_templates', 'deactivate_templates']
    
    def activate_templates(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"Activated {queryset.count()} templates")
    activate_templates.short_description = "Activate selected templates"
    
    def deactivate_templates(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"Deactivated {queryset.count()} templates")
    deactivate_templates.short_description = "Deactivate selected templates"


@admin.register(CertificateSignatory)
class CertificateSignatoryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'get_position_display_custom', 'email',
        'display_order', 'is_active', 'created_at'
    ]
    list_filter = ['position', 'is_active', 'created_at']
    search_fields = ['name', 'custom_position', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Signatory Information', {
            'fields': (
                ('name', 'is_active'),
                ('position', 'custom_position'),
                ('display_order',),
            )
        }),
        ('Contact', {
            'fields': (
                ('email', 'phone'),
            )
        }),
        ('Signature', {
            'fields': (
                ('signature_image',),
            )
        }),
        ('Metadata', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['display_order', 'name']
    
    # Custom actions
    actions = ['activate_signatories', 'deactivate_signatories']
    
    def get_position_display_custom(self, obj):
        return obj.get_position_title()
    get_position_display_custom.short_description = "Position"
    
    def activate_signatories(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"Activated {queryset.count()} signatories")
    activate_signatories.short_description = "Activate selected signatories"
    
    def deactivate_signatories(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"Deactivated {queryset.count()} signatories")
    deactivate_signatories.short_description = "Deactivate selected signatories"


@admin.register(StudentCertificate)
class StudentCertificateAdmin(admin.ModelAdmin):
    list_display = [
        'certificate_number', 'student', 'course', 'grade',
        'issue_date', 'get_status_badge', 'is_valid', 'verification_count', 'issued_by'
    ]
    list_filter = [
        'status', 'grade', 'issue_date', 'template',
        'issued_at', 'created_at'
    ]
    search_fields = [
        'certificate_number', 'verification_code',
        'student__student_name', 'student__student_id',
        'course__name', 'remarks'
    ]
    readonly_fields = [
        'certificate_number', 'verification_code', 'issued_at',
        'verification_count', 'last_verified', 'created_at', 'updated_at',
        'get_verification_url_display'
    ]
    filter_horizontal = ['signatories']
    raw_id_fields = ['student', 'course', 'template', 'issued_by', 'revoked_by']
    date_hierarchy = 'issue_date'
    
    fieldsets = (
        ('Certificate Information', {
            'fields': (
                ('certificate_number', 'status'),
                ('verification_code',),
                ('student', 'course'),
                ('template',),
            )
        }),
        ('Dates', {
            'fields': (
                ('issue_date', 'completion_date'),
                ('valid_from', 'valid_until'),
            )
        }),
        ('Performance', {
            'fields': (
                ('grade', 'percentage'),
                ('duration_hours',),
            )
        }),
        ('Issuance', {
            'fields': (
                ('issued_by', 'issued_at'),
                ('signatories',),
            )
        }),
        ('Collection Tracking', {
            'fields': (
                ('printed_date',),
                ('collected_date', 'collected_by'),
                ('collection_remarks',),
            ),
            'classes': ('collapse',)
        }),
        ('Revocation', {
            'fields': (
                ('revoked_date', 'revoked_by'),
                ('revocation_reason',),
            ),
            'classes': ('collapse',)
        }),
        ('Additional', {
            'fields': (
                ('remarks',),
                ('custom_text',),
            ),
            'classes': ('collapse',)
        }),
        ('Files', {
            'fields': (
                ('certificate_pdf',),
                ('certificate_image',),
            ),
            'classes': ('collapse',)
        }),
        ('Verification Statistics', {
            'fields': (
                ('verification_count', 'last_verified'),
                ('get_verification_url_display',),
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-issue_date', '-created_at']
    
    # Custom actions
    actions = [
        'mark_as_issued', 'mark_as_printed', 'mark_as_collected',
        'revoke_certificates', 'generate_pdfs'
    ]
    
    def get_status_badge(self, obj):
        """Display status as colored badge"""
        color = obj.get_status_color()
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color,
            obj.get_status_display()
        )
    get_status_badge.short_description = "Status"
    
    def get_verification_url_display(self, obj):
        """Display verification URL"""
        if obj.pk:
            url = f"/verify-certificate/{obj.verification_code}/"
            full_url = f"http://edu.brillianzinstitute.com{url}"
            return format_html(
                '<a href="{}" target="_blank">{}</a>',
                full_url,
                full_url
            )
        return "-"
    get_verification_url_display.short_description = "Public Verification URL"
    
    def mark_as_issued(self, request, queryset):
        count = queryset.filter(status='draft').update(
            status='issued',
            issued_by=request.user,
            issued_at=timezone.now()
        )
        self.message_user(request, f"Marked {count} certificates as issued")
    mark_as_issued.short_description = "Mark as Issued"
    
    def mark_as_printed(self, request, queryset):
        count = queryset.filter(status='issued').update(
            status='printed',
            printed_date=timezone.now().date()
        )
        self.message_user(request, f"Marked {count} certificates as printed")
    mark_as_printed.short_description = "Mark as Printed"
    
    def mark_as_collected(self, request, queryset):
        count = queryset.filter(status='printed').update(
            status='collected',
            collected_date=timezone.now().date()
        )
        self.message_user(request, f"Marked {count} certificates as collected")
    mark_as_collected.short_description = "Mark as Collected"
    
    def revoke_certificates(self, request, queryset):
        count = queryset.exclude(status='revoked').update(
            status='revoked',
            revoked_by=request.user,
            revoked_date=timezone.now().date()
        )
        self.message_user(request, f"Revoked {count} certificates", level='warning')
    revoke_certificates.short_description = "Revoke selected certificates"
    
    def generate_pdfs(self, request, queryset):
        # This would integrate with PDF generation
        count = queryset.filter(status='issued', certificate_pdf='').count()
        self.message_user(request, f"PDF generation would process {count} certificates")
    generate_pdfs.short_description = "Generate PDFs"


@admin.register(CertificateVerification)
class CertificateVerificationAdmin(admin.ModelAdmin):
    list_display = [
        'certificate', 'verification_method', 'verification_result',
        'ip_address', 'country', 'organization', 'verified_at'
    ]
    list_filter = [
        'verification_method', 'verification_result',
        'verified_at', 'country'
    ]
    search_fields = [
        'certificate__certificate_number', 'search_query',
        'ip_address', 'verified_by_name', 'organization', 'purpose'
    ]
    readonly_fields = ['verified_at']
    raw_id_fields = ['certificate']
    date_hierarchy = 'verified_at'
    
    fieldsets = (
        ('Verification Details', {
            'fields': (
                ('certificate', 'verification_result'),
                ('verification_method', 'search_query'),
            )
        }),
        ('Requester Information', {
            'fields': (
                ('ip_address', 'country'),
                ('city',),
                ('user_agent',),
            )
        }),
        ('Additional Information', {
            'fields': (
                ('verified_by_name', 'organization'),
                ('purpose',),
            ),
            'classes': ('collapse',)
        }),
        ('Performance', {
            'fields': (
                ('response_time_ms',),
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': (
                ('verified_at',),
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-verified_at']
    
    def has_add_permission(self, request):
        """Disable manual addition - verifications are logged automatically"""
        return False


@admin.register(CertificateBatch)
class CertificateBatchAdmin(admin.ModelAdmin):
    list_display = [
        'batch_id', 'batch_name', 'course', 'template',
        'total_students', 'processed_count', 'success_count',
        'status', 'get_progress_percentage', 'created_at'
    ]
    list_filter = ['status', 'course', 'created_at', 'completed_at']
    search_fields = [
        'batch_id', 'batch_name', 'course__name', 'error_log'
    ]
    readonly_fields = [
        'processed_count', 'success_count', 'failed_count',
        'started_at', 'completed_at', 'created_at', 'updated_at'
    ]
    raw_id_fields = ['course', 'template', 'created_by']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Batch Information', {
            'fields': (
                ('batch_id', 'status'),
                ('batch_name',),
                ('course', 'template'),
            )
        }),
        ('Statistics', {
            'fields': (
                ('total_students', 'processed_count'),
                ('success_count', 'failed_count'),
            )
        }),
        ('Processing', {
            'fields': (
                ('started_at', 'completed_at'),
                ('error_log',),
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': (
                ('created_by',),
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created_at']
    
    # Custom actions
    actions = ['process_batches']
    
    def get_progress_percentage(self, obj):
        """Display progress percentage"""
        progress = obj.get_progress_percentage()
        return format_html(
            '<div class="progress" style="width:100px;"><div class="progress-bar" role="progressbar" style="width:{}%">{:.1f}%</div></div>',
            progress,
            progress
        )
    get_progress_percentage.short_description = "Progress"
    
    def process_batches(self, request, queryset):
        count = queryset.filter(status='draft').update(
            status='processing',
            started_at=timezone.now()
        )
        self.message_user(request, f"Started processing {count} batches")
    process_batches.short_description = "Process selected batches"
