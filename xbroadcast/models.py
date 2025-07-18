from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, EmailValidator, MinValueValidator
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from xstudent.models import NewStudent
from xcoursefee.models import Course
from xbatch.models import Batch


class BroadcastTemplate(models.Model):
    """Model for predefined broadcast message templates"""
    
    TEMPLATE_TYPE_CHOICES = [
        ('general', 'General'),
        ('new_batch', 'New Batch'),
        ('holiday', 'Holiday'),
        ('fee_reminder', 'Fee Reminder'),
        ('exam_notice', 'Exam Notice'),
        ('event', 'Event Announcement'),
        ('promotion', 'Promotion'),
        ('welcome', 'Welcome Message'),
        ('completion', 'Course Completion'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Template Name")
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPE_CHOICES, verbose_name="Template Type")
    
    # Message Content
    subject = models.CharField(max_length=200, verbose_name="Subject/Title")
    message_content = models.TextField(verbose_name="Message Content")
    sms_content = models.TextField(blank=True, verbose_name="SMS Content (160 chars max)")
    
    # Template Variables (placeholders)
    variables_description = models.TextField(
        blank=True, 
        verbose_name="Variables Description",
        help_text="Describe available variables like {student_name}, {course_name}, etc."
    )
    
    # Settings
    is_active = models.BooleanField(default=True, verbose_name="Active Template")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_templates')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['template_type', 'name']
        verbose_name = 'Broadcast Template'
        verbose_name_plural = 'Broadcast Templates'
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"


class Broadcast(models.Model):
    """Model for broadcast messages sent to students and leads"""
    
    BROADCAST_TYPE_CHOICES = [
        ('general', 'General Broadcast'),
        ('batch_specific', 'Batch Specific'),
        ('course_specific', 'Course Specific'),
        ('fee_reminder', 'Fee Reminder'),
        ('lead_followup', 'Lead Follow-up'),
        ('custom', 'Custom Group'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sending', 'Sending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    CHANNEL_CHOICES = [
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('all', 'All Channels'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200, verbose_name="Broadcast Title")
    broadcast_type = models.CharField(max_length=20, choices=BROADCAST_TYPE_CHOICES, verbose_name="Broadcast Type")
    template = models.ForeignKey(BroadcastTemplate, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name='broadcasts', verbose_name="Template Used")
    
    # Message Content
    subject = models.CharField(max_length=200, verbose_name="Subject/Title")
    message_content = models.TextField(verbose_name="Message Content")
    sms_content = models.TextField(blank=True, verbose_name="SMS Content")
    
    # Targeting
    target_all_students = models.BooleanField(default=False, verbose_name="Target All Students")
    target_all_leads = models.BooleanField(default=False, verbose_name="Target All Leads")
    target_batches = models.ManyToManyField(Batch, blank=True, verbose_name="Target Batches")
    target_courses = models.ManyToManyField(Course, blank=True, verbose_name="Target Courses")
    target_students = models.ManyToManyField(NewStudent, blank=True, verbose_name="Target Students")
    
    # Custom Targeting Criteria
    target_grade_filter = models.CharField(max_length=100, blank=True, verbose_name="Grade Filter")
    target_program_filter = models.CharField(max_length=100, blank=True, verbose_name="Program Filter")
    target_fee_status_filter = models.CharField(
        max_length=20, 
        choices=[
            ('paid', 'Paid'),
            ('pending', 'Pending'),
            ('overdue', 'Overdue'),
        ],
        blank=True,
        verbose_name="Fee Status Filter"
    )
    
    # Delivery Settings
    channels = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default='all', verbose_name="Channels")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal', verbose_name="Priority")
    
    # Scheduling
    send_immediately = models.BooleanField(default=True, verbose_name="Send Immediately")
    scheduled_time = models.DateTimeField(null=True, blank=True, verbose_name="Scheduled Time")
    
    # Status and Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    total_recipients = models.PositiveIntegerField(default=0, verbose_name="Total Recipients")
    sent_count = models.PositiveIntegerField(default=0, verbose_name="Successfully Sent")
    failed_count = models.PositiveIntegerField(default=0, verbose_name="Failed")
    delivery_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Delivery Rate (%)"
    )
    
    # Cost Tracking
    sms_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        default=Decimal('0.000'),
        validators=[MinValueValidator(Decimal('0.000'))],
        verbose_name="SMS Cost (KWD)"
    )
    email_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        default=Decimal('0.000'),
        validators=[MinValueValidator(Decimal('0.000'))],
        verbose_name="Email Cost (KWD)"
    )
    whatsapp_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        default=Decimal('0.000'),
        validators=[MinValueValidator(Decimal('0.000'))],
        verbose_name="WhatsApp Cost (KWD)"
    )
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_broadcasts')
    sent_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_broadcasts')
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Settings
    track_clicks = models.BooleanField(default=True, verbose_name="Track Link Clicks")
    track_opens = models.BooleanField(default=True, verbose_name="Track Email Opens")
    allow_replies = models.BooleanField(default=True, verbose_name="Allow Replies")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Broadcast'
        verbose_name_plural = 'Broadcasts'
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
    
    def get_absolute_url(self):
        return reverse('broadcast_detail', kwargs={'pk': self.pk})
    
    def calculate_total_cost(self):
        """Calculate total broadcast cost"""
        return self.sms_cost + self.email_cost + self.whatsapp_cost
    
    def update_delivery_rate(self):
        """Update delivery rate percentage"""
        if self.total_recipients > 0:
            self.delivery_rate = (self.sent_count / self.total_recipients) * 100
        else:
            self.delivery_rate = Decimal('0.00')
        self.save(update_fields=['delivery_rate'])
    
    def get_target_recipients_count(self):
        """Calculate number of target recipients"""
        count = 0
        
        if self.target_all_students:
            count += NewStudent.objects.filter(status='active').count()
        
        if self.target_all_leads:
            count += Lead.objects.filter(status__in=['new', 'contacted', 'interested']).count()
        
        # Add batch-specific counts
        for batch in self.target_batches.all():
            count += batch.get_enrolled_students().count()
        
        # Add course-specific counts
        for course in self.target_courses.all():
            count += course.get_current_enrollments()
        
        # Add individual students/leads
        count += self.target_students.count()
        
        return count


