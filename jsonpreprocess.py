import pandas as pd
import requests
from datetime import datetime
from datetime import timedelta
import numpy as np
def convertJSONToDataFrame(jsonobj,startD=datetime(2019,1,1), endD=datetime(2019,12,22)):
	ts=pd.DataFrame(index=pd.date_range(startD,endD))
	prices=[float(d["close"]) for d in jsonobj]
	ts["Today"]=prices
	ts["Volume"]=[float(d["volume"]) for d in jsonobj]
	for i in range(0,5): ts["Lag{}".format(i+1)]=ts["Today"].shift(i+1)
	return ts
def getJSONObjectCP(symbol,startDate="2019-01-01",endDate="2019-12-22"):
	r=requests.get("https://api.coinpaprika.com/v1/coins/"+symbol+"/ohlcv/historical?start="+startDate+"&end="+endDate)
	return r.json()
def timeSeriesReturns(ts,startD=datetime(2019,1,1)):
	tsret=pd.DataFrame(index=ts.index)
	tsret["Volume"]=ts["Volume"]
	tsret["Today"]=ts["Today"].pct_change()*100.0
	tsret["Today"][0]=0.0001
	for i,x in enumerate(tsret["Today"]):
		if(abs(x)<0.0001): tsret["Today"][i]=0.0001
	for i in range(0,5):
		tsret["Lag{}".format(i+1)]=ts["Lag{}".format(i+1)].pct_change()*100.0
	tsret["Direction"]=np.sign(tsret["Today"])
	deleteNans=startD+timedelta(days=6)
	tsret=tsret[tsret.index>=deleteNans]
	return tsret
