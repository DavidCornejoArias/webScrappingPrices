# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 15:14:27 2020

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

n = 47
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

URL = "https://www.fybeca.com/FybecaWeb/pages/home.jsf#"
headers = random.choice(headers_list)
r = requests.Session()
r.headers = headers
page = r.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
categories = soup.find('div',class_='row-fluid').findAll('li',class_="nav-header")[:-1]

for category in categories:
    shortCategoryLink = category.find('a').attrs['href'][:-2]
    # getting the number of category
    categoryNumberCompiler = re.compile(r'(?<=cat\=)\d+')
    categoryNumberResult =  categoryNumberCompiler.search(shortCategoryLink)
    categoryNumber = shortCategoryLink[categoryNumberResult.start():categoryNumberResult.end()]
    # getting the category link for each 100 products
    homeLink = 'https://www.fybeca.com/FybecaWeb/pages/search-results.jsf?s='
    for numberView in range(2):
        longCategoryLink= homeLink +str(numberView*100)+'&pp=100&cat='+ categoryNumber+'&b=-1&ot=0'
        # looking for number of items
        headers = random.choice(headers_list)
        r = requests.Session()
        r.headers = headers
        secondsToWait = random.randint(20,30)
        time.sleep(secondsToWait)
        categoryPage = r.get(longCategoryLink)
        categorySoup = BeautifulSoup(categoryPage.content, 'html.parser')
        #categorySoup.find('div',id='content-content').find('div',id='container-result').find('div',class_='products-tools tools-top')
        try:
            products = categorySoup.find('div',id='content-content').find('div',id='container-result').find('ul',class_='products-list').findAll('li')[:-1]
        except:
            products = []
        if len(products)>0:
            for product in products:
                productName = product.find('a',class_='name').text
                shortProductLInk = product.find('a',class_='name').attrs['href']
                productLink = 'https://www.fybeca.com'+shortProductLInk
                pricesDiscountNotClean = product.find('div',class_='price-member').find('div').attrs['data-bind']
                priceLooker = re.compile(r'(?<=\()\d.+\d(?=\))')
                priceDiscountCleanResult = priceLooker.search(pricesDiscountNotClean)
                priceDiscountClean = pricesDiscountNotClean[priceDiscountCleanResult.start():priceDiscountCleanResult.end()]
                # price discounted
                pricesNotClean = product.find('div',class_='price').attrs['data-bind']
                priceCleanResult = priceLooker.search(pricesNotClean)
                priceClean = pricesNotClean[priceCleanResult.start():priceCleanResult.end()]
                # adding the link
                listOfProductName.append(productName)
                listOfPrices.append(priceClean)
                listOfLinksToProduct.append(productLink)
                listOfOldPrices.append(priceDiscountClean)
# composition
df = pd.DataFrame()
len(listOfProductName)
len(listOfPrices)
df['productName']=listOfProductName
df['prices']=listOfPrices
df['LinksToProducto']=listOfLinksToProduct
df['moneda']= ['Dólar' for i in range(len(listOfPrices))]
df['Farmacia']= ['Farmacia Fybeca' for i in range(len(listOfPrices))]
df['oldPrices']= listOfOldPrices
df['Country']= ['Ecuador' for i in range(len(listOfPrices))]
df.to_csv(r'C:\Users\david\Documents\DNM\webscrapping\farmaciaFybeca.csv',encoding='utf-8')




