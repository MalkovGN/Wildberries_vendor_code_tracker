from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError

from .forms import RegisterForm


def home(request):
    return render(request, 'wb_tracker_app/home.html')


def signupuser(request):
    data = {}
    if request.method == 'GET':
        form = RegisterForm()
        data['form'] = form
        return render(request, 'wb_tracker_app/signupuser.html', data)
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('currentuser')
            except IntegrityError:
                return render(
                    request,
                    'wb_tracker_app/signupuser.html',
                    data
                )
        else:
            return render(
                request,
                'wb_tracker_app/signupuser.html',
                data
            )


def currentuser(request):
    return render(request, 'wb_tracker_app/currentuser.html')
