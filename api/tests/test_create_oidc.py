from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from v1.models import User
import json
from django.db import transaction, IntegrityError
from oauth2_provider.models import Application, AccessToken
from django.utils import timezone
from datetime import timedelta
from freezegun import freeze_time


class v1AuthTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='dennisk', password='dennis1996')
        self.admin = User.objects.create_superuser(username='desmondk', password='desmond2000')

        self.app = Application.objects.create(
            name='Test App',
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            user=self.admin
        )

        self.access_token = AccessToken.objects.create(
            user=self.user,
            scope='read write',
            expires=timezone.now() + timedelta(seconds=300),
            token='secret-access-token-key',
            application=self.app
        )


        self.token_url = reverse('oauth2_provider:token')
        self.protected_url = reverse('online_users')


    def test_regular_user_can_access_protected_view_endpoint_with_token(self):
        header = 'Bearer {0}'.format(self.access_token)
        response = self.client.post(self.protected_url, HTTP_AUTHORIZATION=header)

        self.assertEqual(response.status_code, 200)

        self.assertIn('online-users', response.json())

    def test_access_token_expires_in_5_minutes(self):
        expiration_time = timezone.now() + timezone.timedelta(minutes=5)
        AccessToken.objects.filter(token=self.access_token).update(expires=expiration_time)

        with freeze_time(expiration_time):
            header = 'Bearer {0}'.format(self.access_token)
            response = self.client.post(self.protected_url, HTTP_AUTHORIZATION=header)
            self.assertEqual(response.status_code, 403)
            self.assertEqual(response.json()['detail'], 'Invalid or expired token.')

    def test_admin_user_can_access_protected_view_endpoint_without_token(self):
        response = self.client.post(self.protected_url, {'username': self.admin.username, 'password': 'desmond2000' })
        self.assertEqual(response.status_code, 200)
        self.assertIn('online-users', response.json())

    def test_accessing_endpoint_as_regular_user_without_token(self):
        response = self.client.post(self.protected_url, {'username': self.user.username, 'password': 'dennis1996' })
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['error'], 'Unauthorized')

    def test_admin_user_access_protected_view_endpoint_with_wrong_or_invalid_credentials(self):
        response = self.client.post(self.protected_url, {'username': self.admin.username, 'password': 'wrong_password' })    
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['error'], 'Unauthorized')
