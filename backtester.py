import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

class Backtester:
    def __init__(self, initialUSD,pricesData, timestampData):
        self.prices=pricesData
        self.timestamps=timestampData
        self.initial=initialUSD
        self.balance=initialUSD
        self.wallet=0
        self.buyMeanReverseFlag=0
        self.sellMeanReverseFlag=0
        self.historyOfTrades=[]
    def simpleBacktest(self,signal, index):
        #print(signal)
        #print("CURRENT PRICE {}".format(self.prices[index]))
        if signal=='buy':
            self.buy(self.prices[index],index)
        elif signal=='sell':
            self.sell(self.prices[index],index)

    def buyMA(self,currentPrice):
        if self.balance<=0: print("BALANCE NOT ENOUGH")
        else:
            self.buy(currentPrice)
            self.wallet=self.balance/currentPrice
            self.balance=0
            print("BUY SIGNAL. ASSET: ", self.wallet, " BALANCE: ", self.balance, " CURRENTPRICE: ", currentPrice)
    def sellMA(self,currentPrice):
        if self.wallet<=0: print("NO ASSET AVAILABLE")
        else:
            self.sell(currentPrice)
            self.balance=self.wallet*currentPrice
            self.wallet=0
            print("SELL SIGNAL. ASSET: ", self.wallet, " BALANCE: ", self.balance, " CURRENTPRICE: ", currentPrice)
    def buyMeanReverse(self,currentPrice):
        if self.balance<=0:
            print("CANNOT BUY ASSET, NO MONEY LEFT")
        else:
            sell.buy(currentPrice)
    def sellMeanReverse(self,currentPrice):
        if self.wallet<=0:
            if self.sellMeanReverseFlag==0:
                self.sellMeanReverseFlag=1
            else:
                self.sellMeanReverseFlag=2
        else:
            self.sellMeanReverseFlag=0
            self.sell(currentPrice)
    def buy(self,currentPrice,index):
        if self.balance!=0:
            if self.commission_fee(currentPrice):
                self.wallet=self.balance/currentPrice
                self.balance=0
                self.print_trade_details("BUY",index)
                self.historyOfTrades.append(self.getWealth(index))
    def sell(self,currentPrice,index):
        if self.wallet!=0:
            if self.commission_fee(currentPrice):
                self.balance=self.wallet*currentPrice
                self.wallet=0
                self.print_trade_details("SELL",index)
                self.historyOfTrades.append(self.getWealth(index))
    def print_trade_details(self,type,index):
            print(type, " SIGNAL. ASSET: ",self.wallet, " BALANCE: ", self.balance, " CURRENTPRICE: ",self.prices[index])
            print("AT : {}".format(self.timestamps[index]))
    def commission_fee(self,currentPrice):
        fee=currentPrice*0.01
        #wealth=self.getWealth(index)
        if self.balance>=fee:
            #self.balance-=fee
            return True
        elif (self.wallet*currentPrice)>=fee:
            #wealth-=fee
            #self.wallet=(self.wallet*currentPrice-fee)/currentPrice
            return True
        else: return False
    def getBalance(self):
        return self.balance
    def getFlag(self): 
        return self.meanReverseFlag
    def getWealth(self,index):
        if self.balance!=0: return self.balance
        else: return self.wallet*self.prices[index]
    def plotTradeHistory(self):
        fig,ax1=plt.subplots()
        print("ALL MY TRADES: ")
        #for i in self.historyOfTrades: print(i)
        mindom=1
        maxdom=len(self.historyOfTrades)
        ax1.hist([self.historyOfTrades])
        ax1.set_xlim(mindom,maxdom)
        plt.tight_layout()
        plt.show()