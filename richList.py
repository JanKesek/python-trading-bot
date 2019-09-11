import requests
from tempVariables import currs
def getRichListAddresses(currencies):
	addresses={}
	for symbol in currencies:
		reqString = "https://chainz.cryptoid.info/" + symbol.lower() + "/api.dws?q=rich"
		#print(reqString)
		addresses[symbol]=[]
		req=requests.get(reqString)
		if int(req.status_code)==200:
			print("FOUND ", symbol)
			richListJSON=req.json()['rich1000'][0:10]
			for obj in richListJSON:
				print(obj['addr'])
				addresses[symbol].append(obj['addr'])
		else: print("NOT FOUND")
	return addresses
print(getRichListAddresses(currs))