from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
# Create your views here.

def home(request):
    return render(request, "base.html")


def newSearch(request):
    search = request.POST.get('search')
   # print(search)
    frontend = {
        'search':search,
                }
    return render(request, "scrape/newSearch.html", frontend)