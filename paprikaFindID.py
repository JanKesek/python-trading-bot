import requests

def findId(symbol):
    r=requests.get("https://api.coinpaprika.com/v1/coins")
    for obj in r.json():
        if symbol in obj['id']: print(obj['id'])
findId("link")
