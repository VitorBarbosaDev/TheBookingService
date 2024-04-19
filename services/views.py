from django.views.generic import ListView
from .models import Service
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.detail import DetailView
from accounts.models import Category
from business.models import BusinessHours , Business
import logging
from django.db.models import Q


class ServiceListView(ListView):
    model = Service
    template_name = 'services/my_services.html'
    context_object_name = 'services'

    def get_queryset(self):
        return Service.objects.filter(business__owner=self.request.user)

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.get_object()
        business_hours_qs = BusinessHours.objects.filter(business=service.business)


        week_days_order = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4,
                           'Friday': 5, 'Saturday': 6, 'Sunday': 7}


        sorted_business_hours = sorted(business_hours_qs, key=lambda x: week_days_order[x.day])

        context['business_hours_qs'] = sorted_business_hours
        return context


def get_services_by_category(category):
    """Recursively gets services under the given category and its subcategories."""
    services = Service.objects.filter(category=category, is_active=True)
    for subcategory in category.children.all():
        services |= get_services_by_category(subcategory)
    return services

def service_list_by_category(request, category_slug):
    category = None
    services = Service.objects.filter(is_active=True)
    businesses = Business.objects.none()  # Start with no businesses

    if category_slug != 'all':
        category = get_object_or_404(Category, slug=category_slug)
        services = get_services_by_category(category)

    query = request.GET.get('q')
    if query:
        services = services.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        businesses = Business.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    return render(request, 'services/service_list_by_category.html', {
        'category': category,
        'services': services,
        'businesses': businesses
    })


class ServiceCreateView(CreateView):
    model = Service
    fields = ['name', 'description', 'service_type', 'price', 'price_per_hour', 'min_duration_hours', 'is_active', 'category', 'image']  # Include 'image' field
    template_name = 'services/add_service.html'
    success_url = reverse_lazy('services:my_services')

    def form_valid(self, form):
        form.instance.business = self.request.user.business
        return super().form_valid(form)

class ServiceUpdateView(UpdateView):
    model = Service
    fields = ['name', 'description', 'service_type', 'price', 'price_per_hour', 'min_duration_hours', 'is_active', 'category', 'image']  # Include 'image' field
    template_name = 'services/edit_service.html'
    success_url = reverse_lazy('services:my_services')





class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'services/delete_service.html'
    success_url = reverse_lazy('services:my_services')

    def get_queryset(self):
        return Service.objects.filter(business__owner=self.request.user)

def service_list(request):
    query = request.GET.get('q')
    context = {}

    if query:
        services_list = Service.objects.filter(name__icontains=query) | Service.objects.filter(description__icontains=query)
        businesses_list = Business.objects.filter(name__icontains=query) | Business.objects.filter(description__icontains=query)
    else:
        services_list = Service.objects.all()
        businesses_list = Business.objects.none()


    service_paginator = Paginator(services_list, 6)
    page = request.GET.get('page')
    try:
        services = service_paginator.page(page)
    except PageNotAnInteger:
        services = service_paginator.page(1)
    except EmptyPage:
        services = service_paginator.page(service_paginator.num_pages)


    context['services'] = services
    context['businesses'] = businesses_list

    return render(request, 'services/service_list.html', context)

