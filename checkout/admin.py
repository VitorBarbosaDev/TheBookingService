from django.contrib import admin
from .models import Booking
# Register your models here.

class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'service', 'date', 'status']


admin.site.register(Booking, BookingAdmin)