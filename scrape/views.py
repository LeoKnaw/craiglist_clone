from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from .models import Search
# Create your views here.

BASE_URL = 'https://accra.craigslist.org/search/?query={}'
BASE_IMG = 'https://images.craigslist.org/{}_300x300.jpg'

def home(request):
    return render(request, "base.html")


def newSearch(request):
    search = request.POST.get('search')
    Search.objects.create(search=search)
    url = BASE_URL.format(quote_plus(search))
    res = requests.get(url)
    soup = BeautifulSoup(res.text, features='html.parser')

    scrape = soup.find_all('li', {'class':'result-row'})


    finalPost = []


    for post in scrape:
        scrapeTitle = post.find(class_='result-title').text
        scrapeURL = post.find('a').get('href')
        if post.find(class_='result-price'):
            scrapePrice = post.find(class_='result-price').text
        else:
            scrapePrice = 'N/A'

        if post.find(class_='result-image gallery') is not None:
            scrapeId = post.find(class_='result-image gallery').get('data-ids').split(',')[0].split(':')[1]
            scrapeImg = BASE_IMG.format(scrapeId)
        elif post.find(class_='result-image gallery') is None:
            scrapeImg = 'https://accra.craigslist.org/images/peace.jpg'
        finalPost.append((scrapeTitle, scrapeURL, scrapePrice, scrapeImg))




    #print(url)
    frontend = {
        'search':search,
        'finalPost': finalPost,
                }
    return render(request, "scrape/newSearch.html", frontend)