from django.contrib import admin
from .models import NewStudent, OldStudent, Attendance, AttendanceSummary


@admin.register(NewStudent)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'student_name', 'status', 'email_id', 'grade', 'program', 
        'gender', 'father_mobile_no', 'mother_mobile_no', 'created_at'
    ]
    list_filter = [
        'status', 'gender', 'grade', 'program', 'country', 'state_emirates_province',
        'select_mobile_number', 'created_at'
    ]
    search_fields = [
        'student_name', 'email_id', 'grade', 'program', 
        'father_name', 'mother_name', 'guardian_name',
        'area', 'city'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Student Information', {
            'fields': (
                'status',
                ('student_name', 'gender'),
                ('school_name', 'grade'),
                ('program', 'date_of_birth'),
                ('email_id', 'student_profile_picture'),
            )
        }),
        ('Father Details', {
            'fields': (
                ('father_name', 'father_occupation'),
                ('father_company_name', 'father_mobile_no'),
                'father_email_id',
            )
        }),
        ('Mother Details', {
            'fields': (
                ('mother_name', 'mother_occupation'),
                ('mother_company_name', 'mother_mobile_no'),
                'mother_email_id',
            )
        }),
        ('Guardian Details', {
            'fields': (
                ('guardian_name', 'guardian_relationship'),
                'guardian_mobile_no',
            ),
            'classes': ('collapse',),
        }),
        ('Siblings Information', {
            'fields': (
                ('sibling_1_name', 'sibling_1_age'),
                ('sibling_2_name', 'sibling_2_age'),
            ),
            'classes': ('collapse',),
        }),
        ('Address Information', {
            'fields': (
                ('address_line_1', 'address_line_2'),
                ('area', 'city'),
                ('state_emirates_province', 'country'),
                ('postal_code', 'telephone'),
            )
        }),
        ('Contact Information', {
            'fields': (
                ('select_mobile_number', 'mobile_no'),
            )
        }),
        ('Timestamps', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',),
        }),
    )
    
    actions = ['mark_active', 'mark_inactive']
    
    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
    mark_active.short_description = "Mark selected students as active"
    
    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_inactive.short_description = "Mark selected students as inactive"


@admin.register(OldStudent)
class OldStudentAdmin(admin.ModelAdmin):
    list_display = [
        'student_name', 'student_code', 'email', 'mobile_number', 
        'tenth_level_completed_date', 'created_at'
    ]
    list_filter = [
        'tenth_level_completed_date', 'created_at', 'updated_at'
    ]
    search_fields = [
        'student_name', 'student_code', 'email', 'mobile_number'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Student Information', {
            'fields': (
                ('student_name', 'student_code'),
                ('email', 'mobile_number'),
                ('date_of_birth', 'tenth_level_completed_date'),
            )
        }),
        ('Timestamps', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',),
        }),
    )
    
    ordering = ['-created_at']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'date', 'status', 'time_in', 'time_out', 
        'recorded_by', 'created_at'
    ]
    list_filter = [
        'status', 'date', 'recorded_by', 'created_at', 
        'student__grade', 'student__program'
    ]
    search_fields = [
        'student__student_name', 'student__email_id', 
        'notes', 'student__grade', 'student__program'
    ]
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Attendance Information', {
            'fields': (
                ('student', 'date'),
                ('status', 'recorded_by'),
                ('time_in', 'time_out'),
                'notes',
            )
        }),
        ('Timestamps', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',),
        }),
    )
    
    ordering = ['-date', '-created_at']
    
    # Custom actions
    actions = ['mark_present', 'mark_absent', 'mark_late', 'mark_excused']
    
    def mark_present(self, request, queryset):
        queryset.update(status='present')
    mark_present.short_description = "Mark selected records as present"
    
    def mark_absent(self, request, queryset):
        queryset.update(status='absent')
    mark_absent.short_description = "Mark selected records as absent"
    
    def mark_late(self, request, queryset):
        queryset.update(status='late')
    mark_late.short_description = "Mark selected records as late"
    
    def mark_excused(self, request, queryset):
        queryset.update(status='excused')
    mark_excused.short_description = "Mark selected records as excused"
    
    # Auto-fill recorded_by field
    def save_model(self, request, obj, form, change):
        if not obj.recorded_by:
            obj.recorded_by = request.user
        super().save_model(request, obj, form, change)
    
    # Custom queryset to optimize database queries
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'recorded_by')


@admin.register(AttendanceSummary)
class AttendanceSummaryAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'month', 'year', 'total_days', 'present_days', 
        'absent_days', 'attendance_percentage', 'updated_at'
    ]
    list_filter = [
        'year', 'month', 'student__grade', 'student__program', 'updated_at'
    ]
    search_fields = [
        'student__student_name', 'student__email_id'
    ]
    readonly_fields = ['created_at', 'updated_at', 'attendance_percentage']
    
    fieldsets = (
        ('Summary Information', {
            'fields': (
                ('student', 'month', 'year'),
                ('total_days', 'present_days'),
                ('absent_days', 'late_days', 'excused_days'),
                'attendance_percentage',
            )
        }),
        ('Timestamps', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',),
        }),
    )
    
    ordering = ['-year', '-month', 'student__student_name']
    
    # Custom actions
    actions = ['recalculate_percentage']
    
    def recalculate_percentage(self, request, queryset):
        for summary in queryset:
            summary.calculate_percentage()
            summary.save()
    recalculate_percentage.short_description = "Recalculate attendance percentage"
    
    # Custom save to automatically calculate percentage
    def save_model(self, request, obj, form, change):
        obj.calculate_percentage()
        super().save_model(request, obj, form, change)
    
    # Custom queryset to optimize database queries
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student')
