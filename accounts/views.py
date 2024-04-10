from django.shortcuts import render, redirect
from .forms import CustomSignupForm
from django.contrib.auth import login  # Import login method
from .models import Business, UserProfile
from django.contrib.auth.decorators import login_required

def custom_signup_view(request):
    account_type = request.GET.get('type', 'personal')  # Default to 'personal'

    if request.method == 'POST':
        form = CustomSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(request)

            # Log the user in immediately after signing up
            login(request, user)

            if account_type == 'business':
                # Business account setup logic
                Business.objects.create(
                    owner=user,
                    name=form.cleaned_data.get('business_name'),
                    description=form.cleaned_data.get('description', ''),
                    address=form.cleaned_data.get('address', ''),
                    phone_number=form.cleaned_data.get('phone_number', ''),
                    email=form.cleaned_data.get('email', ''),
                    website=form.cleaned_data.get('website', ''),
                    logo=form.cleaned_data.get('logo', None),
                )

                return redirect('business_dashboard_url')
            else:
                # Personal account setup logic
                UserProfile.objects.create(user=user)

                return redirect('some_personal_success_url')
    else:
        form = CustomSignupForm(account_type=account_type)  # Pass account_type here for GET requests too

    context = {'form': form, 'account_type': account_type}
    return render(request, 'accounts/signup.html', context)


@login_required
def profile_view(request):
    """
    Display the user's profile to the user.
    """
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'accounts/profile.html', context)