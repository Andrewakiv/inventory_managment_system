from django import forms
from .models import Material, Transaction


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'unit_price', 'unit', 'quantity']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['material', 'quantity', 'transaction_type', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
