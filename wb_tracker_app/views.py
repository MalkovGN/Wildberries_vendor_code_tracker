import requests
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError

from .forms import RegisterForm, SearchVendorCodeForm, AddingCardForm
from .models import ProductCard


def home(request):
    """
    Home page
    """
    return render(request, 'wb_tracker_app/home.html')


def signupuser(request):
    """
    User registration page,
    with a field for email
    """
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


def loginuser(request):
    """
    Authentication function
    """
    if request.method == 'GET':
        return render(request, 'wb_tracker_app/loginuser.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return(
                request,
                'wb_tracker_app/loginuser.html',
                {'form': AuthenticationForm, 'error': 'Username or password didnt match'}
            )
        else:
            login(request, user)
            return redirect('currentuser')


def logoutuser(request):
    """
    Logout function
    """
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def currentuser(request):
    """
    The first page after
    registration/authentication
    """
    codes = ProductCard.objects.filter(user=request.user)
    return render(request, 'wb_tracker_app/currentuser.html', {'codes': codes})


def addingcard(request):
    """
    The page of adding
    a new card
    """
    if request.method == 'GET':
        return render(request, 'wb_tracker_app/addcard.html', {'adding_form': AddingCardForm})
    else:
        form = AddingCardForm(request.POST)
        new_code = form.save(commit=False)
        new_code.user = request.user
        new_code.save()
        return redirect('currentuser')


def viewcard(request, card_pk):
    """
    The page for viewing the
    added card and viewing the
    price history
    """
    card = get_object_or_404(ProductCard, pk=card_pk, user=request.user)
    if request.method == 'GET':
        form = SearchVendorCodeForm(instance=card)
        return render(request, 'wb_tracker_app/viewcard.html', {'form': form})
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
                    if (datetime.strptime(key, '%Y-%m-%d') >= datetime.strptime(date_from, '%Y-%m-%d')) and (
                            datetime.strptime(key, '%Y-%m-%d') <= datetime.strptime(date_to, '%Y-%m-%d')):
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
