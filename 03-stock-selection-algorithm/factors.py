import pandas as pd
import numpy as np

def momentumfactor(prices, lookback=126): #trailing 6-month return, classic momentum window (skips the most recent month to avoid short-term noise)
    return prices.pct_change(periods=lookback).shift(21)

def lowvolfactor(prices, window=63): #rolling volatility over the last quarter, lower vol = higher factor score so we flip the sign
    returns=prices.pct_change()
    vol=returns.rolling(window=window).std()
    return -vol #negative so that low volatility ranks HIGH like the other factors

def reversalfactor(prices, window=5): #last week's return, flipped negative since we bet against a sharp recent move
    return -prices.pct_change(periods=window)

def zscore(factor): #turns raw factor values into a comparable z-score across the whole universe, for each date
    return factor.sub(factor.mean(axis=1), axis=0).div(factor.std(axis=1), axis=0)

def compositescore(prices, momentumweight=0.4, lowvolweight=0.3, reversalweight=0.3): #blends the 3 factors into one score
    mom=zscore(momentumfactor(prices))
    lowvol=zscore(lowvolfactor(prices))
    reversal=zscore(reversalfactor(prices))
    composite=momentumweight*mom+lowvolweight*lowvol+reversalweight*reversal
    return composite

if __name__ == '__main__':
    from data import getuniverse, cleanuniverse
    tickers=["AAPL","MSFT","GOOGL","AMZN","NVDA","META","TSLA","JPM","BAC","WFC","GS","MS",
              "XOM","CVX","COP","JNJ","PFE","UNH","ABBV","KO","PG","WMT","COST","MCD",
              "DIS","NFLX","V","MA","HD","LOW","BA","CAT","GE","INTC","AMD","CRM","ADBE","ORCL","IBM","CSCO"]
    prices=getuniverse(tickers)
    prices=cleanuniverse(prices)

    scores=compositescore(prices)
    print("Composite scores, most recent date:")
    print(scores.iloc[-1].sort_values(ascending=False))
