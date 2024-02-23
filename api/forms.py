from django import forms
from .models import Customer, Order


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter customer name'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'should start with country code'}),
        }


class OrderForm(forms.Form):
    customer_name = forms.CharField(max_length=60)
    item = forms.CharField(max_length=60)
    amount = forms.IntegerField(min_value=1)
