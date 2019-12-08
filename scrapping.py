# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import os
import time

driver = webdriver.Chrome('/home/doara/Documentos/uns_codigos/Python/bovespa_project/chromedriver_linux64/chromedriver')
a = driver.get("https://br.tradingview.com/symbols/BMFBOVESPA-VVAR3/")
print(a)
time.sleep(2) 
content = driver.find_element_by_css_selector('div.tv-symbol-price-quote__value')
print(content.text)
driver.find_element_by_css_selector('a.tv-feed-widget__title-link').click()
v = driver.find_element_by_css_selector('table.table-1YbYSTk8')
print(v.text)





