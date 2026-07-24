import pandas as pd
from data import getdata, cleandata
from backtest import backtest
from performance import summary

def screenstrategy(tickers, strategyfunc): #runs one strategy across a list of tickers, ranks by sharpe
    results=[]
    for ticker in tickers:
        try:
            df=getdata(ticker)
            df=cleandata(df)
            if len(df)<100:
                continue #not enough history to trust the result
            signal=strategyfunc(df)
            returns=backtest(df, signal)
            stats=summary(returns)
            stats["ticker"]=ticker
            results.append(stats)
        except Exception:
            continue #skip any ticker that fails to download or errors out
    resultsdf=pd.DataFrame(results).set_index("ticker")
    resultsdf=resultsdf.sort_values("Sharpe Ratio", ascending=False)
    return resultsdf

def screenall(tickers, strategyoptions): #runs every strategy across every ticker, one big leaderboard
    results=[]
    for ticker in tickers:
        try:
            df=getdata(ticker)
            df=cleandata(df)
            if len(df)<100:
                continue
        except Exception:
            continue
        for stratname, stratfunc in strategyoptions.items():
            try:
                signal=stratfunc(df)
                returns=backtest(df, signal)
                stats=summary(returns)
                stats["ticker"]=ticker
                stats["strategy"]=stratname
                results.append(stats)
            except Exception:
                continue
    resultsdf=pd.DataFrame(results)
    resultsdf=resultsdf.sort_values("Sharpe Ratio", ascending=False)
    return resultsdf
