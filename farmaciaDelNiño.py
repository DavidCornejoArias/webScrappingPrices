# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 10:56:13 2020

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
listOfComposition = []


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

URL = "https://farmaciasdelnino.mx/esp/items/1/0/medicamentos"
headers = random.choice(headers_list)
r = requests.Session()
r.headers = headers
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
ultimaPagina = int(soup.find('div',id='cuerpo').find('div',class_='pag').findAll('a')[-1].text)
ultimaPagina = 56
for viewPageNumber in range(ultimaPagina):
    viewURL = "https://farmaciasdelnino.mx/esp/items/1/"+str(viewPageNumber)+"/medicamentos"
    headers = random.choice(headers_list)
    r = requests.Session()
    r.headers = headers
    secondsToWait = random.randint(20,30)
    time.sleep(secondsToWait)
    viewPage = r.get(viewURL)
    soup = BeautifulSoup(viewPage.content, 'html.parser')
    # products
    productConatiner = soup.find('div',id='cuerpo').find('div',id='catalogo')
    productos = productConatiner.findAll('div',class_='descripcion')
    precios = productConatiner.findAll('div',class_='precio')
    for productNumber in range(len(productos)):
        productName = productos[productNumber].find('a').text
        productLink = productos[productNumber].find('a').attrs['href']
        prices = precios[productNumber].findAll('span')
        priceCleaner = re.compile(r'  +|\n| MXN|\$|\t')
        if len(prices)==2:
            priceNotClean = prices[1].text
            priceOldNotClean = prices[0].text
            priceClean = priceCleaner.sub('',priceNotClean)
            priceOldClean = priceCleaner.sub('',priceOldNotClean)
        elif len(prices)==1:
            priceNotClean = prices[0].text
            priceOldClean = ""
            priceClean = priceCleaner.sub('',priceNotClean)    
        # appending
        listOfProductName.append(productName)
        listOfPrices.append(priceClean)
        listOfLinksToProduct.append(productLink)
        listOfOldPrices.append(priceOldClean)
# composition
df = pd.DataFrame()
len(listOfProductName)
len(listOfPrices)
df['productName']=listOfProductName
df['prices']=listOfPrices
df['LinksToProducto']=listOfLinksToProduct
df['moneda']= ['Peso mexicano' for i in range(len(listOfPrices))]
df['Farmacia']= ['Farmacia del niño' for i in range(len(listOfPrices))]
df['oldPrices']= listOfOldPrices
df['Country']= ['México' for i in range(len(listOfPrices))]
df.columns
df.drop_duplicates(subset ="productName",keep=False,inplace=True) 
df.to_csv(r'C:\Users\david\Documents\DNM\webscrapping\farmaciaDelNino.csv',encoding='utf-8')

 