from finta import TA
import jsonpreprocess as jp
from datetime import datetime
import datetime as dt
from sklearn import linear_model
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from statistics import stdev
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
def slopeOfTimeSeries(ama):
    #ama['date_ordinal']=pd.to_datetime(ama['open_time']).map(dt.datetime.toordinal)
    ama=ama.dropna()
    date_ordinal=np.array([i for i in range(len(ama['close'].values))])
    reg=linear_model.LinearRegression()
    reg.fit(np.reshape(date_ordinal,(-1,1)),ama['close'])
    return reg.coef_
def SNRRatio(ama,ts,maobj):
    return slopeOfTimeSeries(ama)/stdev(maobj.MA())
def strategy1(data):
    l=0
    while l<=(len(data)-1002):
        subdata=data[l:l+1000]
        first=datetime.strptime(subdata[0]['open_time'],'%Y-%m-%d %H:%M:%S')
        last=datetime.strptime(subdata[len(subdata)-1]['open_time'],'%Y-%m-%d %H:%M:%S')
        #print(first,last)
        df=jp.convertJSONToDataFrame(subdata,first,last)
        ma=MAStrategy(df)
        kama=ma.KAMA()
        sma=ma.MA()
        snr=SNRRatio(kama,df,ma)
        #print("Signal To Noise: ",snr)
        if (df['close'][len(df)-1]<kama['close'][len(kama)-1]) and snr<0.0001: print("Buy")
        if (df['close'][len(df)-1]>kama['close'][len(kama)-1]) and snr<0.0001: print("Sell")
        l+=1000

if __name__ == "__main__":
    data=jp.readJSON("LINK-BTCShort.json")
    strategy1(data)
    #print(data[len(data)-1])
    #subdata=data[0:1000]
    #first=datetime.strptime(subdata[0]['open_time'],'%Y-%m-%d %I:%M:%S')
    #last=datetime.strptime(subdata[len(subdata)-1]['open_time'],'%Y-%m-%d %I:%M:%S')
    #print(first,last)
    #df=jp.convertJSONToDataFrame(subdata,first,last)
    #plt.plot(df)
    #plt.plot(sma)
    #plt.plot(kama)
    #plt.show()