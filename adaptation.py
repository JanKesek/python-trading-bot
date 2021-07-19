from statsmodels.tsa.stattools import adfuller
from backtester import Backtester, getOHLCVByFilename, getOHLCVByFilenameJSON
from simplestrategies import strategy1, strategy2
class Adaptation:
    def __init__(self,ts,interval=500):
        self.ts=ts
        self.interval=interval
    def simulate(self):
        #backtester=Backtester(0.087)
        backtester = Backtester(initialUSD=2000,pricesData=self.ts,timestampData=None)
        j=self.interval
        while j<len(self.ts):
            currData=self.ts[j-self.interval:j]
            if isStationary(currData['close']):
                #print(j)
                #print(currData)
                strategy1(currData,backtester,j-1)
            else:
                #rint(j)
                #print(currData)
                strategy2(currData,backtester,j-1)
            j+=1

def isStationary(arr):
    adftest=adfuller(arr,autolag='AIC')
    return adftest[1]<0.05

if __name__=='__main__':
    data = getOHLCVByFilename("BTC-USDT",'1h')
    adaptation = Adaptation(data)
    adaptation.simulate()