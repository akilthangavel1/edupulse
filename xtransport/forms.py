from django import forms
from .models import TransportFee

class TransportFeeForm(forms.ModelForm):
    class Meta:
        model = TransportFee
        fields = ['student', 'amount', 'payment_date', 'notes']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
        }