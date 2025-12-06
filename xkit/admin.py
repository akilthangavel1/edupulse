from django.contrib import admin
from django.utils import timezone
from .models import (
    MaterialCategory, Supplier, Material, MaterialKit,
    KitMaterial, StockMovement, KitAssemblyLog
)


@admin.register(MaterialCategory)
class MaterialCategoryAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'get_materials_count', 'created_at']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Category Information', {
            'fields': (
                ('code', 'name'),
                ('description',),
            )
        }),
        ('Timestamps', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',)
        }),
    )


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'name', 'contact_person', 'phone', 
        'city', 'status', 'rating', 'get_materials_count'
    ]
    list_filter = ['status', 'city', 'country', 'created_at']
    search_fields = [
        'code', 'name', 'contact_person', 'email', 
        'phone', 'trade_license', 'tax_number'
    ]
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('code', 'name'),
                ('status', 'rating'),
            )
        }),
        ('Contact Details', {
            'fields': (
                ('contact_person',),
                ('email', 'phone'),
                ('mobile',),
            )
        }),
        ('Address', {
            'fields': (
                ('address',),
                ('city', 'country'),
            )
        }),
        ('Business Details', {
            'fields': (
                ('trade_license', 'tax_number'),
                ('payment_terms',),
            )
        }),
        ('Timestamps', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',)
        }),
    )
    
    # Custom actions
    actions = ['activate_suppliers', 'deactivate_suppliers']
    
    def activate_suppliers(self, request, queryset):
        queryset.update(status='active')
        self.message_user(request, f"Activated {queryset.count()} suppliers")
    activate_suppliers.short_description = "Activate selected suppliers"
    
    def deactivate_suppliers(self, request, queryset):
        queryset.update(status='inactive')
        self.message_user(request, f"Deactivated {queryset.count()} suppliers")
    deactivate_suppliers.short_description = "Deactivate selected suppliers"


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = [
        'material_code', 'name', 'category', 'brand', 'unit',
        'unit_cost', 'selling_price', 'current_stock', 'status', 'is_low_stock'
    ]
    list_filter = [
        'status', 'category', 'unit', 'brand', 
        'primary_supplier', 'created_at'
    ]
    search_fields = [
        'material_code', 'name', 'brand', 'model', 
        'description', 'supplier_part_number'
    ]
    readonly_fields = ['times_used', 'created_at', 'updated_at']
    raw_id_fields = ['category', 'primary_supplier', 'created_by']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('material_code', 'status'),
                ('name',),
                ('category',),
                ('description',),
            )
        }),
        ('Specifications', {
            'fields': (
                ('brand', 'model'),
                ('color', 'size'),
                ('weight',),
            )
        }),
        ('Pricing & Unit', {
            'fields': (
                ('unit',),
                ('unit_cost', 'selling_price'),
            )
        }),
        ('Stock Management', {
            'fields': (
                ('current_stock',),
                ('minimum_stock', 'maximum_stock'),
            )
        }),
        ('Supplier Information', {
            'fields': (
                ('primary_supplier',),
                ('supplier_part_number',),
            )
        }),
        ('Storage', {
            'fields': (
                ('storage_location', 'shelf_number'),
            )
        }),
        ('Additional', {
            'fields': (
                ('image',),
                ('times_used',),
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
    
    ordering = ['name']
    
    # Custom actions
    actions = ['mark_available', 'mark_out_of_stock', 'mark_discontinued']
    
    def mark_available(self, request, queryset):
        queryset.update(status='available')
        self.message_user(request, f"Marked {queryset.count()} materials as available")
    mark_available.short_description = "Mark as available"
    
    def mark_out_of_stock(self, request, queryset):
        queryset.update(status='out_of_stock')
        self.message_user(request, f"Marked {queryset.count()} materials as out of stock")
    mark_out_of_stock.short_description = "Mark as out of stock"
    
    def mark_discontinued(self, request, queryset):
        queryset.update(status='discontinued')
        self.message_user(request, f"Marked {queryset.count()} materials as discontinued")
    mark_discontinued.short_description = "Mark as discontinued"
    
    def is_low_stock(self, obj):
        return obj.is_low_stock()
    is_low_stock.boolean = True
    is_low_stock.short_description = "Low Stock"


class KitMaterialInline(admin.TabularInline):
    model = KitMaterial
    extra = 1
    raw_id_fields = ['material', 'added_by']
    fields = [
        'material', 'quantity_needed', 'is_optional', 
        'assembly_order', 'cost_override', 'notes'
    ]


@admin.register(MaterialKit)
class MaterialKitAdmin(admin.ModelAdmin):
    list_display = [
        'kit_code', 'name', 'category', 'status', 
        'base_cost', 'selling_price', 'kits_in_stock', 
        'can_assemble_count', 'get_total_materials_count'
    ]
    list_filter = [
        'status', 'category', 'is_template', 
        'auto_calculate_price', 'created_at'
    ]
    search_fields = [
        'kit_code', 'name', 'description'
    ]
    readonly_fields = [
        'can_assemble_count', 'created_at', 'updated_at'
    ]
    raw_id_fields = ['category', 'template_for', 'linked_coursefee_kit', 'created_by']
    inlines = [KitMaterialInline]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('kit_code', 'status'),
                ('name',),
                ('category',),
                ('description',),
            )
        }),
        ('Template & Linking', {
            'fields': (
                ('is_template', 'template_for'),
                ('linked_coursefee_kit',),
            )
        }),
        ('Pricing', {
            'fields': (
                ('auto_calculate_price',),
                ('base_cost', 'markup_percentage'),
                ('selling_price',),
            )
        }),
        ('Stock & Assembly', {
            'fields': (
                ('kits_in_stock', 'minimum_kit_stock'),
                ('can_assemble_count',),
                ('assembly_time_minutes',),
            )
        }),
        ('Assembly Details', {
            'fields': (
                ('assembly_instructions',),
                ('quality_checklist',),
            ),
            'classes': ('collapse',)
        }),
        ('Tracking', {
            'fields': (
                ('created_by',),
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['name']
    
    # Custom actions
    actions = ['activate_kits', 'deactivate_kits', 'update_assembly_counts', 'sync_with_coursefee']
    
    def activate_kits(self, request, queryset):
        queryset.update(status='active')
        self.message_user(request, f"Activated {queryset.count()} kits")
    activate_kits.short_description = "Activate selected kits"
    
    def deactivate_kits(self, request, queryset):
        queryset.update(status='inactive')
        self.message_user(request, f"Deactivated {queryset.count()} kits")
    deactivate_kits.short_description = "Deactivate selected kits"
    
    def update_assembly_counts(self, request, queryset):
        for kit in queryset:
            kit.update_can_assemble_count()
        self.message_user(request, f"Updated assembly counts for {queryset.count()} kits")
    update_assembly_counts.short_description = "Update assembly counts"
    
    def sync_with_coursefee(self, request, queryset):
        count = 0
        for kit in queryset:
            if kit.linked_coursefee_kit:
                kit.sync_with_coursefee_kit()
                count += 1
        self.message_user(request, f"Synced {count} kits with course fee system")
    sync_with_coursefee.short_description = "Sync with course fee kits"


@admin.register(KitMaterial)
class KitMaterialAdmin(admin.ModelAdmin):
    list_display = [
        'kit', 'material', 'quantity_needed', 'is_optional',
        'assembly_order', 'get_total_cost', 'is_available'
    ]
    list_filter = ['is_optional', 'kit__status', 'added_at']
    search_fields = [
        'kit__name', 'kit__kit_code', 
        'material__name', 'material__material_code'
    ]
    readonly_fields = ['added_at']
    raw_id_fields = ['kit', 'material', 'added_by']
    date_hierarchy = 'added_at'
    
    fieldsets = (
        ('Kit & Material', {
            'fields': (
                ('kit', 'material'),
                ('quantity_needed', 'is_optional'),
            )
        }),
        ('Assembly', {
            'fields': (
                ('assembly_order',),
                ('assembly_notes',),
            )
        }),
        ('Cost', {
            'fields': (
                ('cost_override',),
            )
        }),
        ('Additional', {
            'fields': (
                ('notes',),
                ('added_by', 'added_at'),
            )
        }),
    )
    
    ordering = ['kit', 'assembly_order']


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = [
        'material', 'movement_type', 'quantity', 
        'stock_before', 'stock_after', 'reference_type',
        'reference_id', 'created_at', 'created_by'
    ]
    list_filter = [
        'movement_type', 'reference_type', 'created_at', 'material__category'
    ]
    search_fields = [
        'material__name', 'material__material_code',
        'reference_id', 'reference_description', 'notes'
    ]
    readonly_fields = ['created_at']
    raw_id_fields = ['material', 'created_by']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Movement Details', {
            'fields': (
                ('material',),
                ('movement_type', 'quantity'),
                ('stock_before', 'stock_after'),
            )
        }),
        ('Reference Information', {
            'fields': (
                ('reference_type', 'reference_id'),
                ('reference_description',),
            )
        }),
        ('Cost Information', {
            'fields': (
                ('unit_cost', 'total_cost'),
            )
        }),
        ('Tracking', {
            'fields': (
                ('created_by', 'created_at'),
                ('notes',),
            )
        }),
    )
    
    ordering = ['-created_at']


