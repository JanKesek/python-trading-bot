import pickle
from jsonpreprocess import (actualizeJSON, readJSON,convertJSONToDataFrame)
from missingvalues import (simpleLinearInterpolation,indexCleaningRandom)
import os
import json
import requests

def guiDownloadNewPair(symbol):
	print("DOWNLOADING SYMBOL: ",symbol)
	if not os.path.isdir('data/'):
		os.makedirs('data/')
	if not os.path.isdir('data/df/'):
		os.makedirs('data/df/')
	for tframe in ['1h','1d','1M']:
		obj, filename=actualizeJSON(symbol=symbol,timeframe=tframe)
		setDataFrameForTk(filename, obj)
	print("PAIR DOWNLOADED. RESET PROGRAM TO USE IT")
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
def fetchall_api():
	items_obj = requests.get("http://localhost:9095/user").json()
	text = ""
	for k in items_obj:
		text += k['username'] + " "
	return text
def fetch_markets_bitbay():
	markets = requests.get("https://api.bitbay.net/rest/trading/ticker")
	return list(markets.json()['items'].keys())
def buy_bitbay(amount,price, market):
	print(amount,price, market)
	if amount is None or price is None:
		return
	buy_object = {
		'amount': amount,
		'price': price,
		'offerType':'BUY',
		'rate':None,
		'postOnly':True,
		'mode':'market',
		'fillOrKill':False
	}
	print(buy_object)
	req = requests.post("http://localhost:9095/crypto/buy/{}".format(market),json=buy_object)
	status = req.status_code
	print(req.text, status)
def register_api_key(login, pubkey, privkey):
	api_key_request = {'login':login,'publicKey':pubkey,'privateKey':privkey}
	response = requests.post("http://localhost:9095/account/register",json=api_key_request)
	status = response.status_code
	print(response.text, status)