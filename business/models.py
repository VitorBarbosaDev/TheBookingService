from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg

from services.models import Service
from accounts.models import Review

User = get_user_model()

class Business(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='business')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = CloudinaryField('business_logos', blank=True, null=True)
    category = models.ForeignKey('accounts.Category', on_delete=models.SET_NULL, null=True, related_name='businesses')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, blank=True, null=True)

    def __str__(self):
        return self.name


class BusinessHours(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='business_hours')
    day = models.CharField(max_length=9, choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')])
    open_time = models.TimeField()
    close_time = models.TimeField()


class Slot(models.Model):
    business_hours = models.ForeignKey(BusinessHours, on_delete=models.CASCADE, related_name='slots')
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"
