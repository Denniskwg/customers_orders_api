from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from rest_framework.views import APIView
import requests
from django.contrib.auth import login, authenticate, logout
from oauth2_provider.views.generic import ProtectedResourceView
from django.http import QueryDict
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.password_validation import validate_password
from .forms import LoginForm, RegisterForm, CustomerForm, OrderForm
from .models import User, Customer, Order
import jwt
from .decorators import is_admin_or_has_valid_OIDC_id
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
import os
from api.tasks import send_sms_notification
from django.views import View


def status(request):
    print(request.user)
    return JsonResponse({"status": "ok"})


def oauth_callback(request):
    """callback function for oauth flow
    redirects to a protected resource after obtaining oidc id
    """
    if 'code' in request.GET:
        host_url = os.environ.get('APP_URL_1', 'http://127.0.0.1:8000')
        authorization_code = request.GET.get('code')
        token_endpoint = '{}/openid/token/'.format(host_url)
        redirect_uri = '{}/oauth_callback/'.format(host_url)
        client_id = os.environ.get('CLIENT_ID', None)
        client_secret = os.environ.get('CLIENT_SECRET', None)

        response = requests.post(
            token_endpoint,
            data={
                'grant_type': 'authorization_code',
                'code': authorization_code,
                'redirect_uri': redirect_uri,
                'client_id': client_id,
                'client_secret': client_secret,
            }
        )
        token_data = response.json()
        oidc_id_token = token_data.get('id_token')
        previous_url = request.session.get('previous_url', None)
        if previous_url:
            response = HttpResponseRedirect(previous_url)
            response.set_cookie('oidc_id_token', oidc_id_token)
        else:
            response = HttpResponseRedirect(reverse('home'))
            response.set_cookie('oidc_id_token', oidc_id_token)
        return response
    else:
        return HttpResponse("Authorization code not found.")

class Home(TemplateView):
    """homepage view
    """
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')

class Logout(View):
    """logout view
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class Login(TemplateView):
    """login view
    """
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                request.session['name'] = username
                full_url = request.get_full_path()
                query_params = QueryDict(request.META['QUERY_STRING'])
                next_param = query_params.get('next', None)
                if next_param:
                    return redirect(next_param)
                return JsonResponse({"message": "Logged in!"}, status=200)
            else:
                try:
                    existing_user = User.objects.get(username=username)
                    return JsonResponse({"message": "password missing or incorrect"}, status=400)
                except User.DoesNotExist:
                    return JsonResponse({"message": "user doesn't exist"}, status=404)
        return render(request, 'login.html', {'form': form})

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                request.session['name'] = username
                return JsonResponse({"message": "Logged in!"}, status=200)
            else:
                try:
                    existing_user = User.objects.get(username=username)
                    return JsonResponse({"message": "password missing or incorrect"}, status=400)
                except User.DoesNotExist:
                    return JsonResponse({"message": "user doesn't exist"}, status=404)
        return render(request, 'login.html', {'form': form})




class Register(View):
    """register view
    registers a new user using password and username
    """
    def post(self, request, *args, **kwargs):
        """accepts post requests for the register view and registers user
        """
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                validate_password(password, user=None)
            except ValidationError as e:
                error_messages = [str(message) for message in e.messages]
                return JsonResponse({"error": error_messages}, status=400)

            try:
                user = User.objects.create_user(username=username, password=password)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                user.save()
            except Exception as e:
                response = JsonResponse({ "message": e.args[0] }, status=404)
                return response
            response = JsonResponse({ "message": "User created successfully" }, status=200)
            return response
        return render(request, 'register.html', {'form': RegisterForm()})

    def get(self, request, *args, **kwargs):
        """accepts get requests for the register view and registers user
        """
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                validate_password(password, user=None)
            except ValidationError as e:
                error_messages = [str(message) for message in e.messages]
                return JsonResponse({"error": error_messages}, status=400)
            try:
                user = User.objects.create_user(username=username, password=password)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                user.save()
            except Exception as e:
                response = JsonResponse({ "message": e.args[0] }, status=404)
                return response
            response = JsonResponse({ "message": "User created successfully" }, status=200)
            return response
        return render(request, 'register.html', {'form': RegisterForm()})


class Create_customer(FormView):
    """creates a customer entry
    authorization is required before access
    """
    @is_admin_or_has_valid_OIDC_id
    def post(self, request, *args, **kwargs):
        print(request.user)
        form = CustomerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone_number = form.cleaned_data['phone_number']
            try:
                customer = Customer(name=name, phone_number=phone_number)
                customer.save()
            except Exception as e:
                response = JsonResponse({ "message": e.args[0] }, status=404)
                return response
            return JsonResponse({"message": 'customer added successfully'})
        else:
            return render(request, 'create_customer.html', {'form': form})
        return render(request, 'create_customer.html', {'form': form})

    @is_admin_or_has_valid_OIDC_id
    def get(self, request, *args, **kwargs):
        print(request.user)
        form = CustomerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone_number = form.cleaned_data['phone_number']
            try:
                customer = Customer(name=name, phone_number=phone_number)
                customer.save()
            except Exception as e:
                response = JsonResponse({ "message": e.args[0] }, status=404)
                return response
            return JsonResponse({"message": 'customer added successfully'})
        else:
            return render(request, 'create_customer.html', {'form': form})
        return render(request, 'create_customer.html', {'form': form})

class Create_order(FormView):
    @is_admin_or_has_valid_OIDC_id
    def post(self, request, *args, **kwargs):
        print(request.user)
        form = OrderForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            item = form.cleaned_data['item']
            customer = form.cleaned_data['customer_name']
            try:
                customer_ref = Customer.objects.get(name=customer)
                order = Order.objects.create(amount=amount, item=item, customer=customer_ref)
                order.save()
                recepients = [customer_ref.phone_number]
                send_sms_notification.delay(recepients, item)
            except Exception as e:
                print(e)
                response = JsonResponse({ "message": e.args[0] }, status=404)
                return response
            return JsonResponse({"message": 'order added successfully'})
        else:
            form = OrderForm()
        return render(request, 'create_order.html', {'form': form})



    @is_admin_or_has_valid_OIDC_id
    def get(self, request, *args, **kwargs):
        print(request.user)
        form = OrderForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            item = form.cleaned_data['item']
            customer = form.cleaned_data['customer_name']
            try:
                customer_ref = Customer.objects.get(name=customer)
                order = Order.objects.create(amount=amount, item=item, customer=customer_ref)
                order.save()
                recepients = [customer_ref.phone_number]
                send_sms_notification.delay(recepients, item)
            except Exception as e:
                response = JsonResponse({ "message": e.args[0] }, status=404)
                return response
            return JsonResponse({"message": 'order added successfully'})
        else:
            form = OrderForm()
        return render(request, 'create_order.html', {'form': form})
