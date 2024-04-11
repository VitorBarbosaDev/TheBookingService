from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
from django_countries.fields import CountryField
from services.models import Service


class CustomUser(AbstractUser):
    is_business_owner = models.BooleanField(default=False)

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Country', null=True, blank=True)
    profile_picture = CloudinaryField('profile_pictures', blank=True, null=True)

    @receiver(post_save, sender=CustomUser)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
        instance.userprofile.save()





class Booking(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer_bookings')
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE, related_name='bookings')
    date = models.DateTimeField()
    duration_hours = models.IntegerField(default=1, help_text="Duration of the booking in hours for hourly priced services.")
    status = models.CharField(max_length=50, choices=[('confirmed', 'Confirmed'), ('pending', 'Pending'), ('cancelled', 'Cancelled')])
    notes = models.TextField(blank=True, null=True)

class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)


class UserProfileImage(models.Model):
    user = models.ForeignKey(CustomUser, related_name='profile_images', on_delete=models.CASCADE)
    image = CloudinaryField('image')

    def __str__(self):
        return f"{self.user.username}'s image"

    class Meta:
        verbose_name = "User Profile Image"
        verbose_name_plural = "User Profile Images"