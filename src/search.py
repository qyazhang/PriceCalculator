from requests_html import HTMLSession
from django.shortcuts import redirect, render
import requests
import re
import time
import json

def get_html(request):
    context = {}
    return render(None, 'search.html', context)

# def searchToCalculate(request):
#     context = {}
#     print('here: ' + request.GET['url'])
#     if (request.GET['url'] == None or request.GET['url'] == ''):
#         return redirect('/index', context)
#     return render(request, 'search.html', context)
