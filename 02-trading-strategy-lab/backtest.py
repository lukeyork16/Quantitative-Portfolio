import pandas as pd

def backtest(pricedata, signal): #works for any strategy, just needs price data and a signal series (1,0,-1)
    dailyreturn=pricedata.pct_change()
    strategyreturn=signal.shift(1)*dailyreturn #shift so we trade on yesterday's signal, no lookahead
    return strategyreturn

def backtestpairs(data1, data2, signal): #backtest for pairs trading, signal applies long to stock1 and short to stock2
    return1=data1.pct_change()
    return2=data2.pct_change()
    strategyreturn=signal.shift(1)*return1-signal.shift(1)*return2 #signal 1 = long stock1/short stock2, -1 flips it
    return strategyreturn

if __name__ == '__main__':
    from data import getdata, cleandata
    from strategies import momentum, meanreversion_rsi, meanreversion_bollinger, pairstrade
    df=getdata(["SPY", "QQQ"])
    df=cleandata(df)
    momentumreturns=backtest(df["SPY"], momentum(df["SPY"]))
    rsireturns=backtest(df["SPY"], meanreversion_rsi(df["SPY"]))
    bollingerreturns=backtest(df["SPY"], meanreversion_bollinger(df["SPY"]))
    pairsignal, zscore=pairstrade(df["SPY"], df["QQQ"])
    pairsreturns=backtestpairs(df["SPY"], df["QQQ"], pairsignal)
    print("Momentum total return:", (1+momentumreturns).prod()-1)
    print("RSI total return:", (1+rsireturns).prod()-1)
    print("Bollinger total return:", (1+bollingerreturns).prod()-1)
    print("Pairs total return:", (1+pairsreturns).prod()-1)
