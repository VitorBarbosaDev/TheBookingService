from django.urls import path
from . import views

urlpatterns = [
    path('my-services/', views.ServiceListView.as_view(), name='my_services'),
    path('services/add/', views.ServiceCreateView.as_view(), name='add_service'),
    path('services/<int:pk>/edit/', views.ServiceUpdateView.as_view(), name='edit_service'),
    path('services/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='delete_service'),
]
