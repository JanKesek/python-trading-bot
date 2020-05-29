import pandas as pd
import json
import csv
import requests
from datetime import datetime
from datetime import timedelta
from pandas import concat
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import ccxt
import pprint
from backtester import Backtester
def toSupervised(data, lag=1):
	columns = [data.shift(i) for i in range(1, lag+1)]
	columns.append(data)
	data = concat(columns, axis=1)
	data.fillna(0, inplace=True)
	return data.set_axis(["Volume", "Today","Lag1", "Lag2","Lag3","Lag4","Lag5","Direction1",
				  "VolumeT","Tomorrow","Lag12", "Lag22","Lag32","Lag42","Lag52","Direction2"],axis=1, inplace=False)

def checkDatetimeConsistency(jsonobj, index):
	dates=[d['open_time'] for d in jsonobj]
	print(index)
	for i in range(len(index)): 
		if index[i] not in dates: 
			#index=index.delete(datetime.strprime(d,'%Y-%m-%d %I:%M:%S'))
			index=index.delete(i)
	return index
def convertJSONToDataFrame(jsonobj,startD=datetime(2019,1,1), endD=datetime(2019,12,22), otherVariables=[]):
	#ts=pd.DataFrame(index=pd.date_range(startD,endD))
	index=pd.date_range(startD,endD, freq='1T')
	ts=pd.DataFrame(index=index)
	prices=[float(d['close']) for d in jsonobj]
	#index=checkDatetimeConsistency(jsonobj, index)
	#print("Object length: ", len(jsonobj),"Index: ", len(index), " Length: ", len(prices))
	ts["close"]=prices
	for v in otherVariables: ts[v]=[float(d[v]) for d in jsonobj]
	#ts["DailyLow"]=[float(d["low"]) for d in jsonobj]
	#ts["DailyHigh"]=[float(d["high"]) for d in jsonobj]
	for i in range(0,5): ts["Lag{}".format(i+1)]=ts["close"].shift(i+1)
	return ts
def getJSONObjectCP(symbol,startDate="2019-01-01",endDate="2020-01-09"):
	r=requests.get("https://api.coinpaprika.com/v1/coins/"+symbol+"/ohlcv/historical?start="+startDate+"&end="+endDate)
	return r.json()
def timeSeriesReturns(ts,pct_change=False,startD=datetime(2019,1,1)):
	tsret=pd.DataFrame(index=ts.index)
	tsret["Volume"]=ts["Volume"]
	#or percent change * 100
	if pct_change==True: tsret["Today"]=ts["Today"].pct_change()*100.0
	else: tsret["Today"]=ts["Today"].diff()
	tsret["Today"][0]=0.0001
	for i,x in enumerate(tsret["Today"]):
		if(abs(x)<0.0001): tsret["Today"][i]=0.0001
	for i in range(0,5):
		if pct_change==True: tsret["Lag{}".format(i+1)]=ts["Lag{}".format(i+1)].pct_change()*100.0
		else: tsret["Lag{}".format(i+1)]=ts["Lag{}".format(i+1)].diff()
	tsret["Direction"]=np.sign(tsret["Today"])
	deleteNans=startD+timedelta(days=6)
	tsret=tsret[tsret.index>=deleteNans]
	return tsret
def scale(train, test):
	# fit scaler
	scaler = MinMaxScaler(feature_range=(-1, 1))
	scaler = scaler.fit(train)
	# transform train
	train = train.values.reshape(train.shape[0], train.shape[1])
	train_scaled = scaler.transform(train)
	# transform test
	test = test.values.reshape(test.shape[0], test.shape[1])
	test_scaled = scaler.transform(test)
	return scaler, train_scaled, test_scaled
