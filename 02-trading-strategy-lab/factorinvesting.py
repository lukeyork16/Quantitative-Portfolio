import pandas as pd
from data import getdata, cleandata

def momentumfactor(data, lookback=90): #ranks stocks by trailing return over the lookback period
    trailingreturn=data.pct_change(periods=lookback)
    return trailingreturn

def longshortportfolio(factorscores): #longs the top decile by factor score, shorts the bottom decile
    ranked=factorscores.rank(axis=1, pct=True) #ranks each row across all stocks as a percentile
    signal=pd.DataFrame(0, index=factorscores.index, columns=factorscores.columns)
    signal[ranked>=0.8]=1 #top 20% by factor score, go long
    signal[ranked<=0.2]=-1 #bottom 20% by factor score, go short
    return signal

if __name__ == '__main__':
    tickers=["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "JPM", "XOM", "JNJ"]
    df=getdata(tickers)
    df=cleandata(df)
    factorscores=momentumfactor(df)
    signal=longshortportfolio(factorscores)
    print(factorscores.tail())
    print(signal.tail())
