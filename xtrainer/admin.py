from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import (
    Faculty, FacultyOnboarding, FacultyLeaveRequest, BackupSchedule,
    FacultyAttendance, FacultyPayment, ExamRequest, NotificationLog
)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = [
        'faculty_id', 'get_full_name', 'email', 'phone', 'status',
        'employment_type', 'qualification', 'experience_years', 'join_date'
    ]
    list_filter = [
        'status', 'employment_type', 'qualification', 'join_date',
        'can_teach_courses', 'created_at'
    ]
    search_fields = [
        'faculty_id', 'first_name', 'last_name', 'email', 'phone',
        'specialization', 'city', 'state'
    ]
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['can_teach_courses']
    date_hierarchy = 'join_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('faculty_id', 'status'),
                ('first_name', 'last_name'),
                ('email', 'phone'),
                ('emergency_contact',),
                ('profile_picture',),
            )
        }),
        ('Professional Information', {
            'fields': (
                ('qualification', 'specialization'),
                ('experience_years', 'employment_type'),
                ('join_date', 'hourly_rate'),
                ('can_teach_courses',),
                ('bio',),
            )
        }),
        ('Address Information', {
            'fields': (
                ('address_line_1', 'address_line_2'),
                ('city', 'state'),
                ('country', 'postal_code'),
            )
        }),
        ('System Information', {
            'fields': (
                ('user',),
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',),
        }),
    )
    
    ordering = ['first_name', 'last_name']
    
    # Custom actions
    actions = ['mark_active', 'mark_inactive', 'mark_suspended']
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = "Full Name"
    
    def mark_active(self, request, queryset):
        queryset.update(status='active')
        self.message_user(request, f"Marked {queryset.count()} faculty as active")
    mark_active.short_description = "Mark selected faculty as active"
    
    def mark_inactive(self, request, queryset):
        queryset.update(status='inactive')
        self.message_user(request, f"Marked {queryset.count()} faculty as inactive")
    mark_inactive.short_description = "Mark selected faculty as inactive"
    
    def mark_suspended(self, request, queryset):
        queryset.update(status='suspended')
        self.message_user(request, f"Marked {queryset.count()} faculty as suspended")
    mark_suspended.short_description = "Mark selected faculty as suspended"


@admin.register(FacultyOnboarding)
class FacultyOnboardingAdmin(admin.ModelAdmin):
    list_display = [
        'request_id', 'get_full_name', 'email', 'qualification', 
        'experience_years', 'status', 'application_date'
    ]
    list_filter = [
        'status', 'qualification', 'preferred_employment_type',
        'application_date', 'review_date', 'approval_date'
    ]
    search_fields = [
        'request_id', 'first_name', 'last_name', 'email', 'phone',
        'specialization'
    ]
    readonly_fields = [
        'request_id', 'application_date', 'review_date', 'approval_date', 'updated_at'
    ]
    filter_horizontal = ['preferred_courses']
    date_hierarchy = 'application_date'
    
    fieldsets = (
        ('Request Information', {
            'fields': (
                ('request_id', 'status'),
                ('application_date',),
            )
        }),
        ('Applicant Information', {
            'fields': (
                ('first_name', 'last_name'),
                ('email', 'phone'),
                ('qualification', 'specialization'),
                ('experience_years', 'preferred_employment_type'),
                ('expected_hourly_rate',),
                ('preferred_courses',),
                ('availability_notes',),
            )
        }),
        ('Documents', {
            'fields': (
                ('cv_file', 'certificates_file'),
                ('other_documents',),
            )
        }),
        ('Review Process', {
            'fields': (
                ('reviewed_by', 'review_date'),
                ('review_notes',),
                ('approved_by', 'approval_date'),
                ('approval_notes',),
                ('created_faculty',),
            )
        }),
        ('Timestamps', {
            'fields': (
                ('updated_at',),
            ),
            'classes': ('collapse',),
        }),
    )
    
    ordering = ['-application_date']
    
    # Custom actions
    actions = ['mark_under_review', 'mark_approved', 'mark_rejected']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = "Full Name"
    
    def mark_under_review(self, request, queryset):
        queryset.filter(status='pending').update(
            status='under_review',
            reviewed_by=request.user,
            review_date=timezone.now()
        )
        self.message_user(request, f"Marked {queryset.count()} requests as under review")
    mark_under_review.short_description = "Mark selected requests as under review"
    
    def mark_approved(self, request, queryset):
        count = queryset.filter(status='under_review').update(
            status='approved',
            approved_by=request.user,
            approval_date=timezone.now()
        )
        self.message_user(request, f"Approved {count} onboarding requests")
    mark_approved.short_description = "Approve selected requests"
    
    def mark_rejected(self, request, queryset):
        count = queryset.filter(status__in=['pending', 'under_review']).update(
            status='rejected',
            reviewed_by=request.user,
            review_date=timezone.now()
        )
        self.message_user(request, f"Rejected {count} onboarding requests")
    mark_rejected.short_description = "Reject selected requests"


