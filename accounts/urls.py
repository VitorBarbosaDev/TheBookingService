from django.urls import path
from .views import profile_view, edit_profile_view, delete_profile_view , bookings_view

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('profile/delete/', delete_profile_view, name='delete_profile'),
    path('profile/bookings/', bookings_view, name='bookings'),
]
