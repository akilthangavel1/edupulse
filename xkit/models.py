from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal


class MaterialCategory(models.Model):
    """Model for categorizing materials"""
    
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    description = models.TextField(blank=True, verbose_name="Description")
    code = models.CharField(max_length=20, unique=True, verbose_name="Category Code")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Material Category'
        verbose_name_plural = 'Material Categories'
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def get_materials_count(self):
        """Get count of materials in this category"""
        return self.materials.count()


class Supplier(models.Model):
    """Model for material suppliers"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blacklisted', 'Blacklisted'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200, verbose_name="Supplier Name")
    code = models.CharField(max_length=20, unique=True, verbose_name="Supplier Code")
    
    # Contact Information
    contact_person = models.CharField(max_length=100, verbose_name="Contact Person")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Phone Number")
    mobile = models.CharField(max_length=20, blank=True, verbose_name="Mobile Number")
    
    # Address
    address = models.TextField(verbose_name="Address")
    city = models.CharField(max_length=100, default="Kuwait City", verbose_name="City")
    country = models.CharField(max_length=100, default="Kuwait", verbose_name="Country")
    
    # Business Details
    trade_license = models.CharField(max_length=100, blank=True, verbose_name="Trade License")
    tax_number = models.CharField(max_length=50, blank=True, verbose_name="Tax Number")
    payment_terms = models.CharField(max_length=100, default="Net 30", verbose_name="Payment Terms")
    
    # Status and Ratings
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2,
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('5.00'))],
        verbose_name="Rating (out of 5)"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def get_absolute_url(self):
        return reverse('supplier_detail', kwargs={'pk': self.pk})
    
    def get_materials_count(self):
        """Get count of materials from this supplier"""
        return self.materials.count()


class Material(models.Model):
    """Model for individual materials that can be combined into kits"""
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('out_of_stock', 'Out of Stock'),
        ('discontinued', 'Discontinued'),
        ('ordered', 'Ordered'),
    ]
    
    UNIT_CHOICES = [
        ('piece', 'Piece'),
        ('set', 'Set'),
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('liter', 'Liter'),
        ('ml', 'Milliliter'),
        ('meter', 'Meter'),
        ('cm', 'Centimeter'),
        ('box', 'Box'),
        ('pack', 'Pack'),
        ('bundle', 'Bundle'),
        ('roll', 'Roll'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200, verbose_name="Material Name")
    material_code = models.CharField(max_length=30, unique=True, verbose_name="Material Code")
    description = models.TextField(verbose_name="Description")
    category = models.ForeignKey(MaterialCategory, on_delete=models.CASCADE, related_name='materials')
    
    # Specifications
    brand = models.CharField(max_length=100, blank=True, verbose_name="Brand")
    model = models.CharField(max_length=100, blank=True, verbose_name="Model")
    color = models.CharField(max_length=50, blank=True, verbose_name="Color")
    size = models.CharField(max_length=50, blank=True, verbose_name="Size")
    weight = models.DecimalField(
        max_digits=8, 
        decimal_places=3,
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Weight (kg)"
    )
    
    # Pricing and Inventory
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='piece', verbose_name="Unit")
    unit_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Unit Cost (KWD)"
    )
    selling_price = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Selling Price (KWD)"
    )
    
    # Stock Management
    current_stock = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        default=Decimal('0.000'),
        validators=[MinValueValidator(Decimal('0.000'))],
        verbose_name="Current Stock"
    )
    minimum_stock = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        default=Decimal('10.000'),
        validators=[MinValueValidator(Decimal('0.000'))],
        verbose_name="Minimum Stock Level"
    )
    maximum_stock = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Maximum Stock Level"
    )
    
    # Supplier Information
    primary_supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name='materials')
    supplier_part_number = models.CharField(max_length=100, blank=True, verbose_name="Supplier Part Number")
    
    # Storage and Location
    storage_location = models.CharField(max_length=100, blank=True, verbose_name="Storage Location")
    shelf_number = models.CharField(max_length=50, blank=True, verbose_name="Shelf Number")
    
    # Status and Images
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    image = models.ImageField(upload_to='material_images/', blank=True, verbose_name="Material Image")
    
    # Usage Tracking
    times_used = models.PositiveIntegerField(default=0, verbose_name="Times Used in Kits")
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_materials')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Material'
        verbose_name_plural = 'Materials'
    
    def __str__(self):
        return f"{self.name} ({self.material_code})"
    
    def get_absolute_url(self):
        return reverse('material_detail', kwargs={'pk': self.pk})
    
    def is_low_stock(self):
        """Check if material stock is below minimum level"""
        return self.current_stock <= self.minimum_stock
    
    def is_available(self):
        """Check if material is available for use"""
        return self.status == 'available' and self.current_stock > 0
    
    def get_profit_margin(self):
        """Calculate profit margin percentage"""
        if self.unit_cost > 0:
            return ((self.selling_price - self.unit_cost) / self.unit_cost) * 100
        return Decimal('0.00')
    
    def get_stock_value(self):
        """Calculate total value of current stock"""
        return self.current_stock * self.unit_cost


class MaterialKit(models.Model):
    """Enhanced kit model that integrates with existing xcoursefee.Kit"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('discontinued', 'Discontinued'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200, verbose_name="Kit Name")
    kit_code = models.CharField(max_length=30, unique=True, verbose_name="Kit Code")
    description = models.TextField(verbose_name="Kit Description")
    category = models.ForeignKey(MaterialCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='kits')
    
    # Kit Type and Usage
    is_template = models.BooleanField(default=False, verbose_name="Template Kit")
    template_for = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='instances', verbose_name="Template For")
    
    # Pricing
    base_cost = models.DecimalField(
        max_digits=12, 
        decimal_places=3,
        default=Decimal('0.000'),
        validators=[MinValueValidator(Decimal('0.000'))],
        verbose_name="Base Cost (KWD)"
    )
    markup_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        default=Decimal('20.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))],
        verbose_name="Markup Percentage"
    )
    selling_price = models.DecimalField(
        max_digits=12, 
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Selling Price (KWD)"
    )
    
    # Assembly and Production
    assembly_time_minutes = models.PositiveIntegerField(default=0, verbose_name="Assembly Time (minutes)")
    assembly_instructions = models.TextField(blank=True, verbose_name="Assembly Instructions")
    quality_checklist = models.TextField(blank=True, verbose_name="Quality Checklist")
    
    # Stock and Availability
    kits_in_stock = models.PositiveIntegerField(default=0, verbose_name="Assembled Kits in Stock")
    minimum_kit_stock = models.PositiveIntegerField(default=5, verbose_name="Minimum Kit Stock")
    can_assemble_count = models.PositiveIntegerField(default=0, verbose_name="Can Assemble Count")
    
    # Status and Management
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    auto_calculate_price = models.BooleanField(default=True, verbose_name="Auto Calculate Price from Materials")
    
    # Integration with existing Kit model
    linked_coursefee_kit = models.OneToOneField(
        'xcoursefee.Kit', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='material_kit',
        verbose_name="Linked Course Fee Kit"
    )
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_kits')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Material Kit'
        verbose_name_plural = 'Material Kits'
    
    def __str__(self):
        return f"{self.name} ({self.kit_code})"
    
    def get_absolute_url(self):
        return reverse('material_kit_detail', kwargs={'pk': self.pk})
    
    def calculate_base_cost(self):
        """Calculate base cost from materials"""
        total_cost = Decimal('0.000')
        for kit_material in self.kit_materials.all():
            total_cost += kit_material.get_total_cost()
        return total_cost
    
    def update_calculated_price(self):
        """Update selling price based on materials and markup"""
        if self.auto_calculate_price:
            self.base_cost = self.calculate_base_cost()
            markup_amount = self.base_cost * (self.markup_percentage / 100)
            self.selling_price = self.base_cost + markup_amount
    
    def can_assemble(self):
        """Check how many kits can be assembled with current materials"""
        min_possible = None
        for kit_material in self.kit_materials.all():
            material = kit_material.material
            if material.current_stock <= 0:
                return 0
            possible = int(material.current_stock // kit_material.quantity_needed)
            if min_possible is None or possible < min_possible:
                min_possible = possible
        return min_possible or 0
    
    def update_can_assemble_count(self):
        """Update the can_assemble_count field"""
        self.can_assemble_count = self.can_assemble()
        self.save(update_fields=['can_assemble_count'])
    
    def get_total_materials_count(self):
        """Get total number of materials in this kit"""
        return self.kit_materials.count()
    
    def is_available_for_assembly(self):
        """Check if kit can be assembled"""
        return self.status == 'active' and self.can_assemble() > 0
    
    def sync_with_coursefee_kit(self):
        """Sync data with linked xcoursefee.Kit model"""
        if self.linked_coursefee_kit:
            # Update the coursefee kit with current data
            kit = self.linked_coursefee_kit
            kit.name = self.name
            kit.kit_code = self.kit_code
            kit.description = self.description
            kit.price = self.selling_price
            kit.stock_quantity = self.kits_in_stock
            kit.minimum_stock = self.minimum_kit_stock
            
            # Update contents from materials
            contents = []
            for kit_material in self.kit_materials.select_related('material'):
                contents.append(f"{kit_material.material.name} x{kit_material.quantity_needed}")
            kit.contents = ", ".join(contents)
            
            kit.save()


class KitMaterial(models.Model):
    """Model linking materials to kits with quantities"""
    
    kit = models.ForeignKey(MaterialKit, on_delete=models.CASCADE, related_name='kit_materials')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='kit_usages')
    
    # Quantity and Specifications
    quantity_needed = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Quantity Needed"
    )
    is_optional = models.BooleanField(default=False, verbose_name="Optional Material")
    notes = models.TextField(blank=True, verbose_name="Usage Notes")
    
    # Cost Override (if different from material's unit cost)
    cost_override = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Cost Override (KWD)"
    )
    
    # Assembly Details
    assembly_order = models.PositiveIntegerField(default=1, verbose_name="Assembly Order")
    assembly_notes = models.TextField(blank=True, verbose_name="Assembly Notes")
    
    # Metadata
    added_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        unique_together = ['kit', 'material']
        ordering = ['assembly_order', 'material__name']
        verbose_name = 'Kit Material'
        verbose_name_plural = 'Kit Materials'
    
    def __str__(self):
        return f"{self.kit.name} - {self.material.name} x{self.quantity_needed}"
    
    def get_effective_cost(self):
        """Get the effective cost per unit (override or material cost)"""
        return self.cost_override if self.cost_override else self.material.unit_cost
    
    def get_total_cost(self):
        """Calculate total cost for this material in the kit"""
        return self.quantity_needed * self.get_effective_cost()
    
    def is_available(self):
        """Check if required quantity is available"""
        return self.material.current_stock >= self.quantity_needed
    
    def get_shortage(self):
        """Get shortage quantity if any"""
        if self.material.current_stock < self.quantity_needed:
            return self.quantity_needed - self.material.current_stock
        return Decimal('0.000')


