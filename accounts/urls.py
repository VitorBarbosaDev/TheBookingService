from django.urls import path
from .views import profile_view, edit_profile_view, delete_profile_view , bookings_view , mark_as_completed,submit_review,review_thank_you

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('profile/delete/', delete_profile_view, name='delete_profile'),
    path('profile/bookings/', bookings_view, name='bookings'),
    path('booking/<int:booking_id>/complete/', mark_as_completed, name='mark_as_completed'),
    path('booking/<int:booking_id>/review/', submit_review, name='submit_review'),
    path('review/thank-you/', review_thank_you, name='review_thank_you'),
]
