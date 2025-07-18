from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, RegexValidator, MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from xstudent.models import NewStudent
from xcoursefee.models import Course, StudentEnrollment


class Faculty(models.Model):
    """Main Faculty model for trainer/instructor information"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'), 
        ('pending', 'Pending'),
        ('suspended', 'Suspended'),
        ('terminated', 'Terminated'),
    ]
    
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
    ]
    
    QUALIFICATION_CHOICES = [
        ('bachelor', 'Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('phd', 'PhD'),
        ('diploma', 'Diploma'),
        ('certificate', 'Professional Certificate'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    faculty_id = models.CharField(max_length=20, unique=True, verbose_name="Faculty ID")
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="User Account")
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    email = models.EmailField(unique=True, validators=[EmailValidator()], verbose_name="Email")
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be valid')],
        verbose_name="Phone Number"
    )
    emergency_contact = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be valid')],
        blank=True,
        verbose_name="Emergency Contact"
    )
    
    # Professional Information
    qualification = models.CharField(max_length=20, choices=QUALIFICATION_CHOICES, verbose_name="Highest Qualification")
    specialization = models.CharField(max_length=200, verbose_name="Specialization/Subject Area")
    experience_years = models.PositiveIntegerField(verbose_name="Years of Experience")
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, default='full_time')
    join_date = models.DateField(verbose_name="Joining Date")
    
    # Contact & Address
    address_line_1 = models.CharField(max_length=200, verbose_name="Address Line 1")
    address_line_2 = models.CharField(max_length=200, blank=True, verbose_name="Address Line 2")
    city = models.CharField(max_length=100, verbose_name="City")
    state = models.CharField(max_length=100, verbose_name="State/Province")
    country = models.CharField(max_length=100, default='Kuwait', verbose_name="Country")
    postal_code = models.CharField(max_length=20, verbose_name="Postal Code")
    
    # Status and Settings
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    can_teach_courses = models.ManyToManyField(Course, blank=True, verbose_name="Can Teach Courses")
    hourly_rate = models.DecimalField(
        max_digits=8, 
        decimal_places=3, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Hourly Rate (KWD)"
    )
    
    # Profile
    profile_picture = models.ImageField(upload_to='faculty_photos/', null=True, blank=True, verbose_name="Profile Picture")
    bio = models.TextField(blank=True, verbose_name="Biography")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculty'
    
    def __str__(self):
        return f"{self.faculty_id} - {self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        return reverse('faculty_detail', kwargs={'pk': self.pk})
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_active_courses(self):
        """Get currently active courses this faculty is teaching"""
        return self.teaching_courses.filter(status='active').distinct()
    
    def get_total_students(self):
        """Get total number of students taught by this faculty"""
        return NewStudent.objects.filter(
            course_enrollments__course__in=self.get_active_courses(),
            course_enrollments__status='active'
        ).distinct().count()


class FacultyOnboarding(models.Model):
    """Faculty Onboarding Request and Approval Workflow"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Onboarding Completed'),
    ]
    
    DOCUMENT_CHOICES = [
        ('cv_resume', 'CV/Resume'),
        ('certificates', 'Educational Certificates'),
        ('experience_letter', 'Experience Letters'),
        ('id_copy', 'ID Copy'),
        ('photo', 'Passport Photo'),
        ('other', 'Other Documents'),
    ]
    
    # Basic Request Information
    request_id = models.CharField(max_length=20, unique=True, verbose_name="Request ID")
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    email = models.EmailField(validators=[EmailValidator()], verbose_name="Email")
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be valid')],
        verbose_name="Phone Number"
    )
    
    # Professional Details
    qualification = models.CharField(max_length=20, choices=Faculty.QUALIFICATION_CHOICES)
    specialization = models.CharField(max_length=200, verbose_name="Specialization")
    experience_years = models.PositiveIntegerField(verbose_name="Years of Experience")
    preferred_employment_type = models.CharField(max_length=20, choices=Faculty.EMPLOYMENT_TYPE_CHOICES)
    expected_hourly_rate = models.DecimalField(
        max_digits=8, 
        decimal_places=3,
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Expected Hourly Rate (KWD)"
    )
    
    # Course Preferences
    preferred_courses = models.ManyToManyField(Course, blank=True, verbose_name="Preferred Courses to Teach")
    availability_notes = models.TextField(blank=True, verbose_name="Availability Notes")
    
    # Documents
    cv_file = models.FileField(upload_to='faculty_documents/', null=True, blank=True, verbose_name="CV/Resume")
    certificates_file = models.FileField(upload_to='faculty_documents/', null=True, blank=True, verbose_name="Certificates")
    other_documents = models.FileField(upload_to='faculty_documents/', null=True, blank=True, verbose_name="Other Documents")
    
    # Application Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    application_date = models.DateTimeField(auto_now_add=True, verbose_name="Application Date")
    
    # Review Process
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_onboardings')
    review_date = models.DateTimeField(null=True, blank=True, verbose_name="Review Date")
    review_notes = models.TextField(blank=True, verbose_name="Review Notes")
    
    # Approval Process
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_onboardings')
    approval_date = models.DateTimeField(null=True, blank=True, verbose_name="Approval Date")
    approval_notes = models.TextField(blank=True, verbose_name="Approval Notes")
    
    # Faculty Creation
    created_faculty = models.OneToOneField(Faculty, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Created Faculty")
    
    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-application_date']
        verbose_name = 'Faculty Onboarding'
        verbose_name_plural = 'Faculty Onboardings'
    
    def __str__(self):
        return f"{self.request_id} - {self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        return reverse('faculty_onboarding_detail', kwargs={'pk': self.pk})
    
    def can_approve(self):
        """Check if onboarding can be approved"""
        return self.status == 'under_review'
    
    def can_reject(self):
        """Check if onboarding can be rejected"""
        return self.status in ['pending', 'under_review']


class FacultyLeaveRequest(models.Model):
    """Faculty Leave and Batch Time Change Requests"""
    
    REQUEST_TYPE_CHOICES = [
        ('leave', 'Leave Request'),
        ('batch_time_change', 'Batch Time Change'),
        ('emergency_leave', 'Emergency Leave'),
        ('sick_leave', 'Sick Leave'),
        ('vacation', 'Vacation Leave'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Request Information
    request_id = models.CharField(max_length=20, unique=True, verbose_name="Request ID")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='leave_requests')
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES, verbose_name="Request Type")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Leave Details
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    start_time = models.TimeField(null=True, blank=True, verbose_name="Start Time")
    end_time = models.TimeField(null=True, blank=True, verbose_name="End Time")
    
    # Affected Details
    affected_courses = models.ManyToManyField(Course, blank=True, verbose_name="Affected Courses")
    affected_batches = models.TextField(blank=True, verbose_name="Affected Batches/Classes")
    reason = models.TextField(verbose_name="Reason for Request")
    
    # Backup Arrangements
    backup_required = models.BooleanField(default=True, verbose_name="Backup Faculty Required")
    suggested_backup = models.ForeignKey(
        Faculty, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='backup_requests',
        verbose_name="Suggested Backup Faculty"
    )
    backup_notes = models.TextField(blank=True, verbose_name="Backup Arrangement Notes")
    
    # Request Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    request_date = models.DateTimeField(auto_now_add=True, verbose_name="Request Date")
    
    # Approval Process
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_leave_requests')
    review_date = models.DateTimeField(null=True, blank=True, verbose_name="Review Date")
    approval_notes = models.TextField(blank=True, verbose_name="Approval/Rejection Notes")
    
    # Notifications
    notification_sent = models.BooleanField(default=False, verbose_name="Notification Sent")
    notification_date = models.DateTimeField(null=True, blank=True, verbose_name="Notification Date")
    
    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-request_date']
        verbose_name = 'Faculty Leave Request'
        verbose_name_plural = 'Faculty Leave Requests'
    
    def __str__(self):
        return f"{self.request_id} - {self.faculty.get_full_name()} - {self.get_request_type_display()}"
    
    def get_absolute_url(self):
        return reverse('faculty_leave_request_detail', kwargs={'pk': self.pk})
    
    def get_duration_days(self):
        """Calculate duration in days"""
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 0
    
    def is_emergency(self):
        """Check if this is an emergency request"""
        return self.request_type == 'emergency_leave' or self.priority == 'urgent'


class BackupSchedule(models.Model):
    """Backup Faculty Schedule Management"""
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    # Schedule Information
    schedule_id = models.CharField(max_length=20, unique=True, verbose_name="Schedule ID")
    original_faculty = models.ForeignKey(
        Faculty, 
        on_delete=models.CASCADE, 
        related_name='original_schedules',
        verbose_name="Original Faculty"
    )
    backup_faculty = models.ForeignKey(
        Faculty, 
        on_delete=models.CASCADE, 
        related_name='backup_schedules',
        verbose_name="Backup Faculty"
    )
    
    # Related Leave Request
    leave_request = models.ForeignKey(
        FacultyLeaveRequest, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='backup_schedules',
        verbose_name="Related Leave Request"
    )
    
    # Schedule Details
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Course")
    batch_name = models.CharField(max_length=100, verbose_name="Batch/Class Name")
    date = models.DateField(verbose_name="Date")
    start_time = models.TimeField(verbose_name="Start Time")
    end_time = models.TimeField(verbose_name="End Time")
    
    # Schedule Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Created By")
    
    # Confirmation and Notifications
    backup_confirmed = models.BooleanField(default=False, verbose_name="Backup Confirmed")
    backup_confirmation_date = models.DateTimeField(null=True, blank=True)
    
    # Notifications
    notification_sent_to_backup = models.BooleanField(default=False)
    notification_sent_to_students = models.BooleanField(default=False)
    notification_date = models.DateTimeField(null=True, blank=True)
    
    # Additional Information
    notes = models.TextField(blank=True, verbose_name="Additional Notes")
    room_location = models.CharField(max_length=100, blank=True, verbose_name="Room/Location")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['backup_faculty', 'date', 'start_time', 'course']
        verbose_name = 'Backup Schedule'
        verbose_name_plural = 'Backup Schedules'
    
    def __str__(self):
        return f"{self.schedule_id} - {self.backup_faculty.get_full_name()} for {self.original_faculty.get_full_name()}"
    
    def get_absolute_url(self):
        return reverse('backup_schedule_detail', kwargs={'pk': self.pk})
    
    def get_duration_hours(self):
        """Calculate duration in hours"""
        if self.start_time and self.end_time:
            start_minutes = self.start_time.hour * 60 + self.start_time.minute
            end_minutes = self.end_time.hour * 60 + self.end_time.minute
            duration_minutes = end_minutes - start_minutes
            return round(duration_minutes / 60, 2)
        return 0


class FacultyAttendance(models.Model):
    """Faculty Attendance Tracking"""
    
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('partial', 'Partial Attendance'),
    ]
    
    # Attendance Information
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='attendance_records')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Course")
    date = models.DateField(verbose_name="Date")
    
    # Time Tracking
    scheduled_start_time = models.TimeField(verbose_name="Scheduled Start Time")
    scheduled_end_time = models.TimeField(verbose_name="Scheduled End Time")
    actual_start_time = models.TimeField(null=True, blank=True, verbose_name="Actual Start Time")
    actual_end_time = models.TimeField(null=True, blank=True, verbose_name="Actual End Time")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Attendance Status")
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    # Tracking
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Recorded By")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', 'faculty']
        unique_together = ['faculty', 'course', 'date']
        verbose_name = 'Faculty Attendance'
        verbose_name_plural = 'Faculty Attendance Records'
    
    def __str__(self):
        return f"{self.faculty.get_full_name()} - {self.course.name} - {self.date}"
    
    def get_duration_hours(self):
        """Calculate actual duration in hours"""
        if self.actual_start_time and self.actual_end_time:
            start_minutes = self.actual_start_time.hour * 60 + self.actual_start_time.minute
            end_minutes = self.actual_end_time.hour * 60 + self.actual_end_time.minute
            duration_minutes = end_minutes - start_minutes
            return round(duration_minutes / 60, 2)
        return 0


