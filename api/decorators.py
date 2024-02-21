from functools import wraps
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import authentication
from rest_framework import exceptions
import jwt
from datetime import datetime
from django.shortcuts import redirect
from .models import User
import requests
import os
from jose import jwk



def is_admin_or_has_valid_OIDC_id(view_func):
    """checks if user accessing view is an admin user or has valid_OIDC_id
    """
    @wraps(view_func)
    def wrapped_view(instance, request, *args, **kwargs):
        client_id = os.environ.get('CLIENT_ID', None)
        host_url = os.environ.get('APP_URL_1', 'http://127.0.0.1:8000')
        base_url = 'openid/authorize/?'
        url = '{}response_type=code&client_id={}&redirect_uri={}&scope={}'.format(
            base_url,
            client_id,
            '{}/oauth_callback/'.format(host_url),
            'openid',
        )
        if request.user.is_authenticated and request.user.is_staff:
            print("ADMIN")
            return view_func(instance, request, *args, **kwargs)
        else:
            jwk_url = '{}/openid/jwks/'.format(host_url)
            response = requests.get(jwk_url)
            response_jwk = response.json()
            identifier = os.environ.get('OIDC_KEY_IDENTIFIER', None)
            jwk_dict = next(key for key in response_jwk["keys"] if key["kid"] == identifier)

            public_key = jwk.construct(jwk_dict)
            key = public_key.to_pem().decode('utf-8')

            oidc_id_token = request.COOKIES.get('oidc_id_token', None)
            if oidc_id_token is None:
                request.session['previous_url'] = request.build_absolute_uri()
                return redirect(url)
            try:
                decoded_token = jwt.decode(oidc_id_token, key=key, algorithms=['RS256'], audience=[client_id])
                current_time = datetime.utcnow()
                exp_time = datetime.utcfromtimestamp(decoded_token['exp'])
                if current_time > exp_time:
                    raise jwt.ExpiredSignatureError
                return view_func(instance, request, *args, **kwargs)
            except jwt.InvalidSignatureError as e:
                print(repr(e))
                return JsonResponse({'message': 'Invalid credentials!'}, status=403)
            except jwt.ExpiredSignatureError:
                request.session['previous_url'] = request.build_absolute_uri()
                return redirect(url)
            except jwt.InvalidTokenError as e:
                print(repr(e))
                return JsonResponse({'message': 'Invalid credentials!'}, status=403)
    return wrapped_view
