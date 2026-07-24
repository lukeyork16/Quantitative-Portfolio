import pandas as pd
import numpy as np
import yfinance as yf

def getuniverse(tickers, start="2018-01-01", end="2024-01-01"): #pulls price history for a whole universe of stocks at once
    data=yf.download(tickers, start=start, end=end, progress=False)["Close"]
    return data

def cleanuniverse(data): #keeps only tickers with enough history, drops rows with any gaps
    data=data.dropna(axis=1, thresh=int(len(data)*0.9)) #drop tickers missing more than 10% of their history
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
    print(f"Tickers kept: {list(data.columns)}")
