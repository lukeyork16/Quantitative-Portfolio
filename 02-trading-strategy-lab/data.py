import pandas as pd
import numpy as np
import yfinance as yf

#pulls price data for one or several tickers at once, always returns just closing prices
def getdata(tickers, start="2019-01-01", end="2024-01-01"):
    data=yf.download(tickers, start=start, end=end, progress=False)["Close"]

    #if its a single ticker, make sure we get back a clean plain series, not an oddly shaped table
    if isinstance(data, pd.DataFrame) and data.shape[1] == 1:
        data=data.iloc[:, 0]
    return data
#drops any date where data is missing, keeps everything aligned across tickers
def cleandata(data):
    data = data.dropna(axis=0, how="any")
    return data

if __name__ == '__main__':
    df=getdata("SPY")
    df=cleandata(df)
    print(df.tail())
