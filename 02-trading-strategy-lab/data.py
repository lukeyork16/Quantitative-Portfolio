import pandas as pd
import numpy as np
import yfinance as yf
#this will pull price data for one or several tickers at once, then it will always returns just closing prices so we can use that to make strategy
def getdata(tickers, start="2019-01-01", end="2024-01-01"):
    data = yf.download(tickers, start=start,end=end,progress=False)["Close"]
    return data
#removes missing values
def cleandata(data):
    data=data.dropna(axis=0, how="any")
    return data

if __name__ == '__main__':
    df=getdata("SPY")
    df=cleandata(df)
    print(df.tail())
