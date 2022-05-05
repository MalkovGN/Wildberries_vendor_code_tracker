import requests
from datetime import datetime



# def create_url(vendor_code):
#     request_url = 'https://www.wildberries.ru/catalog/' + str(vendor_code) + '/detail.aspx?targetUrl=GP'
#     return request_url


# response = requests.get(create_url(12345678))
# print(response.status_code)

# JSON с историей цены
# https://wbx-content-v2.wbstatic.net/price-history/26424401.json


def get_info(vendor_code):
    response = requests.get('https://wbx-content-v2.wbstatic.net/price-history/' + str(vendor_code) + '.json')
    json_file = response.json()
    dates_list = []
    prices_list = []
    info = {}
    for item in json_file:

        unix_time = item.get('dt')
        price = (item.get('price')).get('RUB')

        dates_list.append((datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d')))
        prices_list.append(str(price / 100))

    info = dict(zip(dates_list, prices_list))
    print(info)
    for key in info.keys():
        print(key, end=' ')
        if (datetime.strptime(key, '%Y-%m-%d') >= datetime.strptime('2021-11-21', '%Y-%m-%d')) and (
                datetime.strptime(key, '%Y-%m-%d') <= datetime.strptime('2021-12-05', '%Y-%m-%d')):
            print('Yeap')
    # # #
    # for d, p in info.items():
    #     d1 = datetime.strptime(d, '%Y-%m-%d').date()
    #     print(type(d1), p)

get_info(26414401)

# print(datetime.strptime('2021-12-05', '%Y-%m-%d'))