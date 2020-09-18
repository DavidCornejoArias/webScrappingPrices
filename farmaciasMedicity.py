# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 09:33:33 2020

@author: david
"""

import os
import random
import pandas as pd
import math
import time
import requests
import numpy
from bs4 import BeautifulSoup
import re
from lxml.html import fromstring
from collections import OrderedDict

n = 47
#list
listOfProductName = []
listOfPrices = []
listOfLinksToProduct = []
listOfOldPrices = []


headers_list = [
    # Firefox 77 Mac
     {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    },
    # Firefox 77 Windows
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    },
    # Chrome 83 Mac
    {
        "Connection": "keep-alive",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    },
    # Chrome 83 Windows 
    {
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"
    }
]

# Create ordered dict from Headers above
ordered_headers_list = []
for headers in headers_list:
    h = OrderedDict()
    for header,value in headers.items():
        h[header]=value
    ordered_headers_list.append(h)

URL = "https://www.farmaciasmedicity.com/shop/category/medicinas-1328/page/47"
headers = random.choice(headers_list)
r = requests.Session()
r.headers = headers
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
for pageNumber in range(1,n+1):
    urlView = "https://www.farmaciasmedicity.com/shop/category/medicinas-1328/page/"+str(pageNumber)
    headers = random.choice(headers_list)
    s = requests.Session()
    s.headers = headers
    secondsToWait = random.randint(20,30)
    time.sleep(secondsToWait)
    viewPage = s.get(urlView)
    viewSoup = BeautifulSoup(viewPage.content, 'html.parser')
    products = viewSoup.find('body').find('div',id='products_grid').findAll('div',id='grid_list')
    for product in products:
        len(products)
        productName = product.find('h5').find('a').attrs['content']
        prices = product.find('div',class_='product-price').findAll('span',class_='oe_currency_value')
        if len(prices)==2:
            precioViejo = prices[0].text
            precio = prices[1].text
        elif len(prices)==1:
            precio = prices[0].text
            precioViejo = ""
        shortLink = product.find('div',class_='pro-img').find('a').attrs['href']
        farmaciaLink = 'https://www.farmaciasmedicity.com'
        longLink = farmaciaLink + shortLink
        listOfProductName.append(productName)
        listOfPrices.append(precio)
        listOfLinksToProduct.append(longLink)
        listOfOldPrices.append(precioViejo)
# composition
df = pd.DataFrame()
len(listOfProductName)
len(listOfPrices)
df['productName']=listOfProductName
df['prices']=listOfPrices
df['LinksToProducto']=listOfLinksToProduct
df['moneda']= ['Dólar' for i in range(len(listOfPrices))]
df['Farmacia']= ['Farmacia Medicit' for i in range(len(listOfPrices))]
df['oldPrices']= listOfOldPrices
df['Country']= ['Ecuador' for i in range(len(listOfPrices))]
df.to_csv(r'C:\Users\david\Documents\DNM\webscrapping\farmaciaMedicit.csv',encoding='utf-8')

 



