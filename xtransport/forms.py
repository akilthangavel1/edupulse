from django import forms
from .models import TransportFee

class TransportFeeForm(forms.ModelForm):
    class Meta:
        model = TransportFee
        fields = ['student', 'amount', 'payment_date', 'notes']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }