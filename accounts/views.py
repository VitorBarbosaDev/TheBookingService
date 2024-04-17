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
        if account_type == 'business':
            form = BusinessSignupForm(request.POST, request.FILES)
        else:
            form = CustomSignupForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
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
                    category=form.cleaned_data.get('category', None)
                )
                messages.success(request, "Your business account has been successfully created!")
            else:
                UserProfile.objects.create(user=user)
                messages.success(request, "Your personal account has been successfully created!")
            return redirect('profile')
    else:
        form = BusinessSignupForm() if account_type == 'business' else CustomSignupForm()

    context = {
        'form': form,
        'account_type': account_type
    }
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
    context = {'user_type': 'business' if hasattr(user, 'business') else 'personal'}


    if hasattr(user, 'business'):
        received_query = Booking.objects.filter(service__business=user.business)
        status_received = request.GET.get('status_received')
        if status_received:
            received_query = received_query.filter(status=status_received)
        received_paginator = Paginator(received_query, 6)
        context['page_obj_received'] = received_paginator.get_page(request.GET.get('page_received', 1))


    made_query = Booking.objects.filter(customer=user)
    status_made = request.GET.get('status_made')
    if status_made:
        made_query = made_query.filter(status=status_made)
    made_paginator = Paginator(made_query, 6)
    context['page_obj_made'] = made_paginator.get_page(request.GET.get('page_made', 1))

    return render(request, 'accounts/bookings.html', context)
