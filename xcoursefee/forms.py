from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
from datetime import date, timedelta
from .models import (
    Course, FeeStructure, StudentEnrollment, 
    Discount, Invoice, Payment, Kit, CourseKit, KitFee
)
from xstudent.models import NewStudent


class CourseForm(forms.ModelForm):
    """Form for creating and editing courses"""
    
    class Meta:
        model = Course
        exclude = ['created_at', 'updated_at']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter course description...'
            }),
            'course_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., MAT101, ENG201'
            }),
            'course_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'duration_unit': forms.Select(attrs={
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
            'max_students': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 100
            }),
            'min_age': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 3,
                'max': 25
            }),
            'max_age': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 3,
                'max': 25
            }),
            'prerequisites': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter any prerequisites...'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'instructor_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter instructor name'
            }),
        }
        
        labels = {
            'name': 'Course Name *',
            'description': 'Description',
            'course_code': 'Course Code *',
            'course_type': 'Course Type *',
            'duration': 'Duration *',
            'duration_unit': 'Duration Unit *',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'max_students': 'Maximum Students *',
            'min_age': 'Minimum Age',
            'max_age': 'Maximum Age',
            'prerequisites': 'Prerequisites',
            'status': 'Status *',
            'instructor_name': 'Instructor Name',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        min_age = cleaned_data.get('min_age')
        max_age = cleaned_data.get('max_age')
        
        if start_date and end_date:
            if start_date >= end_date:
                raise ValidationError("End date must be after start date")
        
        if min_age and max_age:
            if min_age >= max_age:
                raise ValidationError("Maximum age must be greater than minimum age")
        
        return cleaned_data


class FeeStructureForm(forms.ModelForm):
    """Form for creating and editing fee structures"""
    
    class Meta:
        model = FeeStructure
        exclude = ['created_at', 'updated_at']
        
        widgets = {
            'course': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fee_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0.001',
                'placeholder': '0.000'
            }),
            'payment_frequency': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_mandatory': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'due_date_offset': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter fee description...'
            }),
        }
        
        labels = {
            'course': 'Course *',
            'fee_type': 'Fee Type *',
            'amount': 'Amount (KWD) *',
            'payment_frequency': 'Payment Frequency *',
            'is_mandatory': 'Mandatory Fee',
            'due_date_offset': 'Due Date Offset (days) *',
            'description': 'Description',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(status='active').order_by('name')


class StudentEnrollmentForm(forms.ModelForm):
    """Form for enrolling students in courses"""
    
    class Meta:
        model = StudentEnrollment
        exclude = ['created_at', 'updated_at', 'completion_date', 'final_grade']
        
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-control'
            }),
            'course': forms.Select(attrs={
                'class': 'form-control'
            }),
            'enrollment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'enrollment_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter any enrollment notes...'
            }),
        }
        
        labels = {
            'student': 'Student *',
            'course': 'Course *',
            'enrollment_date': 'Enrollment Date *',
            'status': 'Status *',
            'enrollment_notes': 'Enrollment Notes',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = NewStudent.objects.filter(status='active').order_by('student_name')
        self.fields['course'].queryset = Course.objects.filter(status='active').order_by('name')
        
        if not self.instance.pk:
            self.fields['enrollment_date'].initial = date.today()
    
    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        course = cleaned_data.get('course')
        
        if student and course:
            # Check if student is already enrolled in this course
            existing_enrollment = StudentEnrollment.objects.filter(
                student=student,
                course=course
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if existing_enrollment.exists():
                raise ValidationError(f"{student.student_name} is already enrolled in {course.name}")
            
            # Check course capacity
            if course.get_current_enrollments() >= course.max_students:
                raise ValidationError(f"Course {course.name} is at full capacity")
            
            # Check age requirements
            if course.min_age or course.max_age:
                today = date.today()
                age = today.year - student.date_of_birth.year - (
                    (today.month, today.day) < (student.date_of_birth.month, student.date_of_birth.day)
                )
                
                if course.min_age and age < course.min_age:
                    raise ValidationError(f"Student is too young for this course (minimum age: {course.min_age})")
                
                if course.max_age and age > course.max_age:
                    raise ValidationError(f"Student is too old for this course (maximum age: {course.max_age})")
        
        return cleaned_data


class PaymentForm(forms.ModelForm):
    """Form for recording payments"""
    
    class Meta:
        model = Payment
        exclude = ['created_at', 'updated_at', 'processed_by', 'receipt_number']
        
        widgets = {
            'enrollment': forms.Select(attrs={
                'class': 'form-control'
            }),
            'invoice': forms.Select(attrs={
                'class': 'form-control'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0.001',
                'placeholder': '0.000'
            }),
            'payment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-control'
            }),
            'reference_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter reference number...'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter payment notes...'
            }),
        }
        
        labels = {
            'enrollment': 'Enrollment *',
            'invoice': 'Invoice',
            'amount': 'Amount (KWD) *',
            'payment_date': 'Payment Date *',
            'payment_method': 'Payment Method *',
            'reference_number': 'Reference Number',
            'status': 'Status *',
            'notes': 'Notes',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['enrollment'].queryset = StudentEnrollment.objects.filter(
            status='active'
        ).select_related('student', 'course').order_by('student__student_name')
        
        if not self.instance.pk:
            self.fields['payment_date'].initial = date.today()


class DiscountForm(forms.ModelForm):
    """Form for creating and editing discounts"""
    
    class Meta:
        model = Discount
        exclude = ['created_at', 'updated_at', 'current_usage']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter discount name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter discount description...'
            }),
            'discount_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0.001'
            }),
            'applicability': forms.Select(attrs={
                'class': 'form-control'
            }),
            'valid_from': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'valid_until': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'max_usage': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'min_enrollment_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'eligible_courses': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        
        labels = {
            'name': 'Discount Name *',
            'description': 'Description',
            'discount_type': 'Discount Type *',
            'value': 'Value *',
            'applicability': 'Applicability *',
            'valid_from': 'Valid From *',
            'valid_until': 'Valid Until *',
            'max_usage': 'Maximum Usage',
            'min_enrollment_count': 'Minimum Enrollments',
            'eligible_courses': 'Eligible Courses',
            'is_active': 'Active',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        valid_from = cleaned_data.get('valid_from')
        valid_until = cleaned_data.get('valid_until')
        discount_type = cleaned_data.get('discount_type')
        value = cleaned_data.get('value')
        
        if valid_from and valid_until:
            if valid_from >= valid_until:
                raise ValidationError("Valid until date must be after valid from date")
        
        if discount_type == 'percentage' and value and value > 100:
            raise ValidationError("Percentage discount cannot exceed 100%")
        
        return cleaned_data


class CourseSearchForm(forms.Form):
    """Form for searching and filtering courses"""
    
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, code, or instructor...'
        }),
        label="Search"
    )
    
    course_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Course.COURSE_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Course Type"
    )
    
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + Course.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status"
    )
    
    min_duration = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min duration'
        }),
        label="Min Duration"
    )
    
    max_duration = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max duration'
        }),
        label="Max Duration"
    )


