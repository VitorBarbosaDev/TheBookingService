from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Business, BusinessHours, Slot
from .forms import BusinessForm, BusinessHoursForm
from datetime import timedelta , datetime


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

    # Fetch business hours
    business_hours_list = BusinessHours.objects.filter(business=business).order_by('day')

    context = {
        'business': business,
        'business_hours_list': business_hours_list
    }
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

            create_slots_for_business_hours(business_hours)

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
            update_slots_for_business_hours(business_hour)

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

        remove_slots_for_business_hours(business_hour)

        business_hour.delete()
        messages.success(request, "Business hours deleted successfully.")
        return redirect('business:business_hours_list_add', business_id=business_id)
    return render(request, 'business/delete_business_hours.html', {'business_hour': business_hour})


def create_slots_for_business_hours(business_hours):
    base_date = datetime.now().date()

    start_datetime = datetime.combine(base_date, business_hours.open_time)
    end_datetime = datetime.combine(base_date, business_hours.close_time)
    while start_datetime < end_datetime:
        end_time_slot = start_datetime + timedelta(hours=1)
        if end_time_slot <= end_datetime:
            Slot.objects.create(
                business_hours=business_hours,
                start_time=start_datetime.time(),
                end_time=end_time_slot.time()
            )
        start_datetime += timedelta(hours=1)

def update_slots_for_business_hours(business_hours):

    slots_to_update = Slot.objects.filter(business_hours=business_hours)
    if business_hours.slots.filter(is_booked=True).exists():
        messages.error(request, "Cannot update business hours because there are bookings in the existing slots.")
        return

    # Now we can delete these slots
    slots_to_update.delete()

    # Create new slots based on the updated business hours
    create_slots_for_business_hours(business_hours)

def remove_slots_for_business_hours(business_hours):
    business_hours.slots.all().delete()
