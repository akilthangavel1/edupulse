from django.contrib import admin
from django.utils.html import format_html
from .models import StudentCertificate


@admin.register(StudentCertificate)
class StudentCertificateAdmin(admin.ModelAdmin):
    """Simple admin for certificate issue tracking"""
    
    list_display = ['certificate_number', 'student', 'course', 'issue_date', 'issued_by', 'created_at']
    list_filter = ['course', 'issue_date', 'created_at']
    search_fields = ['certificate_number', 'student__student_name', 'course__name', 'remarks']
    readonly_fields = ['certificate_number', 'created_at', 'updated_at']
    raw_id_fields = ['student', 'course']
    date_hierarchy = 'issue_date'
    
    fieldsets = (
        ('Certificate Information', {
            'fields': (('student', 'course'), 'issue_date', 'certificate_number')
        }),
        ('Notes', {
            'fields': ('remarks',)
        }),
        ('Tracking', {
            'fields': (('issued_by', 'created_at', 'updated_at'),),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only on creation
            obj.issued_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_list_display_links(self, request, list_display):
        return ['certificate_number']
