import pandas as pd
import numpy np
import yfinance as yf

def getdata(ticker, start="2018-01-01", end="2024-01-01"):
  data=yf.download(ticker, start=start, end=end, progress=False)
  return data[["Close"]]

def add_momentum_avgs(data, short_window=20, long_window=50):
  data["SMA_short"]=data["Close"].rolling(window=short_window).mean()
  data["SMA_long"]=data["Close"].rolling(window=long_window).mean()
  return data

def makesignals(data):
  data["signal"=0
  data.loc[data["SMA_short"]>data["SMA_long"],"signal"]=1
  data.loc[data["SMA_short"]<data["SMA_long"],"signal"]=-1
  return data

def backtest(data):
  data["dailyreturn"]=data["Close"].pct_change()
  data["strategyreturn"]=data["signal"].shift(1)*data["dailyreturn"]
  return data

if __name__ == '__main__':
  df=getdata("SPY")
  df=add_momentum_avgs(df)
  df=makesignals(df)
  df=backtest(df)
  print(df[["Close", "SMA_short", "SMA_long", "signal", "strategyreturn"]].tail(10))
  
