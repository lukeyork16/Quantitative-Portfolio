import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date

def getuniverse(tickers, start="2018-01-01", end=None): #pulls price history, defaults to today if no end date given
    if end is None:
        end=date.today().strftime("%Y-%m-%d")
    data=yf.download(tickers, start=start, end=end, progress=False)["Close"]
    return data

def cleanuniverse(data): #keeps only tickers with enough history, drops rows with any gaps
    data=data.dropna(axis=1, thresh=int(len(data)*0.9)) #drop tickers missing more than 10% of their history
    data=data.dropna(axis=0, how="any")
    return data

def getsp500tickers(): #pulls the current sp500 list straight from wikipedia, keeps the universe up to date automatically
    table=pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
    tickers=table["Symbol"].str.replace(".", "-", regex=False).tolist() #yfinance wants BRK-B not BRK.B
    return tickers

if __name__ == '__main__':
    tickers=getsp500tickers()
    print(f"Pulled {len(tickers)} sp500 tickers")
    data=getuniverse(tickers[:100]) #testing on a slice first, full 500 takes a while
    data=cleanuniverse(data)
    print(data.tail())
    print(f"\nUniverse shape: {data.shape}")
