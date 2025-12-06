from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from xstudent.models import NewStudent


class TransportFee(models.Model):
    """Model for managing transport fee entries."""

    student = models.ForeignKey(NewStudent, on_delete=models.CASCADE, related_name='transport_fees')
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))],
        verbose_name="Fee Amount (KWD)"
    )
    payment_date = models.DateField(verbose_name="Payment Date")
    notes = models.TextField(blank=True, verbose_name="Notes")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-payment_date']
        verbose_name = 'Transport Fee'
        verbose_name_plural = 'Transport Fees'

    def __str__(self):
        return f"{self.student.student_name} - {self.amount} KWD"
