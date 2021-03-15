import websocket
from time import sleep
import json
import requests
import pickle
ws=websocket.WebSocket()
ws.connect("wss://stream.binance.com:9443/ws/btcusdt@depth")

i=0
events=[]
while i<10000:
    #if i%5==0: sleep(1)
    print(i)
    events.append( json.loads(ws.next()))
    #if i%30==0:
    #    obj=requests.get("https://www.binance.com/api/v1/depth?symbol=BTCUSDT&limit=1000").json()
    #    for e in events:
    #        if e['u']<=obj['lastUpdateId']:
    #            events.remove(e)
    if i%50==0:
        pickle.dump(events,open("orderbook.pickle",'wb'))
    i+=1
            