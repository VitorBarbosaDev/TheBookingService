from django import forms
from .models import Business,BusinessHours

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'description', 'address', 'phone_number', 'email', 'website', 'logo', 'category']
        widgets = {
           'logo': forms.FileInput(attrs={'class': 'file-wrap'})
        }


class BusinessHoursForm(forms.ModelForm):
    class Meta:
        model = BusinessHours
        fields = ['day', 'open_time', 'close_time']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-control'}),
            'open_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'close_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }