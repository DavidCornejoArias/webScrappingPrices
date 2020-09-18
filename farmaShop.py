# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 15:53:36 2020

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
# not able to locate the last page automatically so I will do it manually
n = 253
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


pagesList = ['https://tienda.farmashop.com.uy/salud/alivio-del-dolor.html','https://tienda.farmashop.com.uy/salud/antigripales-y-respiratorios.html',
             'https://tienda.farmashop.com.uy/salud/anticonceptivos.html','https://tienda.farmashop.com.uy/salud/cardiovascular.html',
             'https://tienda.farmashop.com.uy/salud/equipos-medicos.html','https://tienda.farmashop.com.uy/salud/autocontrol.html',
             'https://tienda.farmashop.com.uy/salud/otros.html']
len(pagesList)
lastPage = [15,6,4,18,2,2,97]
len(lastPage)
for categoryPageNumber in range(3,len(pagesList)):
    numberOfPages = lastPage[categoryPageNumber]
    for categoryViewPage in range(1,numberOfPages):
        headers = random.choice(headers_list)
        s = requests.Session()
        s.headers = headers
        viewURL = pagesList[categoryPageNumber] + '?p='+ str(categoryViewPage)
        secondsToWait = random.randint(20,30)
        time.sleep(secondsToWait)
        categoryPageViewPage = s.get(viewURL)
        categoryPageViewSoup = BeautifulSoup(categoryPageViewPage.content, 'html.parser')
        products = categoryPageViewSoup.find('div',class_='column main').find('div',class_='products wrapper grid products-grid').find('ol',class_='products list items product-items').findAll('li',class_='item product product-item')
        for product in products:
            productName = product.find('div',class_='product details product-item-details').find('strong',class_='product name product-item-name').find('a').text
            productNameCleaner = re.compile(r'  +|\n')
            productNameClean = productNameCleaner.sub('',productName)
            productLink = product.find('div',class_='product details product-item-details').find('strong',class_='product name product-item-name').find('a').attrs['href']
            priceWrapper = product.find('div',class_='product details product-item-details').findAll('span',class_='price-wrapper')
            if len(priceWrapper) == 1:
                price = priceWrapper[0].attrs['data-price-amount']
                priceOld = ""
            elif len(priceWrapper) == 2:
                price = priceWrapper[0].attrs['data-price-amount']
                priceOld = priceWrapper[1].attrs['data-price-amount']
            listOfProductName.append(productNameClean)
            listOfPrices.append(price)
            listOfLinksToProduct.append(productLink)
            listOfOldPrices.append(priceOld)
# composition
df = pd.DataFrame()
len(listOfProductName)
len(listOfPrices)
df['productName']=listOfProductName
df['prices']=listOfPrices
df['LinksToProducto']=listOfLinksToProduct
df['moneda']= ['Pesos uruguayos' for i in range(len(listOfPrices))]
df['Farmacia']= ['Farmashop' for i in range(len(listOfPrices))]
df['oldPrices']= listOfOldPrices
df['Country']= ['Uruguay' for i in range(len(listOfPrices))]
df.to_csv(r'FarmaShop2.csv',encoding='utf-8')
    
            





