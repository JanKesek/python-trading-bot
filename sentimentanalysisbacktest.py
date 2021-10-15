import pandas as pd
from backtester import Backtester, getPricesFromTimeIntervalCSVData, getOHLCVByFilename, getSinglePriceByPostDateHour


def backtest_btc(dicscores,dataprices,backtester : Backtester):
    for hour in dicscores:
        for curr in dicscores[hour]:
            currentPrice = getSinglePriceByPostDateHour(dicscores[hour][curr][1],dataprices[curr])
            #print(currentPrice)
            if dicscores[hour][curr][0]>2:
                print("BUY " + curr)
                backtester.buy(currentPrice=currentPrice,currency=curr)
            elif dicscores[hour][curr][0]<(-2):
                print("SELL " + curr)
                backtester.sell(currentPrice=currentPrice, currency=curr)
def print_scores(dic):
    s=""
    for h in dic:
        for c in dic[h]:
            if dic[h][c][0]!=0:
                s+= " {}:{} ".format(c,dic[h][c][0])
    print(s)

def backtest(backtester,data):
    backtester.setWallet({'Bitcoin':0,'Dogecoin':0})
    dicbyhour ={}
    currs = data['currency'].unique()
    for index,row in data.iterrows():
        current_hour = row['time']
        current_hour=current_hour.split(":")
        current_hour = current_hour[0]
        if current_hour not in dicbyhour:
            dicbyhour[current_hour]={}
            for curr in currs:
                dicbyhour[current_hour][curr]= [0,current_hour]
        sentiment = row['prediction']
        if sentiment=='positive':
            dicbyhour[current_hour][row['currency']][0]+=(row['number_of_posts'])
        elif sentiment=='negative':
            dicbyhour[current_hour][row['currency']][0]-=(row['number_of_posts'])
        #print("CURRENCY {} SCORE {}".format(row['currency'],dicbyhour[current_hour][row['currency']]))
        #if i%10==0:
            #for curr in currs:
                #makeDecision(dicbyhour[current_hour],current_hour,curr, backtester)
    print_scores(dicbyhour)
    #print(dataprices)
    
    backtest_btc(dicbyhour,dataprices,backtester)
def getName():
    return "Analiza Sentymentalna"
if __name__=='__main__':
    data = pd.read_csv("sentiment.csv")
    dataprices = {
        'Bitcoin':getOHLCVByFilename("BTC-USDT","1h"),
        'Dogecoin':getOHLCVByFilename("DOGE-USDT","1h")
    }
    #print(dataprices)
    #print(data)
    i=0
    currs = data['currency'].unique()
    backtester = Backtester(pricesData=dataprices,initialUSD=2000, timestampData=None)
    backtest(backtester,data)
