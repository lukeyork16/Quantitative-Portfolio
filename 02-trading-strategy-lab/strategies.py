import pandas as pd

def momentum(data, shortwindow=20, longwindow=50): #bet the trend keeps going, long when short avg above long avg, short when below
    from indicators import sma
    smashort=sma(data, shortwindow)
    smalong=sma(data, longwindow)
    signal=pd.Series(0, index=data.index)
    signal[smashort>smalong]=1
    signal[smashort<smalong]=-1
    return signal

def meanreversion_rsi(data, window=14, lowerbound=30, upperbound=70): #betting price snaps back if it stretched too far, buy oversold sell overbought
    from indicators import rsi
    rsivalues=rsi(data, window)
    signal=pd.Series(0, index=data.index)
    signal[rsivalues<lowerbound]=1
    signal[rsivalues>upperbound]=-1
    return signal

def meanreversion_bollinger(data, window=20, numstd=2): #same mean reversion bet, measured by distance from the band instead of RSI
    from indicators import bollinger
    upper, middle, lower=bollinger(data, window, numstd)
    signal=pd.Series(0, index=data.index)
    signal[data<lower]=1
    signal[data>upper]=-1
    return signal

def pairstrade(data1, data2, window=30, numstd=1.5): #bets two correlated stocks revert back toward their normal spread
    spread=data1-data2
    spreadmean=spread.rolling(window=window).mean()
    spreadstd=spread.rolling(window=window).std()
    zscore=(spread-spreadmean)/spreadstd
    signal=pd.Series(0, index=data1.index) #long stock1/short stock2 if spread too low, flip if too high
    signal[zscore<-numstd]=1
    signal[zscore>numstd]=-1
    return signal, zscore

def macdstrategy(data, fast=12, slow=26, signal=9): #long when MACD line crosses above signal line, short when it crosses below
    from indicators import macd
    macdline, signalline=macd(data, fast, slow, signal)
    tradesignal=pd.Series(0, index=data.index)
    tradesignal[macdline>signalline]=1
    tradesignal[macdline<signalline]=-1
    return tradesignal

if __name__ == '__main__':
    from data import getdata, cleandata
    from backtest import backtest, backtestpairs
    from performance import summary
    df=getdata(["SPY", "QQQ"])
    df=cleandata(df)
    momentumreturns=backtest(df["SPY"], momentum(df["SPY"]))
    rsireturns=backtest(df["SPY"], meanreversion_rsi(df["SPY"]))
    bollingerreturns=backtest(df["SPY"], meanreversion_bollinger(df["SPY"]))
    macdreturns=backtest(df["SPY"], macdstrategy(df["SPY"]))
    pairsignal, zscore=pairstrade(df["SPY"], df["QQQ"])
    pairsreturns=backtestpairs(df["SPY"], df["QQQ"], pairsignal)
    benchmarkreturns=df["SPY"].pct_change()
    print("Momentum:", summary(momentumreturns))
    print("RSI:", summary(rsireturns))
    print("Bollinger:", summary(bollingerreturns))
    print("MACD:", summary(macdreturns))
    print("Pairs:", summary(pairsreturns))
    print("Buy & Hold Benchmark:", summary(benchmarkreturns))
