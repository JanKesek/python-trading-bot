from statsmodels.tsa.stattools import adfuller
from backtester import Backtester, getOHLCVByFilename, getOHLCVByFilenameJSON
from simplestrategies import strategy1, strategy2
class Adaptation:
    def __init__(self,ts,backtester,index=None, market=None, interval=500):
        self.ts=ts
        self.interval=interval
        self.backtester= backtester
        self.market=market
        self.index=index
    def setIndex(self,index):
        self.index=index
    def simulate(self):
        #backtester=Backtester(0.087)
        #backtester = Backtester(initialUSD=2000,pricesData=self.ts,timestampData=None)
        backtester = self.backtester
        j=self.interval
        if self.index != None:
            j=self.index-self.interval
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
def getName():
    return "Strategia adaptacyjna"
if __name__=='__main__':
    data = getOHLCVByFilename("BTC-USDT",'1h')
    adaptation = Adaptation(data, backtester= Backtester(initialUSD=2000,pricesData=data,timestampData=None))
    adaptation.simulate()