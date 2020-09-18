# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 15:05:12 2020

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
browser.get(r'https://www.pigalle.com.uy/salud')

#--------------- Aquí se debe iniciar sesión

#------------ Colocando información en firebase
productSizet_1 = 0
WebDriverWait(browser,20).until(ec.visibility_of_all_elements_located((By.CLASS_NAME,'item-box')))
products = browser.find_elements(By.CLASS_NAME,'item-box')
productSize = len(products)
while productSizet_1 != productSize:
    products = browser.find_elements(By.CLASS_NAME,'item-box')
    productSizet_1 = productSize
    print(productSizet_1)
    browser.execute_script("arguments[0].scrollIntoView(true);", products[-1])
    time.sleep(10)
    products = browser.find_elements(By.CLASS_NAME,'item-box')
    products[-1].location_once_scrolled_into_view
    time.sleep(10)
    productSize = len(products)
    print(productSize)
print(productSize)
dir(products[-1])
#list
listOfProductName = []
listOfPrices = []
listOfLinksToProduct = []
listOfOldPrices = []
for product in products:
    productLink = product.find_element_by_tag_name('a').get_attribute('href')
    productName = product.find_element_by_tag_name('a').text
    priceNotClean = product.find_element_by_class_name('prod-box__current-price').text
    priceCleaner = re.compile(r'\$|\.')
    priceClean = priceCleaner.sub('',priceNotClean)
    listOfProductName.append(productName)
    listOfPrices.append(priceClean)
    listOfLinksToProduct.append(productLink)
    listOfOldPrices.append("")
# composition
df = pd.DataFrame()
len(listOfProductName)
len(listOfPrices)
df['productName']=listOfProductName
df['prices']=listOfPrices
df['LinksToProducto']=listOfLinksToProduct
df['moneda']= ['Pesos uruguayos' for i in range(len(listOfPrices))]
df['Farmacia']= ['Pigalle' for i in range(len(listOfPrices))]
df['oldPrices']= listOfOldPrices
df['Country']= ['Uruguay' for i in range(len(listOfPrices))]
df.to_csv(r'C:\Users\david\Documents\DNM\webscrapping\Pigalle.csv',encoding='utf-8')
