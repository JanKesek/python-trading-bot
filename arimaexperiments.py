import pandas
import math
import numpy as np
from statistics import mean,stdev
from matplotlib import pyplot as plt
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error,mean_absolute_error,max_error
import matplotlib.pyplot as plt

def estimateParameters(ts):
    aic=math.inf
    minPDQ=(0,0)
    for i in range(5):
        for j in range(5):
            print(i,j)
            print(aic, minPDQ)
            model=sm.tsa.ARIMA(ts,order=(i,1,j))
            result=model.fit(disp=0)
            if result.aic < aic:
                aic=result.aic
                minPDQ=(i,j)
    return (minPDQ[0],1,minPDQ[1])
def AR(ts,n_lags=10):
    corr=[]
    covariances=[]
    for i in range(1,n_lags):
        print(i)
        covariances.append(covariance(ts,i))
        samplestdev=stdev(ts.iloc[i:])
        corr.append(covariances[-1]/(samplestdev**2))
        #for j in range(len(ts)-i):
        #    print(i,j)
        #    s+= ts[j]*ts[j+i]
        #corr.append(s/(len(ts)-i))
    return corr
def estimateModel(preds_filepath,data):
    with open(preds_filepath,'rb') as f:
        preds=np.load(f,allow_pickle=True)
    print(preds, len(preds))
    trueX=data[len(data)-25:]
    preds=preds[len(preds)-25:]
    assert(len(trueX)==len(preds))
    #trueX=data[len(data)-(len(preds)+1):-1]
    preds=np.array(preds).reshape((-1,1))
    trueX=np.array(trueX).reshape((-1,1))
    print("RMSE: {} MAE: {} MAX_ERROR: {}".format(
        mean_squared_error(trueX,preds),
        mean_absolute_error(trueX,preds),
        max_error(trueX,preds))
    )
    plt.plot(trueX, label="Prawdziwe wartości")
    plt.plot(preds,label="Przewidziane wartości")
    plt.legend()
    plt.show()
def covariance(ts,lag):
    cov=0
    sample=ts.iloc[lag:]
    samplemean=mean(sample)
    for i in range(len(sample)):
        cov+=sample.iloc[i]-samplemean
    return cov/len(sample)-1
if __name__ == "__main__":
    data=pandas.read_json("data/df/BTC-USDT/BTC-USDT_1h.json")
    ts=data['high'].values
    #modelvars = estimateModel("data/df/BTC-USDT/predicted100values.npy",ts)
    #print(modelvars)
    print(estimateParameters(data['close'][:10000]))
    #print(data['high'].iloc[0])
    #corr=AR(data['high'])
    #print(corr)
    #plt.plot(corr)
    #plt.show()