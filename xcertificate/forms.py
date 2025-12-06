from django import forms
from .models import StudentCertificate
from xstudent.models import NewStudent
from xcoursefee.models import Course


class StudentCertificateForm(forms.ModelForm):
    """Simple form for recording certificate issuance"""
    
    class Meta:
        model = StudentCertificate
        fields = ['student', 'course', 'issue_date', 'remarks']
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'course': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'issue_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional notes (e.g., "Given to student" or "Collected by father")'
            }),
        }
        labels = {
            'student': 'Student',
            'course': 'Course',
            'issue_date': 'Issue Date (Date Given)',
            'remarks': 'Remarks (Optional)',
        }


class CertificateSearchForm(forms.Form):
    """Form for searching certificates"""
    
    student_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by student name...'
        })
    )
    certificate_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by certificate number...'
        })
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        empty_label="All Courses"
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label="Issue Date From"
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label="Issue Date To"
    )


class BulkCertificateForm(forms.Form):
    """Simple form for bulk certificate recording"""
    
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label="Course"
    )
    
    issue_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label="Issue Date (same for all)"
    )
    
    remarks = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'e.g., Graduation Ceremony December 2025'
        }),
        label="Remarks (same for all, optional)"
    )
    
    students = forms.ModelMultipleChoiceField(
        queryset=NewStudent.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        label="Select Students"
    )
