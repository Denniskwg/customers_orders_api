from django.test import TestCase, Client
from django.urls import reverse
from api.models import Customer
import json
from django.db import transaction, IntegrityError
import unittest

class apiCreateCustomerTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer_url = reverse('create_customer')
        self.register_url = reverse('register')
        self.login_url = reverse('login')

    def test_add_customer(self):
        data = {
            'name': 'dennis',
            'phone_number': '+254772440686'
        }

        response = self.client.post(self.customer_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Customer.objects.filter(name='dennis').exists())
