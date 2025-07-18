from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html
from .models import (
    Course, FeeStructure, StudentEnrollment, 
    Discount, Invoice, Payment, Kit, CourseKit, KitFee
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'course_code', 'course_type', 'status', 'instructor_name',
        'duration_display', 'max_students', 'enrollment_count', 'created_at'
    ]
    list_filter = [
        'course_type', 'status', 'duration_unit', 'created_at'
    ]
    search_fields = [
        'name', 'course_code', 'instructor_name', 'description'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('name', 'course_code'),
                ('course_type', 'status'),
                ('description',),
                ('instructor_name',),
            )
        }),
        ('Duration & Scheduling', {
            'fields': (
                ('duration', 'duration_unit'),
                ('start_date', 'end_date'),
            )
        }),
        ('Capacity & Requirements', {
            'fields': (
                ('max_students',),
                ('min_age', 'max_age'),
                ('prerequisites',),
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
    
    def duration_display(self, obj):
        return f"{obj.duration} {obj.get_duration_unit_display()}"
    duration_display.short_description = "Duration"
    
    def enrollment_count(self, obj):
        count = obj.enrollments.filter(status='active').count()
        return format_html(
            '<span style="color: {};">{}/{}</span>',
            'red' if count >= obj.max_students else 'green',
            count,
            obj.max_students
        )
    enrollment_count.short_description = "Enrollments"
    
    def mark_active(self, request, queryset):
        queryset.update(status='active')
    mark_active.short_description = "Mark selected courses as active"
    
    def mark_inactive(self, request, queryset):
        queryset.update(status='inactive')
    mark_inactive.short_description = "Mark selected courses as inactive"


class FeeStructureInline(admin.TabularInline):
    model = FeeStructure
    extra = 1
    fields = ['fee_type', 'amount', 'payment_frequency', 'is_mandatory', 'due_date_offset']


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = [
        'course', 'fee_type', 'amount', 'payment_frequency', 
        'is_mandatory', 'due_date_offset'
    ]
    list_filter = [
        'fee_type', 'payment_frequency', 'is_mandatory', 'course__status'
    ]
    search_fields = [
        'course__name', 'course__course_code', 'description'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Fee Information', {
            'fields': (
                ('course', 'fee_type'),
                ('amount', 'payment_frequency'),
                ('is_mandatory', 'due_date_offset'),
                ('description',),
            )
        }),
        ('Timestamps', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',),
        }),
    )