class BroadcastRecipient(models.Model):
    """Model tracking individual recipient status for broadcasts"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('bounced', 'Bounced'),
        ('opened', 'Opened'),
        ('clicked', 'Clicked'),
        ('replied', 'Replied'),
    ]
    
    RECIPIENT_TYPE_CHOICES = [
        ('student', 'Student'),
        ('lead', 'Lead'),
        ('custom', 'Custom Contact'),
    ]
    
    broadcast = models.ForeignKey(Broadcast, on_delete=models.CASCADE, related_name='recipients')
    
    # Recipient Information
    recipient_type = models.CharField(max_length=20, choices=RECIPIENT_TYPE_CHOICES, verbose_name="Recipient Type")
    student = models.ForeignKey(NewStudent, on_delete=models.CASCADE, null=True, blank=True, related_name='broadcast_history')
    lead = models.ForeignKey('Lead', on_delete=models.CASCADE, null=True, blank=True, related_name='broadcast_history')
    
    # Contact Details (for custom contacts)
    custom_name = models.CharField(max_length=100, blank=True, verbose_name="Custom Name")
    custom_email = models.EmailField(blank=True, verbose_name="Custom Email")
    custom_phone = models.CharField(
        max_length=15,
        blank=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be valid')],
        verbose_name="Custom Phone"
    )
    
    # Channel-specific Status
    sms_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    email_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    whatsapp_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Delivery Details
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    
    # Error Tracking
    error_message = models.TextField(blank=True, verbose_name="Error Message")
    retry_count = models.PositiveIntegerField(default=0, verbose_name="Retry Count")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['broadcast', 'student', 'lead']
        ordering = ['-created_at']
        verbose_name = 'Broadcast Recipient'
        verbose_name_plural = 'Broadcast Recipients'
    
    def __str__(self):
        recipient_name = self.get_recipient_name()
        return f"{self.broadcast.title} - {recipient_name}"
    
    def get_recipient_name(self):
        """Get the name of the recipient"""
        if self.student:
            return self.student.student_name
        elif self.lead:
            return self.lead.name
        else:
            return self.custom_name or "Unknown"
    
    def get_recipient_contact(self):
        """Get contact information for the recipient"""
        if self.student:
            return {
                'email': self.student.email_id,
                'phone': self.student.father_mobile_no,  # or mother_mobile_no
            }
        elif self.lead:
            return {
                'email': self.lead.email,
                'phone': self.lead.phone,
            }
        else:
            return {
                'email': self.custom_email,
                'phone': self.custom_phone,
            }


class Lead(models.Model):
    """Model for managing prospective students and leads"""
    
    STATUS_CHOICES = [
        ('new', 'New Lead'),
        ('contacted', 'Contacted'),
        ('interested', 'Interested'),
        ('not_interested', 'Not Interested'),
        ('enrolled', 'Enrolled'),
        ('closed_lost', 'Closed - Lost'),
        ('invalid', 'Invalid'),
    ]
    
    SOURCE_CHOICES = [
        ('website', 'Website'),
        ('social_media', 'Social Media'),
        ('referral', 'Referral'),
        ('advertisement', 'Advertisement'),
        ('walk_in', 'Walk-in'),
        ('phone_inquiry', 'Phone Inquiry'),
        ('email_inquiry', 'Email Inquiry'),
        ('event', 'Event/Exhibition'),
        ('partner', 'Partner'),
        ('other', 'Other'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('hot', 'Hot Lead'),
    ]
    
    # Basic Information
    lead_id = models.CharField(max_length=20, unique=True, verbose_name="Lead ID")
    name = models.CharField(max_length=100, verbose_name="Lead Name")
    email = models.EmailField(validators=[EmailValidator()], verbose_name="Email")
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be valid')],
        verbose_name="Phone Number"
    )
    whatsapp_number = models.CharField(
        max_length=15,
        blank=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be valid')],
        verbose_name="WhatsApp Number"
    )
    
    # Demographics
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name="Age")
    gender = models.CharField(
        max_length=1,
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        blank=True,
        verbose_name="Gender"
    )
    nationality = models.CharField(max_length=100, blank=True, verbose_name="Nationality")
    
    # Interest Information
    interested_courses = models.ManyToManyField(Course, blank=True, verbose_name="Interested Courses")
    preferred_time_slot = models.CharField(
        max_length=20,
        choices=[
            ('morning', 'Morning'),
            ('afternoon', 'Afternoon'),
            ('evening', 'Evening'),
            ('weekend', 'Weekend'),
            ('flexible', 'Flexible'),
        ],
        blank=True,
        verbose_name="Preferred Time Slot"
    )
    budget_range = models.CharField(max_length=100, blank=True, verbose_name="Budget Range")
    
    # Lead Tracking
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, verbose_name="Lead Source")
    source_details = models.CharField(max_length=200, blank=True, verbose_name="Source Details")
    referred_by = models.CharField(max_length=100, blank=True, verbose_name="Referred By")
    
    # Status and Priority
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Follow-up Information
    next_followup_date = models.DateField(null=True, blank=True, verbose_name="Next Follow-up Date")
    last_contacted = models.DateTimeField(null=True, blank=True, verbose_name="Last Contacted")
    contact_attempts = models.PositiveIntegerField(default=0, verbose_name="Contact Attempts")
    
    # Conversion
    enrolled_student = models.OneToOneField(
        NewStudent, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='original_lead',
        verbose_name="Enrolled Student"
    )
    enrollment_date = models.DateField(null=True, blank=True, verbose_name="Enrollment Date")
    
    # Assignment
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                  related_name='assigned_leads', verbose_name="Assigned To")
    
    # Additional Information
    notes = models.TextField(blank=True, verbose_name="Notes")
    address = models.TextField(blank=True, verbose_name="Address")
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_leads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
    
    def __str__(self):
        return f"{self.lead_id} - {self.name}"
    
    def get_absolute_url(self):
        return reverse('lead_detail', kwargs={'pk': self.pk})
    
    def is_hot_lead(self):
        """Check if this is a hot lead"""
        return self.priority == 'hot' or self.status == 'interested'
    
    def days_since_created(self):
        """Get days since lead was created"""
        return (timezone.now().date() - self.created_at.date()).days
    
    def is_overdue_followup(self):
        """Check if follow-up is overdue"""
        if self.next_followup_date:
            return timezone.now().date() > self.next_followup_date
        return False
    
    def get_interested_courses_names(self):
        """Get comma-separated list of interested course names"""
        return ", ".join([course.name for course in self.interested_courses.all()])


class LeadActivity(models.Model):
    """Model for tracking lead interaction activities"""
    
    ACTIVITY_TYPE_CHOICES = [
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
        ('meeting', 'Meeting'),
        ('visit', 'Campus Visit'),
        ('demo', 'Demo Session'),
        ('note', 'Note'),
        ('status_change', 'Status Change'),
        ('broadcast', 'Broadcast Received'),
    ]
    
    OUTCOME_CHOICES = [
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
        ('no_response', 'No Response'),
        ('callback_requested', 'Callback Requested'),
        ('meeting_scheduled', 'Meeting Scheduled'),
        ('interested', 'Expressed Interest'),
        ('not_interested', 'Not Interested'),
    ]
    
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='activities')
    
    # Activity Details
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES, verbose_name="Activity Type")
    subject = models.CharField(max_length=200, verbose_name="Subject")
    description = models.TextField(verbose_name="Description")
    outcome = models.CharField(max_length=20, choices=OUTCOME_CHOICES, blank=True, verbose_name="Outcome")
    
    # Scheduling
    activity_date = models.DateTimeField(default=timezone.now, verbose_name="Activity Date")
    duration_minutes = models.PositiveIntegerField(null=True, blank=True, verbose_name="Duration (minutes)")
    
    # Follow-up
    follow_up_required = models.BooleanField(default=False, verbose_name="Follow-up Required")
    follow_up_date = models.DateField(null=True, blank=True, verbose_name="Follow-up Date")
    follow_up_notes = models.TextField(blank=True, verbose_name="Follow-up Notes")
    
    # Related Records
    related_broadcast = models.ForeignKey(Broadcast, on_delete=models.SET_NULL, null=True, blank=True, 
                                        related_name='lead_activities')
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-activity_date']
        verbose_name = 'Lead Activity'
        verbose_name_plural = 'Lead Activities'
    
    def __str__(self):
        return f"{self.lead.name} - {self.get_activity_type_display()} - {self.activity_date.strftime('%Y-%m-%d')}"


class LeadScore(models.Model):
    """Model for lead scoring based on activities and engagement"""
    
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE, related_name='score')
    
    # Score Components
    engagement_score = models.PositiveIntegerField(default=0, verbose_name="Engagement Score")
    interest_score = models.PositiveIntegerField(default=0, verbose_name="Interest Score")
    demographic_score = models.PositiveIntegerField(default=0, verbose_name="Demographic Score")
    behavior_score = models.PositiveIntegerField(default=0, verbose_name="Behavior Score")
    
    # Total Score
    total_score = models.PositiveIntegerField(default=0, verbose_name="Total Score")
    grade = models.CharField(
        max_length=1,
        choices=[
            ('A', 'A - Hot Lead'),
            ('B', 'B - Warm Lead'),
            ('C', 'C - Cold Lead'),
            ('D', 'D - Poor Lead'),
        ],
        default='C',
        verbose_name="Lead Grade"
    )
    
    # Metadata
    last_calculated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Lead Score'
        verbose_name_plural = 'Lead Scores'
    
    def __str__(self):
        return f"{self.lead.name} - Grade {self.grade} ({self.total_score})"
    
    def calculate_score(self):
        """Recalculate lead score based on activities and data"""
        # Reset scores
        self.engagement_score = 0
        self.interest_score = 0
        self.demographic_score = 0
        self.behavior_score = 0
        
        # Calculate engagement score (based on activities)
        activities = self.lead.activities.all()
        self.engagement_score = min(100, activities.count() * 10)
        
        # Calculate interest score (based on interested courses and positive outcomes)
        if self.lead.interested_courses.exists():
            self.interest_score += 30
        
        positive_activities = activities.filter(outcome='positive').count()
        self.interest_score += min(50, positive_activities * 15)
        
        # Calculate demographic score (based on completeness)
        if self.lead.age:
            self.demographic_score += 10
        if self.lead.gender:
            self.demographic_score += 10
        if self.lead.address:
            self.demographic_score += 10
        if self.lead.budget_range:
            self.demographic_score += 20
        
        # Calculate behavior score (based on responsiveness)
        if self.lead.contact_attempts == 0:
            self.behavior_score = 50  # New lead
        elif self.lead.contact_attempts <= 3:
            self.behavior_score = 80  # Responsive
        else:
            self.behavior_score = 20  # Hard to reach
        
        # Calculate total score
        self.total_score = (
            self.engagement_score + 
            self.interest_score + 
            self.demographic_score + 
            self.behavior_score
        ) // 4
        
        # Assign grade
        if self.total_score >= 80:
            self.grade = 'A'
        elif self.total_score >= 60:
            self.grade = 'B'
        elif self.total_score >= 40:
            self.grade = 'C'
        else:
            self.grade = 'D'
        
        self.save()


class CommunicationLog(models.Model):
    """Model for logging all communications across the system"""
    
    COMMUNICATION_TYPE_CHOICES = [
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('call', 'Phone Call'),
        ('broadcast', 'Broadcast'),
        ('notification', 'System Notification'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('opened', 'Opened'),
        ('clicked', 'Clicked'),
        ('replied', 'Replied'),
    ]
    
    # Communication Details
    communication_type = models.CharField(max_length=20, choices=COMMUNICATION_TYPE_CHOICES)
    subject = models.CharField(max_length=200, blank=True, verbose_name="Subject")
    content = models.TextField(verbose_name="Content")
    
    # Recipient Information
    recipient_type = models.CharField(
        max_length=20,
        choices=[
            ('student', 'Student'),
            ('lead', 'Lead'),
            ('faculty', 'Faculty'),
            ('parent', 'Parent'),
            ('custom', 'Custom'),
        ]
    )
    recipient_name = models.CharField(max_length=100, verbose_name="Recipient Name")
    recipient_contact = models.CharField(max_length=200, verbose_name="Recipient Contact")
    
    # Related Records
    student = models.ForeignKey(NewStudent, on_delete=models.SET_NULL, null=True, blank=True, 
                              related_name='communications')
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True, 
                           related_name='communications')
    broadcast = models.ForeignKey(Broadcast, on_delete=models.SET_NULL, null=True, blank=True, 
                                related_name='communication_logs')
    
    # Status and Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    
    # Cost and Provider
    cost = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        default=Decimal('0.000'),
        validators=[MinValueValidator(Decimal('0.000'))],
        verbose_name="Cost (KWD)"
    )
    provider = models.CharField(max_length=100, blank=True, verbose_name="Service Provider")
    
    # Error Handling
    error_message = models.TextField(blank=True, verbose_name="Error Message")
    retry_count = models.PositiveIntegerField(default=0, verbose_name="Retry Count")
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Communication Log'
        verbose_name_plural = 'Communication Logs'
        indexes = [
            models.Index(fields=['communication_type', 'status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['recipient_type']),
        ]
    
    def __str__(self):
        return f"{self.get_communication_type_display()} to {self.recipient_name} - {self.get_status_display()}"
