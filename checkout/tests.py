from django.test import TestCase, Client
from django.urls import reverse
from checkout.models import Booking, Transaction, Service
from django.contrib.auth import get_user_model
from unittest.mock import patch
import json
from django.conf import settings
from django.utils import timezone
User = get_user_model()

from services.models import Service
from business.models import Business
from datetime import datetime

class CheckoutViewTests(TestCase):
    def setUp(self):
        # Create a user for the owner of the business
        user = User.objects.create_user(username='testuser', password='12345')

        # Create a Business object
        self.business = Business.objects.create(
            name="Test Business",
            owner=user,
            description="Test Description",
            address="Test Address",
            phone_number="12345",
            email=""
        )

        # Create a Service object associated with the business
        self.service = Service.objects.create(
            name="Test Service",
            price=100.00,
            service_type='fixed',
            business=self.business  # Ensure this line is correctly referencing the Business object
        )

        self.client = Client()
        unique_username = 'testuser' + datetime.now().strftime('%Y%m%d%H%M%S')  # Append current timestamp to username
        self.user = User.objects.create_user(username=unique_username, password='12345', email='test@example.com')
        self.client.login(username=unique_username, password='12345')

        self.booking = Booking.objects.create(
            customer=self.user,
            service=self.service,
            date=timezone.now(),
            status='pending',
            price=100.00
        )

        settings.STRIPE_SECRET_KEY = 'sk_test_yourkey'


