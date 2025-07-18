from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from datetime import date, timedelta
from .models import (
    Faculty, FacultyOnboarding, FacultyLeaveRequest, BackupSchedule,
    FacultyAttendance, FacultyPayment, ExamRequest, NotificationLog
)
from xcoursefee.models import Course, StudentEnrollment
from xstudent.models import NewStudent


class FacultyForm(forms.ModelForm):
    """Form for creating and editing faculty profiles"""
    
    class Meta:
        model = Faculty
        exclude = ['created_at', 'updated_at', 'user']
        
        widgets = {
            'faculty_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., FAC001, T2024001'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+965XXXXXXXX'
            }),
            'emergency_contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+965XXXXXXXX'
            }),
            'qualification': forms.Select(attrs={
                'class': 'form-control'
            }),
            'specialization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Mathematics, English, Science'
            }),
            'experience_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 50
            }),
            'employment_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'join_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'address_line_1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter address line 1'
            }),
            'address_line_2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter address line 2 (optional)'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter city'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter state/province'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'value': 'Kuwait'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter postal code'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'can_teach_courses': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': 5
            }),
            'hourly_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0.001',
                'placeholder': '0.000'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Brief biography...'
            }),
        }
        
        labels = {
            'faculty_id': 'Faculty ID *',
            'first_name': 'First Name *',
            'last_name': 'Last Name *',
            'email': 'Email Address *',
            'phone': 'Phone Number *',
            'emergency_contact': 'Emergency Contact',
            'qualification': 'Highest Qualification *',
            'specialization': 'Specialization *',
            'experience_years': 'Years of Experience *',
            'employment_type': 'Employment Type *',
            'join_date': 'Joining Date *',
            'address_line_1': 'Address Line 1 *',
            'address_line_2': 'Address Line 2',
            'city': 'City *',
            'state': 'State/Province *',
            'country': 'Country *',
            'postal_code': 'Postal Code *',
            'status': 'Status *',
            'can_teach_courses': 'Can Teach Courses',
            'hourly_rate': 'Hourly Rate (KWD)',
            'profile_picture': 'Profile Picture',
            'bio': 'Biography',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['can_teach_courses'].queryset = Course.objects.filter(status='active').order_by('name')
        
        if not self.instance.pk:
            self.fields['join_date'].initial = date.today()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Check if email already exists for other faculty
            existing = Faculty.objects.filter(email=email)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError("A faculty member with this email already exists.")
        return email
    
    def clean_faculty_id(self):
        faculty_id = self.cleaned_data.get('faculty_id')
        if faculty_id:
            # Check if faculty ID already exists
            existing = Faculty.objects.filter(faculty_id=faculty_id)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError("This Faculty ID already exists.")
        return faculty_id


class FacultyOnboardingForm(forms.ModelForm):
    """Form for faculty onboarding requests"""
    
    class Meta:
        model = FacultyOnboarding
        exclude = [
            'request_id', 'status', 'application_date', 'reviewed_by', 'review_date',
            'review_notes', 'approved_by', 'approval_date', 'approval_notes',
            'created_faculty', 'updated_at'
        ]
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+965XXXXXXXX'
            }),
            'qualification': forms.Select(attrs={
                'class': 'form-control'
            }),
            'specialization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Mathematics, English, Science'
            }),
            'experience_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 50
            }),
            'preferred_employment_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'expected_hourly_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0.001',
                'placeholder': '0.000'
            }),
            'preferred_courses': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': 5
            }),
            'availability_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe your availability and preferred teaching times...'
            }),
            'cv_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'certificates_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
            }),
            'other_documents': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
            }),
        }
        
        labels = {
            'first_name': 'First Name *',
            'last_name': 'Last Name *',
            'email': 'Email Address *',
            'phone': 'Phone Number *',
            'qualification': 'Highest Qualification *',
            'specialization': 'Specialization *',
            'experience_years': 'Years of Experience *',
            'preferred_employment_type': 'Preferred Employment Type *',
            'expected_hourly_rate': 'Expected Hourly Rate (KWD)',
            'preferred_courses': 'Preferred Courses to Teach',
            'availability_notes': 'Availability Notes',
            'cv_file': 'CV/Resume',
            'certificates_file': 'Educational Certificates',
            'other_documents': 'Other Documents',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['preferred_courses'].queryset = Course.objects.filter(status='active').order_by('name')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Check if email already exists in faculty or pending onboarding
            if Faculty.objects.filter(email=email).exists():
                raise ValidationError("A faculty member with this email already exists.")
            if FacultyOnboarding.objects.filter(email=email, status__in=['pending', 'under_review']).exists():
                raise ValidationError("An onboarding request with this email is already pending.")
        return email


class FacultyLeaveRequestForm(forms.ModelForm):
    """Form for faculty leave and batch time change requests"""
    
    class Meta:
        model = FacultyLeaveRequest
        exclude = [
            'request_id', 'status', 'request_date', 'reviewed_by', 'review_date',
            'approval_notes', 'notification_sent', 'notification_date', 'updated_at'
        ]
        
        widgets = {
            'faculty': forms.Select(attrs={
                'class': 'form-control'
            }),
            'request_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'affected_courses': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': 4
            }),
            'affected_batches': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'List affected batches/classes...'
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Provide detailed reason for this request...'
            }),
            'backup_required': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'suggested_backup': forms.Select(attrs={
                'class': 'form-control'
            }),
            'backup_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes about backup arrangements...'
            }),
        }
        
        labels = {
            'faculty': 'Faculty Member *',
            'request_type': 'Request Type *',
            'priority': 'Priority *',
            'start_date': 'Start Date *',
            'end_date': 'End Date *',
            'start_time': 'Start Time',
            'end_time': 'End Time',
            'affected_courses': 'Affected Courses',
            'affected_batches': 'Affected Batches/Classes',
            'reason': 'Reason *',
            'backup_required': 'Backup Faculty Required',
            'suggested_backup': 'Suggested Backup Faculty',
            'backup_notes': 'Backup Arrangement Notes',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['faculty'].queryset = Faculty.objects.filter(status='active').order_by('first_name', 'last_name')
        self.fields['affected_courses'].queryset = Course.objects.filter(status='active').order_by('name')
        self.fields['suggested_backup'].queryset = Faculty.objects.filter(status='active').order_by('first_name', 'last_name')
        self.fields['suggested_backup'].required = False
        
        # Set minimum date to tomorrow
        tomorrow = date.today() + timedelta(days=1)
        self.fields['start_date'].widget.attrs['min'] = tomorrow.strftime('%Y-%m-%d')
        self.fields['end_date'].widget.attrs['min'] = tomorrow.strftime('%Y-%m-%d')
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        backup_required = cleaned_data.get('backup_required')
        suggested_backup = cleaned_data.get('suggested_backup')
        faculty = cleaned_data.get('faculty')
        
        # Validate date range
        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError("End date must be after start date")
            if start_date < date.today():
                raise ValidationError("Start date cannot be in the past")
        
        # Validate time range for same-day requests
        if start_date and end_date and start_date == end_date and start_time and end_time:
            if start_time >= end_time:
                raise ValidationError("End time must be after start time")
        
        # Validate backup arrangements
        if backup_required and suggested_backup and suggested_backup == faculty:
            raise ValidationError("Backup faculty cannot be the same as the requesting faculty")
        
        return cleaned_data


class BackupScheduleForm(forms.ModelForm):
    """Form for creating backup schedules"""
    
    class Meta:
        model = BackupSchedule
        exclude = [
            'schedule_id', 'status', 'created_by', 'backup_confirmed',
            'backup_confirmation_date', 'notification_sent_to_backup',
            'notification_sent_to_students', 'notification_date',
            'created_at', 'updated_at'
        ]
        
        widgets = {
            'original_faculty': forms.Select(attrs={
                'class': 'form-control'
            }),
            'backup_faculty': forms.Select(attrs={
                'class': 'form-control'
            }),
            'leave_request': forms.Select(attrs={
                'class': 'form-control'
            }),
            'course': forms.Select(attrs={
                'class': 'form-control'
            }),
            'batch_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Morning Batch, Evening Batch'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes or instructions...'
            }),
            'room_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Room number or location'
            }),
        }
        
        labels = {
            'original_faculty': 'Original Faculty *',
            'backup_faculty': 'Backup Faculty *',
            'leave_request': 'Related Leave Request',
            'course': 'Course *',
            'batch_name': 'Batch/Class Name *',
            'date': 'Date *',
            'start_time': 'Start Time *',
            'end_time': 'End Time *',
            'notes': 'Additional Notes',
            'room_location': 'Room/Location',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['original_faculty'].queryset = Faculty.objects.filter(status='active').order_by('first_name', 'last_name')
        self.fields['backup_faculty'].queryset = Faculty.objects.filter(status='active').order_by('first_name', 'last_name')
        self.fields['leave_request'].queryset = FacultyLeaveRequest.objects.filter(status='approved').order_by('-request_date')
        self.fields['course'].queryset = Course.objects.filter(status='active').order_by('name')
        self.fields['leave_request'].required = False
        
        # Set minimum date to today
        today = date.today()
        self.fields['date'].widget.attrs['min'] = today.strftime('%Y-%m-%d')
    
    def clean(self):
        cleaned_data = super().clean()
        original_faculty = cleaned_data.get('original_faculty')
        backup_faculty = cleaned_data.get('backup_faculty')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        date_value = cleaned_data.get('date')
        
        # Validate faculty selection
        if original_faculty and backup_faculty and original_faculty == backup_faculty:
            raise ValidationError("Backup faculty must be different from original faculty")
        
        # Validate time range
        if start_time and end_time and start_time >= end_time:
            raise ValidationError("End time must be after start time")
        
        # Check for conflicts with existing schedules
        if backup_faculty and date_value and start_time and end_time:
            conflicting_schedules = BackupSchedule.objects.filter(
                backup_faculty=backup_faculty,
                date=date_value,
                status__in=['scheduled', 'confirmed']
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            for schedule in conflicting_schedules:
                if (start_time < schedule.end_time and end_time > schedule.start_time):
                    raise ValidationError(f"Backup faculty has a conflicting schedule from {schedule.start_time} to {schedule.end_time}")
        
        return cleaned_data


class FacultyAttendanceForm(forms.ModelForm):
    """Form for recording faculty attendance"""
    
    class Meta:
        model = FacultyAttendance
        exclude = ['recorded_by', 'created_at', 'updated_at']
        
        widgets = {
            'faculty': forms.Select(attrs={
                'class': 'form-control'
            }),
            'course': forms.Select(attrs={
                'class': 'form-control'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'scheduled_start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'scheduled_end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'actual_start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'actual_end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes about attendance...'
            }),
        }
        
        labels = {
            'faculty': 'Faculty Member *',
            'course': 'Course *',
            'date': 'Date *',
            'scheduled_start_time': 'Scheduled Start Time *',
            'scheduled_end_time': 'Scheduled End Time *',
            'actual_start_time': 'Actual Start Time',
            'actual_end_time': 'Actual End Time',
            'status': 'Attendance Status *',
            'notes': 'Notes',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['faculty'].queryset = Faculty.objects.filter(status='active').order_by('first_name', 'last_name')
        self.fields['course'].queryset = Course.objects.filter(status='active').order_by('name')
        
        if not self.instance.pk:
            self.fields['date'].initial = date.today()


class FacultyPaymentForm(forms.ModelForm):
    """Form for creating faculty payments"""
    
    class Meta:
        model = FacultyPayment
        exclude = [
            'payment_id', 'gross_amount', 'net_amount', 'status',
            'payment_date', 'generated_by', 'approved_by', 'processed_by',
            'created_at', 'updated_at'
        ]
        
        widgets = {
            'faculty': forms.Select(attrs={
                'class': 'form-control'
            }),
            'payment_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'period_start': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'period_end': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'total_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00'
            }),
            'hourly_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0.001',
                'placeholder': '0.000'
            }),
            'deductions': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0.000',
                'placeholder': '0.000'
            }),
            'bonus_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0.000',
                'placeholder': '0.000'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-control'
            }),
            'reference_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Payment reference number'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Payment notes...'
            }),
        }
        
        labels = {
            'faculty': 'Faculty Member *',
            'payment_type': 'Payment Type *',
            'period_start': 'Period Start Date *',
            'period_end': 'Period End Date *',
            'total_hours': 'Total Hours *',
            'hourly_rate': 'Hourly Rate (KWD) *',
            'deductions': 'Deductions (KWD)',
            'bonus_amount': 'Bonus Amount (KWD)',
            'payment_method': 'Payment Method',
            'reference_number': 'Reference Number',
            'notes': 'Notes',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['faculty'].queryset = Faculty.objects.filter(status='active').order_by('first_name', 'last_name')
        
        # Pre-fill hourly rate if faculty is selected
        if self.instance.pk and self.instance.faculty:
            if self.instance.faculty.hourly_rate:
                self.fields['hourly_rate'].initial = self.instance.faculty.hourly_rate
    
    def clean(self):
        cleaned_data = super().clean()
        period_start = cleaned_data.get('period_start')
        period_end = cleaned_data.get('period_end')
        faculty = cleaned_data.get('faculty')
        
        # Validate period dates
        if period_start and period_end:
            if period_start > period_end:
                raise ValidationError("Period end date must be after start date")
            if period_end > date.today():
                raise ValidationError("Period end date cannot be in the future")
        
        # Auto-fill hourly rate from faculty profile if not provided
        hourly_rate = cleaned_data.get('hourly_rate')
        if not hourly_rate and faculty and faculty.hourly_rate:
            cleaned_data['hourly_rate'] = faculty.hourly_rate
        
        return cleaned_data


class ExamRequestForm(forms.ModelForm):
    """Form for faculty exam creation requests"""
    
    class Meta:
        model = ExamRequest
        exclude = [
            'request_id', 'status', 'request_date', 'reviewed_by', 'review_date',
            'approval_notes', 'final_date', 'final_start_time', 'assigned_room',
            'notification_sent', 'notification_date', 'updated_at'
        ]
        
        widgets = {
            'faculty': forms.Select(attrs={
                'class': 'form-control'
            }),
            'course': forms.Select(attrs={
                'class': 'form-control'
            }),
            'exam_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Mathematics Midterm Exam'
            }),
            'exam_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Exam description and requirements...'
            }),
            'proposed_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'proposed_start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'duration_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.25',
                'min': '0.25',
                'max': '8.00',
                'placeholder': '1.50'
            }),
            'total_marks': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 1000,
                'placeholder': '100'
            }),
            'passing_marks': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': '60'
            }),
            'number_of_questions': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': '50'
            }),
            'room_requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Special room requirements...'
            }),
            'special_materials': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Required materials or equipment...'
            }),
            'supervision_required': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'target_students': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': 6
            }),
        }
        
        labels = {
            'faculty': 'Faculty Member *',
            'course': 'Course *',
            'exam_title': 'Exam Title *',
            'exam_type': 'Exam Type *',
            'description': 'Description',
            'proposed_date': 'Proposed Exam Date *',
            'proposed_start_time': 'Proposed Start Time *',
            'duration_hours': 'Duration (Hours) *',
            'total_marks': 'Total Marks *',
            'passing_marks': 'Passing Marks *',
            'number_of_questions': 'Number of Questions',
            'room_requirements': 'Room Requirements',
            'special_materials': 'Special Materials Required',
            'supervision_required': 'Supervision Required',
            'target_students': 'Target Students',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['faculty'].queryset = Faculty.objects.filter(status='active').order_by('first_name', 'last_name')
        self.fields['course'].queryset = Course.objects.filter(status='active').order_by('name')
        self.fields['target_students'].queryset = StudentEnrollment.objects.filter(status='active').select_related('student', 'course').order_by('student__student_name')
        
        # Set minimum date to tomorrow
        tomorrow = date.today() + timedelta(days=1)
        self.fields['proposed_date'].widget.attrs['min'] = tomorrow.strftime('%Y-%m-%d')
    
    def clean(self):
        cleaned_data = super().clean()
        proposed_date = cleaned_data.get('proposed_date')
        total_marks = cleaned_data.get('total_marks')
        passing_marks = cleaned_data.get('passing_marks')
        
        # Validate exam date
        if proposed_date and proposed_date <= date.today():
            raise ValidationError("Proposed exam date must be in the future")
        
        # Validate passing marks
        if total_marks and passing_marks and passing_marks >= total_marks:
            raise ValidationError("Passing marks must be less than total marks")
        
        return cleaned_data


class FacultySearchForm(forms.Form):
    """Form for searching and filtering faculty"""
    
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, email, faculty ID...'
        }),
        label="Search"
    )
    
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + Faculty.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status"
    )
    
    employment_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Faculty.EMPLOYMENT_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Employment Type"
    )
    
    qualification = forms.ChoiceField(
        choices=[('', 'All Qualifications')] + Faculty.QUALIFICATION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Qualification"
    )
    
    can_teach_course = forms.ModelChoiceField(
        queryset=Course.objects.filter(status='active').order_by('name'),
        required=False,
        empty_label="Any Course",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Can Teach Course"
    )


class AttendanceReportForm(forms.Form):
    """Form for generating faculty attendance reports"""
    
    faculty = forms.ModelChoiceField(
        queryset=Faculty.objects.filter(status='active').order_by('first_name', 'last_name'),
        required=False,
        empty_label="All Faculty",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Faculty Member"
    )
    
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(status='active').order_by('name'),
        required=False,
        empty_label="All Courses",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Course"
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label="From Date"
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label="To Date"
    )
    
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + FacultyAttendance.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Attendance Status"
    ) 