from bs4 import BeautifulSoup
import requests
import pandas as pd
class Scraper:
	def __init__(self, url):
		self.url=url
	def get(self):
		content=requests.get(self.url).content
		soup = BeautifulSoup(content,'html.parser')
		table = soup.find('table', {'class': 'table'})
		data = [[td.text.strip() for td in tr.findChildren('td')] 
        for tr in table.findChildren('tr')]
		return data
#url = "https://coinmarketcap.com/currencies/ripple/historical-data/?start=20130428&end=20180802"

