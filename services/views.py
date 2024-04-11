from django.views.generic import ListView
from .models import Service
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from django.urls import reverse_lazy


class ServiceListView(ListView):
    model = Service
    template_name = 'services/my_services.html'
    context_object_name = 'services'

    def get_queryset(self):
        return Service.objects.filter(business__owner=self.request.user)




class ServiceCreateView(CreateView):
    model = Service
    fields = ['name', 'description', 'service_type', 'price', 'price_per_hour', 'min_duration_hours', 'is_active', 'category']
    template_name = 'services/add_service.html'
    success_url = reverse_lazy('services:my_services')

    def form_valid(self, form):
        form.instance.business = self.request.user.business
        return super().form_valid(form)




class ServiceUpdateView(UpdateView):
    model = Service
    fields = ['name', 'description', 'service_type', 'price', 'price_per_hour', 'min_duration_hours', 'is_active', 'category']
    template_name = 'services/edit_service.html'
    success_url = reverse_lazy('services:my_services')




class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'services/delete_service.html'
    success_url = reverse_lazy('services:my_services')

    def get_queryset(self):
        return Service.objects.filter(business__owner=self.request.user)

