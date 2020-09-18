# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 09:02:23 2020

@author: david
"""

import selenium
import random
import webbrowser
import datetime
from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
import time
import logging
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
import pdb
import re

listOfProductName = []
listOfPrices = []
listOfLinksToProduct = []
listOfOldPrices = []
listOfLaboratorios = []

# Estableciendo los parámetros
path = r'C:\Users\david\Documents\DNM\webscrapping'
os.chdir(path)

#---------------------------------------------------------------

#Estableciendo la consola para recibir información durante el proceso

logger = logging.getLogger("root")

logger.setLevel(logging.DEBUG)

# Alistando las opciones de chrome de default para el bot

options = webdriver.ChromeOptions()

options.add_argument("--allow-running-insecure-content")

options.add_experimental_option("prefs", {

 

    "download.default_directory": os.getcwd(),

 

    "download.prompt_for_download": False,

 

    "download.directory_upgrade": True,

 

    "safebrowsing.enabled": True

 

})

# Abriendo el chromeDriver.exe

browser = webdriver.Chrome(chrome_options=options,executable_path=r"C:\Users\david\Documents\DNM\webscrapping\chromedriver.exe")
#pdb.set_trace()
# Abriendo la dirección
browser.get(r'https://salemmaonline.com.py/higiene-personal/farmacia')
secondsToWait = random.randint(20,30)
time.sleep(secondsToWait)
# categories
categories = browser.find_element(By.XPATH,'/html/body/div/section/div/div/div[1]/div/div/div/div[12]/div[2]/ul/li[3]/div[2]').find_element(By.CLASS_NAME,'list-group').find_elements(By.TAG_NAME,'a')
categoriesForReal = []
for category in categories:
    categoriesForReal.append(category.get_attribute('href'))
len(categoriesForReal)
#category
categoriesForReal = categoriesForReal
for category in categoriesForReal:
    browser.get(category)
    secondsToWait = random.randint(10,20)
    time.sleep(secondsToWait)
    try:
        closeAnoyingWindowButton = browser.find_element(By.XPATH,'/html/body/div[1]/div[4]/div/div/form/div[1]/button')
        closeAnoyingWindowButton.click()
    except:
        print('Sin Anuncio')
    moreThanOnePage = False
    secondsToWait = random.randint(3,5)
    time.sleep(secondsToWait)
    try:
        pages = browser.find_element(By.XPATH,'/html/body/div/section/div/div/div[2]/div/div[43]/div/div/ul').find_elements(By.CLASS_NAME,'page-item')
        lastItem = pages[-1].find_element(By.TAG_NAME,'a').text
        moreThanOnePage = True
    except:
        moreThanOnePage = False
    lastPageNumber = None
    lastPageNumberCorrect = False
    if moreThanOnePage:
        if lastItem=='›':
            lastPageNumber = int(pages[-2].find_element(By.TAG_NAME,'a').text)
            lastPageNumberCorrect = True
        elif type(lastItem)==int:
            lastPageNumber = lastItem
            lastPageNumberCorrect = True
        else:
            lastPageNumberCorrect = False
        if lastPageNumberCorrect:
            for pageView in range(1,lastPageNumber+1):
                pageViewLink = category+'?page='+str(pageView)
                browser.get(pageViewLink)
                secondsToWait = random.randint(10,20)
                time.sleep(secondsToWait)            
                try:
                    closeAnoyingWindowButton = browser.find_element(By.XPATH,'/html/body/div[1]/div[4]/div/div/form/div[1]/button')
                    closeAnoyingWindowButton.click()
                except:
                    print('Sin Anuncio')
                products = browser.find_element(By.XPATH,'/html/body/div/section/div/div/div[2]').find_elements(By.XPATH,"//div[contains(@class, 'col-lg-3 col-md-4 col-sm-4 col-6 pdivp div-product-list')]")
                for product in products:
                    priceNotClean = product.find_element(By.CLASS_NAME,'pprice').text
                    priceCleaner = re.compile(r'Gs\. |\.')
                    priceClean = priceCleaner.sub('',priceNotClean)
                    laboratorio = product.find_element(By.CLASS_NAME,'ptitle').text
                    productName = product.find_element(By.CLASS_NAME,'psubtitle').text
                    productLink = product.find_element(By.CLASS_NAME,'psubtitle').find_element(By.TAG_NAME,'a').get_attribute('href')
                    listOfProductName.append(productName)
                    listOfPrices.append(priceClean)
                    listOfLinksToProduct.append(productLink)
                    listOfOldPrices.append("")
                    listOfLaboratorios.append(laboratorio)
    else:
        products = browser.find_element(By.XPATH,'/html/body/div/section/div/div/div[2]').find_elements(By.XPATH,"//div[contains(@class, 'col-lg-3 col-md-4 col-sm-4 col-6 pdivp div-product-list')]")
        for product in products:
            priceNotClean = product.find_element(By.CLASS_NAME,'pprice').text
            priceCleaner = re.compile(r'Gs\. |\.')
            priceClean = priceCleaner.sub('',priceNotClean)
            laboratorio = product.find_element(By.CLASS_NAME,'ptitle').text
            productName = product.find_element(By.CLASS_NAME,'psubtitle').text
            productLink = product.find_element(By.CLASS_NAME,'psubtitle').find_element(By.TAG_NAME,'a').get_attribute('href')
            listOfProductName.append(productName)
            listOfPrices.append(priceClean)
            listOfLinksToProduct.append(productLink)
            listOfOldPrices.append("")
            listOfLaboratorios.append(laboratorio)
df = pd.DataFrame()
len(listOfProductName)
len(listOfPrices)
df['productName']=listOfProductName
df['prices']=listOfPrices
df['LinksToProducto']=listOfLinksToProduct
df['moneda']= ['Guaraní Paraguayo' for i in range(len(listOfPrices))]
df['Farmacia']= ['SalemmaOnline' for i in range(len(listOfPrices))]
df['oldPrices']= listOfOldPrices
df['Country']= ['Paraguay' for i in range(len(listOfPrices))]
df.to_csv(r'C:\Users\david\Documents\DNM\webscrapping\salemmaOnline.csv',encoding='utf-8')
