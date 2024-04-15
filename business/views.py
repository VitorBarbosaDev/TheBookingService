from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Business, BusinessHours
from .forms import BusinessForm, BusinessHoursForm

@login_required
def business_detail(request, pk=None):
    business = None
    if pk:
        business = get_object_or_404(Business, pk=pk)
    else:
        try:
            business = Business.objects.get(owner=request.user)
        except Business.DoesNotExist:
            messages.error(request, "Business profile not found.")
            return redirect('home')

    context = {'business': business}
    return render(request, 'business/business_detail.html', context)


@login_required
def edit_business(request, pk):
    business = get_object_or_404(Business, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES, instance=business)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your business profile has been updated.')
            return redirect('business:business_detail')
    else:
        form = BusinessForm(instance=business)
    return render(request, 'business/edit_business.html', {'form': form, 'business': business})




@login_required
def delete_business(request, pk):
    business = get_object_or_404(Business, pk=pk, owner=request.user)
    if request.method == 'POST':
        business.delete()
        messages.success(request, 'Your business profile has been deleted.')
        return redirect('home')
    return render(request, 'business/delete_business.html', {'business': business})



@login_required
def business_hours_list_add(request, business_id):
    business = get_object_or_404(Business, id=business_id, owner=request.user)
    if request.method == 'POST':
        form = BusinessHoursForm(request.POST)
        if form.is_valid():
            business_hours = form.save(commit=False)
            business_hours.business = business
            business_hours.save()
            messages.success(request, 'Business hours added successfully.')
            return redirect('business:business_hours_list_add', business_id=business.id)
    else:
        form = BusinessHoursForm()
    business_hours_list = BusinessHours.objects.filter(business=business)
    return render(request, 'business/business_hours_list_add.html', {'form': form, 'business_hours_list': business_hours_list, 'business': business})


@login_required
def edit_business_hours(request, pk):
    business_hour = get_object_or_404(BusinessHours, pk=pk, business__owner=request.user)
    if request.method == "POST":
        form = BusinessHoursForm(request.POST, instance=business_hour)
        if form.is_valid():
            form.save()
            messages.success(request, "Business hours updated successfully.")
            return redirect('business:business_hours_list_add', business_id=business_hour.business.id)
    else:
        form = BusinessHoursForm(instance=business_hour)
    return render(request, 'business/edit_business_hours.html', {'form': form})

@login_required
def delete_business_hours(request, pk):
    business_hour = get_object_or_404(BusinessHours, pk=pk, business__owner=request.user)
    if request.method == "POST":
        business_id = business_hour.business.id
        business_hour.delete()
        messages.success(request, "Business hours deleted successfully.")
        return redirect('business:business_hours_list_add', business_id=business_id)
    return render(request, 'business/delete_business_hours.html', {'business_hour': business_hour})