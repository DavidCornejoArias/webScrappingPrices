# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 09:17:51 2020

@author: david
"""
# note: you need tospecify the number of pages in 
# https://www.farmaciasanantonio.hn/Tienda/?
#n = 728 
n = 728

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

URL = "https://www.farmaciasanantonio.hn/Tienda/?"
headers = random.choice(headers_list)
r = requests.Session()
r.headers = headers
page = r.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
# Looping through categories:
for pageViewNumber in range(695,n+1):
    viewUrl = URL+'pagina='+str(pageViewNumber)
    headers = random.choice(headers_list)
    s = requests.Session()
    s.headers = headers
    secondsToWait = random.randint(10,20)
    time.sleep(secondsToWait)
    viewPage = s.get(viewUrl)
    viewSup = BeautifulSoup(viewPage.content, 'html.parser')
    products = viewSup.find(id='main').find('ul',class_='products columns-4').findAll('li')
    for product in products:
        productName= product.find('h2',class_='woocommerce-loop-product__title').text
        pricesList = product.findAll('span',class_='woocommerce-Price-amount amount')
        PriceCleaner = re.compile(r'L\.')
        if len(pricesList) == 2:    
            oldPriceNotClean = pricesList[0].text    
            oldPriceClean = PriceCleaner.sub('',oldPriceNotClean)
            newPriceNotClean = pricesList[1].text    
            newPriceClean = PriceCleaner.sub('',newPriceNotClean)
        elif len(pricesList)==1:
            newPriceNotClean = pricesList[0].text    
            newPriceClean = PriceCleaner.sub('',newPriceNotClean)
            oldPriceClean=""
        linkToProduct = product.find('a',class_='button').attrs['href']   
        # adding prices
        listOfProductName.append(productName)
        listOfPrices.append(newPriceClean)
        listOfLinksToProduct.append(linkToProduct)
        listOfOldPrices.append(oldPriceClean)
df = pd.DataFrame()
len(listOfProductName)
# page, 692
len(listOfLinksToProduct)
df['productName']=listOfProductName
df['prices']=listOfPrices
df['LinksToProducto']=listOfLinksToProduct
df['moneda']= ['Lémpira' for i in range(len(listOfPrices))]
df['Farmacia']= ['Farmacia San Antonio' for i in range(len(listOfPrices))]
df['oldPrices']= listOfOldPrices
df['Country']= ['Honduras' for i in range(len(listOfPrices))]
df.to_csv(r'C:\Users\david\Documents\DNM\webscrapping\farmaciaSanAntonio5.csv',encoding='utf-8')


# for dataframe Order
#'productName', 'prices','farmaciaLink',  'moneda','Farmacia', 'oldPrices','Country'