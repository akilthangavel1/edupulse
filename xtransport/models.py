from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, EmailValidator
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from xstudent.models import NewStudent


class Vendor(models.Model):
    """Model for transport vendors"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('blacklisted', 'Blacklisted'),
        ('pending_approval', 'Pending Approval'),
    ]
    
    VEHICLE_TYPE_CHOICES = [
        ('bus', 'Bus'),
        ('van', 'Van'),
        ('car', 'Car'),
        ('taxi', 'Taxi'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    vendor_code = models.CharField(max_length=20, unique=True, verbose_name="Vendor Code")
    company_name = models.CharField(max_length=200, verbose_name="Company Name")
    trade_license = models.CharField(max_length=100, unique=True, verbose_name="Trade License")
    
    # Contact Information
    contact_person = models.CharField(max_length=100, verbose_name="Contact Person")
    email = models.EmailField(validators=[EmailValidator()], verbose_name="Email")
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be valid')],
        verbose_name="Phone Number"
    )
    mobile = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Mobile number must be valid')],
        verbose_name="Mobile Number"
    )
    
    # Address
    address = models.TextField(verbose_name="Address")
    area = models.CharField(max_length=100, verbose_name="Area")
    city = models.CharField(max_length=100, default="Kuwait City", verbose_name="City")
    postal_code = models.CharField(max_length=20, blank=True, verbose_name="Postal Code")
    
    # Service Details
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES, verbose_name="Primary Vehicle Type")
    fleet_size = models.PositiveIntegerField(verbose_name="Fleet Size")
    service_areas = models.TextField(verbose_name="Service Areas", help_text="Areas covered by this vendor")
    
    # Financial Information
    rate_per_km = models.DecimalField(
        max_digits=8, 
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Rate per KM (KWD)"
    )
    monthly_rate = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Monthly Rate (KWD)"
    )
    security_deposit = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        default=Decimal('0.000'),
        validators=[MinValueValidator(Decimal('0.000'))],
        verbose_name="Security Deposit (KWD)"
    )
    
    # Contract Details
    contract_start_date = models.DateField(null=True, blank=True, verbose_name="Contract Start Date")
    contract_end_date = models.DateField(null=True, blank=True, verbose_name="Contract End Date")
    payment_terms = models.CharField(max_length=100, default="Net 30", verbose_name="Payment Terms")
    
    # Documents
    trade_license_copy = models.FileField(upload_to='vendor_documents/', blank=True, verbose_name="Trade License Copy")
    insurance_copy = models.FileField(upload_to='vendor_documents/', blank=True, verbose_name="Insurance Copy")
    vehicle_registration = models.FileField(upload_to='vendor_documents/', blank=True, verbose_name="Vehicle Registration")
    
    # Status and Ratings
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_approval')
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2,
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('5.00'))],
        verbose_name="Rating (out of 5)"
    )
    total_reviews = models.PositiveIntegerField(default=0, verbose_name="Total Reviews")
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_vendors')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_vendors')
    approval_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional Notes
    notes = models.TextField(blank=True, verbose_name="Internal Notes")
    
    class Meta:
        ordering = ['company_name']
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'
    
    def __str__(self):
        return f"{self.vendor_code} - {self.company_name}"
    
    def get_absolute_url(self):
        return reverse('vendor_detail', kwargs={'pk': self.pk})
    
    def get_active_students_count(self):
        """Get number of students currently using this vendor"""
        return self.transport_assignments.filter(status='active').count()


class VendorRequest(models.Model):
    """Model for vendor registration requests and approval workflow"""
    
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('requires_documents', 'Requires Additional Documents'),
    ]
    
    # Request Information
    request_id = models.CharField(max_length=20, unique=True, verbose_name="Request ID")
    submission_date = models.DateTimeField(default=timezone.now)
    
    # Company Information
    company_name = models.CharField(max_length=200, verbose_name="Company Name")
    trade_license = models.CharField(max_length=100, verbose_name="Trade License")
    
    # Contact Information
    contact_person = models.CharField(max_length=100, verbose_name="Contact Person")
    email = models.EmailField(validators=[EmailValidator()], verbose_name="Email")
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be valid')],
        verbose_name="Phone Number"
    )
    
    # Service Details
    vehicle_type = models.CharField(max_length=20, choices=Vendor.VEHICLE_TYPE_CHOICES, verbose_name="Primary Vehicle Type")
    fleet_size = models.PositiveIntegerField(verbose_name="Fleet Size")
    service_areas = models.TextField(verbose_name="Service Areas")
    proposed_rate_per_km = models.DecimalField(
        max_digits=8, 
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Proposed Rate per KM (KWD)"
    )
    
    # Documents
    trade_license_copy = models.FileField(upload_to='vendor_requests/', verbose_name="Trade License Copy")
    insurance_copy = models.FileField(upload_to='vendor_requests/', verbose_name="Insurance Copy")
    vehicle_registration = models.FileField(upload_to='vendor_requests/', verbose_name="Vehicle Registration")
    
    # Approval Workflow
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_vendor_requests')
    review_date = models.DateTimeField(null=True, blank=True)
    review_comments = models.TextField(blank=True, verbose_name="Review Comments")
    
    # If approved, link to created vendor
    created_vendor = models.OneToOneField(Vendor, on_delete=models.SET_NULL, null=True, blank=True, related_name='original_request')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-submission_date']
        verbose_name = 'Vendor Request'
        verbose_name_plural = 'Vendor Requests'
    
    def __str__(self):
        return f"{self.request_id} - {self.company_name}"
    
    def approve_request(self, user):
        """Approve vendor request and create vendor"""
        if self.status == 'under_review':
            # Create vendor from request
            vendor = Vendor.objects.create(
                vendor_code=f"VEN{self.id:04d}",
                company_name=self.company_name,
                trade_license=self.trade_license,
                contact_person=self.contact_person,
                email=self.email,
                phone=self.phone,
                vehicle_type=self.vehicle_type,
                fleet_size=self.fleet_size,
                service_areas=self.service_areas,
                rate_per_km=self.proposed_rate_per_km,
                status='active',
                created_by=user,
                approved_by=user,
                approval_date=timezone.now(),
                trade_license_copy=self.trade_license_copy,
                insurance_copy=self.insurance_copy,
                vehicle_registration=self.vehicle_registration,
            )
            
            # Update request
            self.status = 'approved'
            self.reviewed_by = user
            self.review_date = timezone.now()
            self.created_vendor = vendor
            self.save()
            
            return vendor


class StudentTransportAssignment(models.Model):
    """Model for assigning students to transport vendors"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('cancelled', 'Cancelled'),
    ]
    
    TRANSPORT_TYPE_CHOICES = [
        ('pickup_only', 'Pickup Only'),
        ('drop_only', 'Drop Only'),
        ('both_ways', 'Both Ways'),
    ]
    
    # Assignment Details
    student = models.ForeignKey(NewStudent, on_delete=models.CASCADE, related_name='transport_assignments')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='transport_assignments')
    
    # Service Details
    transport_type = models.CharField(max_length=20, choices=TRANSPORT_TYPE_CHOICES, default='both_ways')
    pickup_address = models.TextField(verbose_name="Pickup Address")
    drop_address = models.TextField(blank=True, verbose_name="Drop Address")
    pickup_time = models.TimeField(verbose_name="Pickup Time")
    drop_time = models.TimeField(null=True, blank=True, verbose_name="Drop Time")
    
    # Pricing
    monthly_rate = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Monthly Rate (KWD)"
    )
    
    # Duration
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(null=True, blank=True, verbose_name="End Date")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Emergency Contact
    emergency_contact = models.CharField(max_length=100, verbose_name="Emergency Contact Person")
    emergency_phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be valid')],
        verbose_name="Emergency Phone Number"
    )
    
    # Metadata
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Notes
    special_instructions = models.TextField(blank=True, verbose_name="Special Instructions")
    
    class Meta:
        unique_together = ['student', 'vendor', 'start_date']
        ordering = ['-created_at']
        verbose_name = 'Student Transport Assignment'
        verbose_name_plural = 'Student Transport Assignments'
    
    def __str__(self):
        return f"{self.student.student_name} - {self.vendor.company_name}"


class VendorPayment(models.Model):
    """Model for vendor payment entries and tracking"""
    
    PAYMENT_TYPE_CHOICES = [
        ('monthly', 'Monthly Payment'),
        ('advance', 'Advance Payment'),
        ('adjustment', 'Adjustment'),
        ('bonus', 'Bonus'),
        ('penalty', 'Penalty'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
        ('disputed', 'Disputed'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('bank_transfer', 'Bank Transfer'),
        ('cheque', 'Cheque'),
        ('cash', 'Cash'),
        ('online', 'Online Payment'),
    ]
    
    # Payment Information
    payment_id = models.CharField(max_length=20, unique=True, verbose_name="Payment ID")
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='payments')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, default='monthly')
    
    # Amount Details
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Amount (KWD)"
    )
    tax_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        default=Decimal('0.000'),
        validators=[MinValueValidator(Decimal('0.000'))],
        verbose_name="Tax Amount (KWD)"
    )
    total_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Total Amount (KWD)"
    )
    
    # Period Details (for monthly payments)
    payment_month = models.DateField(null=True, blank=True, verbose_name="Payment Month")
    from_date = models.DateField(null=True, blank=True, verbose_name="From Date")
    to_date = models.DateField(null=True, blank=True, verbose_name="To Date")
    
    # Students covered in this payment
    students_covered = models.ManyToManyField(NewStudent, blank=True, verbose_name="Students Covered")
    student_count = models.PositiveIntegerField(default=0, verbose_name="Number of Students")
    
    # Payment Details
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Payment Method")
    reference_number = models.CharField(max_length=100, blank=True, verbose_name="Reference Number")
    payment_date = models.DateField(null=True, blank=True, verbose_name="Payment Date")
    
    # Status and Approval
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_vendor_payments')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_vendor_payments')
    approval_date = models.DateTimeField(null=True, blank=True)
    
    # Invoice and Receipt
    invoice_number = models.CharField(max_length=50, blank=True, verbose_name="Invoice Number")
    receipt_uploaded = models.FileField(upload_to='vendor_receipts/', blank=True, verbose_name="Receipt/Invoice")
    
    # Notes and Description
    description = models.TextField(verbose_name="Payment Description")
    notes = models.TextField(blank=True, verbose_name="Internal Notes")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Vendor Payment'
        verbose_name_plural = 'Vendor Payments'
    
    def __str__(self):
        return f"{self.payment_id} - {self.vendor.company_name} - {self.total_amount} KWD"
    
    def save(self, *args, **kwargs):
        # Auto-calculate total amount
        self.total_amount = self.amount + self.tax_amount
        super().save(*args, **kwargs)


