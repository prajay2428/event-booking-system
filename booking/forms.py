from django import forms
from .models import Booking,BookingSeat

class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'first_name',
            'last_name',
            'email'
        ]
