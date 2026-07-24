import pandas as pd
import numpy as np
import yfinance as yf

def getdata(tickers, start="2019-01-01", end="2024-01-01"): #pulls closing prices for one or several tickers at once
    data=yf.download(tickers, start=start, end=end, progress=False)["Close"]
    if isinstance(data, pd.DataFrame) and data.shape[1]==1: #single ticker, make sure we get a plain series not a weird shaped table
        data=data.iloc[:, 0]
    return data

def cleandata(data): #drops any date where data is missing, keeps everything aligned
    data=data.dropna(axis=0, how="any")
    return data

if __name__ == '__main__':
    df=getdata("SPY")
    df=cleandata(df)
    print(df.tail())
