from django.contrib import admin
from .models import Batch, BatchStudent, BatchTransfer, BatchFacultyChange, WhatsAppGroup


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['batch_code', 'name', 'course', 'status', 'start_date', 'current_students', 'max_students']
    list_filter = ['status', 'course', 'start_date']
    search_fields = ['batch_code', 'name', 'course__name']
    filter_horizontal = ['assistant_faculty']
    date_hierarchy = 'start_date'


@admin.register(BatchStudent)
class BatchStudentAdmin(admin.ModelAdmin):
    list_display = ['batch', 'student', 'status', 'enrollment_date', 'added_to_whatsapp']
    list_filter = ['status', 'batch', 'enrollment_date', 'added_to_whatsapp']
    search_fields = ['student__student_name', 'batch__batch_code']
    date_hierarchy = 'enrollment_date'


@admin.register(BatchTransfer)
class BatchTransferAdmin(admin.ModelAdmin):
    list_display = ['student', 'from_batch', 'to_batch', 'status', 'request_date', 'effective_date']
    list_filter = ['status', 'transfer_reason', 'request_date']
    search_fields = ['student__student_name', 'from_batch__batch_code', 'to_batch__batch_code']
    date_hierarchy = 'request_date'


@admin.register(BatchFacultyChange)
class BatchFacultyChangeAdmin(admin.ModelAdmin):
    list_display = ['batch', 'change_type', 'old_faculty', 'new_faculty', 'status', 'effective_date']
    list_filter = ['status', 'change_type', 'request_date']
    search_fields = ['batch__batch_code', 'old_faculty__first_name', 'new_faculty__first_name']
    date_hierarchy = 'request_date'


@admin.register(WhatsAppGroup)
class WhatsAppGroupAdmin(admin.ModelAdmin):
    list_display = ['group_name', 'batch', 'status', 'total_members', 'auto_add_members', 'last_sync']
    list_filter = ['status', 'auto_add_members']
    search_fields = ['group_name', 'batch__batch_code', 'group_id']