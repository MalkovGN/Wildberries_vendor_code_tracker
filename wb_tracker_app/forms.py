from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import VendorCode, CodeResponse


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class SearchVendorCodeForm(ModelForm):
    class Meta:
        model = VendorCode
        fields = ['vendor_code', 'date_from', 'date_to']

#
# class CodeResponseForm(forms.Form):
#     vendor_code = forms.IntegerField()
