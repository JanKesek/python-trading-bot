from finta import TA
import jsonpreprocess as jp
from datetime import datetime, time
import datetime as dt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from statistics import stdev
from statistics import mean
from backtester import Backtester
import math
from missingvalues import (simpleLinearInterpolation, indexCleaningRandom)
class MAStrategy:
    def __init__(self, ts):
        self.ts=ts
    def KAMA(self):
        period=len(self.ts)//2+200
        #period=200
        kama=TA.KAMA(ohlc=self.ts, period=period)
        kamadf=kama.to_frame()
        kamadf.rename(columns={'{} period KAMA.'.format(period): 'close'}, inplace=True)        
        return kamadf
    def EMA(self):
        return TA.EMA(ohlc=self.ts, period=len(self.ts)//2+200)
    def MA(self):
        #TODO in theory it should be MA of returns (Lag1)
        maArr=[0]
        for i in range(1,len(self.ts)+1):
            maArr.append(sum(self.ts['close'][0:i])/i)
        return maArr
class MeanReversion:
    def __init__(self,ts,intervalLength):
        self.ts=ts
        self.shortCounter=0
        self.longCounter=0
        self.intervalLength=intervalLength
    def longLimit(self,t):
        ts = self.ts['close']
        return ts[t-1]/(1+volatility_change(self.ts['low'],self.ts['high'],t))
        #return ts[t-1]/(1+stdev(ts))
    def shortLimit(self,t):
        ts = self.ts['close']
        return ts[t-1]*(1+volatility_change(self.ts['low'],self.ts['high'],t))
        #return ts[t-1]*(1+stdev(ts))
def volatility_change(low,high,t):
    vol_change=abs((low[t] + high[t])-(low[t-1]+high[t-1]))/2
    return vol_change
    
def slopeOfTimeSeries(ama):
    #ama['date_ordinal']=pd.to_datetime(ama['open_time']).map(dt.datetime.toordinal)
    ama=ama.dropna()
    date_ordinal=np.array([i for i in range(len(ama['close'].values))])
    reg=linear_model.LinearRegression()
    reg.fit(np.reshape(date_ordinal,(-1,1)),ama['close'])
    return reg.coef_
def SNRRatio(ama,ts,maobj):
    return slopeOfTimeSeries(ama)/stdev(maobj.MA())
def strategy1(data, backtester,l):
    datalen=len(data)
    #initial balance: 0.087 is 470$ today
    #back=Backtester(0.087)
    mainterval=500
    subdata=data[l:l+mainterval]
    #try:
        #first=datetime.strptime(subdata[0]['open_time'],'%Y-%m-%d %H:%M:%S')
        #last=datetime.strptime(subdata[len(subdata)-1]['open_time'],'%Y-%m-%d %H:%M:%S')
    #except ValueError as ve:
    #    print(ve)
    #print(first,last)
    try:
        #df=jp.convertJSONToDataFrame(subdata,first,last)
        #ma=MAStrategy(df)
        df= data
        ma = MAStrategy(df)
        kama=ma.KAMA()
        #sma=ma.MA()
        #snr=SNRRatio(kama,df,ma)
    #print("Signal To Noise: ",snr)
        #print(df)
        currentPrice=df['close'][l]
        transactionTime = df['open_time'][l]
        #print("CURR {} KAMA {}".format(currentPrice,kama))
        #print("KAMA {} ".format(kama))
        if (currentPrice<kama['close'][l]):
            backtester.buy(currentPrice, time=transactionTime)
        if (currentPrice>kama['close'][l]):
            backtester.sell(currentPrice, time=transactionTime)
    except ValueError as ve:
        print(ve)
    #print("SIMULATION ORDER: ", l, " LENGTH: ", datalen)
    #print(backtester.getBalance())
    return l
def strategy2(data,backtester,j):
    mr=MeanReversion(data, 500)
    l=mr.longLimit(j-1)
    s=mr.shortLimit(j-1)
    i=j
    while i<=j:
        #print(i)
        currentPrice = data['close'][i]
        transactionTime = data['open_time'][i]
        #print("CURR {} L {} S {}".format(currentPrice,l,s))
        if currentPrice>s:
            backtester.sellMeanReverse(currentPrice,transactionTime=transactionTime)
        elif currentPrice<l:
            backtester.buyMeanReverse(currentPrice,transactionTime=transactionTime)
            if backtester.sellMeanReverseFlag==2:
                backtester.sellMeanReverse(currentPrice, transactionTime=transactionTime)
        i+=1
    return i
#def volatility_change(low,high,arr):
#    vol_change=[ ((low+high)-(low+high))/2 for i in range(1,len(arr)) ]
#    return vol_change
def findTrend(data,j):
    pass
def arimaForecast(ts):
    #X=ts['Close'].values
    X=ts['close'][:10000]
    #size=int(len(X)*0.98)
    size=len(X)-100
    train,test=X[0:size],X[size:]
    test_length=len(test)
    preds=[]
    history=[x for x in train]
    backtest=Backtester(2000,X,ts.index)
    print(train)
    backtest.buy(train[len(train)-1])
    bought_at=train[len(train)-1]
    sold_at=None
    i=0
    #print(history)
    #print(test)
    minGlobalDifference=math.inf
    dailyforecast=[]
    globaldiffs=[]
    n_forecast=0
    while i< len(test):
        print(i," : ",test_length)
        if i!=0 and i%24==0:
            plt.delaxes()
            plt.bar(np.arange(len(dailyforecast)),dailyforecast)
            plt.savefig("testingarimaplots/error_histogram{}.png".format(n_forecast))
            print("SUMMARY OF PERIOD MEAN OF DIFFERENCES: {}".format(mean(dailyforecast)))
            if min(dailyforecast)<minGlobalDifference: minGlobalDifference=min(dailyforecast)
            print("STARTING FORECASTING PERIOD (DAY AHEAD)")
            history=history[0:-24]+[x for x in test[i-24:i]]
            dailyforecast=[]
            n_forecast+=1
        print(history)
        model=ARIMA(history,order=(4, 1, 4))
        fit=model.fit(disp=0)
        out=fit.forecast()
        if out[0]>=bought_at*1.18:
            backtest.sell(test[i])
            sold_at=out[0]
        if sold_at!=None:
            if out[0]<=sold_at*0.82:
                backtest.buy(test[i])
                bought_at=out[0]
        if i%100==0:
            print("WEALTH {} ".format(backtest.getWealth(len(train)+i)))
        if backtest.getWealth(len(train)+i)<=53:
            return
        preds.append(out[0])
        print(preds)
        diff=abs(preds[-1]-test[i])
        dailyforecast.append(diff[0])
        globaldiffs.append(diff[0])
        #if diff>=150: history.append(test[i])
        #else: history.append(preds[-1])
        history.append(test[i])
        print("PREDICTED {} EXPECTED {} DIFFERENCE {}".
                format(out[0],test[i], diff[0]))
        i+=1
    plt.plot(preds)
    plt.plot(test)
    plt.show()
    print("RMSE: {}, SMALLEST DIFF BETWEEN REAL AND PREDICTED {} MEAN OF ABSOLUTE DIFFERENCES {}".
            format(mean_squared_error(test,preds),minGlobalDifference,mean(globaldiffs)))
if __name__ == "__main__":
    #filename="data/BTC-USD.json"
    filename="data/df/BTC-USDT/BTC-USDT_1h.json"
    ts=pd.read_json(filename)
    #data=jp.readJSON(filename)
    #data=simpleLinearInterpolation(data)
    #ts=indexCleaningRandom(data)
    #ts=jp.convertJSONToDataFrame(data,ts)
    arimaForecast(ts)