@admin.register(FacultyLeaveRequest)
class FacultyLeaveRequestAdmin(admin.ModelAdmin):
    list_display = [
        'request_id', 'faculty', 'request_type', 'start_date', 'end_date',
        'priority', 'status', 'request_date'
    ]
    list_filter = [
        'status', 'request_type', 'priority', 'request_date',
        'start_date', 'backup_required'
    ]
    search_fields = [
        'request_id', 'faculty__first_name', 'faculty__last_name',
        'reason', 'affected_batches'
    ]
    readonly_fields = [
        'request_id', 'request_date', 'review_date', 'notification_date', 'updated_at'
    ]
    filter_horizontal = ['affected_courses']
    date_hierarchy = 'request_date'
    
    fieldsets = (
        ('Request Information', {
            'fields': (
                ('request_id', 'status'),
                ('faculty', 'request_type'),
                ('priority', 'request_date'),
            )
        }),
        ('Leave Details', {
            'fields': (
                ('start_date', 'end_date'),
                ('start_time', 'end_time'),
                ('affected_courses',),
                ('affected_batches',),
                ('reason',),
            )
        }),
        ('Backup Arrangements', {
            'fields': (
                ('backup_required', 'suggested_backup'),
                ('backup_notes',),
            )
        }),
        ('Review Process', {
            'fields': (
                ('reviewed_by', 'review_date'),
                ('approval_notes',),
            )
        }),
        ('Notifications', {
            'fields': (
                ('notification_sent', 'notification_date'),
            ),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': (
                ('updated_at',),
            ),
            'classes': ('collapse',),
        }),
    )
    
    ordering = ['-request_date']
    
    # Custom actions
    actions = ['approve_requests', 'reject_requests']
    
    def approve_requests(self, request, queryset):
        count = queryset.filter(status='pending').update(
            status='approved',
            reviewed_by=request.user,
            review_date=timezone.now()
        )
        self.message_user(request, f"Approved {count} leave requests")
    approve_requests.short_description = "Approve selected leave requests"
    
    def reject_requests(self, request, queryset):
        count = queryset.filter(status='pending').update(
            status='rejected',
            reviewed_by=request.user,
            review_date=timezone.now()
        )
        self.message_user(request, f"Rejected {count} leave requests")
    reject_requests.short_description = "Reject selected leave requests"


@admin.register(BackupSchedule)
class BackupScheduleAdmin(admin.ModelAdmin):
    list_display = [
        'schedule_id', 'original_faculty', 'backup_faculty', 'course',
        'date', 'start_time', 'end_time', 'status'
    ]
    list_filter = [
        'status', 'date', 'course', 'backup_confirmed',
        'notification_sent_to_backup', 'notification_sent_to_students'
    ]
    search_fields = [
        'schedule_id', 'original_faculty__first_name', 'original_faculty__last_name',
        'backup_faculty__first_name', 'backup_faculty__last_name',
        'course__name', 'batch_name', 'room_location'
    ]
    readonly_fields = [
        'schedule_id', 'backup_confirmation_date', 'notification_date',
        'created_at', 'updated_at'
    ]
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Schedule Information', {
            'fields': (
                ('schedule_id', 'status'),
                ('original_faculty', 'backup_faculty'),
                ('leave_request',),
                ('course', 'batch_name'),
            )
        }),
        ('Schedule Details', {
            'fields': (
                ('date',),
                ('start_time', 'end_time'),
                ('room_location',),
                ('notes',),
            )
        }),
        ('Confirmation & Notifications', {
            'fields': (
                ('backup_confirmed', 'backup_confirmation_date'),
                ('notification_sent_to_backup', 'notification_sent_to_students'),
                ('notification_date',),
            )
        }),
        ('System Information', {
            'fields': (
                ('created_by',),
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',),
        }),
    )
    
    ordering = ['date', 'start_time']
    
    # Custom actions
    actions = ['mark_confirmed', 'mark_completed', 'send_notifications']
    
    def mark_confirmed(self, request, queryset):
        queryset.update(
            status='confirmed',
            backup_confirmed=True,
            backup_confirmation_date=timezone.now()
        )
        self.message_user(request, f"Marked {queryset.count()} schedules as confirmed")
    mark_confirmed.short_description = "Mark selected schedules as confirmed"
    
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, f"Marked {queryset.count()} schedules as completed")
    mark_completed.short_description = "Mark selected schedules as completed"
    
    def send_notifications(self, request, queryset):
        queryset.update(
            notification_sent_to_backup=True,
            notification_sent_to_students=True,
            notification_date=timezone.now()
        )
        self.message_user(request, f"Sent notifications for {queryset.count()} schedules")
    send_notifications.short_description = "Send notifications for selected schedules"


