from rest_framework import serializers 
from .itemModel import ItemModel


class ItemModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemModel
        fields = (
                  'price_jpy',
                  'price_cny',
                  'item_name',
                  'img_url',
                  'shipping_fee_tag',
                  'sold_out_flag')