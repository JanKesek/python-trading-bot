import pickle
from jsonpreprocess import (actualizeJSON, readJSON,convertJSONToDataFrame)
from missingvalues import (simpleLinearInterpolation,indexCleaningRandom)
import os
import json
def guiDownloadNewPair(symbol):
	for tframe in ['1h','1d','1M']:
		obj, filename=actualizeJSON(symbol=symbol,timeframe=tframe)
		setDataFrameForTk(filename, obj)
def setDataFrameForTk(filename,jsonObj=None):
	datafilename="data/"+filename
	if jsonObj==None:
		jsonObj=readJSON(datafilename)
	jsonObj=simpleLinearInterpolation(jsonObj)
	dirname=filename.split('_')[0]
	timeframe=filename.split("_")[1].split('.')[0]	
	#ts=convertJSONToDataFrame(jsonObj,indexCleaningRandom(jsonObj,timeframe))
	if not os.path.isdir('data/df/'+dirname):
		os.makedirs('data/df/'+dirname)
	with open('data/df/'+dirname+'/'+filename, 'w') as dataframefile:
		json.dump(jsonObj,dataframefile)
	#	pickle.dump(ts, dataframefile)
def getDataFrameForTk(filename):
	timeframe=filename.split("_")[1].split('.')[0]
	with open(filename,'r') as jsonfile:
		jsonObj=json.load(jsonfile)
	ts=convertJSONToDataFrame(jsonObj,indexCleaningRandom(jsonObj,timeframe))
	return ts[-30:]