@admin.register(FacultyAttendance)
class FacultyAttendanceAdmin(admin.ModelAdmin):
    list_display = [
        'faculty', 'course', 'date', 'status',
        'scheduled_start_time', 'actual_start_time',
        'recorded_by'
    ]
    list_filter = [
        'status', 'date', 'course', 'recorded_by', 'created_at'
    ]
    search_fields = [
        'faculty__first_name', 'faculty__last_name',
        'course__name', 'notes'
    ]
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Attendance Information', {
            'fields': (
                ('faculty', 'course'),
                ('date', 'status'),
            )
        }),
        ('Time Tracking', {
            'fields': (
                ('scheduled_start_time', 'scheduled_end_time'),
                ('actual_start_time', 'actual_end_time'),
            )
        }),
        ('Additional Information', {
            'fields': (
                ('notes',),
                ('recorded_by',),
            )
        }),
        ('Timestamps', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',),
        }),
    )
    
    ordering = ['-date', 'faculty']
    
    # Custom actions
    actions = ['mark_present', 'mark_absent', 'mark_late']
    
    def mark_present(self, request, queryset):
        queryset.update(status='present')
        self.message_user(request, f"Marked {queryset.count()} records as present")
    mark_present.short_description = "Mark selected records as present"
    
    def mark_absent(self, request, queryset):
        queryset.update(status='absent')
        self.message_user(request, f"Marked {queryset.count()} records as absent")
    mark_absent.short_description = "Mark selected records as absent"
    
    def mark_late(self, request, queryset):
        queryset.update(status='late')
        self.message_user(request, f"Marked {queryset.count()} records as late")
    mark_late.short_description = "Mark selected records as late"


@admin.register(FacultyPayment)
class FacultyPaymentAdmin(admin.ModelAdmin):
    list_display = [
        'payment_id', 'faculty', 'payment_type', 'period_start', 'period_end',
        'total_hours', 'net_amount', 'status', 'payment_date'
    ]
    list_filter = [
        'status', 'payment_type', 'payment_method', 'payment_date',
        'period_end', 'generated_by', 'approved_by'
    ]
    search_fields = [
        'payment_id', 'faculty__first_name', 'faculty__last_name',
        'reference_number', 'notes'
    ]
    readonly_fields = [
        'payment_id', 'gross_amount', 'net_amount', 'created_at', 'updated_at'
    ]
    date_hierarchy = 'period_end'
    
    fieldsets = (
        ('Payment Information', {
            'fields': (
                ('payment_id', 'status'),
                ('faculty', 'payment_type'),
                ('period_start', 'period_end'),
            )
        }),
        ('Hours and Calculation', {
            'fields': (
                ('total_hours', 'hourly_rate'),
                ('gross_amount',),
                ('deductions', 'bonus_amount'),
                ('net_amount',),
            )
        }),
        ('Payment Details', {
            'fields': (
                ('payment_method', 'payment_date'),
                ('reference_number',),
                ('notes',),
            )
        }),
        ('Approval Process', {
            'fields': (
                ('generated_by', 'approved_by'),
                ('processed_by',),
            )
        }),
        ('Timestamps', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',),
        }),
    )
    
    ordering = ['-period_end', '-created_at']
    
    # Custom actions
    actions = ['approve_payments', 'mark_paid', 'generate_payslips']
    
    def approve_payments(self, request, queryset):
        count = queryset.filter(status='pending').update(
            status='approved',
            approved_by=request.user
        )
        self.message_user(request, f"Approved {count} payments")
    approve_payments.short_description = "Approve selected payments"
    
    def mark_paid(self, request, queryset):
        count = queryset.filter(status='approved').update(
            status='paid',
            processed_by=request.user,
            payment_date=timezone.now().date()
        )
        self.message_user(request, f"Marked {count} payments as paid")
    mark_paid.short_description = "Mark selected payments as paid"
    
    def generate_payslips(self, request, queryset):
        # This would integrate with a payslip generation system
        self.message_user(request, f"Generated payslips for {queryset.count()} payments")
    generate_payslips.short_description = "Generate payslips for selected payments"


