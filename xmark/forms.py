from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Subject, AssessmentType, StudentMark, GradeScale, StudentGradeSummary
from xstudent.models import NewStudent
from xcoursefee.models import Course


class SubjectForm(forms.ModelForm):
    """Form for creating and editing subjects"""
    
    class Meta:
        model = Subject
        fields = ['name', 'code', 'course', 'description', 'credit_hours', 'instructor', 'is_active']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(status='active')
        
        # Add CSS classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Subject description...'
        })
        
        self.fields['code'].widget.attrs.update({
            'placeholder': 'e.g., MATH101, ENG102',
            'style': 'text-transform: uppercase;'
        })


class AssessmentTypeForm(forms.ModelForm):
    """Form for creating and editing assessment types"""
    
    class Meta:
        model = AssessmentType
        fields = ['name', 'category', 'description', 'weight_percentage', 'is_active']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add CSS classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        self.fields['description'].widget.attrs.update({
            'rows': 2,
            'placeholder': 'Assessment description...'
        })
        
        self.fields['weight_percentage'].widget.attrs.update({
            'step': '0.01',
            'min': '0',
            'max': '100',
            'placeholder': 'e.g., 25.00'
        })


class StudentMarkForm(forms.ModelForm):
    """Form for entering student marks"""
    
    class Meta:
        model = StudentMark
        fields = [
            'student', 'subject', 'assessment_type', 'marks_obtained', 
            'total_marks', 'assessment_date', 'submission_date', 
            'status', 'remarks', 'private_notes'
        ]
        widgets = {
            'assessment_date': forms.DateInput(attrs={'type': 'date'}),
            'submission_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'remarks': forms.Textarea(attrs={'rows': 2}),
            'private_notes': forms.Textarea(attrs={'rows': 2}),
        }
        
    def __init__(self, *args, **kwargs):
        course_id = kwargs.pop('course_id', None)
        super().__init__(*args, **kwargs)
        
        # Filter students by course if provided
        if course_id:
            enrolled_students = NewStudent.objects.filter(
                enrollments__course_id=course_id,
                enrollments__status='active',
                status='active'
            ).distinct()
            self.fields['student'].queryset = enrolled_students
            self.fields['subject'].queryset = Subject.objects.filter(
                course_id=course_id, 
                is_active=True
            )
        else:
            self.fields['student'].queryset = NewStudent.objects.filter(status='active')
            self.fields['subject'].queryset = Subject.objects.filter(is_active=True)
        
        self.fields['assessment_type'].queryset = AssessmentType.objects.filter(is_active=True)
        
        # Add CSS classes
        for field_name, field in self.fields.items():
            if field_name not in ['assessment_date', 'submission_date']:
                field.widget.attrs['class'] = 'form-control'
        
        # Special styling for date fields
        self.fields['assessment_date'].widget.attrs.update({
            'class': 'form-control',
            'required': True
        })
        
        self.fields['submission_date'].widget.attrs.update({
            'class': 'form-control'
        })
        
        # Number field styling
        for field_name in ['marks_obtained', 'total_marks']:
            self.fields[field_name].widget.attrs.update({
                'step': '0.01',
                'min': '0',
                'placeholder': 'e.g., 85.50'
            })


class BulkMarkEntryForm(forms.Form):
    """Form for bulk mark entry for multiple students"""
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    assessment_type = forms.ModelChoiceField(
        queryset=AssessmentType.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    total_marks = forms.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0.01',
            'placeholder': 'e.g., 100.00'
        })
    )
    assessment_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    def __init__(self, *args, **kwargs):
        course_id = kwargs.pop('course_id', None)
        super().__init__(*args, **kwargs)
        
        if course_id:
            self.fields['subject'].queryset = Subject.objects.filter(
                course_id=course_id, 
                is_active=True
            )


class GradeScaleForm(forms.ModelForm):
    """Form for creating and editing grade scales"""
    
    class Meta:
        model = GradeScale
        fields = ['grade', 'min_percentage', 'max_percentage', 'grade_points', 'description', 'is_active']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add CSS classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        # Number field styling
        for field_name in ['min_percentage', 'max_percentage', 'grade_points']:
            self.fields[field_name].widget.attrs.update({
                'step': '0.01',
                'min': '0'
            })
        
        self.fields['min_percentage'].widget.attrs.update({
            'max': '100',
            'placeholder': 'e.g., 90.00'
        })
        
        self.fields['max_percentage'].widget.attrs.update({
            'max': '100',
            'placeholder': 'e.g., 100.00'
        })
        
        self.fields['grade_points'].widget.attrs.update({
            'max': '4.00',
            'placeholder': 'e.g., 4.00'
        })
        
        self.fields['grade'].widget.attrs.update({
            'placeholder': 'e.g., A+, A, B+',
            'style': 'text-transform: uppercase;'
        })

    def clean(self):
        cleaned_data = super().clean()
        min_percentage = cleaned_data.get('min_percentage')
        max_percentage = cleaned_data.get('max_percentage')
        
        if min_percentage and max_percentage:
            if min_percentage >= max_percentage:
                raise forms.ValidationError(
                    "Minimum percentage must be less than maximum percentage."
                )
        
        return cleaned_data


class MarkSearchForm(forms.Form):
    """Form for searching and filtering marks"""
    student = forms.ModelChoiceField(
        queryset=NewStudent.objects.filter(status='active'),
        required=False,
        empty_label="All Students",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.filter(is_active=True),
        required=False,
        empty_label="All Subjects",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    assessment_type = forms.ModelChoiceField(
        queryset=AssessmentType.objects.filter(is_active=True),
        required=False,
        empty_label="All Assessment Types",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + StudentMark.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'From Date'
        })
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'To Date'
        })
    )
    grade = forms.CharField(
        required=False,
        max_length=5,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Grade (e.g., A, B+)'
        })
    )
    
    def __init__(self, *args, **kwargs):
        course_id = kwargs.pop('course_id', None)
        super().__init__(*args, **kwargs)
        
        if course_id:
            # Filter by course if provided
            enrolled_students = NewStudent.objects.filter(
                enrollments__course_id=course_id,
                enrollments__status='active',
                status='active'
            ).distinct()
            self.fields['student'].queryset = enrolled_students
            self.fields['subject'].queryset = Subject.objects.filter(
                course_id=course_id, 
                is_active=True
            )


class StudentReportForm(forms.Form):
    """Form for generating student reports"""
    student = forms.ModelChoiceField(
        queryset=NewStudent.objects.filter(status='active'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    semester = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Fall 2024'
        })
    )
    academic_year = forms.CharField(
        required=False,
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 2024-25'
        })
    )
    include_drafts = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class SubjectSearchForm(forms.Form):
    """Form for searching subjects"""
    search_query = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name or code...'
        })
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(status='active'),
        required=False,
        empty_label="All Courses",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    is_active = forms.ChoiceField(
        choices=[('', 'All'), ('true', 'Active Only'), ('false', 'Inactive Only')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    ) 