@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'course', 'enrollment_date', 'status', 
        'total_fees_display', 'total_paid_display', 'balance_display'
    ]
    list_filter = [
        'status', 'enrollment_date', 'course__course_type', 'course__status'
    ]
    search_fields = [
        'student__student_name', 'student__email_id', 
        'course__name', 'course__course_code'
    ]
    readonly_fields = ['created_at', 'updated_at', 'total_fees_display', 'total_paid_display', 'balance_display']
    date_hierarchy = 'enrollment_date'
    
    fieldsets = (
        ('Enrollment Information', {
            'fields': (
                ('student', 'course'),
                ('enrollment_date', 'status'),
                ('enrollment_notes',),
            )
        }),
        ('Completion Details', {
            'fields': (
                ('completion_date', 'final_grade'),
            ),
            'classes': ('collapse',),
        }),
        ('Financial Summary', {
            'fields': (
                ('total_fees_display', 'total_paid_display', 'balance_display'),
            ),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',),
        }),
    )
    
    actions = ['mark_completed', 'mark_active', 'mark_dropped']
    
    def total_fees_display(self, obj):
        return f"{obj.get_total_fees()} KWD"
    total_fees_display.short_description = "Total Fees"
    
    def total_paid_display(self, obj):
        return f"{obj.get_total_paid()} KWD"
    total_paid_display.short_description = "Total Paid"
    
    def balance_display(self, obj):
        balance = obj.get_outstanding_balance()
        color = 'red' if balance > 0 else 'green'
        return format_html(
            '<span style="color: {};">{} KWD</span>',
            color,
            balance
        )
    balance_display.short_description = "Outstanding Balance"
    
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_completed.short_description = "Mark selected enrollments as completed"
    
    def mark_active(self, request, queryset):
        queryset.update(status='active')
    mark_active.short_description = "Mark selected enrollments as active"
    
    def mark_dropped(self, request, queryset):
        queryset.update(status='dropped')
    mark_dropped.short_description = "Mark selected enrollments as dropped"


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'enrollment_student', 'enrollment_course', 'amount', 'payment_date',
        'payment_method', 'status', 'receipt_number', 'processed_by'
    ]
    list_filter = [
        'status', 'payment_method', 'payment_date', 'processed_by'
    ]
    search_fields = [
        'enrollment__student__student_name', 'enrollment__course__name',
        'reference_number', 'receipt_number', 'notes'
    ]
    readonly_fields = ['created_at', 'updated_at', 'receipt_number']
    date_hierarchy = 'payment_date'
    
    fieldsets = (
        ('Payment Information', {
            'fields': (
                ('enrollment', 'invoice'),
                ('amount', 'payment_date'),
                ('payment_method', 'status'),
                ('reference_number', 'receipt_number'),
                ('processed_by',),
                ('notes',),
            )
        }),
        ('Timestamps', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',),
        }),
    )
    
    actions = ['mark_completed', 'mark_pending', 'mark_failed']
    
    def enrollment_student(self, obj):
        return obj.enrollment.student.student_name
    enrollment_student.short_description = "Student"
    
    def enrollment_course(self, obj):
        return obj.enrollment.course.name
    enrollment_course.short_description = "Course"
    
    def mark_completed(self, request, queryset):
        queryset.update(status='completed', processed_by=request.user)
    mark_completed.short_description = "Mark selected payments as completed"
    
    def mark_pending(self, request, queryset):
        queryset.update(status='pending')
    mark_pending.short_description = "Mark selected payments as pending"
    
    def mark_failed(self, request, queryset):
        queryset.update(status='failed')
    mark_failed.short_description = "Mark selected payments as failed"
    
    def save_model(self, request, obj, form, change):
        if not obj.processed_by:
            obj.processed_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'invoice_number', 'enrollment_student', 'enrollment_course',
        'issue_date', 'due_date', 'total_amount', 'status', 'is_overdue'
    ]
    list_filter = [
        'status', 'issue_date', 'due_date'
    ]
    search_fields = [
        'invoice_number', 'enrollment__student__student_name',
        'enrollment__course__name', 'notes'
    ]
    readonly_fields = ['created_at', 'updated_at', 'invoice_number', 'is_overdue']
    date_hierarchy = 'issue_date'
    
    fieldsets = (
        ('Invoice Information', {
            'fields': (
                ('enrollment', 'invoice_number'),
                ('issue_date', 'due_date'),
                ('status',),
            )
        }),
        ('Amount Details', {
            'fields': (
                ('subtotal', 'discount_amount'),
                ('total_amount', 'applied_discount'),
            )
        }),
        ('Additional Information', {
            'fields': (
                ('notes',),
                ('is_overdue',),
            ),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',),
        }),
    )
    
    actions = ['mark_sent', 'mark_paid', 'mark_overdue']
    
    def enrollment_student(self, obj):
        return obj.enrollment.student.student_name
    enrollment_student.short_description = "Student"
    
    def enrollment_course(self, obj):
        return obj.enrollment.course.name
    enrollment_course.short_description = "Course"
    
    def is_overdue(self, obj):
        from django.utils import timezone
        if obj.status == 'sent' and obj.due_date < timezone.now().date():
            return format_html('<span style="color: red;">Yes</span>')
        return 'No'
    is_overdue.short_description = "Overdue"
    
    def mark_sent(self, request, queryset):
        queryset.update(status='sent')
    mark_sent.short_description = "Mark selected invoices as sent"
    
    def mark_paid(self, request, queryset):
        queryset.update(status='paid')
    mark_paid.short_description = "Mark selected invoices as paid"
    
    def mark_overdue(self, request, queryset):
        queryset.update(status='overdue')
    mark_overdue.short_description = "Mark selected invoices as overdue"


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'discount_type', 'value_display', 'applicability',
        'valid_from', 'valid_until', 'usage_display', 'is_active', 'is_valid_now'
    ]
    list_filter = [
        'discount_type', 'applicability', 'is_active', 'valid_from', 'valid_until'
    ]
    search_fields = [
        'name', 'description'
    ]
    readonly_fields = ['created_at', 'updated_at', 'current_usage', 'is_valid_now']
    filter_horizontal = ['eligible_courses']
    
    fieldsets = (
        ('Discount Information', {
            'fields': (
                ('name', 'discount_type'),
                ('value', 'applicability'),
                ('description',),
                ('is_active',),
            )
        }),
        ('Validity & Usage', {
            'fields': (
                ('valid_from', 'valid_until'),
                ('max_usage', 'current_usage'),
                ('min_enrollment_count',),
                ('is_valid_now',),
            )
        }),
        ('Eligible Courses', {
            'fields': (
                ('eligible_courses',),
            ),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',),
        }),
    )
    
    actions = ['activate_discount', 'deactivate_discount']
    
    def value_display(self, obj):
        if obj.discount_type == 'percentage':
            return f"{obj.value}%"
        else:
            return f"{obj.value} KWD"
    value_display.short_description = "Value"
    
    def usage_display(self, obj):
        if obj.max_usage:
            return f"{obj.current_usage}/{obj.max_usage}"
        return f"{obj.current_usage}/∞"
    usage_display.short_description = "Usage"
    
    def is_valid_now(self, obj):
        return obj.is_valid()
    is_valid_now.short_description = "Valid Now"
    is_valid_now.boolean = True
    
    def activate_discount(self, request, queryset):
        queryset.update(is_active=True)
    activate_discount.short_description = "Activate selected discounts"
    
    def deactivate_discount(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_discount.short_description = "Deactivate selected discounts"


@admin.register(Kit)
class KitAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'kit_code', 'price', 'status', 'stock_display', 
        'is_mandatory', 'supplier', 'created_at'
    ]
    list_filter = [
        'status', 'is_mandatory', 'created_at', 'supplier'
    ]
    search_fields = [
        'name', 'kit_code', 'description', 'contents', 'supplier'
    ]
    readonly_fields = ['created_at', 'updated_at', 'stock_status']
    
    fieldsets = (
        ('Kit Information', {
            'fields': (
                ('name', 'kit_code'),
                ('description',),
                ('price', 'status'),
                ('is_mandatory',),
                ('contents',),
            )
        }),
        ('Inventory Management', {
            'fields': (
                ('stock_quantity', 'minimum_stock'),
                ('stock_status',),
            )
        }),
        ('Supplier Information', {
            'fields': (
                ('supplier', 'supplier_contact'),
            ),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',),
        }),
    )
    
    actions = ['mark_available', 'mark_out_of_stock', 'mark_discontinued', 'restock_alert']
    
    def stock_display(self, obj):
        color = 'red' if obj.is_low_stock() else 'green'
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            f"{obj.stock_quantity} (Min: {obj.minimum_stock})"
        )
    stock_display.short_description = "Stock Level"
    
    def stock_status(self, obj):
        if obj.is_low_stock():
            return format_html('<span style="color: red; font-weight: bold;">LOW STOCK</span>')
        elif obj.stock_quantity == 0:
            return format_html('<span style="color: red; font-weight: bold;">OUT OF STOCK</span>')
        else:
            return format_html('<span style="color: green;">ADEQUATE</span>')
    stock_status.short_description = "Stock Status"
    
    def mark_available(self, request, queryset):
        queryset.update(status='available')
    mark_available.short_description = "Mark selected kits as available"
    
    def mark_out_of_stock(self, request, queryset):
        queryset.update(status='out_of_stock')
    mark_out_of_stock.short_description = "Mark selected kits as out of stock"
    
    def mark_discontinued(self, request, queryset):
        queryset.update(status='discontinued')
    mark_discontinued.short_description = "Mark selected kits as discontinued"
    
    def restock_alert(self, request, queryset):
        low_stock_kits = [kit for kit in queryset if kit.is_low_stock()]
        if low_stock_kits:
            kit_names = ', '.join([kit.name for kit in low_stock_kits])
            self.message_user(request, f"Low stock alert for: {kit_names}")
        else:
            self.message_user(request, "No low stock kits in selection")
    restock_alert.short_description = "Check stock levels"


