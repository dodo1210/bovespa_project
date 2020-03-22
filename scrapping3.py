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
f = open("dados_azul_02-01.csv", "a")
#f.write("Indice_de_Força_Relativa;Estocastico_%K;Indice_do_canal_de_commodities;Indice_Direcional_Medio;Oscilador_extraordinario;Momentum;NIvel_MACD;IFR_Estocastico_Rapido;Range_Percentual_de_Williams;Força_Bull_Bear;Oscilador_Definitivo;Status\n")

def main():
    driver = webdriver.Chrome(chrome_options=options,executable_path='/home/doara/Documentos/uns_codigos/Python/bovespa_project/chromedriver_linux64/chromedriver')
    a = driver.get("https://br.tradingview.com/symbols/BMFBOVESPA-AZUL4/")
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
    #f.write(str(data[1]+';'+data[2]+';'+data[3]+';'+data[4]+';'+data[5]+';'+data[6]+';'+data[7]+';'+data[8]+';'+data[9]+';'+data[10]+';'+data[11])+'\n')
    print(data[1]+';'+data[2]+';'+data[3]+';'+data[4]+';'+data[5]+';'+data[6]+';'+data[7]+';'+data[8]+';'+data[9]+';'+data[10]+';'+data[11])
    v = ""
    cut1 = []
    cut2 = []
    cut3 = []
    driver.close()
    time.sleep(25)

def predict():
    print("oi")
    data = pd.read_csv('dados_vvar_27-12.csv',sep=';')

    data = pd.DataFrame(data)

    for f in data.columns: 
        if data[f].dtype=='object': 
            lbl = preprocessing.LabelEncoder() 
            lbl.fit(list(data[f].values)) 
            data[f] = lbl.transform(list(data[f].values))

    X = data[["Indice_de_Força_Relativa","Estocastico_%K","Indice_do_canal_de_commodities","Indice_Direcional_Medio","Oscilador_extraordinario","Momentum","NIvel_MACD","IFR_Estocastico_Rapido","Range_Percentual_de_Williams","Força_Bull_Bear","Oscilador_Definitivo"]]
    y = data["Status"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    xg_reg = xgb.XGBRegressor(n_estimators = 1000, learning_rate=0.05)

    xg_reg.fit(X_train,y_train)
    score = xg_reg.score(X_test, y_test)
    preds = xg_reg.predict(X_test)
    print(preds)
    print("Score: %f" %(score))
    print("Media: %f" %preds.mean())
    print("Quartil 1: %f" %(np.quantile(preds, 0.25)))
    print("Mediana: %f" %(np.median(preds)))
    print("Quartil 3: %f" %(np.quantile(preds, 0.75)))
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    print("RMSE: %f" % (rmse))
    r2 = r2_score(y_test, preds)
    print("R2: %f" % (r2))

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

