# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 13:44:17 2020

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

URL = "https://lineavital.com.co/tienda/"
headers = random.choice(headers_list)
r = requests.Session()
r.headers = headers
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
pagination = soup.find('div',id='primary')
pages = pagination.find('nav',class_='woocommerce-pagination').findAll('li')
lastPageNumber = int(pages[-2].find('a').text)
pageViewNumber = lastPageNumber
# for view
for pageNumber in range(1,lastPageNumber+1):
    viewURL = "https://lineavital.com.co/tienda/page/"+str(pageNumber)+"/"
    headers = random.choice(headers_list)
    r = requests.Session()
    r.headers = headers
    viewPage = requests.get(viewURL)
    secondsToWait = random.randint(20,30)
    time.sleep(secondsToWait)
    viewSoup = BeautifulSoup(viewPage.content, 'html.parser')
    productContainer = viewSoup.find('div',id='primary').find('ul',class_='products columns-3')
    products = productContainer.findAll('li')
    for product in products:
        productName = product.find('h2').text
        priceNoClean = product.find('span',class_='price')
        if priceNoClean != None:
            priceNoClean = priceNoClean.text
        else:
            priceNoClean = ""
        priceCleaner = re.compile(r'\$')
        priceClean = priceCleaner.sub('',priceNoClean)
        productLink = product.find('a',class_='woocommerce-LoopProduct-link woocommerce-loop-product__link').attrs['href']
        listOfProductName.append(productName)
        listOfPrices.append(priceClean)
        listOfLinksToProduct.append(productLink)
        listOfOldPrices.append("")
        listOfFarmacias.append("")        
df = pd.DataFrame()
len(listOfProductName)
len(listOfPrices)
df['productName']=listOfProductName
df['prices']=listOfPrices
df['LinksToProducto']=listOfLinksToProduct
df['moneda']= ['Peso colombiano' for i in range(len(listOfPrices))]
df['Farmacia']= ['Farmacia linea vital' for i in range(len(listOfPrices))]
df['oldPrices']= listOfOldPrices
df['Country']= ['Colombia' for i in range(len(listOfPrices))]
df['Farmacias del Producto']= listOfFarmacias
df.to_csv(r'C:\Users\david\Documents\DNM\webscrapping\farmaciaLineaVital.csv',encoding='utf-8')

    









