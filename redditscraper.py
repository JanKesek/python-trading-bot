import ccxt
from jsonpreprocess import getCurrencySymbols
import json
from datetime import datetime
from datetime import timedelta
import time
import requests

def scrape_and_save_market_currency_symbols():
    markets = [ccxt.bittrex()]
    currencies = {m.name : [] for m in markets}
    for market in markets:
        market.load_markets()
        for marketCurr in getCurrencySymbols(market):
            if marketCurr not in currencies:
                currencies[market.name].append(marketCurr)
    with open('Market-Currencies.json', 'w') as outfile:
        json.dump(currencies, outfile)
def save_posts_to_json(symbols, posts):
    url="https://api.pushshift.io/reddit/search/submission/?subreddit={}&sort=desc&sort_type=created_utc&after={}&before={}&size=1000"
    now= datetime.now()
    then = now - timedelta(days=(365*3)-80)
    unixtimeFrom = time.mktime(then.timetuple())
    while then<=now:
        then = then + timedelta(hours=1)
        unixtimeTo = time.mktime(then.timetuple())
        fromKey = then.strftime("%m/%d/%Y, %H:%M:%S")
        print(fromKey)
        posts[fromKey] = {}
        for symbol in symbols:
            try:
                print("Arguments {} {} {}".format(symbol,unixtimeFrom,unixtimeTo))
                data = requests.get(url.format(symbol,int(unixtimeFrom), int(unixtimeTo))).json()['data']
                print(symbol)
                posts[fromKey][symbol] = []
                for post in data:
                    if 'selftext' in post:
                        if post['selftext'] is not None and len(post['selftext'])!=0:
                            posts[fromKey][symbol].append(post['selftext']) 
            except Exception as e:
                print(e)
                time.sleep(5)
        unixtimeFrom = unixtimeTo
        print(fromKey)
        save_posts(posts)
    print("KOniec")
def read_symbols_from_file():
    currencies={}
    with open('Market-Currencies.json', 'r') as infile:
        currencies=json.load(infile)
    return currencies
def save_posts(posts):
    with open('Scraped-Posts.json', 'w') as outfile:
        json.dump(posts, outfile)
def read_posts_from_file():
    with open('Scraped-Posts.json', 'r') as infile:
        posts = json.load(infile)
    return posts
if __name__ == "__main__":
    currencies=read_symbols_from_file()
    posts= read_posts_from_file()
    save_posts_to_json(currencies['Bittrex'][0:5], posts)