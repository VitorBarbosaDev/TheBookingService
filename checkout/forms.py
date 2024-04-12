from django import forms
from .models import Booking, Transaction
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class BookingForm(forms.ModelForm):
    start_time = forms.ChoiceField(choices=[])

    class Meta:
        model = Booking
        fields = ['start_time', 'duration_hours', 'notes', 'first_name', 'last_name', 'phone_number', 'default_country', 'default_county', 'default_postcode', 'default_town_or_city', 'default_street_address1', 'default_street_address2']

    def __init__(self, *args, **kwargs):
        slots = kwargs.pop('slots', [])
        user = kwargs.pop('user', None)
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].choices = slots
        if user:
            try:
                user_profile = user.userprofile
                self.fields['first_name'].initial = user.first_name
                self.fields['last_name'].initial = user.last_name
                self.fields['phone_number'].initial = user_profile.default_phone_number
                self.fields['default_street_address1'].initial = user_profile.default_street_address1
                self.fields['default_street_address2'].initial = user_profile.default_street_address2
                self.fields['default_town_or_city'].initial = user_profile.default_town_or_city
                self.fields['default_county'].initial = user_profile.default_county
                self.fields['default_postcode'].initial = user_profile.default_postcode
                self.fields['default_country'].initial = user_profile.default_country
            except UserProfile.DoesNotExist:

                  pass
    # Added billing details fields
    first_name = forms.CharField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100)
    phone_number = forms.CharField(required=True, max_length=20)
    default_street_address1 = forms.CharField(max_length=80, required=False)
    default_street_address2 = forms.CharField(max_length=80, required=False)
    default_town_or_city = forms.CharField(max_length=40, required=False)
    default_county = forms.CharField(max_length=80, required=False)
    default_postcode = forms.CharField(max_length=20, required=False)
    default_country = forms.ChoiceField(choices=CountryField().choices, required=False, widget=CountrySelectWidget())



class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ['booking','amount', 'transaction_id']
