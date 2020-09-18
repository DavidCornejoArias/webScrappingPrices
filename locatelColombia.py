# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 12:29:57 2020

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
browser.get(r'https://www.locatelcolombia.com/drogueria/medicina-alternativa')

#--------------- Aquí se debe iniciar sesión

#------------ Colocando información en firebase
# cookies
boton = browser.find_element(By.XPATH,'/html/body/div[7]/footer/div[2]/div[2]/div[2]/a')
boton.click()
# starting process
#SOLUTION RUN CODE FOR BOTH WEBSITES
#https://www.locatelcolombia.com/drogueria/medicamentos-otc
#https://www.locatelcolombia.com/drogueria/medicamento
productSizet_1 = 0
dir(By)

WebDriverWait(browser,20).until(ec.visibility_of_all_elements_located((By.CLASS_NAME,'main')))
products = browser.find_element(By.CLASS_NAME,'main').find_elements(By.CLASS_NAME,'box-item')
products[-1].text
productSize = len(products)
while productSizet_1 != productSize:
    products = browser.find_element(By.CLASS_NAME,'main').find_elements(By.CLASS_NAME,'box-item')
    productSizet_1 = productSize
    print(productSizet_1)
    browser.execute_script("arguments[0].scrollIntoView(true);", products[-1])
    time.sleep(20)
    products = browser.find_element(By.CLASS_NAME,'main').find_elements(By.CLASS_NAME,'box-item')
    products[-1].location_once_scrolled_into_view
    time.sleep(10)
    productSize = len(products)
    print(productSize)
print(productSize)
dir(products[-1])
listOfProductName = []
listOfPrices = []
listOfLinksToProduct = []
listOfOldPrices = []
listOfPresentations = []
for product in products:
    priceCleaner = re.compile(r'\$|\.')
    productName = product.find_element_by_class_name('product-name').text
    productLink = product.find_element_by_class_name('product-name').get_attribute('href')
    priceNotClean = product.find_element_by_class_name('product-price').find_element_by_class_name('bestPrice').text
    try:
        oldpriceNotClean = product.find_element_by_class_name('product-price').find_element_by_class_name('oldPrice').text
        oldPriceClean = priceCleaner.sub('',oldpriceNotClean)
    except:
        oldPriceClean = 0
    priceClean = priceCleaner.sub('',priceNotClean)
    presentationNotClean = product.find_element_by_class_name('unit-measure').text
    presentationCleaner = re.compile(r'PUM - Unidad de Medida |PUM - Medida|\n')
    presentationClean = presentationCleaner.sub('',presentationNotClean)
    listOfProductName.append(productName)
    listOfPrices.append(priceClean)
    listOfLinksToProduct.append(productLink)
    listOfOldPrices.append(oldPriceClean)
    listOfPresentations.append(presentationClean)
# composition
df = pd.DataFrame()
len(listOfProductName)
len(listOfPrices)
df['productName']=listOfProductName
df['prices']=listOfPrices
df['LinksToProducto']=listOfLinksToProduct
df['presentations']=listOfPresentations
df['moneda']= ['Pesos colombianos' for i in range(len(listOfPrices))]
df['Farmacia']= ['locatel' for i in range(len(listOfPrices))]
df['oldPrices']= listOfOldPrices
df['Country']= ['Colombia' for i in range(len(listOfPrices))]
df.to_csv(r'C:\Users\david\Documents\DNM\webscrapping\locatelColombia3.csv',encoding='utf-8')
