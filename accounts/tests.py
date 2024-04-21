from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import UserProfile,CustomUser,Review,Category
from business.models import Business, Service
from checkout.models import Booking
from django.utils import timezone


User = get_user_model()

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        UserProfile.objects.get_or_create(user=self.user)
        self.business = Business.objects.create(owner=self.user, name="Test Business")
        self.service = Service.objects.create(
            business=self.business,
            name="Test Service",
            service_type='fixed',
            price=100
        )

    def tearDown(self):
        self.user.delete()


    def test_custom_signup_view_get(self):

        self.client.logout()
        response = self.client.get(reverse('custom_signup_view'))


        self.assertEqual(response.status_code, 200, f"Expected HTTP 200, but got HTTP {response.status_code}")
        self.assertTemplateUsed(response, 'account/signup.html')


    def test_profile_view(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_edit_profile_view_post(self):
        response = self.client.post(reverse('edit_profile'), {'bio': 'New bio'})
        self.assertEqual(response.status_code, 302)

    def test_delete_profile_view(self):
        response = self.client.post(reverse('delete_profile'))
        self.assertEqual(response.status_code, 302)

    def test_bookings_view(self):
        response = self.client.get(reverse('bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/bookings.html')

    def test_submit_review_get(self):
        booking = Booking.objects.create(
            customer=self.user,
            service=self.service,
            date=timezone.now()
        )
        response = self.client.get(reverse('submit_review', args=[booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/submit_review.html')

    def test_submit_review_post(self):
        booking = Booking.objects.create(
            customer=self.user,
            service=self.service,
            date=timezone.now()
        )
        response = self.client.post(reverse('submit_review', args=[booking.id]), {
            'rating': 5,
            'comment': 'Great service!'
        })
        self.assertEqual(response.status_code, 302)

    def test_mark_as_completed(self):
        booking = Booking.objects.create(
            customer=self.user,
            service=self.service,
            status='pending',
            date=timezone.now()
        )
        response = self.client.post(reverse('mark_as_completed', args=[booking.id]))
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'completed')
        self.assertEqual(response.status_code, 302)

    def test_review_thank_you(self):
        response = self.client.get(reverse('review_thank_you'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/review_thank_you.html')

