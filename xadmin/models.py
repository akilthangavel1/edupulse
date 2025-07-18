from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import RegexValidator
from django.utils import timezone
from django.urls import reverse
import json


class SystemRole(models.Model):
    """Extended role system beyond Django's default groups"""
    
    ROLE_TYPE_CHOICES = [
        ('admin', 'Administrator'),
        ('staff', 'Staff'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
        ('parent', 'Parent'),
        ('support', 'Support Staff'),
        ('readonly', 'Read Only'),
    ]
    
    name = models.CharField(max_length=100, unique=True, verbose_name="Role Name")
    role_type = models.CharField(max_length=20, choices=ROLE_TYPE_CHOICES, verbose_name="Role Type")
    description = models.TextField(verbose_name="Role Description")
    
    # Permissions
    can_create = models.BooleanField(default=False, verbose_name="Can Create Records")
    can_edit = models.BooleanField(default=False, verbose_name="Can Edit Records")
    can_delete = models.BooleanField(default=False, verbose_name="Can Delete Records")
    can_view_all = models.BooleanField(default=False, verbose_name="Can View All Records")
    can_export = models.BooleanField(default=False, verbose_name="Can Export Data")
    can_import = models.BooleanField(default=False, verbose_name="Can Import Data")
    
    # Module Access
    access_students = models.BooleanField(default=False, verbose_name="Access Student Module")
    access_courses = models.BooleanField(default=False, verbose_name="Access Course Module")
    access_fees = models.BooleanField(default=False, verbose_name="Access Fee Module")
    access_marks = models.BooleanField(default=False, verbose_name="Access Marks Module")
    access_faculty = models.BooleanField(default=False, verbose_name="Access Faculty Module")
    access_batches = models.BooleanField(default=False, verbose_name="Access Batch Module")
    access_transport = models.BooleanField(default=False, verbose_name="Access Transport Module")
    access_kits = models.BooleanField(default=False, verbose_name="Access Kit Module")
    access_broadcasts = models.BooleanField(default=False, verbose_name="Access Broadcast Module")
    access_leads = models.BooleanField(default=False, verbose_name="Access Lead Module")
    access_reports = models.BooleanField(default=False, verbose_name="Access Reports")
    access_admin = models.BooleanField(default=False, verbose_name="Access Admin Panel")
    
    # Financial Access
    can_view_finances = models.BooleanField(default=False, verbose_name="Can View Financial Data")
    can_process_payments = models.BooleanField(default=False, verbose_name="Can Process Payments")
    can_generate_invoices = models.BooleanField(default=False, verbose_name="Can Generate Invoices")
    
    # Advanced Permissions
    can_backup_restore = models.BooleanField(default=False, verbose_name="Can Backup/Restore")
    can_manage_users = models.BooleanField(default=False, verbose_name="Can Manage Users")
    can_view_audit_logs = models.BooleanField(default=False, verbose_name="Can View Audit Logs")
    can_configure_system = models.BooleanField(default=False, verbose_name="Can Configure System")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Active Role")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['role_type', 'name']
        verbose_name = 'System Role'
        verbose_name_plural = 'System Roles'
    
    def __str__(self):
        return f"{self.name} ({self.get_role_type_display()})"


class UserProfile(models.Model):
    """Extended user profile with role and additional information"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('pending', 'Pending Activation'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    system_role = models.ForeignKey(SystemRole, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Additional Information
    employee_id = models.CharField(max_length=20, blank=True, unique=True, verbose_name="Employee ID")
    phone = models.CharField(
        max_length=15,
        blank=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be valid')],
        verbose_name="Phone Number"
    )
    department = models.CharField(max_length=100, blank=True, verbose_name="Department")
    position = models.CharField(max_length=100, blank=True, verbose_name="Position")
    
    # Access Control
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    last_login_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="Last Login IP")
    failed_login_attempts = models.PositiveIntegerField(default=0, verbose_name="Failed Login Attempts")
    account_locked_until = models.DateTimeField(null=True, blank=True, verbose_name="Account Locked Until")
    
    # Session Management
    force_password_change = models.BooleanField(default=False, verbose_name="Force Password Change")
    session_timeout_minutes = models.PositiveIntegerField(default=60, verbose_name="Session Timeout (minutes)")
    
    # Notifications
    email_notifications = models.BooleanField(default=True, verbose_name="Email Notifications")
    sms_notifications = models.BooleanField(default=False, verbose_name="SMS Notifications")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.system_role.name if self.system_role else 'No Role'}"
    
    def is_locked(self):
        """Check if account is currently locked"""
        if self.account_locked_until:
            return timezone.now() < self.account_locked_until
        return False
    
    def lock_account(self, duration_minutes=30):
        """Lock account for specified duration"""
        self.account_locked_until = timezone.now() + timezone.timedelta(minutes=duration_minutes)
        self.save()


class AuditLog(models.Model):
    """Comprehensive audit logging for all system activities"""
    
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('read', 'Read'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('login_failed', 'Login Failed'),
        ('export', 'Export'),
        ('import', 'Import'),
        ('backup', 'Backup'),
        ('restore', 'Restore'),
        ('config_change', 'Configuration Change'),
        ('payment', 'Payment'),
        ('broadcast', 'Broadcast'),
        ('system', 'System Action'),
    ]
    
    SEVERITY_CHOICES = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('critical', 'Critical'),
        ('security', 'Security'),
    ]
    
    # Basic Information
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name="Action")
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='info', verbose_name="Severity")
    
    # Target Object (what was acted upon)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Activity Details
    description = models.TextField(verbose_name="Description")
    table_name = models.CharField(max_length=100, blank=True, verbose_name="Table Name")
    record_id = models.CharField(max_length=100, blank=True, verbose_name="Record ID")
    
    # Change Tracking
    old_values = models.TextField(blank=True, verbose_name="Old Values (JSON)")
    new_values = models.TextField(blank=True, verbose_name="New Values (JSON)")
    changed_fields = models.TextField(blank=True, verbose_name="Changed Fields")
    
    # Request Information
    ip_address = models.GenericIPAddressField(verbose_name="IP Address")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    request_method = models.CharField(max_length=10, blank=True, verbose_name="Request Method")
    request_path = models.TextField(blank=True, verbose_name="Request Path")
    
    # Additional Context
    module = models.CharField(max_length=50, blank=True, verbose_name="Module")
    function = models.CharField(max_length=100, blank=True, verbose_name="Function/View")
    session_key = models.CharField(max_length=40, blank=True, verbose_name="Session Key")
    
    # System Information
    server_name = models.CharField(max_length=100, blank=True, verbose_name="Server Name")
    process_id = models.PositiveIntegerField(null=True, blank=True, verbose_name="Process ID")
    
    # Metadata
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
            models.Index(fields=['severity', 'timestamp']),
            models.Index(fields=['table_name', 'timestamp']),
            models.Index(fields=['ip_address']),
        ]
    
    def __str__(self):
        user_str = self.user.username if self.user else "System"
        return f"{user_str} - {self.get_action_display()} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def set_old_values(self, data):
        """Set old values as JSON"""
        self.old_values = json.dumps(data, default=str, ensure_ascii=False)
    
    def set_new_values(self, data):
        """Set new values as JSON"""
        self.new_values = json.dumps(data, default=str, ensure_ascii=False)
    
    def get_old_values_dict(self):
        """Get old values as dictionary"""
        try:
            return json.loads(self.old_values) if self.old_values else {}
        except json.JSONDecodeError:
            return {}
    
    def get_new_values_dict(self):
        """Get new values as dictionary"""
        try:
            return json.loads(self.new_values) if self.new_values else {}
        except json.JSONDecodeError:
            return {}


class SecurityLog(models.Model):
    """Security-specific logging for suspicious activities"""
    
    INCIDENT_TYPE_CHOICES = [
        ('failed_login', 'Failed Login'),
        ('account_lockout', 'Account Lockout'),
        ('permission_denied', 'Permission Denied'),
        ('suspicious_activity', 'Suspicious Activity'),
        ('data_breach_attempt', 'Data Breach Attempt'),
        ('unauthorized_access', 'Unauthorized Access'),
        ('privilege_escalation', 'Privilege Escalation'),
        ('sql_injection', 'SQL Injection Attempt'),
        ('xss_attempt', 'XSS Attempt'),
        ('file_upload', 'Suspicious File Upload'),
        ('mass_download', 'Mass Data Download'),
    ]
    
    RISK_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
        ('false_positive', 'False Positive'),
    ]
    
    # Incident Information
    incident_id = models.CharField(max_length=20, unique=True, verbose_name="Incident ID")
    incident_type = models.CharField(max_length=30, choices=INCIDENT_TYPE_CHOICES, verbose_name="Incident Type")
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES, verbose_name="Risk Level")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', verbose_name="Status")
    
    # User and Request Information
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='security_incidents')
    username_attempted = models.CharField(max_length=150, blank=True, verbose_name="Username Attempted")
    ip_address = models.GenericIPAddressField(verbose_name="IP Address")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    
    # Request Details
    request_method = models.CharField(max_length=10, blank=True, verbose_name="Request Method")
    request_path = models.TextField(blank=True, verbose_name="Request Path")
    request_data = models.TextField(blank=True, verbose_name="Request Data")
    response_code = models.PositiveIntegerField(null=True, blank=True, verbose_name="Response Code")
    
    # Geographic Information
    country = models.CharField(max_length=100, blank=True, verbose_name="Country")
    city = models.CharField(max_length=100, blank=True, verbose_name="City")
    
    # Incident Details
    description = models.TextField(verbose_name="Description")
    affected_resources = models.TextField(blank=True, verbose_name="Affected Resources")
    potential_impact = models.TextField(blank=True, verbose_name="Potential Impact")
    
    # Investigation
    investigated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                      related_name='investigated_incidents', verbose_name="Investigated By")
    investigation_notes = models.TextField(blank=True, verbose_name="Investigation Notes")
    resolution = models.TextField(blank=True, verbose_name="Resolution")
    
    # Prevention
    action_taken = models.TextField(blank=True, verbose_name="Action Taken")
    prevention_measures = models.TextField(blank=True, verbose_name="Prevention Measures")
    
    # Metadata
    detected_at = models.DateTimeField(auto_now_add=True, verbose_name="Detected At")
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name="Resolved At")
    
    class Meta:
        ordering = ['-detected_at']
        verbose_name = 'Security Log'
        verbose_name_plural = 'Security Logs'
        indexes = [
            models.Index(fields=['incident_type', 'detected_at']),
            models.Index(fields=['risk_level', 'status']),
            models.Index(fields=['ip_address']),
            models.Index(fields=['user', 'detected_at']),
        ]
    
    def __str__(self):
        return f"{self.incident_id} - {self.get_incident_type_display()} - {self.get_risk_level_display()}"
    
    def is_high_risk(self):
        """Check if this is a high risk incident"""
        return self.risk_level in ['high', 'critical']


class SystemBackup(models.Model):
    """System backup management and tracking"""
    
    BACKUP_TYPE_CHOICES = [
        ('full', 'Full Backup'),
        ('incremental', 'Incremental Backup'),
        ('differential', 'Differential Backup'),
        ('database_only', 'Database Only'),
        ('files_only', 'Files Only'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Backup Information
    backup_id = models.CharField(max_length=20, unique=True, verbose_name="Backup ID")
    backup_type = models.CharField(max_length=20, choices=BACKUP_TYPE_CHOICES, verbose_name="Backup Type")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    
    # Scheduling
    is_scheduled = models.BooleanField(default=False, verbose_name="Scheduled Backup")
    schedule_frequency = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('manual', 'Manual'),
        ],
        default='manual',
        verbose_name="Schedule Frequency"
    )
    
    # File Information
    filename = models.CharField(max_length=255, blank=True, verbose_name="Backup Filename")
    file_path = models.TextField(blank=True, verbose_name="File Path")
    file_size_bytes = models.BigIntegerField(null=True, blank=True, verbose_name="File Size (bytes)")
    compression_ratio = models.FloatField(null=True, blank=True, verbose_name="Compression Ratio")
    
    # Content Information
    includes_database = models.BooleanField(default=True, verbose_name="Includes Database")
    includes_media = models.BooleanField(default=True, verbose_name="Includes Media Files")
    includes_config = models.BooleanField(default=True, verbose_name="Includes Configuration")
    
    # Statistics
    total_records = models.PositiveIntegerField(null=True, blank=True, verbose_name="Total Records")
    total_files = models.PositiveIntegerField(null=True, blank=True, verbose_name="Total Files")
    
    # Process Information
    started_at = models.DateTimeField(null=True, blank=True, verbose_name="Started At")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Completed At")
    duration_seconds = models.PositiveIntegerField(null=True, blank=True, verbose_name="Duration (seconds)")
    
    # Error Information
    error_message = models.TextField(blank=True, verbose_name="Error Message")
    warning_count = models.PositiveIntegerField(default=0, verbose_name="Warning Count")
    
    # Storage Information
    storage_location = models.CharField(max_length=200, blank=True, verbose_name="Storage Location")
    checksum = models.CharField(max_length=64, blank=True, verbose_name="Checksum (SHA-256)")
    
    # Retention
    retention_days = models.PositiveIntegerField(default=30, verbose_name="Retention Days")
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Expires At")
    
    # User Information
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_backups')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'System Backup'
        verbose_name_plural = 'System Backups'
    
    def __str__(self):
        return f"{self.backup_id} - {self.get_backup_type_display()} - {self.get_status_display()}"
    
    def get_duration_formatted(self):
        """Get formatted duration string"""
        if self.duration_seconds:
            hours = self.duration_seconds // 3600
            minutes = (self.duration_seconds % 3600) // 60
            seconds = self.duration_seconds % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return None
    
    def get_file_size_formatted(self):
        """Get formatted file size"""
        if self.file_size_bytes:
            size = self.file_size_bytes
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
        return None
    
    def is_expired(self):
        """Check if backup has expired"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False


class SystemRestore(models.Model):
    """System restore operations tracking"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    RESTORE_TYPE_CHOICES = [
        ('full', 'Full Restore'),
        ('database_only', 'Database Only'),
        ('files_only', 'Files Only'),
        ('selective', 'Selective Restore'),
    ]
    
    # Restore Information
    restore_id = models.CharField(max_length=20, unique=True, verbose_name="Restore ID")
    backup = models.ForeignKey(SystemBackup, on_delete=models.CASCADE, related_name='restores')
    restore_type = models.CharField(max_length=20, choices=RESTORE_TYPE_CHOICES, verbose_name="Restore Type")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    
    # Restoration Options
    restore_database = models.BooleanField(default=True, verbose_name="Restore Database")
    restore_media = models.BooleanField(default=True, verbose_name="Restore Media Files")
    restore_config = models.BooleanField(default=False, verbose_name="Restore Configuration")
    
    # Target Information
    target_environment = models.CharField(max_length=100, blank=True, verbose_name="Target Environment")
    target_path = models.TextField(blank=True, verbose_name="Target Path")
    
    # Process Information
    started_at = models.DateTimeField(null=True, blank=True, verbose_name="Started At")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Completed At")
    duration_seconds = models.PositiveIntegerField(null=True, blank=True, verbose_name="Duration (seconds)")
    
    # Progress Tracking
    progress_percentage = models.PositiveIntegerField(default=0, verbose_name="Progress (%)")
    current_operation = models.CharField(max_length=200, blank=True, verbose_name="Current Operation")
    
    # Results
    records_restored = models.PositiveIntegerField(null=True, blank=True, verbose_name="Records Restored")
    files_restored = models.PositiveIntegerField(null=True, blank=True, verbose_name="Files Restored")
    error_count = models.PositiveIntegerField(default=0, verbose_name="Error Count")
    warning_count = models.PositiveIntegerField(default=0, verbose_name="Warning Count")
    
    # Error Information
    error_message = models.TextField(blank=True, verbose_name="Error Message")
    error_log = models.TextField(blank=True, verbose_name="Error Log")
    
    # User Information
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='requested_restores')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_restores')
    
    # Approval Process
    requires_approval = models.BooleanField(default=True, verbose_name="Requires Approval")
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name="Approved At")
    approval_notes = models.TextField(blank=True, verbose_name="Approval Notes")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'System Restore'
        verbose_name_plural = 'System Restores'
    
    def __str__(self):
        return f"{self.restore_id} - {self.backup.backup_id} - {self.get_status_display()}"


class SystemConfiguration(models.Model):
    """System configuration settings"""
    
    CONFIG_TYPE_CHOICES = [
        ('general', 'General'),
        ('security', 'Security'),
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('backup', 'Backup'),
        ('notification', 'Notification'),
        ('integration', 'Integration'),
        ('ui', 'User Interface'),
    ]
    
    DATA_TYPE_CHOICES = [
        ('string', 'String'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'),
        ('json', 'JSON'),
        ('list', 'List'),
    ]
    
    # Configuration Information
    key = models.CharField(max_length=100, unique=True, verbose_name="Configuration Key")
    config_type = models.CharField(max_length=20, choices=CONFIG_TYPE_CHOICES, verbose_name="Configuration Type")
    data_type = models.CharField(max_length=20, choices=DATA_TYPE_CHOICES, default='string', verbose_name="Data Type")
    
    # Value Storage
    value = models.TextField(verbose_name="Configuration Value")
    default_value = models.TextField(blank=True, verbose_name="Default Value")
    
    # Metadata
    name = models.CharField(max_length=200, verbose_name="Display Name")
    description = models.TextField(verbose_name="Description")
    is_sensitive = models.BooleanField(default=False, verbose_name="Sensitive Data")
    is_readonly = models.BooleanField(default=False, verbose_name="Read Only")
    
    # Validation
    validation_rules = models.TextField(blank=True, verbose_name="Validation Rules (JSON)")
    choices = models.TextField(blank=True, verbose_name="Allowed Choices (JSON)")
    
    # Change Tracking
    last_modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['config_type', 'key']
        verbose_name = 'System Configuration'
        verbose_name_plural = 'System Configurations'
    
    def __str__(self):
        return f"{self.key} ({self.get_config_type_display()})"
    
    def get_typed_value(self):
        """Get value converted to appropriate type"""
        if self.data_type == 'integer':
            return int(self.value)
        elif self.data_type == 'float':
            return float(self.value)
        elif self.data_type == 'boolean':
            return self.value.lower() in ['true', '1', 'yes', 'on']
        elif self.data_type == 'json':
            return json.loads(self.value)
        elif self.data_type == 'list':
            return [item.strip() for item in self.value.split(',')]
        else:
            return self.value
