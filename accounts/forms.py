from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    is_business_owner = forms.BooleanField(required=False, label='Register as business owner')
    business_name = forms.CharField(max_length=255, required=False, label='Business Name')

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['business_name'].widget.attrs['placeholder'] = 'Business Name (Required if registering as a business)'
        self.fields['business_name'].widget.attrs['class'] = 'form-control'
        self.fields['is_business_owner'].widget.attrs['class'] = 'form-check-input'

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.is_business_owner = self.cleaned_data['is_business_owner']
        user.save()

        if user.is_business_owner:
            # Assuming you have a signal or method to create the UserProfile
            user_profile = user.userprofile
            user_profile.business_name = self.cleaned_data['business_name']
            user_profile.save()

        return user
