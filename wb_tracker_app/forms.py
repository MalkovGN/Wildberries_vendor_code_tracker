from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import ProductCard


class RegisterForm(UserCreationForm):
    """
    Registration form
    with email field
    """
    email = forms.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class SearchVendorCodeForm(ModelForm):
    """
    Form for input
    a vendor code
    and time interval
    """
    class Meta:
        model = ProductCard
        fields = ['product_name', 'vendor_code', 'date_from', 'date_to']


class AddingCardForm(ModelForm):
    """
    Form for adding and
    save vendor code
    """
    class Meta:
        model = ProductCard
        fields = ['vendor_code', 'date_from', 'date_to']
