#from marketCapScan import midMarketCapCurr
import requests, ccxt
from datetime import datetime, timedelta
import pickler
import historicalDataScraper as hDS
cap=ccxt.coinmarketcap().fetch_currencies()
def circulatingToTotalRatio(currencies):
	goodRatio = []
	for symbol in currencies:
		if symbol in cap.keys():
			circSupp=cap[symbol]['info']['available_supply']
			totalSupp=cap[symbol]['info']['total_supply']
			#print(symbol, " => ", circSupp, " => ", totalSupp, "\n")
			if float(circSupp)>(float(totalSupp)/4):
				#print("GOTCHA") 
				if symbol not in goodRatio: goodRatio.append(symbol)
	return goodRatio
def circulatingTo24HVolRatio(currencies):
	lst=[]
	for symbol in currencies:
		req=requests.get("https://api.coingecko.com/api/v3/coins/" + symbol.lower()+ "/market_chart?vs_currency=usd&days=360")
		if req.status_code==200:
			obj=req.json()
			dayIter=0
			print("11")
			for vol in obj['total_volumes']:
				print(dayIter)
				if symbol in cap.keys():
					print("FOUND SUPPLY", symbol)
					if float(vol[1])>(float(cap[symbol]['info']['available_supply'])/10):
						lst.append([symbol ,datetime.today() - timedelta(dayIter) ])
				dayIter+=1
		else: print("Currency not supported by coingecko")
	return lst
def findDayData(currencies):
	json=[]
	for curr in currencies:
		data=curr[1]
		symbol=curr[0]
		url = "https://coinmarketcap.com/currencies/" +symbol+"/historical-data/?start="+"".join(str(data)[0:10].split("-"))+"&end="+"".join(str(data+timedelta(1))[0:10].split("-"))
		print(url)
		try: json.append(hDS.Scraper(url).get())
		except: print("Data unavailable") 
	return json		
def buyToSellRatio(currArr):
	for curr in currArr:
		print(str(curr[0]))
		print(curr[1])
		print(str(curr[1]))
		print(requests.get("https://coinmarketcap.com/currencies/" + curr[0].lower() + "/historical-data/?start=" + ("").join(str(curr[1])[0:10].split("-"))))
def removeDupplicated(arr):
    arr2={}
    for i in arr:
        if i[0] not in arr2: arr2[i[0]]=i[1]
    return arr2
    
listOfCurrencies=pickler.Pickler("midMarketCapCurrPickle", None).retrieve()
listOfCurrencies.append('ONE')
#for w in requests.get("https://api.coingecko.com/api/v3/coins/list").json():
#	listOfCurrencies.append(w['symbol'])
#print(circulatingToTotalRatio(listOfCurrencies))
#print(listOfCurrencies)
#c24hObj=circulatingTo24HVolRatio(listOfCurrencies)
c24hObj= [['EOS', 'bla1'],['EOS', 'bla2'],['LINK', 'ala1'],['LINK', 'ala2'],['BTC','ccc1'],['ETH', 'ccc2']]
print(c24hObj)
print(removeDupplicated(c24hObj))
#pickler.Pickler("circToVol", c24hObj).save()
obj=pickler.Pickler("circToVolShorter")
arr=obj.retrieve()
arr.append(['ONE', datetime(2019, 9, 18, 20, 53, 12, 529759)])
print(arr)
d=buyToSellRatio(obj.retrieve())
print(d)
