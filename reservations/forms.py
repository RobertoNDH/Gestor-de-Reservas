from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    is_recurring = forms.BooleanField(
        required=False, 
        label='Reserva Recurrente', 
        help_text='Repetir esta reserva cada semana',
        widget=forms.CheckboxInput(attrs={'autocomplete': 'off'})
    )
    recurrence_weeks = forms.IntegerField(
        required=False, 
        initial=1, 
        min_value=1, 
        max_value=12,
        label='Semanas a repetir',
        help_text='Si es recurrente, ¿cuántas semanas seguidas se repetirá?',
        widget=forms.NumberInput(attrs={'autocomplete': 'off'})
    )

    class Meta:
        model = Booking
        fields = ['start_time', 'end_time', 'notes']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'autocomplete': 'off'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'autocomplete': 'off'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'autocomplete': 'off'}),
        }
