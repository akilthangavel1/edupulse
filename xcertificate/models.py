from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from xstudent.models import NewStudent
from xcoursefee.models import Course


class StudentCertificate(models.Model):
    """Simple certificate issue tracker - records when certificates are given"""
    
    # Certificate Identification
    certificate_number = models.CharField(max_length=50, unique=True, blank=True, verbose_name="Certificate Number")
    
    # Student and Course Information
    student = models.ForeignKey(NewStudent, on_delete=models.CASCADE, related_name='certificates', verbose_name="Student")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates', verbose_name="Course")
    
    # Certificate Details
    issue_date = models.DateField(verbose_name="Issue Date (Date Given to Student)")
    
    # Issuance Information
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Issued By")
    
    # Optional Notes
    remarks = models.TextField(blank=True, verbose_name="Remarks (Optional)")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-issue_date', '-created_at']
        verbose_name = 'Certificate Issue Record'
        verbose_name_plural = 'Certificate Issue Records'
    
    def __str__(self):
        return f"{self.certificate_number} - {self.student.student_name} - {self.course.name}"
    
    def save(self, *args, **kwargs):
        # Auto-generate certificate number if not exists
        if not self.certificate_number:
            year = timezone.now().year
            # Get the last certificate for this year
            last_cert = StudentCertificate.objects.filter(
                certificate_number__startswith=f'CERT/{year}/'
            ).order_by('-certificate_number').first()
            
            if last_cert:
                # Extract number and increment
                last_num = int(last_cert.certificate_number.split('/')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            
            self.certificate_number = f'CERT/{year}/{new_num:04d}'
        
        super().save(*args, **kwargs)
