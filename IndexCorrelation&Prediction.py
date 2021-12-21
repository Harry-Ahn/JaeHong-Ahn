#!/usr/bin/env python
# coding: utf-8

# In[265]:


from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import requests
import seaborn as sb
from fbprophet import Prophet

url = 'https://finance.yahoo.com/world-indices/'
df_list = pd.read_html(requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text)

majorStockIdx = df_list[0]

tickerData = yf.Ticker('^GSPC')
tickerDf1 = tickerData.history(period='1d', start='2000-1-1', end='2021-12-18')

SnP=[]
for s in majorStockIdx.Symbol: 
    if s in ['^GSPC']:
        tickerData = yf.Ticker(s)
        tickerDf1 = tickerData.history(period='1d', start='2000-1-4', end='2021-12-18')
        tickerDf1['ticker'] = s 
        SnP.append(tickerDf1)
SnP500=pd.concat(SnP, axis=0)   

ND=[]
for s in majorStockIdx.Symbol: 
    if s in ['^DJI']:
        tickerData = yf.Ticker(s)
        tickerDf1 = tickerData.history(period='1d', start='2000-1-4', end='2021-12-18')
        tickerDf1['ticker'] = s 
        ND.append(tickerDf1)
Nasdaq=pd.concat(ND, axis=0)   
        
DJ=[]
for s in majorStockIdx.Symbol: 
    if s in ['^IXIC']:
        tickerData = yf.Ticker(s)
        tickerDf1 = tickerData.history(period='1d', start='2000-1-4', end='2021-12-18')
        tickerDf1['ticker'] = s
        DJ.append(tickerDf1)
DowJones=pd.concat(DJ, axis=0)   

RUS=[]
for s in majorStockIdx.Symbol: 
    if s in ['^RUT']:
        tickerData = yf.Ticker(s)
        tickerDf1 = tickerData.history(period='1d', start='2000-1-4', end='2021-12-18')
        tickerDf1['ticker'] = s 
        RUS.append(tickerDf1)
Russell2000=pd.concat(RUS, axis=0)
    
KOR = []
for s in majorStockIdx.Symbol: 
    if s in ['^KS11']:
        tickerData = yf.Ticker(s)
        tickerDf1 = tickerData.history(period='1d', start='2000-1-4', end='2021-12-18')
        tickerDf1['ticker'] = s 
        KOR.append(tickerDf1)
Kospi = pd.concat(KOR, axis = 0)        


plt.plot(SnP500['Close'],label='S&P 500',color='r')
plt.legend()
plt.xlabel('Date')
plt.ylabel('Index')
plt.show()

plt.plot(DowJones['Close'],label='Dow Jones',color='b')
plt.legend()
plt.xlabel('Date')
plt.ylabel('Index')
plt.show()

plt.plot(Nasdaq['Close'],label='NASDAQ',color='g')
plt.legend()
plt.xlabel('Date')
plt.ylabel('Index')
plt.show()

plt.plot(Russell2000['Close'],label='Russell 2000',color='c')
plt.legend()
plt.xlabel('Date')
plt.ylabel('Index')
plt.show()

plt.plot(Kospi['Close'],label='KOSPI',color='m')
plt.legend()
plt.xlabel('Date')
plt.ylabel('Index')
plt.show()

Indices = pd.concat([SnP500, DowJones,Nasdaq,Russell2000,Kospi],axis=1)
Indices=Indices[['Close']]
Indices.columns=['S&P 500','Dow Jones', 'NASDAQ', 'Russell 2000', 'KOSPI']
plt.title('Correlation Table')
sb.heatmap(data=Indices.corr(), annot=True, fmt ='.2f', linewidths=.5, cmap='Blues')
plt.show()


# In[266]:


Kospi['MA5']=Kospi['Close'].shift(1).rolling(window=5).mean()
Kospi['MA20']=Kospi['Close'].shift(1).rolling(window=20).mean()
Kospi['MA60']=Kospi['Close'].shift(1).rolling(window=60).mean()
Kospi['MA120']=Kospi['Close'].shift(1).rolling(window=120).mean()
Kospi['MA240']=Kospi['Close'].shift(1).rolling(window=240).mean()

Kospi=Kospi.dropna()

X=Kospi[['MA5','MA20','MA60','MA120','MA240']]
y=Kospi[['Close']]

training=0.75
t=int(training*len(Kospi))

X_train=X[:t]
y_train=y[:t]

X_test=X[t:]
y_test=y[t:]

model = LinearRegression().fit(X_train,y_train)

Kospi1=Kospi['Close']
Kospi1 = Kospi1.reset_index()
Kospi1.columns=['ds','y']

predicted_price=model.predict(X_test)
predicted_price=pd.DataFrame(predicted_price,index=y_test.index, columns = ['price'])
R_squared_score = model.score(X[t:],y[t:])*100
accuracy = ("{0:.2f}".format(R_squared_score))
plt.title(f'Accuracy: {accuracy} %')
plt.plot(predicted_price, color='r')
plt.plot(y_test, color='b')
plt.legend(['Predicted', 'Actual'])
plt.ylabel("Index Price")
plt.show()


# In[262]:


model1=Prophet(changepoint_prior_scale=0.3,
               daily_seasonality=True,
              yearly_seasonality=True)
model1.fit(Kospi1)
future_data=model1.make_future_dataframe(periods=365,freq='D')
forecast_data=model1.predict(future_data)
model1.plot(forecast_data, xlabel='Date', ylabel = 'Index')
plt.show()


# In[267]:



Indices=Indices.dropna()

X=Indices[['S&P 500','Dow Jones', 'NASDAQ', 'Russell 2000']]
y=Indices[['KOSPI']]

training=0.85
t=int(training*len(Indices))

X_train=X[:t]
y_train=y[:t]

X_test=X[t:]
y_test=y[t:]

model = LinearRegression().fit(X_train,y_train)
    
predicted_price=model.predict(X_test)
predicted_price=pd.DataFrame(predicted_price,index=y_test.index, columns = ['price'])
R_squared_score = model.score(X[t:],y[t:])*100
accuracy = ("{0:.2f}".format(R_squared_score))
plt.title(f'Accuracy: {accuracy}%')
plt.plot(predicted_price, color='r')
plt.plot(y_test, color='b')
plt.legend(['Predicted', 'Actual'])
plt.ylabel("Index Price")
plt.show()


# In[ ]:




