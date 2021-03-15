from statsmodels.tsa.stattools import adfuller
from backtester import Backtester
from simplestrategies import strategy1, strategy2
class Adaptation:
    def __init__(self,ts,interval=500):
        self.ts=ts
        self.interval=interval
    def simulate(self):
        backtester=Backtester(0.087)
        j=self.interval
        while j<=len(self.ts):
            currData=self.ts[j-self.interval:j]
            #if isStationary(currData):
                #strategy1(currData,)
def isStationary(arr):
    adftest=adfuller(arr,autolag='AIC')
    return adftest[1]<0.05
