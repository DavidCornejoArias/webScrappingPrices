# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 09:32:21 2020

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

URL = "https://farmex.cl/collections/medicamentos"
headers = random.choice(headers_list)
r = requests.Session()
r.headers = headers
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
# trying to find the number of the page
totalNumberPages = int(soup.find('div',id='body-content').find('div',class_='page-cata').find('div',class_='pagination-holder').findAll('a')[-2].text)
for pageNumber in range(1,totalNumberPages+1):
    URL = "https://farmex.cl/collections/medicamentos?page="+str(pageNumber)
    headers = random.choice(headers_list)
    r = requests.Session()
    r.headers = headers
    secondsToWait = random.randint(20,30)
    time.sleep(secondsToWait)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    products = soup.find('div',id='body-content').find('div',class_='page-cata').find('div',class_='cata-product cp-grid clearfix no-sidebar').findAll('div',class_='product-grid-item product-price-range')
    for product in products:
        productNameNotClean = product.find('div',class_='product-content').find('h5',class_='product-name').text
        nameCleaner = re.compile(r'\n')
        productNameClean = nameCleaner.sub('',productNameNotClean)
        # short product Link
        shortLink = product.find('div',class_='product-content').find('h5',class_='product-name').find('a').attrs['href']
        longLink = 'https://farmex.cl'+shortLink
        pricesNotClean = product.find('div',class_='product-content').find('div',class_='product-price').findAll('span')
        priceCleaner = re.compile(r'\n| |\$|[A-z]')
        changingDotByComma = re.compile(r'\.')
        if len(pricesNotClean) ==2:
            priceClean = priceCleaner.sub('',pricesNotClean[1].text)
            priceClean = changingDotByComma.sub(',',priceClean)
            oldPriceNotClean = priceCleaner.sub('',pricesNotClean[0].text)
            oldPriceClean = changingDotByComma.sub(',',oldPriceNotClean)
        elif len(pricesNotClean) ==1:
            priceClean = priceCleaner.sub('',pricesNotClean[0].text)
            priceClean = changingDotByComma.sub(',',priceClean)   
            oldPriceClean = ""
        listOfProductName.append(productNameClean)
        listOfPrices.append(priceClean)
        listOfLinksToProduct.append(longLink)
        listOfOldPrices.append(oldPriceClean)
# composition
df = pd.DataFrame()
len(products)
len(listOfPrices)
df['productName']=listOfProductName
df['prices']=listOfPrices
df['LinksToProducto']=listOfLinksToProduct
df['moneda']= ['Pesos chilenos' for i in range(len(listOfPrices))]
df['Farmacia']= ['Farmaex' for i in range(len(listOfPrices))]
df['oldPrices']= listOfOldPrices
df['Country']= ['Chile' for i in range(len(listOfPrices))]
df.to_csv(r'C:\Users\david\Documents\DNM\webscrapping\farmazEx.csv',encoding='utf-8')











