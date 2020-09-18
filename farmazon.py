# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 08:33:39 2020

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

URL = "https://www.farmazon.cl/categorias/medicamentos.html?p=1"
headers = random.choice(headers_list)
r = requests.Session()
r.headers = headers
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
# first get number of pages and logic how they move
for pageNumber in range(1,n+1):
    pageUrl = "https://www.farmazon.cl/categorias/medicamentos.html?p="+str(pageNumber)
    headers = random.choice(headers_list)
    r = requests.Session()
    r.headers = headers
    secondsToWait = random.randint(20,30)
    time.sleep(secondsToWait)
    viewPage = requests.get(pageUrl)
    viewSoup = BeautifulSoup(viewPage.content, 'html.parser')    
    products = viewSoup.find('body').find('main',id='maincontent').find('div',class_='columns').find('div',class_='column main').find('div',class_='products wrapper grid products-grid').findAll('li',class_='item product product-item')
    for product in products:
        productName = product.find('div',class_='product details product-item-details').find('a',class_='product-item-link').text
        productLink = product.find('div',class_='product details product-item-details').find('a',class_='product-item-link').attrs['href']
        pricesForProduct = product.find('div',class_='product details product-item-details').findAll('span',class_='price-wrapper')
        if len(pricesForProduct)==2:
            price = pricesForProduct[0].attrs['data-price-amount']
            newPrice = pricesForProduct[1].attrs['data-price-amount']
        elif len(pricesForProduct)==1:
            price = pricesForProduct[0].attrs['data-price-amount']
            newPrice = ""
        listOfProductName.append(productName)
        listOfPrices.append(price)
        listOfLinksToProduct.append(productLink)
        listOfOldPrices.append(newPrice)
# composition
df = pd.DataFrame()
len(listOfProductName)
len(listOfPrices)
df['productName']=listOfProductName
df['prices']=listOfPrices
df['LinksToProducto']=listOfLinksToProduct
df['moneda']= ['Pesos mexicanos' for i in range(len(listOfPrices))]
df['Farmacia']= ['Superama' for i in range(len(listOfPrices))]
df['oldPrices']= listOfOldPrices
df['Country']= ['México' for i in range(len(listOfPrices))]
df.to_csv(r'C:\Users\david\Documents\DNM\webscrapping\superama.csv',encoding='utf-8')



