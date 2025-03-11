from django import forms
from .models import MeterReading, Tariff

class MeterReadingForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = MeterReading
        fields = ['date', 'kwh_used']

class TariffForm(forms.ModelForm):
    class Meta:
        model = Tariff
        fields = ['price_per_kwh']
        widgets = {
            'price_per_kwh': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 1}),
        }
