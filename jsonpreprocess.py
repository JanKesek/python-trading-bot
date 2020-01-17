import pandas as pd
import requests
from datetime import datetime
from datetime import timedelta
from pandas import concat
import numpy as np
from sklearn.preprocessing import MinMaxScaler
def toSupervised(data, lag=1):
	columns = [data.shift(i) for i in range(1, lag+1)]
	columns.append(data)
	data = concat(columns, axis=1)
	data.fillna(0, inplace=True)
	return data.set_axis(["Volume", "Today","Lag1", "Lag2","Lag3","Lag4","Lag5","Direction1",
				  "VolumeT","Tomorrow","Lag12", "Lag22","Lag32","Lag42","Lag52","Direction2"],axis=1, inplace=False)

def convertJSONToDataFrame(jsonobj,startD=datetime(2019,1,1), endD=datetime(2019,12,22)):
	ts=pd.DataFrame(index=pd.date_range(startD,endD))
	prices=[float(d["close"]) for d in jsonobj]
	ts["Today"]=prices
	ts["Volume"]=[float(d["volume"]) for d in jsonobj]
	for i in range(0,5): ts["Lag{}".format(i+1)]=ts["Today"].shift(i+1)
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