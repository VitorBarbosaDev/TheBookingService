from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from services.models import Service
from business.models import Business

class ServiceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.business = Business.objects.create(owner=self.user, name="Test Business")
        self.service = Service.objects.create(
            name="Test Service",
            business=self.business,
            service_type='fixed',
            price=100.00,
            is_active=True
        )

    def test_service_create_view(self):
        response = self.client.get(reverse('services:add_service'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'services/add_service.html')

    def test_service_update_view(self):
        response = self.client.get(reverse('services:edit_service', args=[str(self.service.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'services/edit_service.html')

    def test_service_delete_view(self):
        response = self.client.get(reverse('services:delete_service', args=[str(self.service.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'services/delete_service.html')

    def test_service_list_view(self):
        response = self.client.get(reverse('services:service_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'services/service_list.html')
        self.assertContains(response, 'Test Service')