# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 10:56:14 2020

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

URL = "https://fraccion.cl/medicamentos#/pageSize=48&orderBy=10&pageNumber=4"
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
categories = soup.find('div',class_='master-wrapper-page').find('div',class_='master-wrapper-content').find('div',class_='master-column-wrapper').find('div',class_='page-body').find('div',class_='category-grid sub-category-grid').findAll('div',class_='item-box')
for category in categories:
    headers = random.choice(headers_list)
    r = requests.Session()
    r.headers = headers
    categoryShortLink = category.find('a').attrs['href']
    categoryLongLink = 'https://fraccion.cl'+categoryShortLink+"#/pageSize=24&orderBy=10&pageNumber=1"
    categoryPage = r.get(categoryLongLink)
    categorySoup = BeautifulSoup(categoryPage.content, 'html.parser')
    # number of pages
    try:
        totalPages = int(categorySoup.find('div',class_='master-wrapper-content').find('div',class_='page-body').find('div',class_='pager').find('ul').findAll('li')[-2].text)
    except:
        totalPages = None
    if totalPages!=None:
        for pageNumber in range(1,totalPages+1):
            headers = random.choice(headers_list)
            s = requests.Session()
            s.headers = headers
            pageLongLink = 'https://fraccion.cl'+categoryShortLink+"#/pageSize=24&orderBy=10&pageNumber="+str(pageNumber)
            numberPage = s.get(pageLongLink)
            numberSoup = BeautifulSoup(numberPage.content, 'html.parser')
            productGrid = numberSoup.find('div',class_='master-wrapper-content').find('div',class_='page-body').find('div',class_='item-grid')
            products = productGrid.findAll('div',class_='item-box')
            for product in products:
                productName = product.find('h2',class_='product-title').find('a').text
                priceNotClean = product.find('div',class_='prices').find('span').text
                priceCleaner = re.compile(r'\$')
                priceClean = priceCleaner.sub('',priceNotClean)
                subsPointByComa = re.compile(r'\.')
                priceClean = subsPointByComa.sub(',',priceClean)
                productShortLink = product.find('h2',class_='product-title').find('a').attrs['href']
                longProductLink = 'https://fraccion.cl'+productShortLink
                listOfProductName.append(productName)
                listOfPrices.append(priceClean)
                listOfLinksToProduct.append(longProductLink)
                listOfOldPrices.append("")
    else:
        try:
            productGrid = categorySoup.find('div',class_='master-wrapper-content').find('div',class_='page-body').find('div',class_='item-grid')
        except:
            productGrid = None
        if productGrid !=None:
            products = productGrid.findAll('div',class_='item-box')
            for product in products:
                productName = product.find('h2',class_='product-title').find('a').text
                priceNotClean = product.find('div',class_='prices').find('span').text
                priceCleaner = re.compile(r'\$')
                priceClean = priceCleaner.sub('',priceNotClean)
                subsPointByComa = re.compile(r'\.')
                priceClean = subsPointByComa.sub(',',priceClean)
                productShortLink = product.find('h2',class_='product-title').find('a').attrs['href']
                longProductLink = 'https://fraccion.cl'+productShortLink
                listOfProductName.append(productName)
                listOfPrices.append(priceClean)
                listOfLinksToProduct.append(longProductLink)
                listOfOldPrices.append("")
# composition
df = pd.DataFrame()
len(listOfProductName)
len(listOfPrices)
df['productName']=listOfProductName
df['prices']=listOfPrices
df['LinksToProducto']=listOfLinksToProduct
df['moneda']= ['Pesos chilenos' for i in range(len(listOfPrices))]
df['Farmacia']= ['Farmacia Fracción' for i in range(len(listOfPrices))]
df['oldPrices']= listOfOldPrices
df['Country']= ['Chile' for i in range(len(listOfPrices))]
df.to_csv(r'C:\Users\david\Documents\DNM\webscrapping\fraccion.csv',encoding='utf-8')
    


