import requests
import pandas as pd
from bs4 import BeautifulSoup

def crawl_stock(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text,"html.parser")

    tables = soup.findAll("table")

    stock = tables[14]
    if stock.findParent("table") is None:
        t = pd.read_html(str(stock))
        return t[0]
    
df = crawl_stock("https://www.finanzen.net/aktien/adidas-aktie")
print(df.head())