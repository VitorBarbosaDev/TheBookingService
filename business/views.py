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

            # Delete all existing slots for this business and regenerate
            Slot.objects.filter(business_hours__business=business).delete()
            print(f"Deleted all slots for business {business.name}")

            start_date = datetime.now().date()
            end_date = start_date + timedelta(days=30)  # Modify the range as needed
            generate_slots_for_business(business, start_date, end_date)

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

            # Regenerate slots after updating business hours
            Slot.objects.filter(business_hours=business_hour).delete()


            start_date = datetime.now().date()
            end_date = start_date + timedelta(days=30)  # Adjust the range as necessary
            generate_slots_for_business(business_hour.business, start_date, end_date)

            messages.success(request, "Business hours updated successfully.")
            return redirect('business:business_hours_list_add', business_id=business_hour.business.id)
    else:
        form = BusinessHoursForm(instance=business_hour)
    return render(request, 'business/edit_business_hours.html', {'form': form})

def update_slots_for_business_hours_on_date(business_hours, specific_date):
    Slot.objects.filter(business_hours=business_hours, date=specific_date).delete()
    generate_slots_for_date(business_hours, specific_date)






@login_required
def delete_business_hours(request, pk):
    business_hour = get_object_or_404(BusinessHours, pk=pk, business__owner=request.user)
    if request.method == "POST":
        business_id = business_hour.business.id
        if not business_hour.slots.filter(is_booked=True).exists():
            business_hour.slots.filter(date__week_day=business_hour.day_to_weekday()).delete()
            business_hour.delete()
            messages.success(request, "Business hours and all associated slots deleted successfully.")

        else:
            messages.error(request, "Cannot delete business hours because there are booked slots.")

        return redirect('business:business_hours_list_add', business_id=business_id)
    return render(request, 'business/delete_business_hours.html', {'business_hour': business_hour})



def create_slots_for_business_hours(business_hours):
    current_date = datetime.now().date()
    end_date = current_date + timedelta(days=30)
    while current_date <= end_date:
        if current_date.strftime('%A') == business_hours.day:
            start_datetime = datetime.combine(current_date, business_hours.open_time)
            end_datetime = datetime.combine(current_date, business_hours.close_time)
            while start_datetime < end_datetime:
                end_time_slot = start_datetime + timedelta(hours=1)
                if end_time_slot <= end_datetime:
                    Slot.objects.create(
                        business_hours=business_hours,
                        date=current_date,
                        start_time=start_datetime.time(),
                        end_time=end_time_slot.time(),
                        is_booked=False
                    )

                start_datetime += timedelta(hours=1)
        current_date += timedelta(days=1)






def generate_slots_for_date(business_hours, date):
    if date.strftime('%A') == business_hours.day:
        start_datetime = datetime.combine(date, business_hours.open_time)
        end_datetime = datetime.combine(date, business_hours.close_time)
        while start_datetime < end_datetime:
            end_time_slot = start_datetime + timedelta(hours=1)
            if end_time_slot <= end_datetime:
                Slot.objects.create(
                    business_hours=business_hours,
                    date=date,
                    start_time=start_datetime.time(),
                    end_time=end_time_slot.time(),
                    is_booked=False
                )

            start_datetime += timedelta(hours=1)

def generate_slots_for_business(business, start_date, end_date):

    current_date = start_date
    while current_date <= end_date:
        for business_hours in BusinessHours.objects.filter(business=business):
            generate_slots_for_date(business_hours, current_date)
        current_date += timedelta(days=1)