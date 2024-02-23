from django.test import TestCase, Client, LiveServerTestCase, override_settings
from django.urls import reverse
from api.models import Customer
import json
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
import unittest
from api.decorators import is_admin_or_has_valid_OIDC_id
from oidc_provider.models import Client as oidc_client
from oidc_provider.models import ResponseType
from api.models import User, Customer, Order
from unittest.mock import patch
import jwt
import os
import datetime
from django.core.exceptions import ValidationError
#from selenium import webdriver

class apiCreateCustomerTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        client_id = os.environ.get('CLIENT_ID')
        client_secret = os.environ.get('CLIENT_SECRET')
        host_url = os.environ.get('APP_URL', 'http://127.0.0.1:8001')

        cls.client = Client()
        cls.customer_url = reverse('create_customer')
        cls.order_url = reverse('create_order')
        cls.register_url = reverse('register')
        cls.login_url = reverse('login')
        cls.admin = User.objects.create_superuser(username='desmondk', password='desmond2000')
        cls.user = User.objects.create_user(username='dennisk', password='d@123456')
        cls.oidc_client = oidc_client.objects.create(
            name="customers_orders",
            client_id=client_id,
            client_secret=client_secret,
            client_type="confidential",
            jwt_alg="RS256",
            redirect_uris='{}/oauth_callback/'.format(host_url)
        )

        response_type_code = ResponseType.objects.get(value='code')
        cls.oidc_client.response_types.set([response_type_code])
        cls.oidc_client.scope = ["openid"]

    def generate_oidc_id_token(self):
        client_id = os.environ.get('CLIENT_ID')
        client_secret = os.environ.get('CLIENT_SECRET')
        host_url = os.environ.get('APP_URL', 'http://127.0.0.1:8001')
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        with open('private_key.pem', 'rb') as private_key_file:
            private_key = private_key_file.read()
        payload = {
            'iss': host_url,
            'sub': str(self.user.id),
            'aud': self.oidc_client.client_id,
            'exp': expiration_time,
            'iat': datetime.datetime.utcnow(),
        }
        token = jwt.encode(payload, private_key, algorithm='RS256')
        return token

    def test_add_customer(self):
        data = {
            'name': 'dennis',
            'phone_number': '+254772440686',
        }

        oidc_id = self.generate_oidc_id_token()
        os.environ['OIDC_KEY_IDENTIFIER'] = '8f30c477c271c38e3f6102a96cd58182'
        os.environ['APP_URL_1'] = self.live_server_url
        os.environ['ENV'] = 'Test'
        with open('public_key.pem', 'rb') as public_key_file:
            os.environ['PUB_KEY'] = public_key_file.read().decode('utf-8')

        

        self.client.cookies['oidc_id_token'] = oidc_id

        response = self.client.post(self.customer_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Customer.objects.filter(name='dennis').exists())


    def test_add_customer_wrong_format_phone_number(self):
        data = {
            'name': 'dennis',
            'phone_number': '0772440686',
        }

        oidc_id = self.generate_oidc_id_token()
        os.environ['OIDC_KEY_IDENTIFIER'] = '8f30c477c271c38e3f6102a96cd58182'
        os.environ['APP_URL_1'] = self.live_server_url
        os.environ['ENV'] = 'Test'
        with open('public_key.pem', 'rb') as public_key_file:
            os.environ['PUB_KEY'] = public_key_file.read().decode('utf-8')



        self.client.cookies['oidc_id_token'] = oidc_id

        try:
            with transaction.atomic():
                response = self.client.post(self.customer_url, data)
                self.assertFalse(Customer.objects.filter(name='dennis').exists())
        except ValidationError as e:
            pass


    def test_add_customer_empty_name(self):
        data = {
            'name': '',
            'phone_number': '0772440686',
        }

        oidc_id = self.generate_oidc_id_token()
        os.environ['OIDC_KEY_IDENTIFIER'] = '8f30c477c271c38e3f6102a96cd58182'
        os.environ['APP_URL_1'] = self.live_server_url
        os.environ['ENV'] = 'Test'
        with open('public_key.pem', 'rb') as public_key_file:
            os.environ['PUB_KEY'] = public_key_file.read().decode('utf-8')



        self.client.cookies['oidc_id_token'] = oidc_id

        try:
            with transaction.atomic():
                response = self.client.post(self.customer_url, data)
        except ValidationError as e:
            pass


    def test_add_order(self):
        data_order = {
            'customer_name': 'dennis',
            'item': 'iphone x',
            'amount': 1,
        }

        data_customer = {
            'name': 'dennis',
            'phone_number': '+254743460363',
        }

        oidc_id = self.generate_oidc_id_token()
        os.environ['OIDC_KEY_IDENTIFIER'] = '8f30c477c271c38e3f6102a96cd58182'
        os.environ['APP_URL_1'] = self.live_server_url
        os.environ['ENV'] = 'Test'
        with open('public_key.pem', 'rb') as public_key_file:
            os.environ['PUB_KEY'] = public_key_file.read().decode('utf-8')



        self.client.cookies['oidc_id_token'] = oidc_id

        #create customer
        self.client.post(self.customer_url, data_customer)

        response = self.client.post(self.order_url, data_order)

        customer = Customer.objects.get(name='dennis')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Order.objects.filter(customer=customer).exists())


    def test_add_order_for_non_existent_customer(self):
        data_order = {
            'customer_name': 'dennis',
            'item': 'iphone x',
            'amount': 1,
        }

        oidc_id = self.generate_oidc_id_token()
        os.environ['OIDC_KEY_IDENTIFIER'] = '8f30c477c271c38e3f6102a96cd58182'
        os.environ['APP_URL_1'] = self.live_server_url
        os.environ['ENV'] = 'Test'
        with open('public_key.pem', 'rb') as public_key_file:
            os.environ['PUB_KEY'] = public_key_file.read().decode('utf-8')



        self.client.cookies['oidc_id_token'] = oidc_id

        try:
            with transaction.atomic():
                response = self.client.post(self.order_url, data_order)
                self.assertEqual(response.status_code, 404)
        except ValidationError as e:
            pass

    """
    def test_notification_after_order_with_valid_phone_number(self):
        data_order = {
            'customer_name': 'dennis',
            'item': 'iphone x',
            'amount': 1,
        }

        data_customer = {
            'name': 'dennis',
            'phone_number': '+254743460363',
        }

        oidc_id = self.generate_oidc_id_token()
        os.environ['OIDC_KEY_IDENTIFIER'] = '8f30c477c271c38e3f6102a96cd58182'
        os.environ['APP_URL_1'] = self.live_server_url
        os.environ['ENV'] = 'TEST_SMS'
        with open('public_key.pem', 'rb') as public_key_file:
            os.environ['PUB_KEY'] = public_key_file.read().decode('utf-8')

        self.client.cookies['oidc_id_token'] = oidc_id

        #create customer
        self.client.post(self.customer_url, data_customer)

        response = self.client.post(self.order_url, data_order)
        print(response.json())

        customer = Customer.objects.get(name='dennis')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('notification_status'), 'Success')
        self.assertTrue(Order.objects.filter(customer=customer).exists())
        """

    def test_notification_after_order_with_invalid_phone_number(self):
        data_order = {
            'customer_name': 'dennis',
            'item': 'iphone x',
            'amount': 1,
        }

        data_customer = {
            'name': 'dennis',
            'phone_number': '+254123456756',
        }

        oidc_id = self.generate_oidc_id_token()
        os.environ['OIDC_KEY_IDENTIFIER'] = '8f30c477c271c38e3f6102a96cd58182'
        os.environ['APP_URL_1'] = self.live_server_url
        os.environ['ENV'] = 'TEST_SMS'
        with open('public_key.pem', 'rb') as public_key_file:
            os.environ['PUB_KEY'] = public_key_file.read().decode('utf-8')

        self.client.cookies['oidc_id_token'] = oidc_id
        #create customer with invalid number
        self.client.post(self.customer_url, data_customer)
        response = self.client.post(self.order_url, data_order)
        print(response.json())

        customer = Customer.objects.get(name='dennis')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('notification_status'), 'InvalidPhoneNumber')
        self.assertFalse(Order.objects.filter(customer=customer).exists())
