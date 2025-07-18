from django import forms
from django.core.exceptions import ValidationError
from .models import NewStudent, OldStudent, Attendance
import re
from datetime import date, datetime


class StudentForm(forms.ModelForm):
    class Meta:
        model = NewStudent
        exclude = ['created_at', 'updated_at', 'status']
        
        widgets = {
            # Basic Student Information
            'student_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter student name'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'school_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter school name'
            }),
            'grade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter grade'
            }),
            'program': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter program'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'email_id': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'student_profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            
            # Father Details
            'father_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter father\'s name'
            }),
            'father_occupation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter father\'s occupation'
            }),
            'father_company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter father\'s company name'
            }),
            'father_mobile_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+965XXXXXXXX'
            }),
            'father_email_id': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter father\'s email'
            }),
            
            # Mother Details
            'mother_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter mother\'s name'
            }),
            'mother_occupation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter mother\'s occupation'
            }),
            'mother_company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter mother\'s company name'
            }),
            'mother_mobile_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+965XXXXXXXX'
            }),
            'mother_email_id': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter mother\'s email'
            }),
            
            # Guardian Details
            'guardian_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter guardian\'s name (if applicable)'
            }),
            'guardian_relationship': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Relationship to student'
            }),
            'guardian_mobile_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+965XXXXXXXX'
            }),
            
            # Siblings
            'sibling_1_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter sibling 1 name'
            }),
            'sibling_1_age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Age'
            }),
            'sibling_2_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter sibling 2 name'
            }),
            'sibling_2_age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Age'
            }),
            
            # Address
            'address_line_1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter address line 1'
            }),
            'address_line_2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter address line 2'
            }),
            'area': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter area'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter country name'
            }),
            'state_emirates_province': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter state/emirate/province'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter city name'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter postal code'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+965XXXXXXXX'
            }),
            
            # Mobile Number Selection
            'select_mobile_number': forms.Select(attrs={
                'class': 'form-control'
            }),
            'mobile_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+965XXXXXXXX'
            }),
        }
        
        labels = {
            'student_name': 'Student Name *',
            'gender': 'Gender *',
            'school_name': 'School Name',
            'grade': 'Grade *',
            'program': 'Program *',
            'date_of_birth': 'Date of Birth *',
            'email_id': 'Email ID *',
            'student_profile_picture': 'Student Profile Picture',
            'father_name': 'Father Name *',
            'father_occupation': 'Father Occupation',
            'father_company_name': 'Father Company Name',
            'father_mobile_no': 'Father Mobile No *',
            'father_email_id': 'Father Email ID *',
            'mother_name': 'Mother Name *',
            'mother_occupation': 'Mother Occupation',
            'mother_company_name': 'Mother Company Name',
            'mother_mobile_no': 'Mother Mobile No *',
            'mother_email_id': 'Mother Email ID *',
            'guardian_name': 'Guardian Name',
            'guardian_relationship': 'Guardian Relationship',
            'guardian_mobile_no': 'Guardian Mobile No',
            'sibling_1_name': 'Sibling 1 Name',
            'sibling_1_age': 'Sibling 1 Age',
            'sibling_2_name': 'Sibling 2 Name',
            'sibling_2_age': 'Sibling 2 Age',
            'address_line_1': 'Address line 1 *',
            'address_line_2': 'Address line 2',
            'area': 'Area *',
            'country': 'Country *',
            'state_emirates_province': 'State/Emirates/Province *',
            'city': 'City *',
            'postal_code': 'Postal Code *',
            'telephone': 'Telephone',
            'select_mobile_number': 'Select Mobile Number *',
            'mobile_no': 'Mobile No *',
        }

    def __init__(self, *args, **kwargs):
        self.is_draft = kwargs.pop('is_draft', False)
        super().__init__(*args, **kwargs)
        
        # Make fields optional for drafts
        if self.is_draft:
            required_fields = [
                'student_name', 'gender', 'grade', 'program', 'date_of_birth',
                'email_id', 'father_name', 'father_mobile_no', 'father_email_id',
                'mother_name', 'mother_mobile_no', 'mother_email_id',
                'address_line_1', 'area', 'country', 'state_emirates_province',
                'city', 'postal_code', 'select_mobile_number', 'mobile_no'
            ]
            for field_name in required_fields:
                if field_name in self.fields:
                    self.fields[field_name].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        
        # If this is a draft submission, only require student_name
        if self.is_draft:
            student_name = cleaned_data.get('student_name')
            if not student_name:
                raise ValidationError("Please provide at least a student name to save as draft.")
        else:
            # For regular submission, validate that we have enough information
            # Only check for the most critical fields to avoid too many validation errors
            critical_fields = ['student_name', 'gender', 'grade', 'program', 'email_id']
            missing_critical = []
            
            for field_name in critical_fields:
                if not cleaned_data.get(field_name):
                    field_label = self.fields[field_name].label or field_name.replace('_', ' ').title()
                    missing_critical.append(field_label)
            
            if missing_critical:
                raise ValidationError(f"Critical fields missing: {', '.join(missing_critical)}")
        
        return cleaned_data
    
    def clean_student_profile_picture(self):
        picture = self.cleaned_data.get('student_profile_picture')
        if picture:
            # Only validate newly uploaded files, not existing ImageFieldFile objects
            if hasattr(picture, 'content_type'):
                # Check file size (limit to 5MB)
                if picture.size > 5 * 1024 * 1024:
                    raise ValidationError("Image file size should not exceed 5MB.")
                
                # Check file type
                if not picture.content_type.startswith('image/'):
                    raise ValidationError("Please upload a valid image file.")
                
        return picture

    def clean_father_mobile_no(self):
        phone = self.cleaned_data.get('father_mobile_no')
        if phone and not re.match(r'^\+?1?\d{9,15}$', phone):
            raise ValidationError('Please enter a valid father\'s mobile number. Format: +965XXXXXXXX or 965XXXXXXXX')
        return phone

    def clean_mother_mobile_no(self):
        phone = self.cleaned_data.get('mother_mobile_no')
        if phone and not re.match(r'^\+?1?\d{9,15}$', phone):
            raise ValidationError('Please enter a valid mother\'s mobile number. Format: +965XXXXXXXX or 965XXXXXXXX')
        return phone

    def clean_guardian_mobile_no(self):
        phone = self.cleaned_data.get('guardian_mobile_no')
        if phone and not re.match(r'^\+?1?\d{9,15}$', phone):
            raise ValidationError('Please enter a valid guardian\'s mobile number. Format: +965XXXXXXXX or 965XXXXXXXX')
        return phone

    def clean_mobile_no(self):
        phone = self.cleaned_data.get('mobile_no')
        if phone and not re.match(r'^\+?1?\d{9,15}$', phone):
            raise ValidationError('Please enter a valid mobile number. Format: +965XXXXXXXX or 965XXXXXXXX')
        return phone

    def clean_telephone(self):
        phone = self.cleaned_data.get('telephone')
        if phone and not re.match(r'^\+?1?\d{9,15}$', phone):
            raise ValidationError('Please enter a valid telephone number. Format: +965XXXXXXXX or 965XXXXXXXX')
        return phone


class StudentSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, email, grade, or program...'
        })
    )
    status = forms.ChoiceField(
        choices=[('', 'All Students')] + NewStudent.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    gender = forms.ChoiceField(
        choices=[('', 'All Genders')] + NewStudent.GENDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    grade = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter grade to filter...'
        })
    )
    program = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter program to filter...'
        })
    )


class OldStudentForm(forms.ModelForm):
    class Meta:
        model = OldStudent
        exclude = ['created_at', 'updated_at']
        
        widgets = {
            'student_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter student name'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'student_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter unique student code'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'mobile_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+965XXXXXXXX'
            }),
            'tenth_level_completed_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        
        labels = {
            'student_name': 'Student Name *',
            'date_of_birth': 'Date of Birth *',
            'student_code': 'Student Code *',
            'email': 'Email *',
            'mobile_number': 'Mobile Number *',
            'tenth_level_completed_date': '10th Level Completed Date *',
        }
    
    def clean_mobile_number(self):
        mobile = self.cleaned_data.get('mobile_number')
        if mobile:
            # Remove spaces and special characters except +
            mobile = re.sub(r'[^\d+]', '', mobile)
            if not re.match(r'^\+?1?\d{9,15}$', mobile):
                raise ValidationError("Please enter a valid mobile number")
        return mobile
    
    def clean_student_code(self):
        student_code = self.cleaned_data.get('student_code')
        if student_code:
            # Check if student code already exists (excluding current instance)
            existing_student = OldStudent.objects.filter(student_code=student_code)
            if self.instance.pk:
                existing_student = existing_student.exclude(pk=self.instance.pk)
            
            if existing_student.exists():
                raise ValidationError("Student code already exists. Please use a unique code.")
        return student_code


class OldStudentSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, code, or email...'
        })
    )
    completion_year = forms.CharField(
        max_length=4,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter completion year...'
        })
    )


class AttendanceForm(forms.ModelForm):
    """Form for recording individual student attendance"""
    
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status', 'time_in', 'time_out', 'notes']
        
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'max': date.today().isoformat()
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'time_in': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'time_out': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes about attendance...'
            }),
        }
        
        labels = {
            'student': 'Student *',
            'date': 'Date *',
            'status': 'Attendance Status *',
            'time_in': 'Time In',
            'time_out': 'Time Out',
            'notes': 'Notes',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active students
        self.fields['student'].queryset = NewStudent.objects.filter(status='active').order_by('student_name')
        
        # Set default date to today
        if not self.instance.pk:
            self.fields['date'].initial = date.today()
    
    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        attendance_date = cleaned_data.get('date')
        time_in = cleaned_data.get('time_in')
        time_out = cleaned_data.get('time_out')
        status = cleaned_data.get('status')
        
        # Check for duplicate attendance on same date
        if student and attendance_date:
            existing_attendance = Attendance.objects.filter(
                student=student,
                date=attendance_date
            )
            if self.instance.pk:
                existing_attendance = existing_attendance.exclude(pk=self.instance.pk)
            
            if existing_attendance.exists():
                raise ValidationError(f"Attendance record already exists for {student.student_name} on {attendance_date}")
        
        # Validate time_out is after time_in
        if time_in and time_out:
            if time_out <= time_in:
                raise ValidationError("Time out must be after time in")
        
        # Require time_in for present status
        if status == 'present' and not time_in:
            raise ValidationError("Time in is required for present status")
        
        return cleaned_data


class BulkAttendanceForm(forms.Form):
    """Form for recording attendance for multiple students at once"""
    
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'max': date.today().isoformat()
        }),
        initial=date.today,
        label="Date *"
    )
    
    grade = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by grade (optional)'
        }),
        label="Grade Filter"
    )
    
    program = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by program (optional)'
        }),
        label="Program Filter"
    )
    
    default_status = forms.ChoiceField(
        choices=Attendance.ATTENDANCE_STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        initial='present',
        label="Default Status"
    )
    
    default_time_in = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time'
        }),
        initial='08:00',
        label="Default Time In"
    )
    
    def clean_date(self):
        attendance_date = self.cleaned_data.get('date')
        if attendance_date and attendance_date > date.today():
            raise ValidationError("Cannot record attendance for future dates")
        return attendance_date


class AttendanceFilterForm(forms.Form):
    """Form for filtering attendance records"""
    
    student = forms.ModelChoiceField(
        queryset=NewStudent.objects.filter(status='active').order_by('student_name'),
        required=False,
        empty_label="All Students",
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label="Student"
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
        choices=[('', 'All Status')] + Attendance.ATTENDANCE_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label="Status"
    )
    
    grade = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by grade...'
        }),
        label="Grade"
    )
    
    program = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by program...'
        }),
        label="Program"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        
        if date_from and date_to:
            if date_from > date_to:
                raise ValidationError("From date must be before to date")
        
        return cleaned_data


class AttendanceReportForm(forms.Form):
    """Form for generating attendance reports"""
    
    REPORT_TYPE_CHOICES = [
        ('daily', 'Daily Report'),
        ('weekly', 'Weekly Report'),
        ('monthly', 'Monthly Report'),
        ('custom', 'Custom Date Range'),
    ]
    
    report_type = forms.ChoiceField(
        choices=REPORT_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label="Report Type"
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
    
    students = forms.ModelMultipleChoiceField(
        queryset=NewStudent.objects.filter(status='active').order_by('student_name'),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        label="Select Students (leave empty for all)"
    )
    
    include_summary = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label="Include Summary Statistics"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        report_type = cleaned_data.get('report_type')
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        
        if report_type == 'custom':
            if not date_from or not date_to:
                raise ValidationError("Custom report requires both from and to dates")
            if date_from > date_to:
                raise ValidationError("From date must be before to date")
        
        return cleaned_data 