@admin.register(ExamRequest)
class ExamRequestAdmin(admin.ModelAdmin):
    list_display = [
        'request_id', 'faculty', 'course', 'exam_title', 'exam_type',
        'proposed_date', 'total_marks', 'status', 'request_date'
    ]
    list_filter = [
        'status', 'exam_type', 'proposed_date', 'request_date',
        'supervision_required', 'notification_sent'
    ]
    search_fields = [
        'request_id', 'faculty__first_name', 'faculty__last_name',
        'course__name', 'exam_title', 'description'
    ]
    readonly_fields = [
        'request_id', 'request_date', 'review_date', 'notification_date', 'updated_at'
    ]
    filter_horizontal = ['target_students']
    date_hierarchy = 'proposed_date'
    
    fieldsets = (
        ('Request Information', {
            'fields': (
                ('request_id', 'status'),
                ('faculty', 'course'),
                ('request_date',),
            )
        }),
        ('Exam Details', {
            'fields': (
                ('exam_title', 'exam_type'),
                ('description',),
                ('proposed_date', 'proposed_start_time'),
                ('duration_hours',),
            )
        }),
        ('Exam Configuration', {
            'fields': (
                ('total_marks', 'passing_marks'),
                ('number_of_questions',),
                ('supervision_required',),
            )
        }),
        ('Resources & Requirements', {
            'fields': (
                ('room_requirements',),
                ('special_materials',),
                ('target_students',),
            )
        }),
        ('Review Process', {
            'fields': (
                ('reviewed_by', 'review_date'),
                ('approval_notes',),
            )
        }),
        ('Final Schedule', {
            'fields': (
                ('final_date', 'final_start_time'),
                ('assigned_room',),
            )
        }),
        ('Notifications', {
            'fields': (
                ('notification_sent', 'notification_date'),
            ),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': (
                ('updated_at',),
            ),
            'classes': ('collapse',),
        }),
    )
    
    ordering = ['-request_date']
    
    # Custom actions
    actions = ['approve_requests', 'reject_requests', 'schedule_exams']
    
    def approve_requests(self, request, queryset):
        count = queryset.filter(status='pending').update(
            status='approved',
            reviewed_by=request.user,
            review_date=timezone.now()
        )
        self.message_user(request, f"Approved {count} exam requests")
    approve_requests.short_description = "Approve selected exam requests"
    
    def reject_requests(self, request, queryset):
        count = queryset.filter(status='pending').update(
            status='rejected',
            reviewed_by=request.user,
            review_date=timezone.now()
        )
        self.message_user(request, f"Rejected {count} exam requests")
    reject_requests.short_description = "Reject selected exam requests"
    
    def schedule_exams(self, request, queryset):
        approved_requests = queryset.filter(status='approved')
        for exam_request in approved_requests:
            exam_request.final_date = exam_request.proposed_date
            exam_request.final_start_time = exam_request.proposed_start_time
            exam_request.status = 'scheduled'
            exam_request.save()
        
        self.message_user(request, f"Scheduled {approved_requests.count()} exams")
    schedule_exams.short_description = "Schedule approved exams"


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = [
        'notification_type', 'recipient_type', 'recipient_contact',
        'subject', 'status', 'sent_at', 'delivered_at'
    ]
    list_filter = [
        'notification_type', 'status', 'recipient_type',
        'sent_at', 'delivered_at', 'created_at'
    ]
    search_fields = [
        'recipient_contact', 'subject', 'message',
        'related_model', 'error_message'
    ]
    readonly_fields = [
        'sent_at', 'delivered_at', 'created_at', 'updated_at'
    ]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Notification Information', {
            'fields': (
                ('notification_type', 'status'),
                ('recipient_type', 'recipient_id'),
                ('recipient_contact',),
            )
        }),
        ('Message Details', {
            'fields': (
                ('subject',),
                ('message',),
            )
        }),
        ('Related Information', {
            'fields': (
                ('related_model', 'related_id'),
                ('sent_by',),
            )
        }),
        ('Status & Timing', {
            'fields': (
                ('sent_at', 'delivered_at'),
                ('error_message',),
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
    
    # Custom actions
    actions = ['mark_sent', 'mark_delivered', 'mark_failed']
    
    def mark_sent(self, request, queryset):
        queryset.update(
            status='sent',
            sent_at=timezone.now()
        )
        self.message_user(request, f"Marked {queryset.count()} notifications as sent")
    mark_sent.short_description = "Mark selected notifications as sent"
    
    def mark_delivered(self, request, queryset):
        queryset.update(
            status='delivered',
            delivered_at=timezone.now()
        )
        self.message_user(request, f"Marked {queryset.count()} notifications as delivered")
    mark_delivered.short_description = "Mark selected notifications as delivered"
    
    def mark_failed(self, request, queryset):
        queryset.update(status='failed')
        self.message_user(request, f"Marked {queryset.count()} notifications as failed")
    mark_failed.short_description = "Mark selected notifications as failed"
