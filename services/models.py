from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class Service(models.Model):
    SERVICE_TYPES = (
        ('fixed', 'Fixed Rate'),
        ('hourly', 'Hourly Rate'),
    )

    business = models.ForeignKey('accounts.Business', on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=255)
    description = models.TextField()
    service_type = models.CharField(max_length=10, choices=SERVICE_TYPES, default='fixed')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_duration_hours = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    image = CloudinaryField('service_images', blank=True, null=True)
    category = models.ForeignKey('accounts.Category', on_delete=models.SET_NULL, null=True, related_name='services')

    def __str__(self):
        return self.name
