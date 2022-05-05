import requests
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError

from .forms import RegisterForm, SearchVendorCodeForm


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


def entervendorcode(request):
    if request.method == 'GET':
        return render(request, 'wb_tracker_app/entervendorcode.html', {'form': SearchVendorCodeForm()})
    # 46617793
    else:
        try:
            dates_list = []
            prices_list = []
            vendor_code = ''
            date_from = ''
            date_to = ''
            form = SearchVendorCodeForm(request.POST)
            if form.is_valid():
                vendor_code = form.cleaned_data.get('vendor_code')
                date_from = form.cleaned_data.get('date_from')
                date_to = form.cleaned_data.get('date_to')
            response = requests.get('https://wbx-content-v2.wbstatic.net/price-history/' + str(vendor_code) + '.json')
            if response.status_code == 200:
                json_file = response.json()

                for item in json_file:

                    unix_time = item.get('dt')
                    price = (item.get('price')).get('RUB')

                    dates_list.append((datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d')))
                    prices_list.append(str(price / 100))
                info = dict(zip(dates_list, prices_list))
                displayed_date = []
                displayed_price = []
                for key in info.keys():
                    if (datetime.strptime(key, '%Y-%m-%d') >= datetime.strptime(date_from, '%Y-%m-%d')) and (datetime.strptime(key, '%Y-%m-%d') <= datetime.strptime(date_to, '%Y-%m-%d')):
                        displayed_date.append(key)
                        displayed_price.append(info.get(key))
                displayed_info = dict(zip(displayed_date, displayed_price))

                return render(
                    request,
                    'wb_tracker_app/response.html',
                    {'get_price': displayed_info})
            else:
                return render(request, 'wb_tracker_app/response.html', {'error': 'Invalid vendor code'})
        except ValueError:
            return render(
                request,
                'wb_tracker_app/entervendorcode.html',
                {'form': SearchVendorCodeForm()}
            )

