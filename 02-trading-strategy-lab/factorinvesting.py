import pandas as pd
from data import getdata, cleandata

#this is the momentum factor and will ranks stocks by their trailing return over the lookback period
def momentumfactor(data, lookback=90):
    trailingreturn=data.pct_change(periods=lookback)
    return trailingreturn

#this builds a long or short portfolio. It will long the top decile of stocks by factor score, short the bottom decile
def longshortportfolio(factorscores):
    ranked=factorscores.rank(axis=1, pct=True)  #ranks each row across all the stocks, puts it in a percentage
    signal=pd.DataFrame(0, index=factorscores.index, columns=factorscores.columns)
    signal[ranked>=0.8]=1   #for top 20% by factor score, go long
    signal[ranked<=0.2]=-1  #for bottom 20% by factor score, go short
    return signal

if __name__ == '__main__':
    tickers=["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "JPM", "XOM", "JNJ"] #selection of tickets made by Claude for testing
    df=getdata(tickers)
    df=cleandata(df)
    factorscores=momentumfactor(df)
    signal=longshortportfolio(factorscores)
    print(factorscores.tail())
    print(signal.tail())
