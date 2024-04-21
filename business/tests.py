from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from business.models import Business

class BusinessViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.business = Business.objects.create(owner=self.user, name="Test Business")

    def test_business_detail_view(self):
        response = self.client.get(reverse('business:business_detail', kwargs={'pk': self.business.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'business/business_detail.html')

    def test_edit_business_view(self):
        response = self.client.get(reverse('business:edit_business', kwargs={'pk': self.business.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'business/edit_business.html')

    def tearDown(self):
        self.user.delete()