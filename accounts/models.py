from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField

class CustomUser(AbstractUser):
    is_business_owner = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = CloudinaryField('profile_pictures', blank=True, null=True)

    @receiver(post_save, sender=CustomUser)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
        instance.userprofile.save()

class Business(models.Model):
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='business')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = CloudinaryField('business_logos', blank=True, null=True)

class Service(models.Model):
    SERVICE_TYPES = (
        ('fixed', 'Fixed Rate'),
        ('hourly', 'Hourly Rate'),
    )

    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=255)
    description = models.TextField()
    service_type = models.CharField(max_length=10, choices=SERVICE_TYPES, default='fixed')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price for fixed rate services.")
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Hourly rate for hourly priced services.")
    min_duration_hours = models.IntegerField(null=True, blank=True, help_text="Minimum duration in hours for bookings, applicable for hourly priced services.")
    is_active = models.BooleanField(default=True)
    image = CloudinaryField('service_images', blank=True, null=True)

class Booking(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer_bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateTimeField()
    duration_hours = models.IntegerField(default=1, help_text="Duration of the booking in hours for hourly priced services.")
    status = models.CharField(max_length=50, choices=[('confirmed', 'Confirmed'), ('pending', 'Pending'), ('cancelled', 'Cancelled')])
    notes = models.TextField(blank=True, null=True)

class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)

class BusinessHours(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='business_hours')
    day = models.CharField(max_length=9, choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')])
    open_time = models.TimeField()
    close_time = models.TimeField()
