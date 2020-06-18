import pickle
from jsonpreprocess import (actualizeJSON, readJSON,convertJSONToDataFrame)
from missingvalues import (simpleLinearInterpolation,indexCleaningRandom)
import os
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
	ts=convertJSONToDataFrame(jsonObj,indexCleaningRandom(jsonObj,timeframe))
	if not os.path.isdir('data/df/'+dirname):
		os.makedirs('data/df/'+dirname)
	with open('data/df/'+dirname+'/'+filename, 'wb') as dataframefile:
		pickle.dump(ts, dataframefile)
def getDataFrameForTk(filename):
	with open(filename,'rb') as pfile:
		ts=pickle.load(pfile)
	return ts[-30:]