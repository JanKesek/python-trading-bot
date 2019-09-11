import importlib
def bidToAskRatio(currenciesPairs, exchanges):
    lst=[]
    for e in exchanges:
        imported_module = importlib.import_module(ccxt)
        imported_object = getattr(imported_module, e)
        for curr in currenciesPairs:
            obookBid= imported_object().fetch_order_book(curr)['bids']
            obookAsks=imported_object().fetch_order_book(curr)['asks']
            lstBid=[]
            lstAsks=[]
            for i in range(len(obookBid)):
                lstBid.append(obookBid[i][1])
                lstAsks.append(obookAsks[i][1])
            sB=sum(lstBid)
            sA=sum(lstAsks)
            print("Sum of bids of curr ",curr," on exchange ", e, " : ", sB)
            print("Sum of asks of curr ", curr," on exchange ", e, " : ", sA)
            if sB >=sA: lst.append(curr)
    return lst

print(bidToAskRatio(['LINK/BTC', 'ONE/BTC'], ['binance', 'bittrex']))