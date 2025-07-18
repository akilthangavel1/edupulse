from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from xstudent.models import NewStudent
from xcoursefee.models import Course
from xtrainer.models import Faculty


class Batch(models.Model):
    """Model for managing student batches"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('suspended', 'Suspended'),
    ]
    
    TIME_SLOT_CHOICES = [
        ('morning', 'Morning (8:00 AM - 12:00 PM)'),
        ('afternoon', 'Afternoon (1:00 PM - 5:00 PM)'),
        ('evening', 'Evening (6:00 PM - 10:00 PM)'),
        ('weekend', 'Weekend'),
        ('custom', 'Custom Time'),
    ]
    
    # Basic Information
    batch_code = models.CharField(max_length=20, unique=True, verbose_name="Batch Code")
    name = models.CharField(max_length=200, verbose_name="Batch Name")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='batches')
    description = models.TextField(blank=True, verbose_name="Description")
    
    # Scheduling
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(null=True, blank=True, verbose_name="End Date")
    time_slot = models.CharField(max_length=20, choices=TIME_SLOT_CHOICES, default='morning')
    custom_time_start = models.TimeField(null=True, blank=True, verbose_name="Custom Start Time")
    custom_time_end = models.TimeField(null=True, blank=True, verbose_name="Custom End Time")
    
    # Capacity and Management
    max_students = models.PositiveIntegerField(default=30, verbose_name="Maximum Students")
    current_students = models.PositiveIntegerField(default=0, verbose_name="Current Student Count")
    primary_faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True, 
                                      related_name='primary_batches', verbose_name="Primary Faculty")
    assistant_faculty = models.ManyToManyField(Faculty, blank=True, related_name='assistant_batches',
                                             verbose_name="Assistant Faculty")
    
    # WhatsApp Integration
    whatsapp_group_name = models.CharField(max_length=200, blank=True, verbose_name="WhatsApp Group Name")
    whatsapp_group_link = models.URLField(blank=True, verbose_name="WhatsApp Group Link")
    whatsapp_group_id = models.CharField(max_length=100, blank=True, verbose_name="WhatsApp Group ID")
    auto_add_students = models.BooleanField(default=True, verbose_name="Auto Add New Students to WhatsApp Group")
    
    # Status and Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_batches')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional Settings
    allow_late_enrollment = models.BooleanField(default=True, verbose_name="Allow Late Enrollment")
    notification_enabled = models.BooleanField(default=True, verbose_name="Enable Notifications")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Batch'
        verbose_name_plural = 'Batches'
    
    def __str__(self):
        return f"{self.batch_code} - {self.name}"
    
    def get_absolute_url(self):
        return reverse('batch_detail', kwargs={'pk': self.pk})
    
    def is_full(self):
        """Check if batch has reached maximum capacity"""
        return self.current_students >= self.max_students
    
    def get_available_spots(self):
        """Get number of available spots in batch"""
        return max(0, self.max_students - self.current_students)
    
    def get_enrolled_students(self):
        """Get all students enrolled in this batch"""
        return self.batch_students.filter(status='active').select_related('student')


class BatchStudent(models.Model):
    """Model for managing student enrollment in batches"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('transferred', 'Transferred'),
        ('dropped', 'Dropped'),
        ('completed', 'Completed'),
        ('suspended', 'Suspended'),
    ]
    
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='batch_students')
    student = models.ForeignKey(NewStudent, on_delete=models.CASCADE, related_name='batch_enrollments')
    enrollment_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # WhatsApp Integration
    added_to_whatsapp = models.BooleanField(default=False, verbose_name="Added to WhatsApp Group")
    whatsapp_phone = models.CharField(
        max_length=15, 
        blank=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be valid')],
        verbose_name="WhatsApp Phone Number"
    )
    
    # Metadata
    enrolled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True, verbose_name="Enrollment Notes")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['batch', 'student']
        ordering = ['-enrollment_date']
        verbose_name = 'Batch Student'
        verbose_name_plural = 'Batch Students'
    
    def __str__(self):
        return f"{self.student.student_name} - {self.batch.batch_code}"


