from allauth.account.forms import SignupForm
from django import forms
from .models import Business

class CustomSignupForm(SignupForm):
    # Removed is_business_owner as it's determined by URL query parameter
    business_name = forms.CharField(max_length=255, required=False, label='Business Name')

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['business_name'].widget.attrs.update({
            'placeholder': 'Business Name (Only if registering as a business)',
            'class': 'form-control',
            'style': 'display:none;'  # Initially hide this field
        })

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        account_type = request.GET.get('type', 'personal')

        if account_type == 'business':
            user.is_business_owner = True
            user.save()

            business_name = self.cleaned_data.get('business_name')
            if business_name:
                Business.objects.create(
                    owner=user,
                    name=business_name,
                    description=self.cleaned_data.get('description', ''),
                    address=self.cleaned_data.get('address', ''),
                    phone_number=self.cleaned_data.get('phone_number', ''),
                    email=self.cleaned_data.get('email', ''),
                    website=self.cleaned_data.get('website', ''),
                    logo=self.cleaned_data.get('logo', None),
                )

        return user
