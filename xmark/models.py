from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from xstudent.models import NewStudent
from xcoursefee.models import Course


class Subject(models.Model):
    """Subject/Topic model for organizing marks"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    description = models.TextField(blank=True)
    credit_hours = models.PositiveIntegerField(default=3)
    instructor = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Subjects"

    def __str__(self):
        return f"{self.code} - {self.name}"

    def get_total_students(self):
        """Get total number of students enrolled in this subject's course"""
        return self.course.enrollments.filter(status='active').count()

    def get_average_marks(self):
        """Calculate average marks for this subject"""
        marks = StudentMark.objects.filter(subject=self, is_active=True)
        if marks.exists():
            total = sum([mark.marks_obtained for mark in marks])
            return round(total / marks.count(), 2)
        return 0


class AssessmentType(models.Model):
    """Types of assessments (Quiz, Midterm, Final, etc.)"""
    CATEGORY_CHOICES = [
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('midterm', 'Midterm Exam'),
        ('final', 'Final Exam'),
        ('project', 'Project'),
        ('presentation', 'Presentation'),
        ('lab', 'Lab Work'),
        ('participation', 'Class Participation'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    weight_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Weight in final grade calculation (0-100%)"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['weight_percentage', 'name']

    def __str__(self):
        return f"{self.name} ({self.weight_percentage}%)"


class GradeScale(models.Model):
    """Grade scale definition (A, B, C, etc.)"""
    grade = models.CharField(max_length=5)  # A+, A, B+, B, etc.
    min_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    max_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    grade_points = models.DecimalField(max_digits=3, decimal_places=2)
    description = models.CharField(max_length=50, blank=True)  # Excellent, Good, etc.
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-min_percentage']
        unique_together = ['grade', 'min_percentage', 'max_percentage']

    def __str__(self):
        return f"{self.grade} ({self.min_percentage}%-{self.max_percentage}%)"

    @classmethod
    def get_grade_for_percentage(cls, percentage):
        """Get grade for a given percentage"""
        try:
            return cls.objects.filter(
                min_percentage__lte=percentage,
                max_percentage__gte=percentage,
                is_active=True
            ).first()
        except:
            return None


class StudentMark(models.Model):
    """Individual student mark entries"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('published', 'Published'),
        ('revised', 'Revised'),
    ]

    student = models.ForeignKey(NewStudent, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='student_marks')
    assessment_type = models.ForeignKey(AssessmentType, on_delete=models.CASCADE, related_name='marks')
    
    # Mark details
    marks_obtained = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    total_marks = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        blank=True, 
        null=True
    )
    grade = models.CharField(max_length=5, blank=True)  # Calculated grade
    grade_points = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    
    # Assessment details
    assessment_date = models.DateField()
    submission_date = models.DateTimeField(blank=True, null=True)
    
    # Status and notes
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    remarks = models.TextField(blank=True)
    private_notes = models.TextField(blank=True, help_text="Internal notes (not visible to students)")
    
    # Tracking
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='entered_marks')
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_marks')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-assessment_date', '-created_at']
        unique_together = ['student', 'subject', 'assessment_type', 'assessment_date']
        verbose_name_plural = "Student Marks"

    def __str__(self):
        return f"{self.student.student_name} - {self.subject.code} - {self.assessment_type.name}"

    def save(self, *args, **kwargs):
        """Auto-calculate percentage and grade on save"""
        if self.total_marks and self.total_marks > 0:
            self.percentage = round((self.marks_obtained / self.total_marks) * 100, 2)
            
            # Get grade from scale
            grade_scale = GradeScale.get_grade_for_percentage(self.percentage)
            if grade_scale:
                self.grade = grade_scale.grade
                self.grade_points = grade_scale.grade_points
        
        super().save(*args, **kwargs)

    def get_percentage_display(self):
        """Get formatted percentage"""
        if self.percentage:
            return f"{self.percentage}%"
        return "-"

    def is_passing(self, passing_percentage=60):
        """Check if mark is passing"""
        return self.percentage and self.percentage >= passing_percentage

    def get_status_color(self):
        """Get Bootstrap color class for status"""
        colors = {
            'draft': 'secondary',
            'submitted': 'warning',
            'published': 'success',
            'revised': 'info'
        }
        return colors.get(self.status, 'secondary')


class StudentGradeSummary(models.Model):
    """Summary of student's overall performance in a subject"""
    student = models.ForeignKey(NewStudent, on_delete=models.CASCADE, related_name='grade_summaries')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grade_summaries')
    
    # Calculated totals
    total_marks_obtained = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_possible_marks = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    weighted_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    final_grade = models.CharField(max_length=5, blank=True)
    final_grade_points = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    
    # Status
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateField(blank=True, null=True)
    semester = models.CharField(max_length=20, blank=True)
    academic_year = models.CharField(max_length=10, blank=True)
    
    # Tracking
    calculated_at = models.DateTimeField(auto_now=True)
    calculated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ['student', 'subject', 'semester', 'academic_year']
        ordering = ['-calculated_at']

    def __str__(self):
        return f"{self.student.student_name} - {self.subject.code} - {self.final_grade}"

    def calculate_weighted_grade(self):
        """Calculate weighted grade based on all assessments"""
        marks = StudentMark.objects.filter(
            student=self.student,
            subject=self.subject,
            status='published',
            is_active=True
        )
        
        total_weighted_score = 0
        total_weight = 0
        
        for mark in marks:
            if mark.percentage and mark.assessment_type.weight_percentage:
                weighted_score = (mark.percentage * mark.assessment_type.weight_percentage) / 100
                total_weighted_score += weighted_score
                total_weight += mark.assessment_type.weight_percentage
        
        if total_weight > 0:
            self.weighted_percentage = round(total_weighted_score, 2)
            
            # Get final grade
            grade_scale = GradeScale.get_grade_for_percentage(self.weighted_percentage)
            if grade_scale:
                self.final_grade = grade_scale.grade
                self.final_grade_points = grade_scale.grade_points
        
        self.save()
        return self.weighted_percentage