class PaymentSearchForm(forms.Form):
    """Form for searching and filtering payments"""
    
    student = forms.ModelChoiceField(
        queryset=NewStudent.objects.filter(status='active').order_by('student_name'),
        required=False,
        empty_label="All Students",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Student"
    )
    
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(status='active').order_by('name'),
        required=False,
        empty_label="All Courses",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Course"
    )
    
    payment_method = forms.ChoiceField(
        choices=[('', 'All Methods')] + Payment.PAYMENT_METHOD_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Payment Method"
    )
    
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + Payment.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status"
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


class InvoiceForm(forms.ModelForm):
    """Form for creating and editing invoices"""
    
    class Meta:
        model = Invoice
        exclude = ['created_at', 'updated_at', 'invoice_number']
        
        widgets = {
            'enrollment': forms.Select(attrs={
                'class': 'form-control'
            }),
            'issue_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'subtotal': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0.001',
                'readonly': True
            }),
            'discount_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0.000'
            }),
            'total_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0.001',
                'readonly': True
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter invoice notes...'
            }),
            'applied_discount': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        
        labels = {
            'enrollment': 'Enrollment *',
            'issue_date': 'Issue Date *',
            'due_date': 'Due Date *',
            'subtotal': 'Subtotal (KWD) *',
            'discount_amount': 'Discount Amount (KWD)',
            'total_amount': 'Total Amount (KWD) *',
            'status': 'Status *',
            'notes': 'Notes',
            'applied_discount': 'Applied Discount',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['enrollment'].queryset = StudentEnrollment.objects.filter(
            status='active'
        ).select_related('student', 'course').order_by('student__student_name')
        
        self.fields['applied_discount'].queryset = Discount.objects.filter(
            is_active=True
        ).order_by('name')
        
        if not self.instance.pk:
            self.fields['issue_date'].initial = date.today()
            self.fields['due_date'].initial = date.today() + timedelta(days=30)
    
    def clean(self):
        cleaned_data = super().clean()
        issue_date = cleaned_data.get('issue_date')
        due_date = cleaned_data.get('due_date')
        
        if issue_date and due_date:
            if issue_date > due_date:
                raise ValidationError("Due date must be after issue date")
        
        return cleaned_data


class KitForm(forms.ModelForm):
    """Form for creating and editing kits"""
    
    class Meta:
        model = Kit
        exclude = ['created_at', 'updated_at']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter kit name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter kit description...'
            }),
            'kit_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., KIT001, ELEC-KIT'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0.001',
                'placeholder': '0.000'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'minimum_stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'contents': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter kit contents...'
            }),
            'supplier': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter supplier name'
            }),
            'supplier_contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter supplier contact'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_mandatory': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        
        labels = {
            'name': 'Kit Name *',
            'description': 'Description *',
            'kit_code': 'Kit Code *',
            'price': 'Price (KWD) *',
            'stock_quantity': 'Stock Quantity *',
            'minimum_stock': 'Minimum Stock Level *',
            'contents': 'Kit Contents',
            'supplier': 'Supplier',
            'supplier_contact': 'Supplier Contact',
            'status': 'Status *',
            'is_mandatory': 'Mandatory Kit',
        }
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise ValidationError("Price must be greater than zero")
        return price
    
    def clean_stock_quantity(self):
        stock_quantity = self.cleaned_data.get('stock_quantity')
        if stock_quantity is not None and stock_quantity < 0:
            raise ValidationError("Stock quantity cannot be negative")
        return stock_quantity


