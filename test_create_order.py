from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from v1.models import User
import json
from django.db import transaction, IntegrityError
import unittest

class v1RegisterTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        data = {
            'username': 'dennisk',
            'password': 'Dennis_1996',
        }
        self.client.post(self.register_url, data)

    def test_register_post(self):
        data = {
            'username': 'desmondk',
            'password': 'Deswk@1996',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='dennisk').exists())

    def test_register_with_existing_username(self):
        data2 = {
            'username': 'dennisk',
            'password': 'dennis1996',
        }

        try:
            with transaction.atomic():
                self.client.post(self.register_url, data2)
        except IntegrityError as e:
            pass

    def test_register_with_short_password(self):
        data = {
            'username': 'desmondk',
            'password': 'desw',
        }

        try:
            with transaction.atomic():
                self.client.post(self.register_url, data)
        except ValueError as e:
            pass

    def test_register_with_password_with_less_than_three_digits(self):
        data = {
            'username': 'desmondk',
            'password': 'Desw@56',
        }

        try:
            with transaction.atomic():
                response = self.client.post(self.register_url, data)
        except ValueError as e:
            pass
