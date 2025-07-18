from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.urls import reverse

class NewStudent(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    MOBILE_NUMBER_CHOICES = [
        ('Father', 'Father'),
        ('Mother', 'Mother'),
    ]
    
    # Status field
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    
    # Basic Student Information
    student_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    school_name = models.CharField(max_length=200, blank=True)
    grade = models.CharField(max_length=50)
    program = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email_id = models.EmailField(validators=[EmailValidator()])
    student_profile_picture = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    
    # Father Details
    father_name = models.CharField(max_length=100)
    father_occupation = models.CharField(max_length=100, blank=True)
    father_company_name = models.CharField(max_length=200, blank=True)
    father_mobile_no = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be valid')]
    )
    father_email_id = models.EmailField(validators=[EmailValidator()])
    
    # Mother Details
    mother_name = models.CharField(max_length=100)
    mother_occupation = models.CharField(max_length=100, blank=True)
    mother_company_name = models.CharField(max_length=200, blank=True)
    mother_mobile_no = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be valid')]
    )
    mother_email_id = models.EmailField(validators=[EmailValidator()])
    
    # Guardian Details
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_relationship = models.CharField(max_length=50, blank=True)
    guardian_mobile_no = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be valid')],
        blank=True
    )
    
    # Siblings
    sibling_1_name = models.CharField(max_length=100, blank=True)
    sibling_1_age = models.PositiveIntegerField(blank=True, null=True)
    sibling_2_name = models.CharField(max_length=100, blank=True)
    sibling_2_age = models.PositiveIntegerField(blank=True, null=True)
    
    # Address
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200, blank=True)
    area = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state_emirates_province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    telephone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be valid')],
        blank=True
    )
    
    # Mobile Number Selection
    select_mobile_number = models.CharField(max_length=10, choices=MOBILE_NUMBER_CHOICES)
    mobile_no = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be valid')]
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
    
    def __str__(self):
        return f"{self.student_name}"
    
    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'pk': self.pk})


class OldStudent(models.Model):
    """Model for old students who have completed 10th level"""
    
    student_name = models.CharField(
        max_length=100,
        verbose_name="Student Name",
        help_text="Full name of the old student"
    )
    
    date_of_birth = models.DateField(
        verbose_name="Date of Birth",
        help_text="Student's date of birth"
    )
    
    student_code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Student Code",
        help_text="Unique identifier for the student"
    )
    
    email = models.EmailField(
        validators=[EmailValidator()],
        verbose_name="Email",
        help_text="Student's email address"
    )
    
    mobile_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$', 
            message='Phone number must be valid'
        )],
        verbose_name="Mobile Number",
        help_text="Student's mobile number"
    )
    
    tenth_level_completed_date = models.DateField(
        verbose_name="10th Level Completed Date",
        help_text="Date when student completed 10th level"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Old Student'
        verbose_name_plural = 'Old Students'
    
    def __str__(self):
        return f"{self.student_name} ({self.student_code})"
    
    def get_absolute_url(self):
        return reverse('old_student_detail', kwargs={'pk': self.pk})


class Attendance(models.Model):
    """Model for tracking student attendance"""
    
    ATTENDANCE_STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]
    
    student = models.ForeignKey(
        NewStudent, 
        on_delete=models.CASCADE, 
        related_name='attendances',
        verbose_name="Student"
    )
    
    date = models.DateField(
        verbose_name="Date",
        help_text="Date of attendance record"
    )
    
    status = models.CharField(
        max_length=10,
        choices=ATTENDANCE_STATUS_CHOICES,
        default='present',
        verbose_name="Attendance Status"
    )
    
    time_in = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Time In",
        help_text="Time when student arrived"
    )
    
    time_out = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Time Out",
        help_text="Time when student left"
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name="Notes",
        help_text="Additional notes about attendance"
    )
    
    recorded_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Recorded By"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        unique_together = ['student', 'date']
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'
    
    def __str__(self):
        return f"{self.student.student_name} - {self.date} ({self.get_status_display()})"
    
    def get_absolute_url(self):
        return reverse('attendance_detail', kwargs={'pk': self.pk})


class AttendanceSummary(models.Model):
    """Model for storing monthly attendance summaries"""
    
    student = models.ForeignKey(
        NewStudent,
        on_delete=models.CASCADE,
        related_name='attendance_summaries',
        verbose_name="Student"
    )
    
    month = models.PositiveIntegerField(
        verbose_name="Month",
        help_text="Month (1-12)"
    )
    
    year = models.PositiveIntegerField(
        verbose_name="Year",
        help_text="Year"
    )
    
    total_days = models.PositiveIntegerField(
        default=0,
        verbose_name="Total Days",
        help_text="Total working days in the month"
    )
    
    present_days = models.PositiveIntegerField(
        default=0,
        verbose_name="Present Days"
    )
    
    absent_days = models.PositiveIntegerField(
        default=0,
        verbose_name="Absent Days"
    )
    
    late_days = models.PositiveIntegerField(
        default=0,
        verbose_name="Late Days"
    )
    
    excused_days = models.PositiveIntegerField(
        default=0,
        verbose_name="Excused Days"
    )
    
    attendance_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        verbose_name="Attendance Percentage"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year', '-month']
        unique_together = ['student', 'month', 'year']
        verbose_name = 'Attendance Summary'
        verbose_name_plural = 'Attendance Summaries'
    
    def __str__(self):
        return f"{self.student.student_name} - {self.month}/{self.year} ({self.attendance_percentage}%)"
    
    def calculate_percentage(self):
        """Calculate attendance percentage"""
        if self.total_days > 0:
            self.attendance_percentage = (self.present_days / self.total_days) * 100
        else:
            self.attendance_percentage = 0
        return self.attendance_percentage
