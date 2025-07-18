from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from xstudent.models import NewStudent


class Course(models.Model):
    """Model representing different courses offered"""
    
    COURSE_TYPE_CHOICES = [
        ('regular', 'Regular Course'),
        ('intensive', 'Intensive Course'),
        ('summer', 'Summer Course'),
        ('workshop', 'Workshop'),
        ('tutorial', 'Tutorial'),
    ]
    
    DURATION_UNIT_CHOICES = [
        ('months', 'Months'),
        ('weeks', 'Weeks'),
        ('days', 'Days'),
        ('hours', 'Hours'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('coming_soon', 'Coming Soon'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Course Name")
    description = models.TextField(blank=True, verbose_name="Description")
    course_code = models.CharField(max_length=20, unique=True, verbose_name="Course Code")
    course_type = models.CharField(max_length=20, choices=COURSE_TYPE_CHOICES, default='regular')
    
    # Duration and scheduling
    duration = models.PositiveIntegerField(verbose_name="Duration")
    duration_unit = models.CharField(max_length=10, choices=DURATION_UNIT_CHOICES, default='months')
    start_date = models.DateField(null=True, blank=True, verbose_name="Start Date")
    end_date = models.DateField(null=True, blank=True, verbose_name="End Date")
    
    # Capacity and requirements
    max_students = models.PositiveIntegerField(default=30, verbose_name="Maximum Students")
    min_age = models.PositiveIntegerField(null=True, blank=True, verbose_name="Minimum Age")
    max_age = models.PositiveIntegerField(null=True, blank=True, verbose_name="Maximum Age")
    prerequisites = models.TextField(blank=True, verbose_name="Prerequisites")
    
    # Status and metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    instructor_name = models.CharField(max_length=100, blank=True, verbose_name="Instructor")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
    
    def __str__(self):
        return f"{self.name} ({self.course_code})"
    
    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'pk': self.pk})
    
    def get_current_enrollments(self):
        return self.enrollments.filter(status='active').count()
    
    def get_available_spots(self):
        return self.max_students - self.get_current_enrollments()

    def has_kits(self):
        """Check if course has any kits"""
        return self.course_kits.exists()
    
    def get_total_kit_fees(self):
        """Calculate total kit fees for this course"""
        total = Decimal('0.000')
        for course_kit in self.course_kits.all():
            total += course_kit.kit.price
        return total


class FeeStructure(models.Model):
    """Model representing different types of fees for courses"""
    
    FEE_TYPE_CHOICES = [
        ('tuition', 'Tuition Fee'),
        ('registration', 'Registration Fee'),
        ('materials', 'Materials Fee'),
        ('exam', 'Examination Fee'),
        ('library', 'Library Fee'),
        ('lab', 'Laboratory Fee'),
        ('transport', 'Transportation Fee'),
        ('activity', 'Activity Fee'),
        ('other', 'Other Fee'),
    ]
    
    PAYMENT_FREQUENCY_CHOICES = [
        ('one_time', 'One Time'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semester', 'Per Semester'),
        ('annual', 'Annual'),
    ]
    
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='fee_structures',
        verbose_name="Course"
    )
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES, verbose_name="Fee Type")
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Amount (KWD)"
    )
    payment_frequency = models.CharField(
        max_length=20, 
        choices=PAYMENT_FREQUENCY_CHOICES, 
        default='one_time',
        verbose_name="Payment Frequency"
    )
    is_mandatory = models.BooleanField(default=True, verbose_name="Mandatory Fee")
    due_date_offset = models.PositiveIntegerField(
        default=0, 
        verbose_name="Due Date Offset (days)",
        help_text="Days after enrollment when this fee is due"
    )
    description = models.TextField(blank=True, verbose_name="Fee Description")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['course', 'fee_type']
        unique_together = ['course', 'fee_type']
        verbose_name = 'Fee Structure'
        verbose_name_plural = 'Fee Structures'
    
    def __str__(self):
        return f"{self.course.name} - {self.get_fee_type_display()}: {self.amount} KWD"


