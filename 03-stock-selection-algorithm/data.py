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
    data=data.dropna(axis=1, thresh=int(len(data)*0.9))
    data=data.dropna(axis=0, how="any")
    return data

if __name__ == '__main__':
    tickers=["AAPL","MSFT","GOOGL","AMZN","NVDA","META","TSLA","JPM","BAC","WFC","GS","MS",
              "XOM","CVX","COP","JNJ","PFE","UNH","ABBV","KO","PG","WMT","COST","MCD",
              "DIS","NFLX","V","MA","HD","LOW","BA","CAT","GE","INTC","AMD","CRM","ADBE","ORCL","IBM","CSCO"]
    data=getuniverse(tickers)
    data=cleanuniverse(data)
    print(data.tail())
    print(f"\nUniverse shape: {data.shape}")
