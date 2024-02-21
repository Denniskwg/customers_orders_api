"""customers_orders_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
import oauth2_provider.views as oauth2_views
from django.conf import settings


# OAuth2 provider endpoints
oauth2_endpoint_views = [
    path('authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path('token/', oauth2_views.TokenView.as_view(), name="token"),
    path('revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
    path('.well-known/openid-configuration/', oauth2_views.ConnectDiscoveryInfoView.as_view(), name='oidc-connect-discovery-info'),
    path('userinfo/', oauth2_views.UserInfoView.as_view(), name='user-info'),
    path('.well-known/jwks.info', oauth2_views.JwksInfoView.as_view(), name='jwks-info'),
]


if settings.DEBUG:
    # OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        path('applications/', oauth2_views.ApplicationList.as_view(), name="list"),
        path('applications/register/', oauth2_views.ApplicationRegistration.as_view(), name="register"),
        path('applications/<pk>/', oauth2_views.ApplicationDetail.as_view(), name="detail"),
        path('applications/<pk>/delete/', oauth2_views.ApplicationDelete.as_view(), name="delete"),
        path('applications/<pk>/update/', oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]

    # OAuth2 Token Management endpoints
    oauth2_endpoint_views += [
        path('authorized-tokens/', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
        path('authorized-tokens/<pk>/delete/', oauth2_views.AuthorizedTokenDeleteView.as_view(), name="authorized-token-delete"),
    ]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('status', views.status, name='status'),
    path('o/', include((oauth2_endpoint_views, 'oauth2_provider'), namespace="oauth2_provider")),
    path('openid/', include('oidc_provider.urls', namespace='oidc_provider')),
    path('oauth_callback/', views.oauth_callback, name='oauth_callback'),
    path('create_customer', views.Create_customer.as_view(), name='create_customer'),
    path('create_order', views.Create_order.as_view(), name='create_order'),
    path('login', views.Login.as_view(), name='login'),
    path('register', views.Register.as_view(), name='register'),
    path('', views.Home.as_view(), name='home'),
    path('logout', views.Logout.as_view(), name='logout'),
]
