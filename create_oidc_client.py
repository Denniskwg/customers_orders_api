#!/usr/bin/env python3
from oidc_provider.models import Client
import os


client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
host_url = os.environ.get('APP_URL', 'http://127.0.0.1:8000')

oidc_client = Client.objects.create(
    name="customers_orders",
    client_id=client_id,
    client_secret=client_secret,
    client_type="confidential",
    response_types=["code"],
    jwt_alg="RS256",
    scope={
        "openid": "OpenID Connect scope"
    },
    redirect_uris='{}/oauth_callback/'.format(host_url)
)

oidc_client.save()
