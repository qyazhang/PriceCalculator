from requests_html import HTMLSession
from django.shortcuts import render, redirect
import requests
import re
import time
import validators
import src.utils.calculatorUtils as calculatorUtils

def calculateOtamartPrice(request, url, context):
    if not url.startswith("https://otamart.com/items/"):
    # and not url.startswith("https://item.mercari.com/jp/") :
        print("invalid otamart item page: " + url)
        return redirect('/index', context)

    if not (validators.url(url)):
        print("input is not valid url: " + url)
        return redirect('/index', context)

    session = HTMLSession()
    page = session.get(url)

    item_name, img_url = parseOtamartMetadata(page)
    if (item_name is None or img_url is None):
        print("failed to parse webpage, maybe url is wrong")
        return redirect('/index', context)
    else:
        print("Get item: " + item_name.text)

    formatted_price, shipping_fee_tag, sold_out_flag = parseOtamartFormattedPrice(page)
    if (item_name is None or img_url is None or formatted_price is None or shipping_fee_tag is None):
        print("failed to parse webpage")
        return redirect('/index', context)

    formatted_final_price_cny = calculatorUtils.calculateFinalCNYPrice(formatted_price)

    context['result'] = f"¥{formatted_final_price_cny}"
    context['item_name'] = item_name.text
    context['img_url'] = img_url.attrs['src']
    context['shipping_fee_tag'] = shipping_fee_tag
    context['sold_out_flag'] = "是" if sold_out_flag else "否"
    return render(request, 'search.html', context)


def parseOtamartFormattedPrice(page):
    price = page.html.xpath(
        "//span[@class='price']", first=True).text
    item_type_elements = page.html.xpath(
        "//div[@class='trade-info']/div/p")
    contain_delivery_fee_flag = False
    for item in item_type_elements:
        if (item.text == "送料込み"):
            contain_delivery_fee_flag = True

    if (contain_delivery_fee_flag):
        shipping_fee_tag = "含岛内运费"
    else:
        shipping_fee_tag = "不含岛内运费"

    sold_out_element = page.html.xpath(
        "//div[@class='sold-out-message']/p", first=True)
    sold_out_flag = False

    if (sold_out_element is not None):
        if ("売り切れました" in sold_out_element.text):
            sold_out_flag = True

    formatted_price = re.sub('\D', '', price)

    return int(formatted_price), shipping_fee_tag, sold_out_flag

def parseOtamartMetadata(page):
    item_name = page.html.xpath("//section[@class='item-name-price']/div/h1", first=True)
    img_url = page.html.xpath(
        "//img[@id='item-picture']", first=True)

    return item_name, img_url