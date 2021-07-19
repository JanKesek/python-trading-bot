import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import json
import requests 

class HistoryOfTrades:
    def __init__(self) -> None:
        self.history=[]
    def appendBuy(self,price):
        self.history.append({
            "buy":price
        })
    def appendSell(self,price):
        self.history.append({
            "sell":price
        })
class Backtester:
    def __init__(self, initialUSD,pricesData, timestampData):
        self.prices=pricesData
        self.timestamps=timestampData
        self.initial=initialUSD
        self.balance=initialUSD
        self.wallet=0
        self.buyMeanReverseFlag=0
        self.sellMeanReverseFlag=0
        self.historyOfTrades=HistoryOfTrades()
    def simpleBacktest(self,signal, index):
        #print(signal)
        #print("CURRENT PRICE {}".format(self.prices[index]))
        if signal=='buy':
            self.buy(self.prices[index],index)
        elif signal=='sell':
            self.sell(self.prices[index],index)
    def simpleBacktestByPrice(self,signal, price):
        #print(signal)
        #print("CURRENT PRICE {}".format(self.prices[index]))
        if signal=='buy':
            self.buy(price,None)
        elif signal=='sell':
            self.sell(price,None)

    def buyMA(self,currentPrice):
        if self.balance<=0:
             print("BALANCE NOT ENOUGH")
        else:
            self.buy(currentPrice)
            self.wallet=self.balance/currentPrice
            self.balance=0
            #print("BUY SIGNAL. ASSET: ", self.wallet, " BALANCE: ", self.balance, " CURRENTPRICE: ", currentPrice)
    def sellMA(self,currentPrice):
        if self.wallet<=0: print("NO ASSET AVAILABLE")
        else:
            self.sell(currentPrice)
            self.balance=self.wallet*currentPrice
            self.wallet=0
            #print("SELL SIGNAL. ASSET: ", self.wallet, " BALANCE: ", self.balance, " CURRENTPRICE: ", currentPrice)
    def buyMeanReverse(self,currentPrice, transactionTime=None):
        if self.balance<=0:
            pass
            #print("CANNOT BUY ASSET, NO MONEY LEFT")
        else:
            self.buy(currentPrice, time=transactionTime)
    def sellMeanReverse(self,currentPrice, transactionTime=None):
        if self.wallet<=0:
            if self.sellMeanReverseFlag==0:
                self.sellMeanReverseFlag=1
            else:
                self.sellMeanReverseFlag=2
        else:
            self.sellMeanReverseFlag=0
            self.sell(currentPrice,time=transactionTime)
    def buy(self,currentPrice,index=None, time=None):
        if self.balance!=0:
            if self.commission_fee(currentPrice) and self.should(currentPrice,"buy"):
                self.wallet=self.balance/currentPrice
                self.balance=0
                if index == None:
                    self.print_trade_details("BUY",index,price=currentPrice, time=time)
                    #self.historyOfTrades.appendBuy(self.getWealth(0,price=currentPrice))
                    self.historyOfTrades.appendBuy(currentPrice)
                    #self.historyOfTrades.appendBuy(self.getWealth(index))
                else:
                    self.print_trade_details("BUY",index)
                    self.historyOfTrades.appendBuy(self.getWealth(index))

                    #self.historyOfTrades.appendBuy(self.getWealth(index))
    def sell(self,currentPrice,index=None, time=None):
        if self.wallet!=0 and self.should(currentPrice,"sell"):
            if self.commission_fee(currentPrice):
                self.balance=self.wallet*currentPrice
                self.wallet=0
                if index != None:
                    self.print_trade_details("SELL",index)
                    self.historyOfTrades.appendSell(self.getWealth(index))
                else:
                    self.print_trade_details("SELL",index,price=currentPrice, time=time)
                    #self.historyOfTrades.appendSell(self.getWealth(0,price=currentPrice))
                    self.historyOfTrades.appendSell(currentPrice)

    def should(self, currPrice, decision):
        i=len(self.historyOfTrades.history)-1
        while i>=0:
            if decision=="buy":
                if "sell" in self.historyOfTrades.history[i].keys():
                    if self.historyOfTrades.history[i]["sell"]-currPrice*0.01>currPrice:
                        return True
                    return False
            else:
                if "buy" in self.historyOfTrades.history[i].keys():
                    if self.historyOfTrades.history[i]["buy"]+currPrice*0.01<currPrice:
                        return True
                    return False
            i-=1
        return True
    def print_trade_details(self,type,index, price=None, time=None):
        if price == None:
            print(type, " SIGNAL. ASSET: ",self.wallet, " BALANCE: ", self.balance, " CURRENTPRICE: ",self.prices[index])
            print("AT : {}".format(self.timestamps[index]))
        else:
            print(type, " SIGNAL. ASSET: ",self.wallet, " BALANCE: ", self.balance, " CURRENTPRICE: ",price, " AT: ",time, " WALLET: ", self.wallet*price)

    def commission_fee(self,currentPrice):
        fee=currentPrice*0.01
        #wealth=self.getWealth(index)
        if self.balance>=fee:
            self.balance-=fee
            return True
        elif (self.wallet*currentPrice)>=fee:
            #wealth-=fee
            self.wallet=(self.wallet*currentPrice-fee)/currentPrice
            return True
        else:
            return False
    def getPrices(self):
        return self.prices
    def getBalance(self):
        return self.balance
    def getFlag(self): 
        return self.meanReverseFlag
    def getWealth(self,index,price=None):
        if self.balance!=0: return self.balance
        else: 
            if price!= None:
                return self.wallet*price
            return self.wallet*self.prices[index]
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
def getPricesFromTimeIntervalCSVData(data):
    h_from = data.tail(1)['time'].iloc[0]
    h_to = data.head(1)['time'].iloc[0]
    coin_id = "btc-bitcoin"
    url = "https://api.coinpaprika.com/v1/coins/{}/ohlcv/historical?start={}&end={}".format(coin_id, prepare_date_for_paprika_get(h_from), prepare_date_for_paprika_get(h_to))
    print(url)
    data = requests.get(url)
    return data.json()
def getOHLCVByFilename(market, timeframe):
    filename = "data/df/{}/{}_{}.json".format(market,market,timeframe)
    return pd.read_json(filename)
def getOHLCVByFilenameJSON(market, timeframe):
    filename = "data/df/{}/{}_{}.json".format(market,market,timeframe)
    data=None
    with open(filename,'r') as f:
        data= json.load(f)
    return data
def getSinglePriceByPostDateHour(post_hour, data):
    #05/31/2021, 15:18:23
    hour = prepare_date_for_paprika_get(post_hour)
    hour = hour.replace("T"," ").replace("Z", " ")
    valueByHour = data[data['open_time']==hour]
    print(valueByHour)
    return valueByHour.index[0]
def prepare_date_for_paprika_get(d):
    d= d.replace(", ","T")
    date_corrected = correct_date(d.split("T")[0])
    d = d.split(":")[0]
    d = d.replace("/","-")
    d = "{}T{}:00:00Z".format(date_corrected,d.split("T")[1])
    return d
def correct_date(date_to_correct):
    lst = date_to_correct.split("/")
    lst2=[lst[2],lst[0],lst[1]]
    return "-".join(lst2)
    