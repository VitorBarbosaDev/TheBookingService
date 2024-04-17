from django.urls import path
from . import views
from .views import ServiceListView, ServiceCreateView, ServiceUpdateView, ServiceDeleteView, ServiceDetailView, service_list,service_list_by_category, global_search

urlpatterns = [
    path('search/', global_search, name='global_search'),
    path('my-services/', views.ServiceListView.as_view(), name='my_services'),
    path('services/add/', views.ServiceCreateView.as_view(), name='add_service'),
    path('services/<int:pk>/edit/', views.ServiceUpdateView.as_view(), name='edit_service'),
    path('services/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='delete_service'),
    path('services/', service_list, name='service_list'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('services/category/<slug:category_slug>/', service_list_by_category, name='service_list_by_category'),
]
