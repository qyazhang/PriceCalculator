from requests_html import HTMLSession
from django.shortcuts import render, redirect
import requests
import re
import time
import validators
import src.utils.calculatorUtils as calculatorUtils

def calculateMercariPrice(request, url, context):
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

    formatted_price_jpy, shipping_fee_tag, sold_out_flag = parseMercariFormattedPrice(page)
    if (item_name is None or img_url is None or formatted_price_jpy is None or shipping_fee_tag is None):
        print("failed to parse webpage")
        return redirect('/index', context)

    formatted_final_price_cny = calculatorUtils.calculateFinalCNYPrice(formatted_price_jpy)

    context['price_jpy'] = f"¥{formatted_price_jpy}"
    context['price_cny'] = f"¥{formatted_final_price_cny}"
    context['item_name'] = item_name.text
    context['img_url'] = img_url.attrs['data-src']
    context['shipping_fee_tag'] = shipping_fee_tag
    context['sold_out_flag'] = "是" if sold_out_flag else "否"
    return render(request, 'search.html', context)


def parseMercariFormattedPrice(page):
    price = page.html.xpath(
        "//span[@class='item-price bold']", first=True).text
    item_type = page.html.xpath(
        "//span[@class='item-shipping-fee']", first=True).text
    sold_out_element = page.html.xpath(
        "//div[@class='item-buy-btn disabled']", first=True)

    if (item_type == "送料込み"):
        shipping_fee_tag = "含岛内运费"
    else:
        shipping_fee_tag = "不含岛内运费"

    formatted_price = re.sub('\D', '', price)

    sold_out_flag = False
    if (sold_out_element is not None):
        if (sold_out_element.text == "売り切れました"):
            sold_out_flag = True

    return int(formatted_price), shipping_fee_tag, sold_out_flag

def parseMercariMetadata(page):
    item_name = page.html.xpath("//h1[@class='item-name']", first=True)
    img_url = page.html.xpath(
        "//span[@class='luminous-gallery']", first=True)

    return item_name, img_url