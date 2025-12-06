from django.contrib import admin
from .models import Subject, AssessmentType, GradeScale, StudentMark, StudentGradeSummary



#########

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'course', 'credit_hours', 'instructor', 'is_active', 'created_at']
    list_filter = ['is_active', 'course', 'created_at']
    search_fields = ['name', 'code', 'instructor']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['course', 'name']


@admin.register(AssessmentType)
class AssessmentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'weight_percentage', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['weight_percentage', 'is_active']
    readonly_fields = ['created_at']
    ordering = ['category', 'weight_percentage']


@admin.register(GradeScale)
class GradeScaleAdmin(admin.ModelAdmin):
    list_display = ['grade', 'min_percentage', 'max_percentage', 'grade_points', 'description', 'is_active']
    list_filter = ['is_active']
    search_fields = ['grade', 'description']
    list_editable = ['is_active']
    ordering = ['-min_percentage']


@admin.register(StudentMark)
class StudentMarkAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'assessment_type', 'marks_obtained', 'total_marks', 'percentage', 'grade', 'status', 'assessment_date']
    list_filter = ['status', 'subject', 'assessment_type', 'assessment_date', 'is_active']
    search_fields = ['student__student_name', 'subject__name', 'subject__code']
    list_editable = ['status']
    readonly_fields = ['percentage', 'grade', 'grade_points', 'created_at', 'updated_at']
    raw_id_fields = ['student', 'entered_by', 'verified_by']
    date_hierarchy = 'assessment_date'
    ordering = ['-assessment_date', 'student', 'subject']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('student', 'subject', 'assessment_type', 'assessment_date')
        }),
        ('Marks', {
            'fields': ('marks_obtained', 'total_marks', 'percentage', 'grade', 'grade_points')
        }),
        ('Status & Notes', {
            'fields': ('status', 'remarks', 'private_notes', 'submission_date')
        }),
        ('Tracking', {
            'fields': ('entered_by', 'verified_by', 'is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(StudentGradeSummary)
class StudentGradeSummaryAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'weighted_percentage', 'final_grade', 'final_grade_points', 'is_completed', 'semester', 'academic_year']
    list_filter = ['is_completed', 'semester', 'academic_year', 'subject']
    search_fields = ['student__student_name', 'subject__name', 'subject__code']
    readonly_fields = ['calculated_at', 'calculated_by']
    raw_id_fields = ['student', 'calculated_by']
    ordering = ['-calculated_at', 'student', 'subject']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('student', 'subject', 'semester', 'academic_year')
        }),
        ('Grade Summary', {
            'fields': ('total_marks_obtained', 'total_possible_marks', 'weighted_percentage', 'final_grade', 'final_grade_points')
        }),
        ('Status', {
            'fields': ('is_completed', 'completion_date')
        }),
        ('Tracking', {
            'fields': ('calculated_at', 'calculated_by'),
            'classes': ('collapse',)
        })
    )
