from django.contrib import admin
from django.db import models
from django.utils import timezone
from .models import (
    BroadcastTemplate, Broadcast, BroadcastRecipient,
    Lead, LeadActivity, LeadScore, CommunicationLog
)


@admin.register(BroadcastTemplate)
class BroadcastTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'subject', 'is_active', 'created_at']
    list_filter = ['template_type', 'is_active', 'created_at']
    search_fields = ['name', 'subject', 'message_content', 'sms_content']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['created_by']
    
    fieldsets = (
        ('Template Information', {
            'fields': (
                ('name', 'template_type'),
                ('is_active',),
            )
        }),
        ('Message Content', {
            'fields': (
                ('subject',),
                ('message_content',),
                ('sms_content',),
            )
        }),
        ('Variables', {
            'fields': (
                ('variables_description',),
            )
        }),
        ('Tracking', {
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


@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'broadcast_type', 'channels', 'status', 'priority',
        'total_recipients', 'sent_count', 'delivery_rate', 'scheduled_time'
    ]
    list_filter = [
        'status', 'broadcast_type', 'channels', 'priority',
        'send_immediately', 'created_at', 'sent_at'
    ]
    search_fields = [
        'title', 'subject', 'message_content', 'sms_content'
    ]
    readonly_fields = [
        'total_recipients', 'sent_count', 'failed_count', 
        'delivery_rate', 'created_at', 'sent_at', 'updated_at'
    ]
    filter_horizontal = ['target_batches', 'target_courses', 'target_students']
    raw_id_fields = ['template', 'created_by', 'sent_by']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('title', 'status'),
                ('broadcast_type', 'priority'),
                ('template',),
            )
        }),
        ('Message Content', {
            'fields': (
                ('subject',),
                ('message_content',),
                ('sms_content',),
            )
        }),
        ('Targeting', {
            'fields': (
                ('target_all_students', 'target_all_leads'),
                ('target_batches',),
                ('target_courses',),
                ('target_students',),
                ('target_grade_filter', 'target_program_filter'),
                ('target_fee_status_filter',),
            )
        }),
        ('Delivery Settings', {
            'fields': (
                ('channels',),
                ('send_immediately', 'scheduled_time'),
            )
        }),
        ('Status & Statistics', {
            'fields': (
                ('total_recipients', 'sent_count'),
                ('failed_count', 'delivery_rate'),
            )
        }),
        ('Cost Tracking', {
            'fields': (
                ('sms_cost', 'email_cost'),
                ('whatsapp_cost',),
            )
        }),
        ('Tracking Options', {
            'fields': (
                ('track_clicks', 'track_opens'),
                ('allow_replies',),
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': (
                ('created_by', 'sent_by'),
                ('created_at', 'sent_at'),
                ('updated_at',),
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created_at']
    
    # Custom actions
    actions = ['mark_scheduled', 'cancel_broadcasts']
    
    def mark_scheduled(self, request, queryset):
        count = queryset.filter(status='draft').update(status='scheduled')
        self.message_user(request, f"Marked {count} broadcasts as scheduled")
    mark_scheduled.short_description = "Mark as scheduled"
    
    def cancel_broadcasts(self, request, queryset):
        count = queryset.filter(status__in=['draft', 'scheduled']).update(status='cancelled')
        self.message_user(request, f"Cancelled {count} broadcasts")
    cancel_broadcasts.short_description = "Cancel selected broadcasts"


@admin.register(BroadcastRecipient)
class BroadcastRecipientAdmin(admin.ModelAdmin):
    list_display = [
        'broadcast', 'get_recipient_name', 'recipient_type',
        'sms_status', 'email_status', 'whatsapp_status',
        'sent_at', 'delivered_at'
    ]
    list_filter = [
        'recipient_type', 'sms_status', 'email_status', 
        'whatsapp_status', 'sent_at', 'delivered_at'
    ]
    search_fields = [
        'broadcast__title', 'custom_name', 'custom_email',
        'custom_phone', 'student__student_name', 'lead__name'
    ]
    readonly_fields = [
        'sent_at', 'delivered_at', 'opened_at', 
        'clicked_at', 'replied_at', 'created_at', 'updated_at'
    ]
    raw_id_fields = ['broadcast', 'student', 'lead']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Broadcast & Recipient', {
            'fields': (
                ('broadcast', 'recipient_type'),
                ('student', 'lead'),
            )
        }),
        ('Custom Contact', {
            'fields': (
                ('custom_name',),
                ('custom_email', 'custom_phone'),
            )
        }),
        ('Delivery Status', {
            'fields': (
                ('sms_status', 'email_status'),
                ('whatsapp_status',),
            )
        }),
        ('Tracking Timestamps', {
            'fields': (
                ('sent_at', 'delivered_at'),
                ('opened_at', 'clicked_at'),
                ('replied_at',),
            )
        }),
        ('Error Handling', {
            'fields': (
                ('error_message',),
                ('retry_count',),
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
    
    ordering = ['-created_at']


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = [
        'lead_id', 'name', 'email', 'phone', 'status', 'priority',
        'source', 'next_followup_date', 'assigned_to', 'created_at'
    ]
    list_filter = [
        'status', 'priority', 'source', 'gender',
        'preferred_time_slot', 'created_at', 'next_followup_date'
    ]
    search_fields = [
        'lead_id', 'name', 'email', 'phone', 'whatsapp_number',
        'referred_by', 'notes', 'address'
    ]
    readonly_fields = [
        'lead_id', 'created_at', 'updated_at', 'last_contacted', 'enrollment_date'
    ]
    filter_horizontal = ['interested_courses']
    raw_id_fields = ['enrolled_student', 'assigned_to', 'created_by']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Lead Information', {
            'fields': (
                ('lead_id', 'status'),
                ('name', 'priority'),
                ('email', 'phone'),
                ('whatsapp_number',),
            )
        }),
        ('Demographics', {
            'fields': (
                ('age', 'gender'),
                ('nationality',),
                ('address',),
            )
        }),
        ('Interest Information', {
            'fields': (
                ('interested_courses',),
                ('preferred_time_slot',),
                ('budget_range',),
            )
        }),
        ('Lead Tracking', {
            'fields': (
                ('source', 'source_details'),
                ('referred_by',),
            )
        }),
        ('Follow-up', {
            'fields': (
                ('next_followup_date', 'last_contacted'),
                ('contact_attempts',),
                ('assigned_to',),
            )
        }),
        ('Conversion', {
            'fields': (
                ('enrolled_student', 'enrollment_date'),
            ),
            'classes': ('collapse',)
        }),
        ('Additional', {
            'fields': (
                ('notes',),
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
    
    ordering = ['-created_at']
    
    # Custom actions
    actions = ['mark_contacted', 'mark_interested', 'mark_not_interested']
    
    def mark_contacted(self, request, queryset):
        queryset.update(
            status='contacted',
            last_contacted=timezone.now(),
            contact_attempts=models.F('contact_attempts') + 1
        )
        self.message_user(request, f"Marked {queryset.count()} leads as contacted")
    mark_contacted.short_description = "Mark as contacted"
    
    def mark_interested(self, request, queryset):
        queryset.update(status='interested', priority='hot')
        self.message_user(request, f"Marked {queryset.count()} leads as interested")
    mark_interested.short_description = "Mark as interested"
    
    def mark_not_interested(self, request, queryset):
        queryset.update(status='not_interested')
        self.message_user(request, f"Marked {queryset.count()} leads as not interested")
    mark_not_interested.short_description = "Mark as not interested"


@admin.register(LeadActivity)
class LeadActivityAdmin(admin.ModelAdmin):
    list_display = [
        'lead', 'activity_type', 'subject', 'outcome',
        'activity_date', 'follow_up_required', 'follow_up_date', 'created_by'
    ]
    list_filter = [
        'activity_type', 'outcome', 'follow_up_required',
        'activity_date', 'created_at'
    ]
    search_fields = [
        'lead__name', 'lead__lead_id', 'subject',
        'description', 'follow_up_notes'
    ]
    readonly_fields = ['created_at']
    raw_id_fields = ['lead', 'related_broadcast', 'created_by']
    date_hierarchy = 'activity_date'
    
    fieldsets = (
        ('Activity Information', {
            'fields': (
                ('lead', 'activity_type'),
                ('subject', 'outcome'),
                ('description',),
            )
        }),
        ('Timing', {
            'fields': (
                ('activity_date', 'duration_minutes'),
            )
        }),
        ('Follow-up', {
            'fields': (
                ('follow_up_required', 'follow_up_date'),
                ('follow_up_notes',),
            )
        }),
        ('Related Records', {
            'fields': (
                ('related_broadcast',),
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': (
                ('created_by', 'created_at'),
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-activity_date']


@admin.register(LeadScore)
class LeadScoreAdmin(admin.ModelAdmin):
    list_display = [
        'lead', 'grade', 'total_score', 'engagement_score',
        'interest_score', 'demographic_score', 'behavior_score', 'last_calculated'
    ]
    list_filter = ['grade', 'last_calculated']
    search_fields = ['lead__name', 'lead__lead_id']
    readonly_fields = ['last_calculated']
    raw_id_fields = ['lead']
    
    fieldsets = (
        ('Lead Information', {
            'fields': (
                ('lead',),
                ('grade', 'total_score'),
            )
        }),
        ('Score Components', {
            'fields': (
                ('engagement_score', 'interest_score'),
                ('demographic_score', 'behavior_score'),
            )
        }),
        ('Metadata', {
            'fields': (
                ('last_calculated',),
            )
        }),
    )
    
    ordering = ['-total_score']
    
    # Custom actions
    actions = ['recalculate_scores']
    
    def recalculate_scores(self, request, queryset):
        for score in queryset:
            score.calculate_score()
        self.message_user(request, f"Recalculated scores for {queryset.count()} leads")
    recalculate_scores.short_description = "Recalculate lead scores"


@admin.register(CommunicationLog)
class CommunicationLogAdmin(admin.ModelAdmin):
    list_display = [
        'communication_type', 'recipient_type', 'recipient_name',
        'status', 'sent_at', 'delivered_at', 'cost', 'provider'
    ]
    list_filter = [
        'communication_type', 'status', 'recipient_type',
        'sent_at', 'delivered_at', 'created_at'
    ]
    search_fields = [
        'subject', 'content', 'recipient_name', 'recipient_contact',
        'provider', 'error_message'
    ]
    readonly_fields = [
        'sent_at', 'delivered_at', 'opened_at', 'created_at'
    ]
    raw_id_fields = ['student', 'lead', 'broadcast', 'created_by']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Communication Details', {
            'fields': (
                ('communication_type', 'status'),
                ('subject',),
                ('content',),
            )
        }),
        ('Recipient Information', {
            'fields': (
                ('recipient_type', 'recipient_name'),
                ('recipient_contact',),
            )
        }),
        ('Related Records', {
            'fields': (
                ('student', 'lead'),
                ('broadcast',),
            )
        }),
        ('Tracking', {
            'fields': (
                ('sent_at', 'delivered_at'),
                ('opened_at',),
            )
        }),
        ('Cost & Provider', {
            'fields': (
                ('cost', 'provider'),
            )
        }),
        ('Error Handling', {
            'fields': (
                ('error_message',),
                ('retry_count',),
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': (
                ('created_by', 'created_at'),
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created_at']