class CourseKitInline(admin.TabularInline):
    model = CourseKit
    extra = 1
    fields = ['kit', 'is_required', 'distribution_date', 'notes']
    autocomplete_fields = ['kit']


@admin.register(CourseKit)
class CourseKitAdmin(admin.ModelAdmin):
    list_display = [
        'course', 'kit', 'kit_price', 'is_required', 'distribution_date', 
        'kit_status', 'created_at'
    ]
    list_filter = [
        'is_required', 'distribution_date', 'kit__status', 'course__status'
    ]
    search_fields = [
        'course__name', 'course__course_code', 'kit__name', 'kit__kit_code'
    ]
    readonly_fields = ['created_at', 'updated_at', 'kit_price', 'kit_status']
    autocomplete_fields = ['course', 'kit']
    
    fieldsets = (
        ('Course-Kit Relationship', {
            'fields': (
                ('course', 'kit'),
                ('is_required', 'distribution_date'),
                ('notes',),
            )
        }),
        ('Kit Details', {
            'fields': (
                ('kit_price', 'kit_status'),
            ),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',),
        }),
    )
    
    actions = ['mark_required', 'mark_optional', 'update_distribution_dates']
    
    def kit_price(self, obj):
        return f"{obj.kit.price} KWD"
    kit_price.short_description = "Kit Price"
    
    def kit_status(self, obj):
        status = obj.kit.status
        color = 'green' if status == 'available' else 'red'
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.kit.get_status_display()
        )
    kit_status.short_description = "Kit Status"
    
    def mark_required(self, request, queryset):
        queryset.update(is_required=True)
    mark_required.short_description = "Mark selected kits as required"
    
    def mark_optional(self, request, queryset):
        queryset.update(is_required=False)
    mark_optional.short_description = "Mark selected kits as optional"
    
    def update_distribution_dates(self, request, queryset):
        from django.utils import timezone
        queryset.update(distribution_date=timezone.now().date())
    update_distribution_dates.short_description = "Set distribution date to today"


