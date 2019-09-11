import ccxt
import pickler
cap= ccxt.coinmarketcap().fetch_currencies()

def findMidMarketCap(currencies):
	t=[]
	for symbol in currencies:
		#print(symbol)
		if symbol in cap.keys():
			capSymbol=cap[symbol]['info']['market_cap_usd']
			if float(capSymbol)>100000 and float(capSymbol) <8000000000: 
				if symbol not in t: t.append(symbol)
	return t

exchangesName=['binance','bittrex','poloniex','kucoin','livecoin','coinexchange']
exchangeObjects=[]
for names in exchangesName:
	market=getattr(ccxt, names)
	t=market()
	t.load_markets()
	exchangeObjects.append(t.fetch_currencies().keys())
exchange=ccxt.binance()
exchange.load_markets()
currencies = exchange.fetch_currencies().keys()
#print(currencies)
#print(findMidMarketCap(list(currencies)))
#print("LOADING MARKETS\n\n\n\n\n\n")

midMarketCapCurr=[]
for n in exchangeObjects:
	midMarketCapCurr.extend(findMidMarketCap(list(n)))
#print(midMarketCapCurr)

pickler.Pickler("midMarketCapCurrPickle", midMarketCapCurr).save()

