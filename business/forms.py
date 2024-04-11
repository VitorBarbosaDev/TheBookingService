from django import forms
from .models import Business

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'description', 'address', 'phone_number', 'email', 'website', 'logo', 'category']
        widgets = {
           'logo': forms.FileInput(attrs={'class': 'file-wrap'})
        }