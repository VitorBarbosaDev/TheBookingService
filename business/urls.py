from django.urls import path
from .views import (
    business_detail, edit_business, delete_business,
    business_hours_list_add, edit_business_hours, delete_business_hours
)

app_name = 'business'

urlpatterns = [
    path('detail/', business_detail, name='business_detail'),
    path('detail/<int:pk>/', business_detail, name='business_detail'),
    path('edit/<int:pk>/', edit_business, name='edit_business'),
    path('delete/<int:pk>/', delete_business, name='delete_business'),
    path('business/<int:business_id>/hours/', business_hours_list_add, name='business_hours_list_add'),
    path('hours/edit/<int:pk>/', edit_business_hours, name='edit_business_hours'),
    path('hours/delete/<int:pk>/', delete_business_hours, name='delete_business_hours'),
]
