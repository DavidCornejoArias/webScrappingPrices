# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 12:26:00 2020

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

URL = "https://www.farmapana.com"
headers = random.choice(headers_list)
r = requests.Session()
r.headers = headers
page = r.get(URL, verify=False)
soup = BeautifulSoup(page.content, 'html.parser')
# Looping through categories:
categories = soup.find('div',class_='dropdown-menu-inner').findAll('li')


for category in categories:
    # getting the link
    categoryURL = category.find('a').attrs['href']
    headers = random.choice(headers_list)
    t = requests.Session()
    t.headers = headers
    secondsToWait = random.randint(10,20)
    categoryPage = t.get(categoryURL, verify=False)
    categorySoup = BeautifulSoup(categoryPage.content, 'html.parser')
    totalPagesNotClean = categorySoup.findAll('a',rel='nofollow')[-1].text
    subsTotalPageComp = re.compile(r' |\n')
    singlePage=False
    try:
        totalPagesClean = int(subsTotalPageComp.sub('',totalPagesNotClean))
    except:
        singlePage=True
    if singlePage:
        products = categorySoup.findAll('h3',class_='h3 product-title')
        for product in products:
            Name = product.text
            productLink = product.find('a').attrs['href']
            priceNotClean = product.parent.parent.find('span',class_='price').find('span',itemprop='price').text
            substituteMoneySign = re.compile(r'\$')
            priceClean = substituteMoneySign.sub("", priceNotClean)
            substituteComaByPoint = re.compile(r'\,')
            priceClean = substituteComaByPoint.sub(".",priceClean)
            listOfProductName.append(Name)
            listOfPrices.append(priceClean)
            listOfLinksToProduct.append(productLink)
    else:
        for pageNumber in range(totalPagesClean):
            s = requests.Session()
            s.headers = headers
            urlView = categoryURL + '?page='+str(pageNumber)
            pageView = s.get(urlView, verify=False)
            secondsToWait = random.randint(10,20)
            time.sleep(secondsToWait)
            pageViewSoup = BeautifulSoup(pageView.content, 'html.parser')
            products = pageViewSoup.findAll('h3',class_='h3 product-title')
            for product in products:
                Name = product.text
                productLink = product.find('a').attrs['href']
                priceNotClean = product.parent.parent.find('span',class_='price').find('span',itemprop='price').text
                substituteMoneySign = re.compile(r'\$')
                priceClean = substituteMoneySign.sub("", priceNotClean)
                substituteComaByPoint = re.compile(r'\,')
                priceClean = substituteComaByPoint.sub(".",priceClean)
                listOfProductName.append(Name)
                listOfPrices.append(priceClean)
                listOfLinksToProduct.append(productLink)
df = pd.DataFrame()
len(listOfProductName)
len(listOfPrices)
df['productName']=listOfProductName
df['prices']=listOfPrices
df['LinksToProducto']=listOfLinksToProduct
df['moneda']= ['Dólar' for i in range(len(listOfPrices))]
df.to_csv(r'C:\Users\david\Documents\DNM\webscrapping\farmaPana2.csv',encoding='utf-8')