class StockMovement(models.Model):
    """Model for tracking stock movements of materials"""
    
    MOVEMENT_TYPE_CHOICES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjustment', 'Stock Adjustment'),
        ('transfer', 'Transfer'),
        ('return', 'Return'),
        ('loss', 'Loss/Damage'),
        ('kit_assembly', 'Kit Assembly'),
    ]
    
    REFERENCE_TYPE_CHOICES = [
        ('purchase', 'Purchase Order'),
        ('sale', 'Sale'),
        ('kit_assembly', 'Kit Assembly'),
        ('adjustment', 'Manual Adjustment'),
        ('transfer', 'Stock Transfer'),
        ('return', 'Return'),
        ('loss', 'Loss/Damage'),
    ]
    
    # Movement Details
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Quantity"
    )
    
    # Stock Levels
    stock_before = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.000'))],
        verbose_name="Stock Before"
    )
    stock_after = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.000'))],
        verbose_name="Stock After"
    )
    
    # Reference Information
    reference_type = models.CharField(max_length=20, choices=REFERENCE_TYPE_CHOICES)
    reference_id = models.CharField(max_length=100, blank=True, verbose_name="Reference ID")
    reference_description = models.TextField(verbose_name="Reference Description")
    
    # Cost Information
    unit_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.000'))],
        verbose_name="Unit Cost (KWD)"
    )
    total_cost = models.DecimalField(
        max_digits=12, 
        decimal_places=3,
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.000'))],
        verbose_name="Total Cost (KWD)"
    )
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Stock Movement'
        verbose_name_plural = 'Stock Movements'
    
    def __str__(self):
        return f"{self.material.name} - {self.get_movement_type_display()} - {self.quantity}"
    
    def save(self, *args, **kwargs):
        # Calculate total cost if unit cost is provided
        if self.unit_cost:
            self.total_cost = self.quantity * self.unit_cost
        super().save(*args, **kwargs)


class KitAssemblyLog(models.Model):
    """Model for logging kit assembly activities"""
    
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Assembly Information
    kit = models.ForeignKey(MaterialKit, on_delete=models.CASCADE, related_name='assembly_logs')
    quantity_to_assemble = models.PositiveIntegerField(verbose_name="Quantity to Assemble")
    quantity_completed = models.PositiveIntegerField(default=0, verbose_name="Quantity Completed")
    
    # Process Details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    actual_assembly_time = models.PositiveIntegerField(null=True, blank=True, verbose_name="Actual Assembly Time (minutes)")
    
    # Quality Control
    quality_check_passed = models.BooleanField(null=True, blank=True, verbose_name="Quality Check Passed")
    quality_notes = models.TextField(blank=True, verbose_name="Quality Notes")
    
    # Cost Tracking
    total_material_cost = models.DecimalField(
        max_digits=12, 
        decimal_places=3,
        default=Decimal('0.000'),
        validators=[MinValueValidator(Decimal('0.000'))],
        verbose_name="Total Material Cost (KWD)"
    )
    labor_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        default=Decimal('0.000'),
        validators=[MinValueValidator(Decimal('0.000'))],
        verbose_name="Labor Cost (KWD)"
    )
    
    # Issues and Problems
    issues_encountered = models.TextField(blank=True, verbose_name="Issues Encountered")
    materials_shortage = models.TextField(blank=True, verbose_name="Materials Shortage")
    
    # Metadata
    assembled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assembled_kits')
    supervised_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='supervised_assemblies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Kit Assembly Log'
        verbose_name_plural = 'Kit Assembly Logs'
    
    def __str__(self):
        return f"{self.kit.name} - {self.quantity_to_assemble} units - {self.get_status_display()}"
    
    def calculate_efficiency(self):
        """Calculate assembly efficiency percentage"""
        if self.quantity_to_assemble > 0:
            return (self.quantity_completed / self.quantity_to_assemble) * 100
        return 0
    
    def get_duration_minutes(self):
        """Get assembly duration in minutes"""
        if self.end_time and self.start_time:
            delta = self.end_time - self.start_time
            return int(delta.total_seconds() / 60)
        return None