class CourseKitForm(forms.ModelForm):
    """Form for linking courses with kits"""
    
    class Meta:
        model = CourseKit
        exclude = ['created_at', 'updated_at']
        
        widgets = {
            'course': forms.Select(attrs={
                'class': 'form-control'
            }),
            'kit': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_required': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'distribution_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter any notes...'
            }),
        }
        
        labels = {
            'course': 'Course *',
            'kit': 'Kit *',
            'is_required': 'Required Kit',
            'distribution_date': 'Distribution Date',
            'notes': 'Notes',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(status='active').order_by('name')
        self.fields['kit'].queryset = Kit.objects.filter(status='available').order_by('name')
    
    def clean(self):
        cleaned_data = super().clean()
        course = cleaned_data.get('course')
        kit = cleaned_data.get('kit')
        
        if course and kit:
            # Check if this course-kit combination already exists
            existing = CourseKit.objects.filter(
                course=course,
                kit=kit
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if existing.exists():
                raise ValidationError(f"Kit '{kit.name}' is already linked to course '{course.name}'")
        
        return cleaned_data


class KitFeeForm(forms.ModelForm):
    """Form for recording kit fee payments"""
    
    class Meta:
        model = KitFee
        exclude = ['created_at', 'updated_at', 'processed_by']
        
        widgets = {
            'enrollment': forms.Select(attrs={
                'class': 'form-control'
            }),
            'course_kit': forms.Select(attrs={
                'class': 'form-control'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0.001',
                'placeholder': '0.000'
            }),
            'payment_status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'payment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-control'
            }),
            'payment_reference': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter payment reference...'
            }),
            'delivery_status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'delivery_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'collected_by': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter collector name...'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter notes...'
            }),
        }
        
        labels = {
            'enrollment': 'Enrollment *',
            'course_kit': 'Course Kit *',
            'amount': 'Kit Fee Amount (KWD) *',
            'payment_status': 'Payment Status *',
            'payment_date': 'Payment Date',
            'payment_method': 'Payment Method',
            'payment_reference': 'Payment Reference',
            'delivery_status': 'Delivery Status *',
            'delivery_date': 'Delivery Date',
            'collected_by': 'Collected By',
            'notes': 'Notes',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['enrollment'].queryset = StudentEnrollment.objects.filter(
            status='active'
        ).select_related('student', 'course').order_by('student__student_name')
        
        # Filter course kits based on available kits
        self.fields['course_kit'].queryset = CourseKit.objects.select_related(
            'course', 'kit'
        ).filter(kit__status='available').order_by('course__name', 'kit__name')
    
    def clean(self):
        cleaned_data = super().clean()
        enrollment = cleaned_data.get('enrollment')
        course_kit = cleaned_data.get('course_kit')
        payment_status = cleaned_data.get('payment_status')
        payment_date = cleaned_data.get('payment_date')
        delivery_status = cleaned_data.get('delivery_status')
        delivery_date = cleaned_data.get('delivery_date')
        
        if enrollment and course_kit:
            # Check if enrollment course matches course kit course
            if enrollment.course != course_kit.course:
                raise ValidationError("Selected course kit must belong to the enrollment's course")
            
            # Check if kit fee already exists for this enrollment and course kit
            existing = KitFee.objects.filter(
                enrollment=enrollment,
                course_kit=course_kit
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if existing.exists():
                raise ValidationError("Kit fee already exists for this enrollment and kit")
        
        # Validate payment date is provided if payment status is paid
        if payment_status == 'paid' and not payment_date:
            raise ValidationError("Payment date is required when payment status is 'paid'")
        
        # Validate delivery date is provided if delivery status is delivered/collected
        if delivery_status in ['delivered', 'collected'] and not delivery_date:
            raise ValidationError("Delivery date is required when delivery status is 'delivered' or 'collected'")
        
        return cleaned_data


class KitSearchForm(forms.Form):
    """Form for searching and filtering kits"""
    
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, code, or supplier...'
        }),
        label="Search"
    )
    
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + Kit.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status"
    )
    
    is_mandatory = forms.ChoiceField(
        choices=[('', 'All'), ('true', 'Mandatory'), ('false', 'Optional')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Type"
    )
    
    min_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.001',
            'placeholder': 'Min price'
        }),
        label="Min Price (KWD)"
    )
    
    max_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.001',
            'placeholder': 'Max price'
        }),
        label="Max Price (KWD)"
    )
    
    low_stock = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Low Stock Only"
    )


class KitFeeSearchForm(forms.Form):
    """Form for searching and filtering kit fees"""
    
    student = forms.ModelChoiceField(
        queryset=NewStudent.objects.filter(status='active').order_by('student_name'),
        required=False,
        empty_label="All Students",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Student"
    )
    
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(status='active').order_by('name'),
        required=False,
        empty_label="All Courses",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Course"
    )
    
    kit = forms.ModelChoiceField(
        queryset=Kit.objects.filter(status='available').order_by('name'),
        required=False,
        empty_label="All Kits",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Kit"
    )
    
    payment_status = forms.ChoiceField(
        choices=[('', 'All Payment Status')] + KitFee.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Payment Status"
    )
    
    delivery_status = forms.ChoiceField(
        choices=[('', 'All Delivery Status')] + KitFee.DELIVERY_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Delivery Status"
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