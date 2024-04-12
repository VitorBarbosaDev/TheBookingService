from django.urls import path
from . import views

app_name = 'checkout'


urlpatterns = [
    path('confirm_booking/<int:service_id>/', views.confirm_booking, name='confirm_booking'),
    path('create/', views.create_checkout_session, name='create_session'),
    path('success/', views.checkout_success, name='success'),
]