@admin.register(KitFee)
class KitFeeAdmin(admin.ModelAdmin):
    list_display = [
        'student_name', 'course_name', 'kit_name', 'amount', 
        'payment_status', 'delivery_status', 'payment_date', 'delivery_date'
    ]
    list_filter = [
        'payment_status', 'delivery_status', 'payment_date', 'delivery_date',
        'course_kit__course__status', 'course_kit__kit__status'
    ]
    search_fields = [
        'enrollment__student__student_name', 'enrollment__course__name',
        'course_kit__kit__name', 'payment_reference', 'notes'
    ]
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['enrollment', 'course_kit', 'processed_by']
    date_hierarchy = 'payment_date'
    
    fieldsets = (
        ('Kit Fee Information', {
            'fields': (
                ('enrollment', 'course_kit'),
                ('amount',),
                ('notes',),
            )
        }),
        ('Payment Details', {
            'fields': (
                ('payment_status', 'payment_date'),
                ('payment_method', 'payment_reference'),
                ('processed_by',),
            )
        }),
        ('Delivery Details', {
            'fields': (
                ('delivery_status', 'delivery_date'),
                ('collected_by',),
            )
        }),
        ('Timestamps', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',),
        }),
    )
    
    actions = [
        'mark_payment_paid', 'mark_payment_pending', 'mark_delivered', 
        'mark_collected', 'process_bulk_payment'
    ]
    
    def student_name(self, obj):
        return obj.enrollment.student.student_name
    student_name.short_description = "Student"
    
    def course_name(self, obj):
        return obj.enrollment.course.name
    course_name.short_description = "Course"
    
    def kit_name(self, obj):
        return obj.course_kit.kit.name
    kit_name.short_description = "Kit"
    
    def mark_payment_paid(self, request, queryset):
        from django.utils import timezone
        queryset.update(
            payment_status='paid',
            payment_date=timezone.now().date(),
            processed_by=request.user
        )
        self.message_user(request, f"Marked {queryset.count()} kit fees as paid")
    mark_payment_paid.short_description = "Mark selected kit fees as paid"
    
    def mark_payment_pending(self, request, queryset):
        queryset.update(payment_status='pending', payment_date=None)
    mark_payment_pending.short_description = "Mark selected kit fees as pending"
    
    def mark_delivered(self, request, queryset):
        from django.utils import timezone
        paid_fees = queryset.filter(payment_status='paid')
        paid_fees.update(
            delivery_status='delivered',
            delivery_date=timezone.now().date()
        )
        
        # Update stock for delivered kits
        for kit_fee in paid_fees:
            kit = kit_fee.course_kit.kit
            if kit.stock_quantity > 0:
                kit.stock_quantity -= 1
                kit.save()
        
        self.message_user(request, f"Marked {paid_fees.count()} kit fees as delivered")
    mark_delivered.short_description = "Mark selected kit fees as delivered (paid only)"
    
    def mark_collected(self, request, queryset):
        from django.utils import timezone
        delivered_fees = queryset.filter(delivery_status='delivered')
        delivered_fees.update(
            delivery_status='collected',
            delivery_date=timezone.now().date()
        )
        self.message_user(request, f"Marked {delivered_fees.count()} kit fees as collected")
    mark_collected.short_description = "Mark selected kit fees as collected"
    
    def process_bulk_payment(self, request, queryset):
        from django.utils import timezone
        pending_fees = queryset.filter(payment_status='pending')
        pending_fees.update(
            payment_status='paid',
            payment_date=timezone.now().date(),
            payment_method='cash',
            processed_by=request.user
        )
        self.message_user(request, f"Processed {pending_fees.count()} kit fee payments")
    process_bulk_payment.short_description = "Process bulk cash payments"
    
    def save_model(self, request, obj, form, change):
        if not obj.processed_by:
            obj.processed_by = request.user
        super().save_model(request, obj, form, change)


# Update Course admin to include kit inlines
CourseAdmin.inlines = [FeeStructureInline, CourseKitInline]


# Customize admin site header
admin.site.site_header = "EduPulse Course Fee Administration"
admin.site.site_title = "EduPulse Course Fee Admin"
admin.site.index_title = "Welcome to Course Fee Management"