class MonthlyPaymentGeneration(models.Model):
    """Model for generating monthly payments for vendors"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('generated', 'Generated'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
    ]
    
    # Generation Details
    generation_id = models.CharField(max_length=20, unique=True, verbose_name="Generation ID")
    payment_month = models.DateField(verbose_name="Payment Month")
    
    # Vendor Selection
    vendors = models.ManyToManyField(Vendor, verbose_name="Vendors")
    exclude_inactive = models.BooleanField(default=True, verbose_name="Exclude Inactive Vendors")
    
    # Generation Settings
    include_tax = models.BooleanField(default=True, verbose_name="Include Tax")
    tax_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        default=Decimal('5.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))],
        verbose_name="Tax Rate (%)"
    )
    
    # Status and Results
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    total_vendors = models.PositiveIntegerField(default=0, verbose_name="Total Vendors")
    total_students = models.PositiveIntegerField(default=0, verbose_name="Total Students")
    total_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=3,
        default=Decimal('0.000'),
        verbose_name="Total Amount (KWD)"
    )
    
    # Generation Process
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='generated_transport_payments')
    generation_date = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_payment_generations')
    approval_date = models.DateTimeField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True, verbose_name="Generation Notes")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-payment_month']
        verbose_name = 'Monthly Payment Generation'
        verbose_name_plural = 'Monthly Payment Generations'
    
    def __str__(self):
        return f"{self.generation_id} - {self.payment_month.strftime('%B %Y')}"
    
    def generate_payments(self):
        """Generate individual vendor payments"""
        if self.status == 'draft':
            total_amount = Decimal('0.000')
            total_vendors = 0
            total_students = 0
            
            for vendor in self.vendors.all():
                if self.exclude_inactive and vendor.status != 'active':
                    continue
                
                # Get active students for this vendor in the payment month
                active_assignments = vendor.transport_assignments.filter(
                    status='active',
                    start_date__lte=self.payment_month,
                ).filter(
                    models.Q(end_date__isnull=True) | models.Q(end_date__gte=self.payment_month)
                )
                
                if active_assignments.exists():
                    # Calculate total amount for this vendor
                    vendor_amount = sum([assignment.monthly_rate for assignment in active_assignments])
                    tax_amount = vendor_amount * (self.tax_rate / 100) if self.include_tax else Decimal('0.000')
                    
                    # Create payment record
                    payment = VendorPayment.objects.create(
                        payment_id=f"MP{self.id:04d}V{vendor.id:04d}",
                        vendor=vendor,
                        payment_type='monthly',
                        amount=vendor_amount,
                        tax_amount=tax_amount,
                        payment_month=self.payment_month,
                        from_date=self.payment_month.replace(day=1),
                        to_date=(self.payment_month.replace(day=28) + timezone.timedelta(days=4)).replace(day=1) - timezone.timedelta(days=1),
                        student_count=active_assignments.count(),
                        description=f"Monthly payment for {self.payment_month.strftime('%B %Y')}",
                        created_by=self.generated_by,
                    )
                    
                    # Add students to the payment
                    for assignment in active_assignments:
                        payment.students_covered.add(assignment.student)
                    
                    total_amount += payment.total_amount
                    total_vendors += 1
                    total_students += active_assignments.count()
            
            # Update generation record
            self.status = 'generated'
            self.generation_date = timezone.now()
            self.total_vendors = total_vendors
            self.total_students = total_students
            self.total_amount = total_amount
            self.save()


class VendorRating(models.Model):
    """Model for vendor ratings and reviews"""
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='ratings')
    student = models.ForeignKey(NewStudent, on_delete=models.CASCADE, related_name='vendor_ratings')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Rating (1-5)"
    )
    review = models.TextField(blank=True, verbose_name="Review Comments")
    
    # Service Aspects
    punctuality_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Punctuality (1-5)"
    )
    safety_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Safety (1-5)"
    )
    driver_behavior_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Driver Behavior (1-5)"
    )
    
    # Metadata
    rated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['vendor', 'student']
        ordering = ['-created_at']
        verbose_name = 'Vendor Rating'
        verbose_name_plural = 'Vendor Ratings'
    
    def __str__(self):
        return f"{self.vendor.company_name} - {self.rating}/5 by {self.student.student_name}"
