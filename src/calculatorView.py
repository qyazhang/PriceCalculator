import src.priceCalculator.mercariCalculator as mercariCalculator
import src.priceCalculator.otamartCalculator as otamartCalculator

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from .priceCalculator.itemModelSerializer import ItemModelSerializer


@api_view(['GET'])
def get_item(request):
    print("hello: " + str(request))
    url = request.query_params.get('url', None)
    if url is not None:
        if "mercari.com" in url:
            item = mercariCalculator.calculateMercariPrice(request, url)
            item_serizalizer = ItemModelSerializer(item)
            return JsonResponse(item_serizalizer.data, status=status.HTTP_200_OK, content_type="application/json")
        if "otamart.com" in url:
            item = otamartCalculator.calculateOtamartPrice(request, url)
            item_serizalizer = ItemModelSerializer(item)
            return JsonResponse(item_serizalizer.data, status=status.HTTP_200_OK, content_type="application/json")
        else:
            return JsonResponse({'status': 'details'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return JsonResponse({'status': 'details'}, status=status.HTTP_404_NOT_FOUND)
