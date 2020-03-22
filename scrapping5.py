# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn import preprocessing
from sklearn.metrics import accuracy_score

from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

s = ''
data = []

def main():
    driver = webdriver.Chrome(chrome_options=options,executable_path='/home/doara/Documentos/uns_codigos/Python/bovespa_project/chromedriver_linux64/chromedriver')
    a = driver.get("https://br.tradingview.com/symbols/BMFBOVESPA-HGTX3/")
    content = driver.find_element_by_css_selector('div.tv-symbol-price-quote__value')
    s = content.text
    driver.find_element_by_css_selector('a.tv-feed-widget__title-link').click()
    v = driver.find_element_by_css_selector('table.table-1YbYSTk8')

    cut1 = ""
    cut1 = v.text.split('\n')

    cut2 = []
    for c in cut1:
        if c.find("Venda")>-1:
            cut2.append(c.split(' Venda'))
        elif c.find("Compra")>-1:
            cut2.append(c.split(' Compra'))
        else:
            cut2.append(c.split(' Vi'))

    cut3 = []

    for c in cut2:
        cut3.append(c[0].split(' '))
    
    for c in cut3:
        if c[len(c)-1].find("A")<0:
            data.append(c[len(c)-1])

    data.append(s)
    print(data[1]+';'+data[2]+';'+data[3]+';'+data[4]+';'+data[5]+';'+data[6]+';'+data[7]+';'+data[8]+';'+data[9]+';'+data[10]+';'+data[11])
    v = ""
    cut1 = []
    cut2 = []
    cut3 = []
    driver.close()
    time.sleep(25)


if __name__=="__main__":
    main()



'''
cut3 = []
for c in cut2[0]:
    cut3.append(c.split(' Compra'))
print(cut3)

cut4 = []
for c in cut3[0]:
    cut4.append(c.split(' Vi'))
print(cut4)

'''

