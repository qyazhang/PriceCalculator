from requests_html import HTMLSession
from django.shortcuts import render, redirect
import requests
import re
import time
import json


def calculatePrice(request):
    context = {}
    if (request.GET['url'] == None or request.GET['url'] == ''):
        return redirect('/index', context)
        
    url = request.GET['url']
    item_name, img_url, formatted_price, shipping_fee_tag = parseMercariFormattedPrice(url)

    pay_rate = getCurrencyRate()

    final_price_jpy = formatted_price
    if (formatted_price < 900):
        final_price_jpy += 100
    elif(formatted_price >= 900 and formatted_price < 1000):
        final_price_jpy = 1000
    else:
        final_price_jpy = final_price_jpy

    final_price_cny = final_price_jpy / 100 * pay_rate
    formatted_final_price_cny = int(final_price_cny + 1)

    context['result'] = f"¥{formatted_final_price_cny}"
    context['item_name'] = item_name
    context['img_url'] = img_url
    context['shipping_fee_tag'] = shipping_fee_tag
    return render(request, 'search.html', context)


def parseMercariFormattedPrice(mercariUrl):
    session = HTMLSession()
    page = session.get(mercariUrl)
    price = page.html.xpath(
        "//span[@class='item-price bold']", first=True).text
    item_type = page.html.xpath(
        "//span[@class='item-shipping-fee']", first=True).text
    item_name = page.html.xpath("//h1[@class='item-name']", first=True).text
    img_url = page.html.xpath(
        "//span[@class='luminous-gallery']", first=True).attrs['data-src']

    if (item_type == "送料込み"):
        shipping_fee_tag = "含岛内运费"
    else:
        shipping_fee_tag = "不含岛内运费"

    formatted_price = re.sub('\D', '', price)
    return item_name, img_url, int(formatted_price), shipping_fee_tag


def getCurrencyRate():
    with open("./resource/currency.json", "r") as currency_file:
        currency_text = currency_file.read()
        currency_data = json.loads(currency_text)

    with open("./resource/config.json", "r") as config_file:
        config_text = config_file.read()
        config_data = json.loads(config_text)
        key = config_data["fixer"]["key"]

    last_modify_time = currency_data["lastModifyTime"]
    current_time = time.time()
    if (float(current_time) - float(last_modify_time) > 3600):
        currency_data["lastModifyTime"] = current_time

        currency_response = requests.get(
            'http://data.fixer.io/api/latest?access_key=' + key + '&format=1')
        currency_res = currency_response.json()
        print(currency_res)
        if (currency_res["success"] == False):
            print("error to update currency")
        else:
            currency_data["data"] = currency_res
            with open("./resource/currency.json", "w") as currency_file:
                json.dump(currency_data, currency_file)

    jpy_currency = currency_data["data"]["rates"]["JPY"]
    cny_currency = currency_data["data"]["rates"]["CNY"]
    original_rate = 100 / (jpy_currency / cny_currency)
    print(original_rate)
    pay_rate = round(original_rate + 0.8, 1)
    print(pay_rate)
    return pay_rate
