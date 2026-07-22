import pandas as pd
from strategies import momentum
from backtest import backtest
from performance import sharpe

#this tries a bunch of short or long window combos for the momentum strategy, and it returns the one with the best sharpe
def optimizemomentum(data, shortrange, longrange):
    results=[]

    for shortwindow in shortrange:
        for longwindow in longrange:
            if shortwindow>=longwindow:
                continue  #the short window has to be shorter than long window, and it will skip nonsense combos

            signal=momentum(data, shortwindow, longwindow)
            returns=backtest(data, signal)
            sharperatio=sharpe(returns)

            results.append({
                "shortwindow": shortwindow,
                "longwindow": longwindow,
                "sharpe": sharperatio,
            })

    resultsdf=pd.DataFrame(results)
    best=resultsdf.loc[resultsdf["sharpe"].idxmax()]
    return resultsdf, best


if __name__ == '__main__':
    from data import getdata, cleandata

    df=getdata("SPY")
    df=cleandata(df)

    shortrange=range(5, 30, 5)   #tries 5-25 increments of 5
    longrange=range(30, 100, 10)  #tries 30-90 increments of 10
    resultsdf, best=optimizemomentum(df, shortrange, longrange)
    print(resultsdf.sort_values("sharpe", ascending=False).head(10))
    print("\nBest combo:")
    print(best)
