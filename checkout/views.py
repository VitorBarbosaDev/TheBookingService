import json
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest , HttpResponse
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
from django.urls import reverse
import stripe
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import get_user_model


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



    if service.service_type == 'fixed' and service.price is not None:
        unit_amount = int(service.price * 100)
    elif service.service_type == 'hourly' and service.price_per_hour is not None:
        unit_amount = int(service.price_per_hour * 100)
    else:
        logger.error(f"Appropriate price for service ID {service_id} is not set.")
        return JsonResponse({'error': 'Appropriate price is not set for this service type'}, status=400)

    form = BookingForm(request.POST, user=request.user)
    if form.is_valid():
        booking = form.save(commit=False)
        booking.service = service
        booking.status = 'pending'  # Default status
        booking.save()

        try:

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

                booking = Booking(
                            service=service,
                            customer=request.user,
                            date=timezone.now(),
                            price=service.price,
                            status='pending',
                            payment_intent_id=checkout_session.payment_intent
                        )

                return JsonResponse({'redirect_url': checkout_session.url})
        except Exception as e:
            logger.exception("Error creating Stripe checkout session: ", exc_info=e)
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid form data'}, status=400)




def checkout_error(request):
    request.session.pop('checkout_session_id', None)
    request.session.pop('payment_status', None)
    request.session.pop('booking_id', None)
    request.session.pop('transaction_id', None)

    service_id = request.session.get('service_id')  # Retrieving service_id from session
    if service_id:
        error_url = reverse('checkout:confirm_booking', args=[service_id])
    else:
        error_url = reverse('home')


    context = {
        'error_url': error_url,
        'message': 'There was a problem processing your payment. Please try again or contact support if the problem persists.'
    }
    return render(request, 'checkout/error.html', context)




def checkout_success(request):

    if request.session.get('payment_status') == 'Success':
        booking_id = request.session.get('booking_id')
        if not booking_id:
            logger.warning("No booking ID found in session.")
            messages.error(request, "Error: Booking ID is missing. Unable to retrieve booking details.")
            return redirect('checkout:error')

        try:
            booking = Booking.objects.get(pk=booking_id)

            booking.status = 'confirmed'
            booking.save()
        except Booking.DoesNotExist:
            logger.error(f"Booking with ID {booking_id} not found.")
            messages.error(request, "Error: No booking found with the provided ID.")
            return redirect('checkout:error')


        del request.session['payment_status']
        if 'booking_id' in request.session:
            del request.session['booking_id']
        if 'checkout_session_id' in request.session:
            del request.session['checkout_session_id']


        messages.success(request, "Booking and payment successful! Thank you for your purchase.")

        context = {'booking': booking}
        return render(request, 'checkout/checkout_success.html', context)
    else:
        messages.error(request, "Payment was not successful. Please try again.")
        return redirect('checkout:error')



def booking_cancel(request):
    booking_id = request.session.get('booking_id')
    if booking_id:
        booking = get_object_or_404(Booking, pk=booking_id)
        transaction = Transaction.objects.filter(booking=booking).first()

        try:
            # Assume we store Stripe's charge ID in Transaction model
            if transaction and transaction.stripe_charge_id:
                refund = stripe.Refund.create(
                    charge=transaction.stripe_charge_id
                )
                transaction.refund_id = refund.id
                transaction.save()
                booking.status = 'cancelled'
                booking.save()
                messages.success(request, "Your booking has been cancelled and refunded.")
            else:
                booking.status = 'cancelled'
                booking.save()
                messages.success(request, "Your booking has been cancelled.")


            del request.session['booking_id']
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    else:
        messages.error(request, "No active booking found to cancel.")

    return render(request, 'checkout/booking_cancel.html', {
        'message': 'Your booking cancellation process has been handled.'
    })

