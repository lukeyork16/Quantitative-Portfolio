import pandas as pd
from data import getdata, cleandata
from backtest import backtest
from performance import summary

#runs one strategy across a whole list of tickers, ranks them by sharpe so we can see where it actually works best
def screenstrategy(tickers, strategyfunc):
    results = []

    for ticker in tickers:
        try:
            df=getdata(ticker)
            df=cleandata(df)
            if len(df)<100:
                continue  #not enough history to trust the result

            signal=strategyfunc(df)
            returns=backtest(df, signal)
            stats=summary(returns)
            stats["ticker"]=ticker
            results.append(stats)
        except Exception:
            continue  #skip any ticker that fails to download or errors out

    resultsdf=pd.DataFrame(results).set_index("ticker")
    resultsdf=resultsdf.sort_values("Sharpe Ratio", ascending=False)
    return resultsdf
