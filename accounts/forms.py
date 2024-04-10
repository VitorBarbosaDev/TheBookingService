from allauth.account.forms import SignupForm
from django import forms
from .models import UserProfile, Business
from cloudinary.uploader import upload
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name', required=True)
    last_name = forms.CharField(max_length=30, label='Last Name', required=True)
    default_phone_number = forms.CharField(max_length=20, required=False)
    default_street_address1 = forms.CharField(max_length=80, required=False)
    default_street_address2 = forms.CharField(max_length=80, required=False)
    default_town_or_city = forms.CharField(max_length=40, required=False)
    default_county = forms.CharField(max_length=80, required=False)
    default_postcode = forms.CharField(max_length=20, required=False)
    default_country = forms.ChoiceField(choices=CountryField().choices, required=False, widget=CountrySelectWidget())
    profile_picture = forms.ImageField(required=False, label='Profile Picture')

    business_name = forms.CharField(max_length=255, required=False, label='Business Name')
    description = forms.CharField(widget=forms.Textarea, required=False, label='Business Description')
    address = forms.CharField(max_length=255, required=False, label='Business Address')
    phone_number = forms.CharField(max_length=20, required=False, label='Business Phone Number')
    email = forms.EmailField(required=False, label='Business Email')
    website = forms.URLField(required=False, label='Business Website')
    logo = forms.ImageField(required=False, label='Business Logo')

    def __init__(self, *args, **kwargs):
        account_type = kwargs.pop('account_type', None)
        super().__init__(*args, **kwargs)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        profile_pic = self.cleaned_data.get('profile_picture')
        if profile_pic:
            upload_result = upload(profile_pic)
            user.userprofile.profile_picture = upload_result.get('url')
            user.userprofile.save()

        # This ensures that the UserProfile is updated rather than creating a new one
        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                'default_phone_number': self.cleaned_data.get('default_phone_number'),
                'default_street_address1': self.cleaned_data.get('default_street_address1'),
                'default_street_address2': self.cleaned_data.get('default_street_address2'),
                'default_town_or_city': self.cleaned_data.get('default_town_or_city'),
                'default_county': self.cleaned_data.get('default_county'),
                'default_postcode': self.cleaned_data.get('default_postcode'),
                'default_country': self.cleaned_data.get('default_country')
            }
        )

        if request.GET.get('type', 'personal') == 'business':
            user.is_business_owner = True
            user.save()

            business_logo = self.cleaned_data.get('logo')
            if business_logo:
                logo_upload_result = upload(business_logo)
                logo_url = logo_upload_result.get('url')
            else:
                logo_url = None

            Business.objects.create(
                owner=user,
                name=self.cleaned_data.get('business_name'),
                description=self.cleaned_data.get('description'),
                address=self.cleaned_data.get('address'),
                phone_number=self.cleaned_data.get('phone_number'),
                email=self.cleaned_data.get('email'),
                website=self.cleaned_data.get('website'),
                logo=logo_url,
            )

        return user
