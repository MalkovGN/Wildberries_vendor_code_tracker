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
            return (
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
    cards = ProductCard.objects.filter(user=request.user)
    return render(request, 'wb_tracker_app/currentuser.html', {'cards': cards})


def addingcard(request):
    """
    The page of adding
    a new card
    """
    if request.method == 'GET':
        return render(request, 'wb_tracker_app/addcard.html', {'adding_form': AddingCardForm})
    else:
        form = AddingCardForm(request.POST)
        if form.is_valid():
            vendor_code = form.cleaned_data.get('vendor_code')
        response = requests.get('https://wbx-content-v2.wbstatic.net/price-history/' + str(vendor_code) + '.json')
        name_brand_response = requests.get('https://wbx-content-v2.wbstatic.net/ru/' + str(vendor_code) + '.json')
        prices_response = requests.get(
            'https://wbxcatalog-ru.wildberries.ru/nm-2-card/catalog?spp=13&regions=68,64,83,4,38,80,33,70,82,86,75,30,69,48,22,1,66,31,40,71&stores=117673,122258,122259,125238,125239,125240,6159,507,3158,117501,120602,6158,120762,121709,124731,159402,2737,130744,117986,1733,686,132043&pricemarginCoeff=1.0&reg=1&appType=1&emp=0&locale=ru&lang=ru&curr=rub&couponsGeo=12,3,18,15,21&dest=-1029256,-102269,-446092,-445279&nm=' + str(
                vendor_code) + ';')
        saler_name_response = requests.get(
            'https://wbx-content-v2.wbstatic.net/sellers/' + str(vendor_code) + '.json')
        name_brand_json = name_brand_response.json()
        prices_json = prices_response.json()
        saler_name_json = saler_name_response.json()

        data_name = name_brand_json.get('imt_name')
        brand_data = name_brand_json.get('selling').get('brand_name')
        full_price_data = int(prices_json.get('data').get('products')[0].get('priceU')) / 100
        sale_price_data = int(prices_json.get('data').get('products')[0].get('salePriceU')) / 100
        saler_name_data = saler_name_json.get('trademark')
        if saler_name_data == '':
            saler_name_data = 'Supplier not specified'

        if response.status_code != 200:
            return render(
                request,
                'wb_tracker_app/addcard.html',
                {'adding_form': AddingCardForm, 'error': 'Invalid vendor code'}
            )
        else:
            card = ProductCard(
                vendor_code=vendor_code,
                product_name=data_name,
                price=full_price_data,
                sale_price=sale_price_data,
                brand=brand_data,
                supplier=saler_name_data,
            )
            card.user = request.user
            card.save()

            return redirect('currentuser')


def viewcard(request, card_pk):
    """
    The page for viewing the
    added card and viewing the
    price history
    """
    cards = get_object_or_404(ProductCard, pk=card_pk, user=request.user)
    if request.method == 'GET':
        form = SearchVendorCodeForm(instance=cards)
        return render(request, 'wb_tracker_app/viewcard.html', {'cards': cards, 'form': form})
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
            list_info = ''
            for date, price in displayed_info.items():
                list_info += f'On {date} price was {price}\n'

            return render(
                request,
                'wb_tracker_app/response.html',
                {'get_price': list_info}
            )
        except ValueError:
            return render(
                request,
                'wb_tracker_app/entervendorcode.html',
                {'form': SearchVendorCodeForm()}
            )


def deletecard(request, card_pk):
    card = get_object_or_404(ProductCard, pk=card_pk, user=request.user)
    if request.method == 'POST':
        card.delete()
        return redirect('currentuser')
