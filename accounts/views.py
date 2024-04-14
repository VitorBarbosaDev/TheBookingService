from django.shortcuts import render, redirect
from .forms import CustomSignupForm, UserProfileForm
from django.contrib.auth import login
from .models import  UserProfile
from business.models import Business
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from checkout.models import Booking
from django.core.paginator import Paginator

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

@login_required
def edit_profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    context = {'form': form, 'user_profile': user_profile}
    return render(request, 'accounts/edit_profile.html', context)


@login_required
def delete_profile_view(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('home')
    return render(request, 'accounts/delete_profile.html')


@login_required
def bookings_view(request):
    user = request.user
    if hasattr(user, 'business'):

        queryset = Booking.objects.filter(service__business=user.business)
        user_type = 'business'
    else:

        queryset = Booking.objects.filter(customer=user)
        user_type = 'personal'


    status = request.GET.get('status')
    if status:
        queryset = queryset.filter(status=status)


    if request.method == 'POST' and user_type == 'business':
        booking_id = request.POST.get('booking_id')
        booking = queryset.get(id=booking_id)
        if booking.is_eligible_for_completion():
            booking.mark_completed()
            messages.success(request, "Booking has been marked as completed.")
        return redirect('bookings_view')

    # Pagination setup
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/bookings.html', {'page_obj': page_obj, 'user_type': user_type})