def csvToJson(csvFName):
	jsonLst=[]
	i=0
	with open(csvFName, 'r') as csvF:
		csvR=csv.reader(csvF)
		for rows in csvR:
			if i!=0:
				print(rows)
				rowDict = {
					'open_time': str(pd.to_datetime(rows[0], unit='ms')),
				 	'open' : float(rows[1]),
				 	'high' : float(rows[2]),
					'low'  : float(rows[3]),
					'close' : float(rows[4]),
					'volume' : float(rows[5]),
				 'close_time' : str(pd.to_datetime(rows[6], unit='ms')),
				 'quote_asset_volume' : rows[7],
				 'number_of_trades' : rows[8],
				 'taker_buy_base_asset_volume': rows[9],
				 'taker_buy_quote_asset_volume': rows[10],
				 'ignore': rows[11]
				}
				print(rowDict)
				jsonLst.append(rowDict)
			i+=1
			#if i>=200: break
	with open('LINK-BTC.json', 'w') as outfile:
		json.dump(jsonLst, outfile)
	return jsonLst
def debloatJSON(jsonFileName, importantVars):
	debloatedJSON=[]
	with open(jsonFileName) as json_file:
		data = json.load(json_file)
		i=0
		l=len(data)
		for p in data:
			print(i, " - ", l)
			i+=1
			jsonDict={}
			for var in importantVars: jsonDict[var]=p[var]
			debloatedJSON.append(jsonDict)
	with open('LINK-BTCShort.json', 'w') as outfile:
		json.dump(debloatedJSON, outfile)
def readJSON(jsonFileName):
	jsonObj=[]
	with open(jsonFileName) as json_file:
		data = json.load(json_file)
		for p in data: jsonObj.append(p)
	return jsonObj
def actualizeJSON(jsonObj,filename,symbol='LINK/BTC',timeframe='1m'):
	binance=ccxt.binance()
	currentTime=(datetime.now()-timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
	since=jsonObj[-1]['open_time']
	previousTime=since
	while since[:-3]!=currentTime[:-3]:
		since=since.replace(" ", "T")
		candles = binance.fetch_ohlcv(symbol=symbol, timeframe=timeframe, since=binance.parse8601(since),limit=1000)
		for c in candles:
			openTime=binance.iso8601(c[0])[:-5]
			#https://github.com/ccxt/ccxt/wiki/Manual look chapter: OHLCV Structure for return parameters
			openTime=openTime.replace("T", " ")
			#i need VOL,H,L for rule-based systems lets leave it for now. Short version only have close
			newPrice={'open_time': openTime, 'high': c[2], 'low': c[3],'close': c[4], 'volume': c[5] }
			#print(open_time)
			jsonObj.append(newPrice)
		since=jsonObj[-1]['open_time']
		print(currentTime[:-3], " : ", since[:-3])
		if previousTime==since: break
		else: previousTime=since
	with open(filename, 'w') as outfile:
		json.dump(jsonObj, outfile)
	return


if __name__ == "__main__":
	from rulebased.rulebasedsystem import RBS
	#filename="LINK-BTCShort.json"
	filename="BTC-USD.json"
	jsonObj=readJSON(filename)
	pricesBacktest=[obj['close'] for obj in jsonObj]
	#print(load_from_file())
	rbs=RBS()
	#rbs.calculate_rv(jsonObj)
	#rbs.calculate_volatilty()
	#rbs.calculate_wbb()
	#rbs.save_rbs_obj_to_json()

	#rbs.calculate_wbb()
	rbs.load_from_file()
	rbs.start()
	rbs.find_in_groups("Plus_ETA_Big")
	rbs.find_in_groups("Minus_ETA_Big")
	rbs.find_in_groups("Plus_C_Big")
	rbs.find_in_groups("Minus_C_Big")
	signals=rbs.finaldecisions
	tester=Backtester(500, pricesBacktest)
	for s in signals:
		tester.simpleBacktest(s[0],s[1])
	#print("WALLET: {} BALANCE: {} WEALTH {}".format(tester.wallet,tester.balance, tester.getWealth()))
	#rbs.calculate_wbb()
	#actualizeJSON(jsonObj,filename,symbol="BTC/USDT", timeframe='1h')
