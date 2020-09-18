# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 12:04:44 2020

@author: david
"""
n = 442
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

URL = "https://www.farmaentrega.com/farmacia"
headers = random.choice(headers_list)
r = requests.Session()
r.headers = headers
page = r.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

categorieHolder = soup.find('div',id="Cnt_Root_Cnt_MainContent_element_3725_ContentHolder").find('ul')
possibleCategories = categorieHolder.findAll('li')
dir(possibleCategories[1].find('a').has_attr('id'))
categories = [possibleCategory for possibleCategory in possibleCategories if possibleCategory.find('a') != None and possibleCategory.find('a').has_attr('id')]
for category in categories:
    secondsToWait = random.randint(10,20)
    time.sleep(secondsToWait)
    urlCategory = 'https://www.farmaentrega.com/'+category.find('a').attrs['href']
    headers = random.choice(headers_list)
    s = requests.Session()
    s.headers = headers
    categoryPage = s.get(urlCategory)
    categorySoup = BeautifulSoup(categoryPage.content, 'html.parser')
    productContainer = categorySoup.find('div',class_='productList')
    products = productContainer.findAll('div',class_='productItem')
    products[0]
    for product in products:
        productDescription = product.find('div',class_='productDescription withImage')
        if productDescription ==None:
            productDescription = product.find('div',class_='productDescription')
        name = productDescription.find('a').text
        shotLinkToProduct = productDescription.find('a').attrs['href']
        linkToProduct = 'https://www.farmaentrega.com/'+shotLinkToProduct
        price = ''
        listOfProductName.append(name)
        listOfPrices.append(price)
        listOfLinksToProduct.append(linkToProduct)
        listOfOldPrices.append(price)
df = pd.DataFrame()
len(listOfProductName)
len(listOfPrices)
df['productName']=listOfProductName
df['prices']=listOfPrices
df['LinksToProducto']=listOfLinksToProduct
df['moneda']= ['' for i in range(len(listOfPrices))]
df['Farmacia']= ['Farmacia Farma Entrega' for i in range(len(listOfPrices))]
df['oldPrices']= listOfOldPrices
df['Country']= ['Panamá' for i in range(len(listOfPrices))]
df.to_csv(r'C:\Users\david\Documents\DNM\webscrapping\farmaciaFarmaEntrega.csv',encoding='utf-8')






    
len(categories)
