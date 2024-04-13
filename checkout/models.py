from django.db import models
from django.conf import settings
from services.models import Service
from django.utils import timezone

class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField()
    duration_hours = models.IntegerField(default=1, help_text="Duration of the booking in hours.")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"Booking {self.pk} for {self.service.name}"

    def is_eligible_for_completion(self):
            """Check if the booking date has passed and status is confirmed."""
            return self.date < timezone.now() and self.status == 'confirmed'

    def mark_completed(self):
            """Mark the booking as completed."""
            self.status = 'completed'
            self.save()



class Transaction(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount in EUR")
    transaction_id = models.CharField(max_length=255, unique=True, help_text="Unique transaction identifier from the payment gateway")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} for Booking {self.booking.id}"