def send_cancellation_email(booking):
    send_mail(
        'Booking Cancellation',
        f'Your booking for {booking.service.name} on {booking.date} has been cancelled.',
        settings.DEFAULT_FROM_EMAIL,
        [booking.customer.email],
        fail_silently=False,
    )

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
    booking_date = timezone.now().date()  # Ensure date is timezone-aware right at the start
    slots = generate_slots_for_business_hours(business_hours_qs, booking_date)

    context = {
        'service': service,
        'slots': slots,
    }

    booking_form = BookingForm(request.POST or None, slots=slots, user=request.user if request.user.is_authenticated else None)
    transaction_form = TransactionForm(request.POST or None)

    if request.method == 'POST':
        if booking_form.is_valid() and transaction_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.service = service
            booking.customer = request.user if request.user.is_authenticated else None
            booking.price = calculate_price(service, booking_form.cleaned_data['duration_hours'])

            slot_time = booking_form.cleaned_data['start_time']
            start_time = datetime.strptime(slot_time.split(' - ')[0], '%H:%M').time()
            booking.date = timezone.make_aware(datetime.combine(booking_date, start_time))
            if request.user.is_authenticated:
                        booking.customer = request.user
            else:

                guest_user = get_user_model().objects.create_user(
                    username=f"guest_{timezone.now().strftime('%Y%m%d%H%M%S')}",
                    email=booking_form.cleaned_data['email'],
                    first_name=booking_form.cleaned_data['first_name'],
                    last_name=booking_form.cleaned_data['last_name'],
                    is_business_owner=False,
                    password=None,
                    is_guest=True
                )
                guest_user.save()
                booking.customer = guest_user

            booking.save()

            # Save the booking_id in the session
            request.session['booking_id'] = booking.pk
            request.session['service_id'] = service.id

            transaction = transaction_form.save(commit=False)
            transaction.booking = booking
            transaction.amount = booking.price
            transaction.transaction_id = f"TXN-{timezone.now().strftime('%Y%m%d%H%M%S')}-{booking.id}"
            transaction.save()


            request.session['transaction_id'] = transaction.transaction_id

            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': service.name,
                            },
                            'unit_amount': int(booking.price * 100),
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('checkout:payment_verification')),
                    cancel_url=request.build_absolute_uri(reverse('checkout:booking_cancel')),
                )
                request.session['checkout_session_id'] = checkout_session.id
                return redirect(checkout_session.url)
            except stripe.error.StripeError as e:
                context['error_message'] = str(e)
                messages.error(request, f"Stripe error: {str(e)}")
        else:
            context['booking_form_errors'] = booking_form.errors
            context['transaction_form_errors'] = transaction_form.errors
            messages.error(request, 'There was an error with your submission.')

    context.update({
        'booking_form': booking_form,
        'transaction_form': transaction_form,
    })

    return render(request, 'checkout/confirm_booking.html', context)


def calculate_price(service, duration_hours):
    if service.service_type == 'hourly':
        return float(service.price_per_hour) * duration_hours
    return service.price

@csrf_exempt
def payment_verification(request):
    session_id = request.session.get('checkout_session_id')
    if not session_id:
        messages.error(request, "No payment session found.")
        return redirect('checkout:error')

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == 'paid':

            request.session['payment_status'] = 'Success'


            del request.session['checkout_session_id']


            return redirect('checkout:success')
        else:

            request.session['payment_status'] = 'Failure'


            del request.session['checkout_session_id']


            return redirect('checkout:error')
    except Exception as e:
        logger.error(f"Failed to verify payment session: {e}")
        messages.error(request, f"Error verifying payment: {e}")


        del request.session['checkout_session_id']
        return redirect('checkout:error')


stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WH_SECRET
        )
    except ValueError as e:
        logger.error(f'Invalid payload: {str(e)}')
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f'Invalid signature: {str(e)}')
        return HttpResponse(status=400)


    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        try:
            booking = Booking.objects.get(payment_intent_id=payment_intent['id'])
            booking.status = 'confirmed'
            booking.save()


            send_mail(
                'Booking Confirmation',
                f'Your booking for {booking.service.name} on {booking.date.strftime("%Y-%m-%d at %H:%M")} has been confirmed. Thank you for your payment.',
                settings.DEFAULT_FROM_EMAIL,
                [booking.customer.email],
                fail_silently=False,
            )
            logger.info(f"Booking {booking.id} confirmed and customer notified via email.")
        except Booking.DoesNotExist:
            logger.error(f'Booking with payment intent ID {payment_intent["id"]} not found.')
            return HttpResponse(status=404)
    else:
        logger.info(f'Unhandled event type {event["type"]}')

    return HttpResponse(status=200)

