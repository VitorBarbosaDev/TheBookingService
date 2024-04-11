from django.urls import path
from .views import business_detail, edit_business, delete_business

urlpatterns = [
    path('', business_detail, name='business_detail'),
    path('edit/<int:pk>/', edit_business, name='edit_business'),
    path('delete/<int:pk>/', delete_business, name='delete_business'),
]