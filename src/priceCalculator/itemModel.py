from django.db import models


class ItemModel(models.Model):
    @property
    def price_jpy(self):
        return self._price_jpy

    @price_jpy.setter
    def price_jpy(self, value):
        self._price_jpy = value

    @property
    def price_cny(self):
        return self._price_cny

    @price_cny.setter
    def price_cny(self, value):
        self._price_cny = value

    @property
    def item_name(self):
        return self._item_name

    @item_name.setter
    def item_name(self, value):
        self._item_name = value

    @property
    def img_url(self):
        return self._img_url

    @img_url.setter
    def img_url(self, value):
        self._img_url = value

    @property
    def shipping_fee_tag(self):
        return self._shipping_fee_tag

    @shipping_fee_tag.setter
    def shipping_fee_tag(self, value):
        self._shipping_fee_tag = value

    @property
    def sold_out_flag(self):
        return self._sold_out_flag

    @sold_out_flag.setter
    def sold_out_flag(self, value):
        self._sold_out_flag = value
