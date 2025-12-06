from django.contrib import admin
from django.utils import timezone
from .models import (
    Vendor, VendorRequest, StudentTransportAssignment,
    VendorPayment, MonthlyPaymentGeneration, VendorRating
)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = [
        'vendor_code', 'company_name', 'contact_person', 'phone', 
        'vehicle_type', 'fleet_size', 'status', 'rating'
    ]
    list_filter = [
        'status', 'vehicle_type', 'city', 'contract_start_date', 
        'contract_end_date', 'created_at'
    ]
    search_fields = [
        'vendor_code', 'company_name', 'trade_license', 'contact_person',
        'email', 'phone', 'area'
    ]
    readonly_fields = ['created_at', 'updated_at', 'approval_date']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('vendor_code', 'status'),
                ('company_name', 'trade_license'),
                ('contact_person',),
            )
        }),
        ('Contact Details', {
            'fields': (
                ('email', 'phone'),
                ('mobile',),
                ('address', 'area'),
                ('city', 'postal_code'),
            )
        }),
        ('Service Information', {
            'fields': (
                ('vehicle_type', 'fleet_size'),
                ('service_areas',),
            )
        }),
        ('Financial Details', {
            'fields': (
                ('rate_per_km', 'monthly_rate'),
                ('security_deposit',),
                ('payment_terms',),
            )
        }),
        ('Contract Details', {
            'fields': (
                ('contract_start_date', 'contract_end_date'),
            )
        }),
        ('Documents', {
            'fields': (
                ('trade_license_copy', 'insurance_copy'),
                ('vehicle_registration',),
            )
        }),
        ('Rating & Reviews', {
            'fields': (
                ('rating', 'total_reviews'),
            )
        }),
        ('Approval & Tracking', {
            'fields': (
                ('created_by', 'approved_by'),
                ('approval_date',),
                ('created_at', 'updated_at'),
                ('notes',),
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['company_name']
    
    # Custom actions
    actions = ['activate_vendors', 'deactivate_vendors', 'suspend_vendors']
    
    def activate_vendors(self, request, queryset):
        queryset.update(status='active')
        self.message_user(request, f"Activated {queryset.count()} vendors")
    activate_vendors.short_description = "Activate selected vendors"
    
    def deactivate_vendors(self, request, queryset):
        queryset.update(status='inactive')
        self.message_user(request, f"Deactivated {queryset.count()} vendors")
    deactivate_vendors.short_description = "Deactivate selected vendors"
    
    def suspend_vendors(self, request, queryset):
        queryset.update(status='suspended')
        self.message_user(request, f"Suspended {queryset.count()} vendors")
    suspend_vendors.short_description = "Suspend selected vendors"


@admin.register(VendorRequest)
class VendorRequestAdmin(admin.ModelAdmin):
    list_display = [
        'request_id', 'company_name', 'contact_person', 'phone',
        'vehicle_type', 'fleet_size', 'status', 'submission_date'
    ]
    list_filter = [
        'status', 'vehicle_type', 'submission_date', 'review_date'
    ]
    search_fields = [
        'request_id', 'company_name', 'trade_license', 'contact_person',
        'email', 'phone'
    ]
    readonly_fields = [
        'request_id', 'submission_date', 'review_date', 'created_at', 'updated_at'
    ]
    date_hierarchy = 'submission_date'
    
    fieldsets = (
        ('Request Information', {
            'fields': (
                ('request_id', 'status'),
                ('submission_date',),
            )
        }),
        ('Company Information', {
            'fields': (
                ('company_name', 'trade_license'),
                ('contact_person',),
                ('email', 'phone'),
            )
        }),
        ('Service Details', {
            'fields': (
                ('vehicle_type', 'fleet_size'),
                ('service_areas',),
                ('proposed_rate_per_km',),
            )
        }),
        ('Documents', {
            'fields': (
                ('trade_license_copy',),
                ('insurance_copy',),
                ('vehicle_registration',),
            )
        }),
        ('Review Process', {
            'fields': (
                ('reviewed_by', 'review_date'),
                ('review_comments',),
                ('created_vendor',),
            )
        }),
        ('Timestamps', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-submission_date']
    
    # Custom actions
    actions = ['mark_under_review', 'approve_requests', 'reject_requests']
    
    def mark_under_review(self, request, queryset):
        count = queryset.filter(status='submitted').update(
            status='under_review',
            reviewed_by=request.user,
            review_date=timezone.now()
        )
        self.message_user(request, f"Marked {count} requests as under review")
    mark_under_review.short_description = "Mark as under review"
    
    def approve_requests(self, request, queryset):
        count = 0
        for vendor_request in queryset.filter(status='under_review'):
            vendor_request.approve_request(request.user)
            count += 1
        self.message_user(request, f"Approved {count} vendor requests")
    approve_requests.short_description = "Approve selected requests"
    
    def reject_requests(self, request, queryset):
        count = queryset.filter(status__in=['submitted', 'under_review']).update(
            status='rejected',
            reviewed_by=request.user,
            review_date=timezone.now()
        )
        self.message_user(request, f"Rejected {count} vendor requests")
    reject_requests.short_description = "Reject selected requests"


@admin.register(StudentTransportAssignment)
class StudentTransportAssignmentAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'vendor', 'transport_type', 'pickup_time',
        'monthly_rate', 'status', 'start_date', 'end_date'
    ]
    list_filter = [
        'status', 'transport_type', 'vendor', 'start_date', 'created_at'
    ]
    search_fields = [
        'student__student_name', 'vendor__company_name',
        'pickup_address', 'drop_address', 'emergency_contact'
    ]
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['student', 'vendor', 'assigned_by']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Assignment Details', {
            'fields': (
                ('student', 'vendor'),
                ('transport_type', 'status'),
            )
        }),
        ('Service Details', {
            'fields': (
                ('pickup_address',),
                ('drop_address',),
                ('pickup_time', 'drop_time'),
            )
        }),
        ('Duration & Pricing', {
            'fields': (
                ('start_date', 'end_date'),
                ('monthly_rate',),
            )
        }),
        ('Emergency Contact', {
            'fields': (
                ('emergency_contact', 'emergency_phone'),
            )
        }),
        ('Additional Information', {
            'fields': (
                ('special_instructions',),
                ('assigned_by',),
            )
        }),
        ('Timestamps', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created_at']
    
    # Custom actions
    actions = ['activate_assignments', 'deactivate_assignments', 'cancel_assignments']
    
    def activate_assignments(self, request, queryset):
        queryset.update(status='active')
        self.message_user(request, f"Activated {queryset.count()} assignments")
    activate_assignments.short_description = "Activate selected assignments"
    
    def deactivate_assignments(self, request, queryset):
        queryset.update(status='inactive')
        self.message_user(request, f"Deactivated {queryset.count()} assignments")
    deactivate_assignments.short_description = "Deactivate selected assignments"
    
    def cancel_assignments(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f"Cancelled {queryset.count()} assignments")
    cancel_assignments.short_description = "Cancel selected assignments"


@admin.register(VendorPayment)
class VendorPaymentAdmin(admin.ModelAdmin):
    list_display = [
        'payment_id', 'vendor', 'payment_type', 'payment_month',
        'student_count', 'total_amount', 'status', 'payment_date'
    ]
    list_filter = [
        'status', 'payment_type', 'payment_method', 'payment_month',
        'payment_date', 'created_at'
    ]
    search_fields = [
        'payment_id', 'vendor__company_name', 'invoice_number',
        'reference_number', 'description'
    ]
    readonly_fields = [
        'payment_id', 'total_amount', 'created_at', 'updated_at'
    ]
    filter_horizontal = ['students_covered']
    raw_id_fields = ['vendor', 'created_by', 'approved_by']
    date_hierarchy = 'payment_month'
    
    fieldsets = (
        ('Payment Information', {
            'fields': (
                ('payment_id', 'status'),
                ('vendor', 'payment_type'),
            )
        }),
        ('Amount Details', {
            'fields': (
                ('amount', 'tax_amount'),
                ('total_amount',),
            )
        }),
        ('Period Details', {
            'fields': (
                ('payment_month',),
                ('from_date', 'to_date'),
                ('student_count',),
                ('students_covered',),
            )
        }),
        ('Payment Details', {
            'fields': (
                ('payment_method', 'payment_date'),
                ('reference_number',),
                ('invoice_number', 'receipt_uploaded'),
            )
        }),
        ('Description', {
            'fields': (
                ('description',),
                ('notes',),
            )
        }),
        ('Approval Process', {
            'fields': (
                ('created_by', 'approved_by'),
                ('approval_date',),
            )
        }),
        ('Timestamps', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-payment_month', '-created_at']
    
    # Custom actions
    actions = ['approve_payments', 'mark_paid']
    
    def approve_payments(self, request, queryset):
        count = queryset.filter(status='pending').update(
            status='processed',
            approved_by=request.user,
            approval_date=timezone.now()
        )
        self.message_user(request, f"Approved {count} payments")
    approve_payments.short_description = "Approve selected payments"
    
    def mark_paid(self, request, queryset):
        count = queryset.filter(status='processed').update(
            status='paid',
            payment_date=timezone.now().date()
        )
        self.message_user(request, f"Marked {count} payments as paid")
    mark_paid.short_description = "Mark selected payments as paid"


@admin.register(MonthlyPaymentGeneration)
class MonthlyPaymentGenerationAdmin(admin.ModelAdmin):
    list_display = [
        'generation_id', 'payment_month', 'status', 'total_vendors',
        'total_students', 'total_amount', 'generation_date'
    ]
    list_filter = [
        'status', 'payment_month', 'exclude_inactive', 'include_tax',
        'generation_date', 'approval_date'
    ]
    search_fields = [
        'generation_id', 'notes'
    ]
    readonly_fields = [
        'generation_id', 'total_vendors', 'total_students', 'total_amount',
        'generation_date', 'approval_date', 'created_at', 'updated_at'
    ]
    filter_horizontal = ['vendors']
    raw_id_fields = ['generated_by', 'approved_by']
    date_hierarchy = 'payment_month'
    
    fieldsets = (
        ('Generation Information', {
            'fields': (
                ('generation_id', 'status'),
                ('payment_month',),
            )
        }),
        ('Vendor Selection', {
            'fields': (
                ('vendors',),
                ('exclude_inactive',),
            )
        }),
        ('Tax Settings', {
            'fields': (
                ('include_tax', 'tax_rate'),
            )
        }),
        ('Results', {
            'fields': (
                ('total_vendors', 'total_students'),
                ('total_amount',),
            )
        }),
        ('Process Tracking', {
            'fields': (
                ('generated_by', 'generation_date'),
                ('approved_by', 'approval_date'),
                ('notes',),
            )
        }),
        ('Timestamps', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-payment_month', '-created_at']
    
    # Custom actions
    actions = ['generate_vendor_payments', 'approve_generations']
    
    def generate_vendor_payments(self, request, queryset):
        count = 0
        for generation in queryset.filter(status='draft'):
            generation.generate_payments()
            count += 1
        self.message_user(request, f"Generated payments for {count} records")
    generate_vendor_payments.short_description = "Generate vendor payments"
    
    def approve_generations(self, request, queryset):
        count = queryset.filter(status='generated').update(
            status='approved',
            approved_by=request.user,
            approval_date=timezone.now()
        )
        self.message_user(request, f"Approved {count} payment generations")
    approve_generations.short_description = "Approve selected generations"


@admin.register(VendorRating)
class VendorRatingAdmin(admin.ModelAdmin):
    list_display = [
        'vendor', 'student', 'rating', 'punctuality_rating',
        'safety_rating', 'driver_behavior_rating', 'created_at'
    ]
    list_filter = [
        'rating', 'punctuality_rating', 'safety_rating',
        'driver_behavior_rating', 'created_at'
    ]
    search_fields = [
        'vendor__company_name', 'student__student_name', 'review'
    ]
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['vendor', 'student', 'rated_by']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Rating Information', {
            'fields': (
                ('vendor', 'student'),
                ('rating',),
            )
        }),
        ('Detailed Ratings', {
            'fields': (
                ('punctuality_rating', 'safety_rating'),
                ('driver_behavior_rating',),
            )
        }),
        ('Review', {
            'fields': (
                ('review',),
            )
        }),
        ('Tracking', {
            'fields': (
                ('rated_by',),
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created_at']
