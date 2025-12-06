from django.contrib import admin
from .models import TransportFee


@admin.register(TransportFee)
class TransportFeeAdmin(admin.ModelAdmin):
    list_display = ['student', 'amount', 'payment_date', 'created_at']
    list_filter = ['payment_date', 'created_at']
    search_fields = ['student__student_name', 'notes']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Fee Details', {
            'fields': (
                ('student', 'amount'),
                ('payment_date',),
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

    ordering = ['-payment_date']