class StudentEnrollment(models.Model):
    """Model representing student enrollment in courses"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('suspended', 'Suspended'),
        ('pending', 'Pending'),
    ]
    
    student = models.ForeignKey(
        NewStudent, 
        on_delete=models.CASCADE, 
        related_name='course_enrollments',
        verbose_name="Student"
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='enrollments',
        verbose_name="Course"
    )
    enrollment_date = models.DateField(default=timezone.now, verbose_name="Enrollment Date")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Additional enrollment details
    enrollment_notes = models.TextField(blank=True, verbose_name="Enrollment Notes")
    completion_date = models.DateField(null=True, blank=True, verbose_name="Completion Date")
    final_grade = models.CharField(max_length=5, blank=True, verbose_name="Final Grade")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-enrollment_date']
        unique_together = ['student', 'course']
        verbose_name = 'Student Enrollment'
        verbose_name_plural = 'Student Enrollments'
    
    def __str__(self):
        return f"{self.student.student_name} - {self.course.name}"
    
    def get_absolute_url(self):
        return reverse('enrollment_detail', kwargs={'pk': self.pk})
    
    def get_total_fees(self):
        """Calculate total fees for this enrollment"""
        total = Decimal('0.000')
        for fee_structure in self.course.fee_structures.all():
            total += fee_structure.amount
        return total
    
    def get_total_kit_fees(self):
        """Calculate total kit fees for this enrollment"""
        total = Decimal('0.000')
        for kit_fee in self.kit_fees.all():
            total += kit_fee.amount
        return total
    
    def get_total_fees_including_kits(self):
        """Calculate total fees including kit fees"""
        return self.get_total_fees() + self.get_total_kit_fees()
    
    def get_total_paid(self):
        """Calculate total amount paid"""
        total = Decimal('0.000')
        for payment in self.payments.filter(status='completed'):
            total += payment.amount
        return total
    
    def get_total_kit_fees_paid(self):
        """Calculate total kit fees paid"""
        total = Decimal('0.000')
        for kit_fee in self.kit_fees.filter(payment_status='paid'):
            total += kit_fee.amount
        return total
    
    def get_outstanding_balance(self):
        """Calculate outstanding balance"""
        return self.get_total_fees() - self.get_total_paid()
    
    def get_outstanding_kit_fees(self):
        """Calculate outstanding kit fees"""
        return self.get_total_kit_fees() - self.get_total_kit_fees_paid()
    
    def get_total_outstanding_balance(self):
        """Calculate total outstanding balance including kit fees"""
        return self.get_outstanding_balance() + self.get_outstanding_kit_fees()


class Discount(models.Model):
    """Model for managing discounts and scholarships"""
    
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed_amount', 'Fixed Amount'),
    ]
    
    APPLICABILITY_CHOICES = [
        ('all_fees', 'All Fees'),
        ('tuition_only', 'Tuition Only'),
        ('specific_fee', 'Specific Fee Type'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Discount Name")
    description = models.TextField(blank=True, verbose_name="Description")
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, default='percentage')
    value = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Discount Value"
    )
    applicability = models.CharField(max_length=20, choices=APPLICABILITY_CHOICES, default='all_fees')
    
    # Validity and conditions
    valid_from = models.DateField(verbose_name="Valid From")
    valid_until = models.DateField(verbose_name="Valid Until")
    max_usage = models.PositiveIntegerField(null=True, blank=True, verbose_name="Maximum Usage")
    current_usage = models.PositiveIntegerField(default=0, verbose_name="Current Usage")
    
    # Eligibility criteria
    min_enrollment_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="Minimum Enrollments")
    eligible_courses = models.ManyToManyField(Course, blank=True, verbose_name="Eligible Courses")
    
    is_active = models.BooleanField(default=True, verbose_name="Active")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'
    
    def __str__(self):
        if self.discount_type == 'percentage':
            return f"{self.name} ({self.value}%)"
        else:
            return f"{self.name} ({self.value} KWD)"
    
    def is_valid(self):
        """Check if discount is currently valid"""
        today = timezone.now().date()
        return (self.is_active and 
                self.valid_from <= today <= self.valid_until and
                (self.max_usage is None or self.current_usage < self.max_usage))


class Invoice(models.Model):
    """Model for managing student invoices"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    enrollment = models.ForeignKey(
        StudentEnrollment, 
        on_delete=models.CASCADE, 
        related_name='invoices',
        verbose_name="Enrollment"
    )
    invoice_number = models.CharField(max_length=20, unique=True, verbose_name="Invoice Number")
    issue_date = models.DateField(default=timezone.now, verbose_name="Issue Date")
    due_date = models.DateField(verbose_name="Due Date")
    
    # Amount details
    subtotal = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Subtotal (KWD)")
    discount_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        default=Decimal('0.000'),
        verbose_name="Discount Amount (KWD)"
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Total Amount (KWD)")
    
    # Status and notes
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    # Applied discount
    applied_discount = models.ForeignKey(
        Discount, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Applied Discount"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-issue_date']
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.enrollment.student.student_name}"
    
    def get_absolute_url(self):
        return reverse('invoice_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Generate invoice number
            today = timezone.now().date()
            prefix = f"INV-{today.year}{today.month:02d}"
            last_invoice = Invoice.objects.filter(
                invoice_number__startswith=prefix
            ).order_by('-invoice_number').first()
            
            if last_invoice:
                last_number = int(last_invoice.invoice_number.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.invoice_number = f"{prefix}-{new_number:04d}"
        
        super().save(*args, **kwargs)


class Payment(models.Model):
    """Model for tracking fee payments"""
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('cheque', 'Cheque'),
        ('online', 'Online Payment'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    ]
    
    enrollment = models.ForeignKey(
        StudentEnrollment, 
        on_delete=models.CASCADE, 
        related_name='payments',
        verbose_name="Enrollment"
    )
    invoice = models.ForeignKey(
        Invoice, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='payments',
        verbose_name="Invoice"
    )
    
    # Payment details
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Amount (KWD)"
    )
    payment_date = models.DateField(default=timezone.now, verbose_name="Payment Date")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Payment Method")
    reference_number = models.CharField(max_length=100, blank=True, verbose_name="Reference Number")
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    processed_by = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Processed By"
    )
    
    # Additional details
    notes = models.TextField(blank=True, verbose_name="Payment Notes")
    receipt_number = models.CharField(max_length=50, blank=True, verbose_name="Receipt Number")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-payment_date', '-created_at']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
    
    def __str__(self):
        return f"Payment {self.amount} KWD - {self.enrollment.student.student_name}"
    
    def get_absolute_url(self):
        return reverse('payment_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        if not self.receipt_number and self.status == 'completed':
            # Generate receipt number
            today = timezone.now().date()
            prefix = f"REC-{today.year}{today.month:02d}"
            last_payment = Payment.objects.filter(
                receipt_number__startswith=prefix
            ).order_by('-receipt_number').first()
            
            if last_payment:
                last_number = int(last_payment.receipt_number.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.receipt_number = f"{prefix}-{new_number:04d}"
        
        super().save(*args, **kwargs)


class Kit(models.Model):
    """Model representing course kits and materials"""
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('out_of_stock', 'Out of Stock'),
        ('discontinued', 'Discontinued'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Kit Name")
    description = models.TextField(verbose_name="Kit Description")
    kit_code = models.CharField(max_length=20, unique=True, verbose_name="Kit Code")
    
    # Pricing
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Kit Price (KWD)"
    )
    
    # Inventory
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Stock Quantity")
    minimum_stock = models.PositiveIntegerField(default=10, verbose_name="Minimum Stock Level")
    
    # Kit details
    contents = models.TextField(blank=True, verbose_name="Kit Contents")
    supplier = models.CharField(max_length=200, blank=True, verbose_name="Supplier")
    supplier_contact = models.CharField(max_length=100, blank=True, verbose_name="Supplier Contact")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    is_mandatory = models.BooleanField(default=True, verbose_name="Mandatory Kit")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Kit'
        verbose_name_plural = 'Kits'
    
    def __str__(self):
        return f"{self.name} ({self.kit_code}) - {self.price} KWD"
    
    def get_absolute_url(self):
        return reverse('kit_detail', kwargs={'pk': self.pk})
    
    def is_low_stock(self):
        """Check if kit stock is below minimum level"""
        return self.stock_quantity <= self.minimum_stock
    
    def is_available(self):
        """Check if kit is available for purchase"""
        return self.status == 'available' and self.stock_quantity > 0


class CourseKit(models.Model):
    """Intermediate model linking courses with kits"""
    
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='course_kits',
        verbose_name="Course"
    )
    kit = models.ForeignKey(
        Kit, 
        on_delete=models.CASCADE, 
        related_name='course_kits',
        verbose_name="Kit"
    )
    
    # Additional details for this course-kit relationship
    is_required = models.BooleanField(default=True, verbose_name="Required Kit")
    distribution_date = models.DateField(null=True, blank=True, verbose_name="Distribution Date")
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['course', 'kit']
        ordering = ['course', 'kit']
        verbose_name = 'Course Kit'
        verbose_name_plural = 'Course Kits'
    
    def __str__(self):
        return f"{self.course.name} - {self.kit.name}"


class KitFee(models.Model):
    """Model for tracking kit fee payments"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    DELIVERY_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('collected', 'Collected'),
        ('returned', 'Returned'),
    ]
    
    enrollment = models.ForeignKey(
        'StudentEnrollment', 
        on_delete=models.CASCADE, 
        related_name='kit_fees',
        verbose_name="Enrollment"
    )
    course_kit = models.ForeignKey(
        CourseKit, 
        on_delete=models.CASCADE, 
        related_name='kit_fees',
        verbose_name="Course Kit"
    )
    
    # Fee details
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Kit Fee Amount (KWD)"
    )
    
    # Payment tracking
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_date = models.DateField(null=True, blank=True, verbose_name="Payment Date")
    payment_method = models.CharField(
        max_length=20, 
        choices=[
            ('cash', 'Cash'),
            ('bank_transfer', 'Bank Transfer'),
            ('credit_card', 'Credit Card'),
            ('debit_card', 'Debit Card'),
            ('cheque', 'Cheque'),
            ('online', 'Online Payment'),
        ],
        blank=True,
        verbose_name="Payment Method"
    )
    payment_reference = models.CharField(max_length=100, blank=True, verbose_name="Payment Reference")
    
    # Kit delivery tracking
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='pending')
    delivery_date = models.DateField(null=True, blank=True, verbose_name="Delivery Date")
    collected_by = models.CharField(max_length=100, blank=True, verbose_name="Collected By")
    
    # Additional details
    notes = models.TextField(blank=True, verbose_name="Notes")
    processed_by = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Processed By"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['enrollment', 'course_kit']
        ordering = ['-created_at']
        verbose_name = 'Kit Fee'
        verbose_name_plural = 'Kit Fees'
    
    def __str__(self):
        return f"{self.enrollment.student.student_name} - {self.course_kit.kit.name} - {self.amount} KWD"
    
    def get_absolute_url(self):
        return reverse('kit_fee_detail', kwargs={'pk': self.pk})
    
    def can_deliver(self):
        """Check if kit can be delivered (payment completed)"""
        return self.payment_status == 'paid' and self.delivery_status == 'pending'
