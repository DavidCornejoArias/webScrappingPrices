# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 15:56:34 2020

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
browser.get(r'https://www.farmacorp.com/web/category/18/192')
secondsToWait = random.randint(20,30)
time.sleep(secondsToWait)

categories = browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div[5]/div/div[9]/div[2]/div/ul').find_elements(By.TAG_NAME,'li')
categoriesForReal= []
for category in categories:
    categoryForReal = category.find_element(By.TAG_NAME,'a').get_attribute('href')
    categoriesForReal.append(categoryForReal)
len(categoriesForReal)
categoryBrowser = browser
for category in categoriesForReal:
    categoryBrowser.get(category)
    secondsToWait = random.randint(20,30)
    time.sleep(secondsToWait)
    moreThanOnePage = False
    try:
        pages = categoryBrowser.find_element(By.ID,'content-pagination-products-head').find_element(By.CLASS_NAME,'pagination').find_elements(By.TAG_NAME,'li')
        moreThanOnePage = True
    except:
        moreThanOnePage = False
        print('no hay más páginas')
    if moreThanOnePage:
        for page in pages:
            if page.text =='»':
                nextPageObject = page
        while nextPageObject !=None:
            products = categoryBrowser.find_element(By.ID,'content-products').find_elements(By.CLASS_NAME,'product')
            for product in products:
                productName = product.find_element(By.CLASS_NAME,'description').find_element(By.TAG_NAME,'a').text
                productLink = product.find_element(By.CLASS_NAME,'description').find_element(By.TAG_NAME,'a').get_attribute('href')
                priceNotClean = product.find_element(By.CLASS_NAME,'price').find_element(By.TAG_NAME,'span').text
                priceCleaner= re.compile(r'Bs\. ')
                priceClean = priceCleaner.sub('',priceNotClean)
                listOfProductName.append(productName)
                listOfPrices.append(priceClean)
                listOfLinksToProduct.append(productLink)
                listOfOldPrices.append("")     
            stillGoing = False
            try:
                pages = categoryBrowser.find_element(By.ID,'content-pagination-products-head').find_element(By.CLASS_NAME,'pagination').find_elements(By.TAG_NAME,'li')
                for page in pages:
                    if page.text =='»':
                        nextPageObject = page
                        stillGoing = True
            except:
                stillGoing = False
            if stillGoing:
                nextPageObject.find_element(By.TAG_NAME,'a').click()
                secondsToWait = random.randint(10,20)
                time.sleep(secondsToWait)
            else:
                nextPageObject = None
    else:
        products = categoryBrowser.find_element(By.ID,'content-products').find_elements(By.CLASS_NAME,'product')
        for product in products:
            productName = product.find_element(By.CLASS_NAME,'description').find_element(By.TAG_NAME,'a').text
            productLink = product.find_element(By.CLASS_NAME,'description').find_element(By.TAG_NAME,'a').get_attribute('href')
            priceNotClean = product.find_element(By.CLASS_NAME,'price').find_element(By.TAG_NAME,'span').text
            priceCleaner= re.compile(r'Bs\. ')
            priceClean = priceCleaner.sub('',priceNotClean)
            listOfProductName.append(productName)
            listOfPrices.append(priceClean)
            listOfLinksToProduct.append(productLink)
            listOfOldPrices.append("")     
        
df = pd.DataFrame()
len(listOfProductName)
len(listOfPrices)
df['productName']=listOfProductName
df['prices']=listOfPrices
df['LinksToProducto']=listOfLinksToProduct
df['moneda']= ['Bolivares' for i in range(len(listOfPrices))]
df['Farmacia']= ['FarmaCorp' for i in range(len(listOfPrices))]
df['oldPrices']= listOfOldPrices
df['Country']= ['Bolivia' for i in range(len(listOfPrices))]
df.to_csv(r'C:\Users\david\Documents\DNM\webscrapping\farmaCorp.csv',encoding='utf-8')