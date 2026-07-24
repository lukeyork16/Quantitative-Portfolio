import pandas as pd
import numpy as np
import yfinance as yf

def getdata(tickers, start="2019-01-01", end="2024-01-01"): #pulls closing prices for a list of tickers
    data=yf.download(tickers, start=start, end=end, progress=False)["Close"]
    return data

def cleandata(data): #drops any date with a missing price, keeps everything aligned
    data=data.dropna(axis=0, how="any")
    return data

if __name__ == '__main__':
    tickers=["AAPL","MSFT","GOOGL","AMZN","SPY"]
    df=getdata(tickers)
    df=cleandata(df)
    print(df.tail())
    print(f"\nShape: {df.shape}")