class FacultyPayment(models.Model):
    """Faculty Payment Tracking"""
    
    PAYMENT_TYPE_CHOICES = [
        ('regular', 'Regular Teaching'),
        ('backup', 'Backup Classes'),
        ('overtime', 'Overtime'),
        ('bonus', 'Bonus'),
        ('exam_supervision', 'Exam Supervision'),
        ('special_project', 'Special Project'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('online', 'Online Payment'),
    ]
    
    # Payment Information
    payment_id = models.CharField(max_length=20, unique=True, verbose_name="Payment ID")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='payments')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, verbose_name="Payment Type")
    
    # Period Information
    period_start = models.DateField(verbose_name="Period Start Date")
    period_end = models.DateField(verbose_name="Period End Date")
    
    # Hours and Rate
    total_hours = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Total Hours"
    )
    hourly_rate = models.DecimalField(
        max_digits=8, 
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Hourly Rate (KWD)"
    )
    
    # Amount Calculation
    gross_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Gross Amount (KWD)"
    )
    deductions = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        default=Decimal('0.000'),
        verbose_name="Deductions (KWD)"
    )
    bonus_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        default=Decimal('0.000'),
        verbose_name="Bonus Amount (KWD)"
    )
    net_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Net Amount (KWD)"
    )
    
    # Payment Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True)
    payment_date = models.DateField(null=True, blank=True, verbose_name="Payment Date")
    
    # References and Notes
    reference_number = models.CharField(max_length=100, blank=True, verbose_name="Reference Number")
    notes = models.TextField(blank=True, verbose_name="Payment Notes")
    
    # Approval Process
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='generated_payments')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_payments')
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_payments')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-period_end', '-created_at']
        verbose_name = 'Faculty Payment'
        verbose_name_plural = 'Faculty Payments'
    
    def __str__(self):
        return f"{self.payment_id} - {self.faculty.get_full_name()} - {self.net_amount} KWD"
    
    def get_absolute_url(self):
        return reverse('faculty_payment_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        """Auto-calculate net amount on save"""
        self.gross_amount = self.total_hours * self.hourly_rate
        self.net_amount = self.gross_amount - self.deductions + self.bonus_amount
        super().save(*args, **kwargs)


class ExamRequest(models.Model):
    """Faculty Exam Creation Requests"""
    
    EXAM_TYPE_CHOICES = [
        ('quiz', 'Quiz'),
        ('midterm', 'Midterm Exam'),
        ('final', 'Final Exam'),
        ('assignment', 'Assignment'),
        ('project', 'Project Evaluation'),
        ('oral', 'Oral Exam'),
        ('practical', 'Practical Exam'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Request Information
    request_id = models.CharField(max_length=20, unique=True, verbose_name="Request ID")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='exam_requests')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Course")
    
    # Exam Details
    exam_title = models.CharField(max_length=200, verbose_name="Exam Title")
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES, verbose_name="Exam Type")
    description = models.TextField(blank=True, verbose_name="Exam Description")
    
    # Scheduling
    proposed_date = models.DateField(verbose_name="Proposed Exam Date")
    proposed_start_time = models.TimeField(verbose_name="Proposed Start Time")
    duration_hours = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.25'))],
        verbose_name="Duration (Hours)"
    )
    
    # Exam Configuration
    total_marks = models.PositiveIntegerField(verbose_name="Total Marks")
    passing_marks = models.PositiveIntegerField(verbose_name="Passing Marks")
    number_of_questions = models.PositiveIntegerField(null=True, blank=True, verbose_name="Number of Questions")
    
    # Resources Required
    room_requirements = models.TextField(blank=True, verbose_name="Room Requirements")
    special_materials = models.TextField(blank=True, verbose_name="Special Materials Required")
    supervision_required = models.BooleanField(default=True, verbose_name="Supervision Required")
    
    # Student Information
    target_students = models.ManyToManyField(
        StudentEnrollment, 
        blank=True, 
        verbose_name="Target Students"
    )
    
    # Request Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    request_date = models.DateTimeField(auto_now_add=True, verbose_name="Request Date")
    
    # Approval Process
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_exam_requests')
    review_date = models.DateTimeField(null=True, blank=True, verbose_name="Review Date")
    approval_notes = models.TextField(blank=True, verbose_name="Approval/Rejection Notes")
    
    # Final Schedule
    final_date = models.DateField(null=True, blank=True, verbose_name="Final Exam Date")
    final_start_time = models.TimeField(null=True, blank=True, verbose_name="Final Start Time")
    assigned_room = models.CharField(max_length=100, blank=True, verbose_name="Assigned Room")
    
    # Notifications
    notification_sent = models.BooleanField(default=False, verbose_name="Students Notified")
    notification_date = models.DateTimeField(null=True, blank=True, verbose_name="Notification Date")
    
    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-request_date']
        verbose_name = 'Exam Request'
        verbose_name_plural = 'Exam Requests'
    
    def __str__(self):
        return f"{self.request_id} - {self.exam_title} - {self.course.name}"
    
    def get_absolute_url(self):
        return reverse('exam_request_detail', kwargs={'pk': self.pk})
    
    def get_enrolled_students_count(self):
        """Get count of enrolled students for this course"""
        return StudentEnrollment.objects.filter(
            course=self.course,
            status='active'
        ).count()
    
    def can_approve(self):
        """Check if exam request can be approved"""
        return self.status == 'pending'


class NotificationLog(models.Model):
    """Log of all notifications sent"""
    
    NOTIFICATION_TYPE_CHOICES = [
        ('sms', 'SMS'),
        ('email', 'Email'), 
        ('whatsapp', 'WhatsApp'),
        ('system', 'System Notification'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('delivered', 'Delivered'),
    ]
    
    # Notification Information
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    recipient_type = models.CharField(max_length=50, verbose_name="Recipient Type")  # Faculty, Student, etc.
    recipient_id = models.PositiveIntegerField(verbose_name="Recipient ID")
    recipient_contact = models.CharField(max_length=100, verbose_name="Recipient Contact")
    
    # Message Details
    subject = models.CharField(max_length=200, blank=True, verbose_name="Subject")
    message = models.TextField(verbose_name="Message Content")
    
    # Related Objects
    related_model = models.CharField(max_length=50, blank=True, verbose_name="Related Model")
    related_id = models.PositiveIntegerField(null=True, blank=True, verbose_name="Related Object ID")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True, verbose_name="Error Message")
    
    # Tracking
    sent_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Sent By")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification Log'
        verbose_name_plural = 'Notification Logs'
    
    def __str__(self):
        return f"{self.get_notification_type_display()} to {self.recipient_contact} - {self.status}"
