from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    is_recurring = forms.BooleanField(
        required=False, 
        label='Reserva Recurrente', 
        help_text='Repetir esta reserva cada semana'
    )
    recurrence_weeks = forms.IntegerField(
        required=False, 
        initial=1, 
        min_value=1, 
        max_value=12,
        label='Semanas a repetir',
        help_text='Si es recurrente, ¿cuántas semanas seguidas se repetirá?'
    )

    class Meta:
        model = Booking
        fields = ['start_time', 'end_time', 'notes']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
