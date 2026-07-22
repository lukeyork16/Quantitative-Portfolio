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

if __name__ == '__main__':
    from data import getdata, cleandata

    df=getdata(["SPY", "QQQ"])
    df=cleandata(df)

    momentumsignal = momentum(df["SPY"])
    rsisignal=meanreversion_rsi(df["SPY"])
    bollingersignal=meanreversion_bollinger(df["SPY"])
    pairsignal, zscore=pairstrade(df["SPY"], df["QQQ"])

    print(momentumsignal.tail(10))
    print(rsisignal.tail(10))
    print(bollingersignal.tail(10))
    print(pairsignal.tail(10))
