import importlib
from tempVariables import currPairs
#import ccxt
def bidToAskRatio(currenciesPairs, exchanges):
	lst=[]
	for e in exchanges:
		imported_module = importlib.import_module('ccxt')
		imported_object = getattr(imported_module, e)
		for curr in currenciesPairs:
			try:
				obookBid= imported_object().fetch_order_book(curr)['bids']
				obookAsks=imported_object().fetch_order_book(curr)['asks']
				lstBid=[]
				lstAsks=[]
				for oB in obookBid: lstBid.append(oB[1])
				for oA in obookAsks: lstAsks.append(oA[1])
				sB=sum(lstBid)
				sA=sum(lstAsks)
				print("Sum of bids of curr ",curr," on exchange ", e, " : ", sB)
				print("Sum of asks of curr ", curr," on exchange ", e, " : ", sA)
				if sA>=sB: lst.append([e, curr])
			except: print("Pair not supported")
	return lst

print(bidToAskRatio(currPairs, ['binance', 'kucoin']))