import pandas as pd
#momentum is where we bet the trend keeps going. long when short-term average is above long-term, short when below
def momentum(data, shortwindow=20, longwindow=50):
    from indicators import sma
    smashort=sma(data, shortwindow)
    smalong=sma(data, longwindow)

    signal=pd.Series(0, index=data.index)
    signal[smashort>smalong]=1
    signal[smashort<smalong]=-1
    return signal

#This is basically betting that if the stock is going too far from its average then it will jump back to its avg. RSI looks at the ratio
#we do the mean reversion using RSI: buy when oversold (below 30), sell/short when overbought (above 70)
def meanreversion_rsi(data, window=14, lowerbound=30, upperbound=70):
    from indicators import rsi
    rsivalues=rsi(data, window)

    signal=pd.Series(0, index=data.index)
    signal[rsivalues<lowerbound]=1
    signal[rsivalues>upperbound]=-1
    return signal

#these mean reversion using bollinger bands. Bollinger uses distance We will buy when price falls below the lower band and then sell when it pushes above the upper band
def meanreversion_bollinger(data, window=20, numstd=2):
    from indicators import bollinger
    upper, middle, lower=bollinger(data, window, numstd)

    signal=pd.Series(0, index=data.index)
    signal[data<lower]=1
    signal[data>upper]=-1
    return signal

#pairs trading are our bets that two historically correlated stocks will revert back toward their normal spread. betting on their relationship
def pairstrade(data1, data2, window=30, numstd=1.5):
    spread=data1-data2
    spreadmean=spread.rolling(window=window).mean()
    spreadstd=spread.rolling(window=window).std()
    zscore=(spread-spreadmean)/spreadstd

    #signal is for the first stock stock: long stock 1/short stock 2 if the spread is too low, and then do the opposite if too high
    signal=pd.Series(0, index=data1.index)
    signal[zscore<-numstd]=1
    signal[zscore>numstd]=-1
    return signal, zscore

#MACD strategy is where we long when MACD line crosses above signal line, and we can short when it crosses below
def macdstrategy(data, fast=12, slow=26, signal=9):
    from indicators import macd
    macdline, signalline=macd(data, fast, slow, signal)

    tradesignal=pd.Series(0, index=data.index)
    tradesignal[macdline>signalline]=1
    tradesignal[macdline<signalline]=-1
    return tradesignal

#MACD strategy: long when MACD line crosses above signal line, short when it crosses below
def macdstrategy(data, fast=12, slow=26, signal=9):
    from indicators import macd
    macdline, signalline = macd(data, fast, slow, signal)

    tradesignal = pd.Series(0, index=data.index)
    tradesignal[macdline > signalline] = 1
    tradesignal[macdline < signalline] = -1
    return tradesignal

if __name__ == '__main__':
    from data import getdata, cleandata
    from strategies import momentum, meanreversion_rsi, meanreversion_bollinger, macdstrategy, pairstrade
    from backtest import backtest, backtestpairs

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
