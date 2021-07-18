import pandas as pd
from backtester import Backtester, getPricesFromTimeIntervalCSVData, getOHLCVByFilename, getSinglePriceByPostDateHour


def makeDecision(postsfromhour, current_hour, currency, backtester):
    score = postsfromhour[currency]
    signal = "hold"
    if score>5:
        signal = "buy"
    else:
        signal="sell"
    backtester.simpleBacktestByPrice(signal,getSinglePriceByPostDateHour(current_hour,backtester.getPrices()))
if __name__=='__main__':
    data = pd.read_csv("sentiment.csv")
    dataprices = getOHLCVByFilename("BTC-USDT","1h")
    print(dataprices)
    dicbyhour ={}
    print(data)
    i=0
    currs = data['currency'].unique()
    backtester = Backtester(pricesData=dataprices,initialUSD=2000, timestampData=None)
    for index,row in data.iterrows():
        current_hour = row['time']
        current_hour=current_hour.split(":")
        current_hour = current_hour[0]
        if current_hour not in dicbyhour:
            dicbyhour[current_hour]={}
            for curr in currs:
                dicbyhour[current_hour][curr]= 0
        sentiment = row['prediction']
        if sentiment=='positive':
            dicbyhour[current_hour][row['currency']]+=1
        elif sentiment=='negative':
            dicbyhour[current_hour][row['currency']]-=1
        if i%10==0:
            for curr in currs:
                makeDecision(dicbyhour[current_hour],current_hour,curr, backtester)
    #print(dicbyhour)
