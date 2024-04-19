from django.urls import path
from . import views
from .views import stripe_webhook

app_name = 'checkout'

urlpatterns = [
    path('confirm_booking/<int:service_id>/', views.confirm_booking, name='confirm_booking'),
    path('fetch_time_slots/', views.fetch_time_slots, name='fetch_time_slots'),
    path('create/', views.create_checkout_session, name='create_session'),
    path('success/', views.checkout_success, name='success'),
    path('error/', views.checkout_error, name='error'),
    path('booking/cancel/', views.booking_cancel, name='booking_cancel'),
    path('payment_verification/', views.payment_verification, name='payment_verification'),
    path('webhook/stripe/', stripe_webhook, name='stripe-webhook'),
]