from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, Business, Service, Booking, Review, BusinessHours

# Register your models here.

# Customizing admin interface for CustomUser
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_staff', 'is_business_owner']  # Customize as needed
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_business_owner',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_business_owner',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

# Simple registrations for other models
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'address']

class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'email', 'website']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'price_per_hour', 'min_duration_hours', 'is_active')


class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'service', 'date', 'status']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['booking', 'rating', 'comment']

class BusinessHoursAdmin(admin.ModelAdmin):
    list_display = ['business', 'day', 'open_time', 'close_time']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Business, BusinessAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(BusinessHours, BusinessHoursAdmin)
