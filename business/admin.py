from django.contrib import admin
from .models import Business , BusinessHours


class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'email', 'website']


class BusinessHoursAdmin(admin.ModelAdmin):
    list_display = ['business', 'day', 'open_time', 'close_time']


admin.site.register(Business, BusinessAdmin)
admin.site.register(BusinessHours, BusinessHoursAdmin)