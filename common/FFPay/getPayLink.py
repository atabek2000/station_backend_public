import json
import xml.etree.ElementTree as ET
import environ
import hashlib

import requests

env = environ.Env()

def getPayLink(order):
    link = 'https://test-api.freedompay.money/init_payment.php' # test
    form_data = form_data_sig = {
        # сумма заказа
        'pg_amount': str(float(order.amount)),

        # описание
        'pg_description': order.comment,

        # тдентификатор мерчанта
        'pg_merchant_id': env.str('FFPAY_MERCH_ID'),

        # номер заказа на базе мерчанта
        'pg_order_id': str(order.order_number),

        # соль для шифрования
        'pg_salt': 'station_shop',

        # курс валюты на котром оплата принимается
        'pg_currency': 'KZT',

        # ссылка в котором отправляется результат оплаты
        'pg_result_url': 'http://209.38.248.1/api/v1/pay/result/',

        # ссылка для перенеправления клиента при удачной оплате
        'pg_success_url': 'http://209.38.248.1:3000/address?pay=success',

        # ссылка для перенеправления клиента при не удачной оплате
        'pg_failure_url': 'http://209.38.248.1:3000/address?pay=failure',

        # для различия тестовоый запрос или боевой
        'pg_testing_mode': 1
    }

    # сортирум словар по альфавиту
    form_data = dict(sorted(form_data.items()))

    # адрес куда отправляется запрос
    sig_str = 'init_payment.php'

    # собираем на строку элементы солваря
    for key, value in form_data.items():
        sig_str += ';'+str(value)

    # добавим ключ мерчанта
    sig_str += f';{env.str("FFPAY_KEY")}'


    # генерируем подпись
    form_data['pg_sig'] = hashlib.md5(sig_str.encode()).hexdigest()

    # отправляем запрос
    response = requests.post(link, data=json.dumps(form_data), headers={'Content-Type': 'application/json'})

    # если ошибка в XML
    if len(ET.fromstring(response.content).findall('pg_error_description')) > 0:
        for err in ET.fromstring(response.content).findall('pg_error_description'):
            raise ConnectionError(str(err.text))
    else:
        return ET.fromstring(response.content)[2].text

