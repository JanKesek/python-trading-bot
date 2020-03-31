class Backtester:
    def __init__(self, initialUSD):
        self.balance=initialUSD
        self.wallet=0
        self.buyMeanReverseFlag=0
        self.sellMeanReverseFlag=0
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
    def buy(self,currentPrice):
        self.wallet=self.balance/currentPrice
        self.balance=0
        print("BUY SIGNAL. ASSET: ", self.wallet, " BALANCE: ", self.balance, " CURRENTPRICE: ", currentPrice)
    def sell(self,currentPrice):
        self.balance=self.wallet*currentPrice
        self.wallet=0
        print("SELL SIGNAL. ASSET: ", self.wallet, " BALANCE: ", self.balance, " CURRENTPRICE: ", currentPrice)
    def getBalance(self):
        return self.balance
    def getFlag(self): 
        return self.meanReverseFlag