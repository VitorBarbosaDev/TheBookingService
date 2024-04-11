from django.shortcuts import render, redirect
from .forms import CustomSignupForm
from django.contrib.auth import login
from .models import Business, UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def custom_signup_view(request):
    account_type = request.GET.get('type', 'personal')

    if request.method == 'POST':
        form = CustomSignupForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save(request)
                login(request, user)

                if account_type == 'business':
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
                    messages.success(request, "Your business account has been successfully created!")
                    return redirect('business_dashboard_url')
                else:
                    UserProfile.objects.create(user=user)
                    messages.success(request, "Your personal account has been successfully created!")
                    return redirect('some_personal_success_url')
            except Exception as e:
                messages.error(request, "An error occurred during account creation. Please try again.")
    else:
        form = CustomSignupForm(account_type=account_type)

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