class BatchTransfer(models.Model):
    """Model for managing student transfers between batches"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    TRANSFER_REASON_CHOICES = [
        ('time_conflict', 'Time Conflict'),
        ('level_mismatch', 'Level Mismatch'),
        ('personal_request', 'Personal Request'),
        ('capacity_issue', 'Capacity Issue'),
        ('faculty_change', 'Faculty Change'),
        ('other', 'Other'),
    ]
    
    # Transfer Details
    student = models.ForeignKey(NewStudent, on_delete=models.CASCADE, related_name='batch_transfers')
    from_batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='transfers_out')
    to_batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='transfers_in')
    
    # Request Information
    transfer_reason = models.CharField(max_length=20, choices=TRANSFER_REASON_CHOICES)
    reason_description = models.TextField(verbose_name="Detailed Reason")
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='requested_transfers')
    request_date = models.DateTimeField(default=timezone.now)
    
    # Approval Workflow
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_transfers')
    approval_date = models.DateTimeField(null=True, blank=True)
    approval_notes = models.TextField(blank=True)
    
    # Transfer Execution
    transfer_date = models.DateTimeField(null=True, blank=True)
    effective_date = models.DateField(verbose_name="Effective Transfer Date")
    
    # WhatsApp Group Management
    remove_from_old_group = models.BooleanField(default=True, verbose_name="Remove from Old WhatsApp Group")
    add_to_new_group = models.BooleanField(default=True, verbose_name="Add to New WhatsApp Group")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-request_date']
        verbose_name = 'Batch Transfer'
        verbose_name_plural = 'Batch Transfers'
    
    def __str__(self):
        return f"{self.student.student_name}: {self.from_batch.batch_code} → {self.to_batch.batch_code}"
    
    def approve_transfer(self, user):
        """Approve the transfer request"""
        self.status = 'approved'
        self.approved_by = user
        self.approval_date = timezone.now()
        self.save()
    
    def complete_transfer(self):
        """Execute the approved transfer"""
        if self.status == 'approved':
            # Update batch student records
            old_enrollment = BatchStudent.objects.get(batch=self.from_batch, student=self.student)
            old_enrollment.status = 'transferred'
            old_enrollment.save()
            
            # Create new enrollment
            BatchStudent.objects.create(
                batch=self.to_batch,
                student=self.student,
                enrolled_by=self.approved_by,
                notes=f"Transferred from {self.from_batch.batch_code}"
            )
            
            # Update batch student counts
            self.from_batch.current_students -= 1
            self.from_batch.save()
            
            self.to_batch.current_students += 1
            self.to_batch.save()
            
            # Update transfer status
            self.status = 'completed'
            self.transfer_date = timezone.now()
            self.save()


class BatchFacultyChange(models.Model):
    """Model for managing faculty changes in active batches"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('implemented', 'Implemented'),
        ('cancelled', 'Cancelled'),
    ]
    
    CHANGE_TYPE_CHOICES = [
        ('primary_change', 'Primary Faculty Change'),
        ('assistant_add', 'Add Assistant Faculty'),
        ('assistant_remove', 'Remove Assistant Faculty'),
        ('temporary_replacement', 'Temporary Replacement'),
    ]
    
    # Change Details
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='faculty_changes')
    change_type = models.CharField(max_length=25, choices=CHANGE_TYPE_CHOICES)
    
    # Faculty Information
    old_faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True, 
                                  related_name='old_faculty_changes')
    new_faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True, 
                                  related_name='new_faculty_changes')
    
    # Request Information
    reason = models.TextField(verbose_name="Reason for Change")
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    request_date = models.DateTimeField(default=timezone.now)
    effective_date = models.DateField(verbose_name="Effective Date")
    
    # Approval
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_faculty_changes')
    approval_date = models.DateTimeField(null=True, blank=True)
    
    # Implementation
    implementation_date = models.DateTimeField(null=True, blank=True)
    implementation_notes = models.TextField(blank=True)
    
    # Student Notification
    notify_students = models.BooleanField(default=True, verbose_name="Notify Students")
    notification_sent = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-request_date']
        verbose_name = 'Batch Faculty Change'
        verbose_name_plural = 'Batch Faculty Changes'
    
    def __str__(self):
        return f"{self.batch.batch_code} - {self.get_change_type_display()}"


class WhatsAppGroup(models.Model):
    """Model for managing WhatsApp group integration"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archived', 'Archived'),
    ]
    
    # Group Information
    group_name = models.CharField(max_length=200, verbose_name="Group Name")
    group_id = models.CharField(max_length=100, unique=True, verbose_name="WhatsApp Group ID")
    group_link = models.URLField(verbose_name="Group Invitation Link")
    
    # Association
    batch = models.OneToOneField(Batch, on_delete=models.CASCADE, related_name='whatsapp_group')
    
    # Settings
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    auto_add_members = models.BooleanField(default=True, verbose_name="Auto Add New Students")
    admin_numbers = models.TextField(verbose_name="Admin Phone Numbers (comma separated)", 
                                   help_text="Phone numbers of group admins")
    
    # Statistics
    total_members = models.PositiveIntegerField(default=0)
    last_sync = models.DateTimeField(null=True, blank=True, verbose_name="Last Member Sync")
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'WhatsApp Group'
        verbose_name_plural = 'WhatsApp Groups'
    
    def __str__(self):
        return f"{self.group_name} ({self.batch.batch_code})"
    
    def sync_members(self):
        """Sync group members with batch students"""
        # This would integrate with WhatsApp Business API
        # Implementation depends on the WhatsApp API being used
        pass
