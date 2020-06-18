from datetime import (datetime, timedelta)
import pandas as pd
import random

def calculateDatetimeIndex(jsonobj,freq='1H'):
	startD=datetime.strptime(jsonobj[0]['open_time'],'%Y-%m-%d %H:%M:%S')
	endD=datetime.strptime(jsonobj[-1]['open_time'],'%Y-%m-%d %H:%M:%S')
	index=pd.date_range(startD,endD, freq=freq)
	return index
def indexCleaningRandom(obj,freq='1H'):
	index=calculateDatetimeIndex(obj, freq=freq)
	print("NUMBER OF TIME UNITS " , len(obj))
	print("NUMBER OF INDEX UNITS ", len(index))
	#print(index)
	while len(obj)!=len(index):
		#print(len(obj))
		obj.remove(obj[random.randint(0,len(obj)-1)])
	return index
def indexCleaning(jsonobj, freq='1H'):
	index=calculateDatetimeIndex(jsonobj, freq)
	times=[o['open_time'] for o in jsonobj]
	timesindex=[str(time) for time in index]
	print(timesindex[0:20])
	print(times[0:20])
	print(len(times), len(timesindex))
	nans=[]
	hoursonly=[d[:-6] for d in times]
	for time in timesindex:
		if time[:-6] not in hoursonly:
			nans.append(time)
	while len(times)!=len(timesindex):
		timesindex.remove(nans[-1])
		nans=nans[:-1]
	print(len(times), len(timesindex))
	datetimes=[datetime.strptime(t,'%Y-%m-%d %H:%M:%S') for t in timesindex]
	return pd.Index(datetimes, dtype='datetime64[ns]')
def simpleLinearInterpolation(obj):
	i=0
	while i<(len(obj))-1:
		tdelta=datetime.strptime(obj[i+1]['open_time'],'%Y-%m-%d %H:%M:%S')-datetime.strptime(obj[i]['open_time'],'%Y-%m-%d %H:%M:%S')
		j=1
		if tdelta.seconds>3600:
			hours_missing=int(tdelta.seconds/60/60)
			secs1=datetime.strptime(obj[i]['open_time'],'%Y-%m-%d %H:%M:%S')-datetime(1970,1,1)
			secs2=datetime.strptime(obj[i+1]['open_time'],'%Y-%m-%d %H:%M:%S')-datetime(1970,1,1)
			while j<hours_missing:
				dic={}
				for k in ['close','low','high','volume']:
					dic[k]=float(obj[i][k])+((secs1.seconds+(3600*j))-secs1.seconds)/(secs2.seconds-secs1.seconds)*(float(obj[i+1][k])-float(obj[i][k]))
				next_hour=datetime(1970,1,1)+(secs1+timedelta(hours=((3600*j)/60/60)))
				dic['open_time']=datetime.strftime(next_hour,'%Y-%m-%d %H:%M:%S')
				obj=obj[:i]+[dic]+obj[i:]
				j+=1				
		i+=j
	return obj
