import ccxt
exchange = ccxt.binance()
#exchange.enableRateLimit=True
#print(dir(exchange))
def findMidMarketCap(currencies):
	t=[]
	for symbol in currencies:
		cap= ccxt.coinmarketcap()[symbol].market_cap_usd()
		if int(cap)>100000 and int(cap) <5000000000: t.append(symbol)
	return t
exchange.limits['price']['min']=0.0019
price={}
price['price']=None
exchange.precision=price
exchange.precision['price']=5
markets = exchange.load_markets()
currencies = exchange.fetch_currencies().keys()

tickers=[]
#print("MARKET USD/BTC \n\n", exchange.fetch_ticker('DOGE/USDC'))
print("currencies SYMBOLS !!!!!!!!!!: \n\n\n\n", currencies)
print(findMidMarketCap(currencies))

