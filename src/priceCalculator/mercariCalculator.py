import re
import time
import validators
import src.utils.calculatorUtils as calculatorUtils
from .itemModel import ItemModel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def calculateMercariPrice(request, url):
    model = ItemModel()
    if not url.startswith("https://www.mercari.com/jp/items/") and not url.startswith("https://item.mercari.com/jp/") and not url.startswith("https://jp.mercari.com/item/"):
        print("invalid mercari item page: " + url)
        return model

    if not (validators.url(url)):
        print("input is not valid url: " + url)
        return model

    driver = webdriver.Remote("http://0.0.0.0:4444/wd/hub", DesiredCapabilities.CHROME)
    driver.get(url)
    time.sleep(1)

    item_name, img_url = parseMercariMetadata(driver)
    if (item_name is None or img_url is None):
        print("failed to parse webpage, maybe url is wrong")
        return model
    else:
        print("Get item: " + item_name)

    formatted_price_jpy, shipping_fee_tag, sold_out_flag = parseMercariFormattedPrice(driver)
    if (item_name is None or img_url is None or formatted_price_jpy is None or shipping_fee_tag is None):
        print("failed to parse webpage")
        return model

    formatted_final_price_cny = calculatorUtils.calculateFinalCNYPrice(formatted_price_jpy)

    model.price_jpy = f"¥{formatted_price_jpy}"
    model.price_cny = f"¥{formatted_final_price_cny}"
    model.item_name = item_name
    model.img_url = img_url
    model.shipping_fee_tag = shipping_fee_tag
    model.sold_out_flag = sold_out_flag
    return model

def parseMercariFormattedPrice(driver):
    price = driver.find_element_by_xpath(
        "//mer-price[@data-testid='price']").text
    print("price:" + price)
    item_type = driver.find_element_by_xpath(
        "//mer-text/span").get_attribute("innerHTML")
    print("type: " + item_type)
    sold_out_element = driver.find_element_by_xpath(
        "//mer-button[@data-testid='checkout-button']/button").get_attribute("innerHTML")
    print("sold status:" + sold_out_element)

    if ("送料込み" in item_type):
        shipping_fee_tag = True
    else:
        shipping_fee_tag = False

    formatted_price = re.sub('\D', '', price)

    sold_out_flag = False
    if (sold_out_element is not None):
        if (sold_out_element == "売り切れました"):
            sold_out_flag = True

    return int(formatted_price), shipping_fee_tag, sold_out_flag

def parseMercariMetadata(driver):
    item_name = driver.find_element_by_xpath("//mer-heading[@class='mer-spacing-b-2']").text
    # print("item_name: " + item_name)
    img_url = driver.find_element_by_xpath(
        "//mer-item-thumbnail[@data-testid='image-0']").get_attribute('src')
    # print("img_url:" + img_url)

    return item_name, img_url
