# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 11:14:40 2020

@author: david
"""

import selenium
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
dir(By)
browser.get(r'https://www.larebajavirtual.com/')
categories = browser.find_element(By.XPATH,'/html/body/div[2]/header/div/section[1]/div[2]/form/div/div[1]/div/div/ul/li[7]').find_elements(By.TAG_NAME,'a')[1:]
len(categories)
for category in categories:
    linkCategory = category.get_attribute('href')
    browser.get(linkCategory)
    time.sleep(10)
    try:
        lastLink = browser.find_element(By.XPATH,'/html/body/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]/section/div/div[3]/ul').find_element(By.CLASS_NAME,'last').find_element(By.TAG_NAME,'a').get_attribute('href')
        lastLinkLooker = re.compile(r'(?<=page/)\d+')
        lastPageNumberResult = lastLinkLooker.search(lastLink)
        lastPageNumber = int(lastLink[lastPageNumberResult.start():lastPageNumberResult.end()])
    except:
        lastLink = None
    if lastLink != None:
        for pageNumberView in range(1,lastPageNumber):
            browser.get(linkCategory+r'/codigoProducto_page/'+str(pageNumberView))
            time.sleep(10)
            products = browser.find_element(By.XPATH,'/html/body/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]/section/div/ul/div').find_elements(By.CLASS_NAME,'itemListGridProductos')
            for product in products:
                productName = product.find_element(By.CLASS_NAME,'nameProduct').find_element(By.TAG_NAME,'a').text
                productLink = product.find_element(By.CLASS_NAME,'nameProduct').find_element(By.TAG_NAME,'a').get_attribute('href')
                productPresentation = product.find_element(By.CLASS_NAME,'presentacionPorductoCard').text
                productPriceNotClean = product.find_element(By.CLASS_NAME,'priceFinal').text
                priceCleaner = re.compile(r'\$|\.')
                priceClean = priceCleaner.sub('',productPriceNotClean)
                listOfProductName.append(productName)
                listOfPrices.append(priceClean)
                listOfLinksToProduct.append(productLink)
                listOfOldPrices.append("")
    else:
        try:
            products = browser.find_element(By.XPATH,'/html/body/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]/section/div/ul/div').find_elements(By.CLASS_NAME,'itemListGridProductos')
        except:
            products = None
        if products != None:
            for product in products:
                productName = product.find_element(By.CLASS_NAME,'nameProduct').find_element(By.TAG_NAME,'a').text
                productLink = product.find_element(By.CLASS_NAME,'nameProduct').find_element(By.TAG_NAME,'a').get_attribute('href')
                productPresentation = product.find_element(By.CLASS_NAME,'presentacionPorductoCard').text
                productPriceNotClean = product.find_element(By.CLASS_NAME,'priceFinal').text
                priceCleaner = re.compile(r'\$|\.')
                priceClean = priceCleaner.sub('',productPriceNotClean)
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
df['moneda']= ['Pesos colombianos' for i in range(len(listOfPrices))]
df['Farmacia']= ['La Rebaja Virtual' for i in range(len(listOfPrices))]
df['oldPrices']= listOfOldPrices
df['Country']= ['Colombia' for i in range(len(listOfPrices))]
df.to_csv(r'C:\Users\david\Documents\DNM\webscrapping\laRebajaVirtual.csv',encoding='utf-8')





