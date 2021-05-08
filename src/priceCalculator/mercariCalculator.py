from requests_html import HTMLSession
from django.shortcuts import render, redirect
import requests
import re
import time
import validators
import src.utils.calculatorUtils as calculatorUtils

def calculateMercariPrice(url, context):
    if not url.startswith("https://www.mercari.com/jp/items/") and not url.startswith("https://item.mercari.com/jp/") :
        print("invalid mercari item page: " + url)
        return redirect('/index', context)

    if not (validators.url(url)):
        print("input is not valid url: " + url)
        return redirect('/index', context)

    session = HTMLSession()
    page = session.get(url)

    item_name, img_url = parseMercariMetadata(page)
    if (item_name is None or img_url is None):
        print("failed to parse webpage, maybe url is wrong")
        return redirect('/index', context)
    else:
        print("Get item: " + item_name.text)

    formatted_price, shipping_fee_tag = parseMercariFormattedPrice(page)
    if (item_name is None or img_url is None or formatted_price is None or shipping_fee_tag is None):
        print("failed to parse webpage")
        return redirect('/index', context)

    pay_rate = calculatorUtils.getCurrencyRate()

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
    context['item_name'] = item_name.text
    context['img_url'] = img_url.attrs['data-src']
    context['shipping_fee_tag'] = shipping_fee_tag
    return render(request, 'search.html', context)


def parseMercariFormattedPrice(page):
    price = page.html.xpath(
        "//span[@class='item-price bold']", first=True).text
    item_type = page.html.xpath(
        "//span[@class='item-shipping-fee']", first=True).text

    if (item_type == "送料込み"):
        shipping_fee_tag = "含岛内运费"
    else:
        shipping_fee_tag = "不含岛内运费"

    formatted_price = re.sub('\D', '', price)
    return int(formatted_price), shipping_fee_tag

def parseMercariMetadata(page):
    item_name = page.html.xpath("//h1[@class='item-name']", first=True)
    img_url = page.html.xpath(
        "//span[@class='luminous-gallery']", first=True)

    return item_name, img_url