import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
import collections

def menor(pred):
    menor = pred[0]
    for i in pred:
        if i < menor:
            menor = i
    return (menor)

def maior(pred):
    maior = 0
    for i in pred:
        if i > maior:
            maior = i
    return (maior)

def porcentagem(pred,base):
    mais = 0
    for i in pred:
        print(str(base)+" "+str(i))
        if i > base:
            mais=+1
    return ((100/len(pred))*mais)

def moda(pred):
    new = []
    soma = ""
    count = 0
    for i in pred:
        for k in str(i):
            if count<=4:
                soma+=k
                count+=1
        new.append(soma)
        soma = ""
        count = 0
    count = 0    
    counter=collections.Counter(new)
    get = 0
    a = float(get)
    for i in counter:
        return str(i)



data = pd.read_csv('dados_mglu3_11e12-02-2019.csv',sep=';')

print(len(data))
data = pd.DataFrame(data)

for f in data.columns: 
    if data[f].dtype=='object': 
        lbl = preprocessing.LabelEncoder() 
        lbl.fit(list(data[f].values)) 
        data[f] = lbl.transform(list(data[f].values))

X = data[["Indice_de_Força_Relativa","Indice_do_canal_de_commodities","Indice_Direcional_Medio","Oscilador_extraordinario","Momentum","NIvel_MACD","IFR_Estocastico_Rapido","Range_Percentual_de_Williams","Força_Bull_Bear","Oscilador_Definitivo"]]
y = data["Status"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

xg_reg = xgb.XGBRegressor(n_estimators = 1000, learning_rate=0.05)

xg_reg.fit(X_train,y_train)
score = xg_reg.score(X_test, y_test)
preds = xg_reg.predict(X_test)
print(str(menor(preds))+" até "+str(maior(preds)))
print("Alta em "+str(porcentagem(preds,21.77))+"%")
print("Score: %f" %(score))
if score<0.91:
    m = float(moda(preds))
    v = m-(m*((100-(score*100))/1000))
    print("Valor mais provável "+str(v))
    print("Valor mais provável "+str(m))
else:
    print("Valor mais provável "+moda(preds))
print("Media: %f" %preds.mean())
print("Quartil 1: %f" %(np.quantile(preds, 0.25)))
print("Mediana: %f" %(np.median(preds)))
print("Quartil 3: %f" %(np.quantile(preds, 0.75)))
rmse = np.sqrt(mean_squared_error(y_test, preds))
print("RMSE: %f" % (rmse))
r2 = r2_score(y_test, preds)
print("R2: %f" % (r2))


