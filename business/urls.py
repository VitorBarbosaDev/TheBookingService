from django.urls import path
from .views import business_detail

urlpatterns = [
    path('details/', business_detail, name='business_detail'),
]
