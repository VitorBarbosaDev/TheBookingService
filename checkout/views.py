import json
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Booking , Transaction
from services.models import Service
import logging
from .forms import BookingForm, TransactionForm
from django.urls import reverse
from business.models import BusinessHours
from collections import defaultdict
from datetime import datetime, timedelta, date




# Set up logging
logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_checkout_session(request):
    data = {}
    if request.body:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return HttpResponseBadRequest("Invalid JSON data.")
    else:
        logger.warning("Empty request body received.")
        return HttpResponseBadRequest("Empty request body.")

    service_id = data.get('service_id')
    if not service_id:
        logger.error("Service ID not provided in the request.")
        return JsonResponse({'error': 'Service ID is required'}, status=400)

    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        logger.error(f"Service with ID {service_id} not found.")
        return JsonResponse({'error': 'Service not found'}, status=404)

    # Determine the unit_amount based on service type
    if service.service_type == 'fixed' and service.price is not None:
        unit_amount = int(service.price * 100)  # Convert to cents
    elif service.service_type == 'hourly' and service.price_per_hour is not None:
        unit_amount = int(service.price_per_hour * 100)  # Convert to cents
    else:
        logger.error(f"Appropriate price for service ID {service_id} is not set.")
        return JsonResponse({'error': 'Appropriate price is not set for this service type'}, status=400)

    try:
        # Create the Stripe checkout session with dynamic unit_amount
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': service.name,
                    },
                    'unit_amount': unit_amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/checkout/success/'),
            cancel_url=request.build_absolute_uri('/checkout/cancel/'),
        )

        return JsonResponse({'redirect_url': checkout_session.url})
    except Exception as e:
        logger.exception("Error creating Stripe checkout session: ", exc_info=e)
        return JsonResponse({'error': str(e)}, status=500)


def checkout_success(request):
    booking_id = request.session.get('booking_id')
    if not booking_id:
        logger.warning("No booking ID found in session.")
        return HttpResponseBadRequest("Booking ID is required.")

    try:
        booking = Booking.objects.get(pk=booking_id)
    except Booking.DoesNotExist:
        logger.error(f"Booking with ID {booking_id} not found.")
        return JsonResponse({'error': 'Booking not found'}, status=404)

    context = {'booking': booking}
    return render(request, 'checkout/success.html', context)



def generate_weekly_slots(business_hours_qs):
    slots_by_day = defaultdict(list)
    week_dates = get_week_dates()  # This should give you a list of dates for the current week

    for day_date in week_dates:
        day_name = day_date.strftime('%A')
        day_hours_qs = business_hours_qs.filter(day=day_name)

        for bh in day_hours_qs:
            start_datetime = datetime.combine(day_date, bh.open_time)
            end_datetime = datetime.combine(day_date, bh.close_time)

            current_time = start_datetime
            while current_time + timedelta(hours=1) <= end_datetime:
                next_time = current_time + timedelta(hours=1)
                slot_format = f"{day_date.strftime('%Y-%m-%d')} {current_time.strftime('%H:%M')} - {next_time.strftime('%H:%M')}"
                slots_by_day[day_name].append(slot_format)
                current_time = next_time

    return slots_by_day

def generate_slots(start_time, end_time, date, duration_hours=1):
    """Generates booking slots within business hours, adjusted to rounded hours."""
    slots = []
    # Ensure start time is at the beginning of an hour
    start_dt = datetime.combine(date, start_time)
    start_dt = start_dt.replace(minute=0, second=0, microsecond=0)

    # Ensure end time is at the end of an hour
    end_dt = datetime.combine(date, end_time)
    end_dt = end_dt.replace(minute=0, second=0, microsecond=0)

    while start_dt + timedelta(hours=duration_hours) <= end_dt:
        slot_start = start_dt.strftime('%H:%M')
        slot_end = (start_dt + timedelta(hours=duration_hours)).strftime('%H:%M')
        slots.append((f"{slot_start} - {slot_end}", f"{slot_start} - {slot_end}"))
        start_dt += timedelta(hours=duration_hours)  # Adjust as needed for different increments

    return slots



def get_week_dates():
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    return [week_start + timedelta(days=i) for i in range(7)]


def generate_slots_for_business_hours(business_hours_qs, date):
    slots = []
    for bh in business_hours_qs:
        start_datetime = datetime.combine(date, bh.open_time)
        end_datetime = datetime.combine(date, bh.close_time)
        current_time = start_datetime
        while current_time + timedelta(hours=1) <= end_datetime:
            next_time = current_time + timedelta(hours=1)
            slot_format = f"{current_time.strftime('%H:%M')} - {next_time.strftime('%H:%M')}"
            slots.append((slot_format, slot_format))
            current_time = next_time
    return slots


@csrf_exempt
def confirm_booking(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    business_hours_qs = BusinessHours.objects.filter(business=service.business)
    booking_date = datetime.today().date()
    slots = generate_slots_for_business_hours(business_hours_qs, booking_date)  # Generate slots for both GET and POST

    if request.method == 'POST':
        booking_form = BookingForm(request.POST, slots=slots, user=request.user if request.user.is_authenticated else None)
        transaction_form = TransactionForm(request.POST)
        if booking_form.is_valid() and transaction_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.service = service
            if request.user.is_authenticated:
                booking.customer = request.user
            if service.service_type == 'hourly':
                booking.price = float(service.price_per_hour) * booking.duration_hours
            else:
                booking.price = service.price

            slot_time = booking_form.cleaned_data['start_time']  # 'HH:MM - HH:MM'
            start_time = datetime.strptime(slot_time.split(' - ')[0], '%H:%M')
            booking.date = datetime.combine(datetime.today(), start_time.time())

            booking.save()
            transaction = transaction_form.save(commit=False)
            transaction.booking = booking
            transaction.amount = booking.price
            transaction.transaction_id = f"TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}-{booking.id}"
            transaction.save()
            return redirect('checkout_success')
    else:
        booking_form = BookingForm(initial={'start_time': slots}, slots=slots, user=request.user if request.user.is_authenticated else None)
        transaction_form = TransactionForm()

    context = {
        'service': service,
        'booking_form': booking_form,
        'transaction_form': transaction_form,
    }
    return render(request, 'checkout/confirm_booking.html', context)

