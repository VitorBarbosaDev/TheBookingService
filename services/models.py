from django.core.exceptions import ValidationError
from django.db import models
from cloudinary.models import CloudinaryField

class Service(models.Model):
    SERVICE_TYPES = (
        ('fixed', 'Fixed Rate'),
        ('hourly', 'Hourly Rate'),
    )

    business = models.ForeignKey('business.Business', on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=255)
    description = models.TextField()
    service_type = models.CharField(max_length=10, choices=SERVICE_TYPES, default='fixed')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Allow null
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Already allows null
    min_duration_hours = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    image = CloudinaryField('service_images', blank=True, null=True)
    category = models.ForeignKey('accounts.Category', on_delete=models.SET_NULL, null=True, related_name='services')

    def __str__(self):
        return self.name

    def clean(self):
        """
        Ensure that either price or price_per_hour is set, but not both or neither.
        """
        if self.service_type == 'fixed' and not self.price:
            raise ValidationError({'price': 'Fixed rate service must have a price.'})
        elif self.service_type == 'hourly' and not self.price_per_hour:
            raise ValidationError({'price_per_hour': 'Hourly rate service must have a price per hour.'})
        elif self.price and self.price_per_hour:
            raise ValidationError('Only one of price or price_per_hour should be set.')
