import os
from datetime import datetime
import xml.etree.ElementTree as et

import requests


def reqeust_data_from_cb():
    current_date = datetime.now().strftime("%d/%m/%Y")
    request_url = "https://www.cbr.ru/scripts/XML_daily.asp?date_req={:s}".format(current_date)
    result = requests.get(request_url)

    if result.status_code != 200:
        raise Exception(
            "Not expected status code {:d}".format(result.status_code))

    return result.text


def parsing_xml_currency(data):
    cb_data = reqeust_data_from_cb()
    root = et.XML(cb_data)

    currencies = {}

    for v in root.findall('./'):
        code = v.find("./CharCode").text
        nominal = v.find("./Nominal").text
        name = v.find("./Name").text
        value = v.find("./Value").text

        currencies[code] = {
            'name': name,
            'nominal': int(nominal),
            'value': float(value.replace(",", "."))
        }

    return currencies


def input_amount():
    while True:
        amount = input("Введите сумму которую хотите поменять:")

        if not amount.isnumeric():
            print("Это должно быть число")
        else:
            break

    return float(amount)


def input_currency(currency_list):
    while True:
        currency = input("Введите валюту:")

        if currency not in prepared_data:
            print("Такую валюту мы не поддреживаем")
        else:
            break

    return currency


if __name__ == '__main__':
    try:
        request_result = reqeust_data_from_cb()
    except Exception as e:
        print(e)
        exit(1)

    prepared_data = parsing_xml_currency(request_result)
    amount = input_amount()
    currency = input_currency(prepared_data)

    exchange_data = prepared_data[currency]

    total = amount / (exchange_data['value'] / exchange_data['nominal'])

    print("Вы получите {:.2f} {:s}".format( total, exchange_data['name']))
