from django.shortcuts import redirect
import src.priceCalculator.mercariCalculator as mercariCalculator
import src.priceCalculator.otamartCalculator as otamartCalculator

def calculatePrice(request):
    context = {}
    if (request.GET['url'] == None or request.GET['url'] == ''):
        return redirect('/index', context)
        
    url = request.GET['url']
    print("ready to parse url: " + url)
    
    if "mercari.com" in url:
        return mercariCalculator.calculateMercariPrice(request, url, context)
    if "otamart.com" in url:
        return otamartCalculator.calculateOtamartPrice(request, url, context)