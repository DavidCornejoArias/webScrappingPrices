# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 11:14:40 2020

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
listOfPresentations = []


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

URL = "https://larebajavirtual.com/catalogo/categoria/categoria/2716"
headers = random.choice(headers_list)
r = requests.Session()
r.headers = headers
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
categories = soup.find('ul',class_='listMenuCategory').findAll('li',class_='itemMenuCategory')[6].findAll('a')[1:]
#categories = browser.find_element(By.XPATH,'/html/body/div[2]/header/div/section[1]/div[2]/form/div/div[1]/div/div/ul/li[7]').find_elements(By.TAG_NAME,'a')[1:]
categories[0].attrs['href']
len(categories)
for category in categories:
    linkCategory = 'https://larebajavirtual.com'+category.attrs['href']
    s = requests.Session()
    s.headers = headers
    categoryPage = s.get(linkCategory)
    categorySoup = BeautifulSoup(categoryPage.content, 'html.parser')
    time.sleep(5)
    try:
        lastLink = categorySoup.find('div',id='lista-productos').find('section').find('div',id='id-productos-list').find('div',class_='pager').find('ul',id='yw0').find('li',class_='last').find('a').attrs['href']
        lastLinkLooker = re.compile(r'(?<=page/)\d+')
        lastPageNumberResult = lastLinkLooker.search(lastLink)
        lastPageNumber = int(lastLink[lastPageNumberResult.start():lastPageNumberResult.end()])
    except:
        lastLink = None
    if lastLink != None:
        for pageNumberView in range(1,lastPageNumber+1):
            t = requests.Session()
            t.headers = headers
            categoryPageView = t.get(linkCategory+r'/codigoProducto_page/'+str(pageNumberView))
            categoryPageViewSoup = BeautifulSoup(categoryPageView.content, 'html.parser')
            time.sleep(5)
            products = categoryPageViewSoup.find('div',id='id-productos-list').find('ul',class_='listaProductos').find('div',class_='items items4').findAll('li',class_='itemListGridProductos')
            len(products)
            for product in products:
                productName = product.find('div',class_='nameProduct').find('a').attrs['title']
                productLink = 'https://larebajavirtual.com' + product.find('div',class_='nameProduct').find('a').attrs['href']
                priceCleaner = re.compile(r'\$|\.|  +|\n')
                try:
                    productPriceNotClean = product.find('div',class_='priceProduct').find('div',class_='priceFinal').text
                    priceClean = priceCleaner.sub('',productPriceNotClean)
                except:
                    priceClean = ""
                presentationNotClean = product.find('div',class_='presentacionPorductoCard').text
                presentationCleaner = re.compile(r'\n|  +')
                presentationClean = presentationCleaner.sub('',presentationNotClean)
                listOfProductName.append(productName)
                listOfPrices.append(priceClean)
                listOfLinksToProduct.append(productLink)
                listOfOldPrices.append("")
                listOfPresentations.append(presentationClean)
    else:
        try:
            products = categorySoup.find('div',id='id-productos-list').find('ul',class_='listaProductos').find('div',class_='items items4').findAll('li',class_='itemListGridProductos')
        except:
            products = None
        if products != None:
            for product in products:
                productName = product.find('div',class_='nameProduct').find('a').attrs['title']
                productLink = 'https://larebajavirtual.com' + product.find('div',class_='nameProduct').find('a').attrs['href']
                priceCleaner = re.compile(r'\$|\.|  +|\n')
                try:
                    productPriceNotClean = product.find('div',class_='priceProduct').find('div',class_='priceFinal').text
                    priceClean = priceCleaner.sub('',productPriceNotClean)
                except:
                    priceClean = ""
                presentationNotClean = product.find('div',class_='presentacionPorductoCard').text
                presentationCleaner = re.compile(r'\n|  +')
                presentationClean = presentationCleaner.sub('',presentationNotClean)
                listOfProductName.append(productName)
                listOfPrices.append(priceClean)
                listOfLinksToProduct.append(productLink)
                listOfOldPrices.append("")
                listOfPresentations.append(presentationClean)
df = pd.DataFrame()
len(listOfProductName)
len(listOfPrices)
df['productName']=listOfProductName
df['prices']=listOfPrices
df['LinksToProducto']=listOfLinksToProduct
df['moneda']= ['Pesos colombianos' for i in range(len(listOfPrices))]
df['Farmacia']= ['La Rebaja Virtual' for i in range(len(listOfPrices))]
df['oldPrices']= listOfOldPrices
df['Country']= ['Colombia' for i in range(len(listOfPrices))]
df.to_csv(r'C:\Users\david\Documents\DNM\webscrapping\laRebajaVirtual.csv',encoding='utf-8')