@admin.register(KitAssemblyLog)
class KitAssemblyLogAdmin(admin.ModelAdmin):
    list_display = [
        'kit', 'quantity_to_assemble', 'quantity_completed',
        'status', 'quality_check_passed', 'start_time', 
        'assembled_by', 'total_material_cost'
    ]
    list_filter = [
        'status', 'quality_check_passed', 'start_time',
        'end_time', 'kit__status'
    ]
    search_fields = [
        'kit__name', 'kit__kit_code', 
        'issues_encountered', 'quality_notes'
    ]
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['kit', 'assembled_by', 'supervised_by']
    date_hierarchy = 'start_time'
    
    fieldsets = (
        ('Assembly Information', {
            'fields': (
                ('kit', 'status'),
                ('quantity_to_assemble', 'quantity_completed'),
            )
        }),
        ('Process Details', {
            'fields': (
                ('start_time', 'end_time'),
                ('actual_assembly_time',),
            )
        }),
        ('Quality Control', {
            'fields': (
                ('quality_check_passed',),
                ('quality_notes',),
            )
        }),
        ('Cost Tracking', {
            'fields': (
                ('total_material_cost', 'labor_cost'),
            )
        }),
        ('Issues', {
            'fields': (
                ('issues_encountered',),
                ('materials_shortage',),
            ),
            'classes': ('collapse',)
        }),
        ('Team', {
            'fields': (
                ('assembled_by', 'supervised_by'),
            )
        }),
        ('Timestamps', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-start_time']
    
    # Custom actions
    actions = ['mark_completed', 'mark_failed']
    
    def mark_completed(self, request, queryset):
        queryset.update(
            status='completed',
            end_time=timezone.now()
        )
        self.message_user(request, f"Marked {queryset.count()} assembly logs as completed")
    mark_completed.short_description = "Mark as completed"
    
    def mark_failed(self, request, queryset):
        queryset.update(
            status='failed',
            end_time=timezone.now()
        )
        self.message_user(request, f"Marked {queryset.count()} assembly logs as failed")
    mark_failed.short_description = "Mark as failed"
