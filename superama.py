# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 14:05:11 2020

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
browser.get(r'https://www.superama.com.mx/catalogo/d-farmacia')

categories = browser.find_element(By.XPATH,'/html/body/div[2]/div[9]/div[1]/div[2]/ul').find_elements(By.TAG_NAME,'a')
for category in categories:
    category.text
    categoryBrowser = webdriver.Chrome(chrome_options=options,executable_path=r"C:\Users\david\Documents\DNM\webscrapping\chromedriver.exe")
    categoryBrowser.get(category.get_attribute('href'))
    secondsToWait = random.randint(20,30)
    time.sleep(secondsToWait)
    try:
        products = categoryBrowser.find_element(By.ID,'resultadosBusquedaContainerGeneral').find_element(By.ID,'resultadoProductosBusqueda').find_elements(By.TAG_NAME,'li')
    except:
        products = None
    if products != None:
        for product in products:
            productName = product.find_element(By.CLASS_NAME,'upcName').find_element(By.TAG_NAME,'p').text
            priceNotClean = product.find_element(By.CLASS_NAME,'upcPrice').text
            priceCleaner = re.compile(r'  +|\$')
            priceClean = priceCleaner.sub('',priceNotClean)
            productLink = product.find_element(By.CLASS_NAME,'upcName').find_element(By.TAG_NAME,'p').find_element(By.TAG_NAME,'a').get_attribute('href')
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
df['moneda']= ['Pesos mexicanos' for i in range(len(listOfPrices))]
df['Farmacia']= ['Superama' for i in range(len(listOfPrices))]
df['oldPrices']= listOfOldPrices
df['Country']= ['México' for i in range(len(listOfPrices))]
df.to_csv(r'C:\Users\david\Documents\DNM\webscrapping\superama.csv',encoding='utf-8')
