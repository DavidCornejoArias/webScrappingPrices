# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 11:42:18 2020

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

#list
listOfProductName = []
listOfPrices = []
listOfLinksToProduct = []
listOfOldPrices = []
listOfFarmacias = []


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

URL = "https://www.cruzverde.com.co/agosto-triple/medicamentos/"
headers = random.choice(headers_list)
r = requests.Session()
r.headers = headers
page = r.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
pagination = soup.find('div',class_='pagination pagination-footer justify-content-center align-items-center flex-md-wrap')
pages = pagination.findAll('button')
lastPageNumber = int(pages[-1].text)

len(products)
for pageViewNumber in range(lastPageNumber):
    urlView = 'https://www.cruzverde.com.co/agosto-triple/medicamentos/?start='+str(pageViewNumber*12)+'&sz=12&maxsize=NaN'
    headers = random.choice(headers_list)
    s = requests.Session()
    s.headers = headers
    secondsToWait = random.randint(20,30)
    time.sleep(secondsToWait)
    viewPage = s.get(urlView)
    viewSoup = BeautifulSoup(viewPage.content, 'html.parser')
    productConatiner = viewSoup.find('div',class_='row products-grid')
    products = productConatiner.findAll('div',class_='product product-wrapper')
    for product in products:
        producNameNotClean = product.find('div',class_='pdp-link').find('a').text
        productNameCleaner = re.compile(r'  +|\n')
        productNameClean = productNameCleaner.sub('',producNameNotClean)
        precios = product.find('div',class_='price').findAll('span',class_='value')
        if len(precios)==2:
            precio = precios[0].attrs['content']
            precioViejo = precios[1].attrs['content']
        elif len(precios)==1:
            precio = precios[0].attrs['content']
            precioViejo = ""
        farmaciaNotClean = product.find('a',class_='product-brand text-uppercase m-0').text
        farmaciaClean = productNameCleaner.sub('',farmaciaNotClean)
        shortProductUrl = product.find('a',class_='w-100 text-center no-outline').attrs['href']
        productUrl ='https://www.cruzverde.com.co/' +shortProductUrl
        listOfProductName.append(productNameClean)
        listOfPrices.append(precio)
        listOfLinksToProduct.append(productUrl)
        listOfOldPrices.append(precioViejo)
        listOfFarmacias.append(farmaciaClean)    
df = pd.DataFrame()
len(listOfProductName)
len(listOfPrices)
df['productName']=listOfProductName
df['prices']=listOfPrices
df['LinksToProducto']=listOfLinksToProduct
df['moneda']= ['Peso colombiano' for i in range(len(listOfPrices))]
df['Farmacia']= ['Farmacia Cruz Verde' for i in range(len(listOfPrices))]
df['oldPrices']= listOfOldPrices
df['Country']= ['Colombia' for i in range(len(listOfPrices))]
df['Farmacias del Producto']= listOfFarmacias
df.to_csv(r'farmaciaCruzVerde.csv',encoding='utf-8')

    







