import pandas as pd
import numpy as np

def backtestselection(prices, weightshistory): #turns portfolio weights into actual realized daily returns
    dailyreturns=prices.pct_change()
    laggedweights=weightshistory.shift(1) #trade on yesterday's weights, no lookahead
    portfolioreturns=(laggedweights*dailyreturns).sum(axis=1)
    return portfolioreturns

def buyholdbenchmark(prices): #equal weight buy and hold across the whole universe, never rebalanced, the fair comparison
    dailyreturns=prices.pct_change()
    equalweights=1/len(prices.columns)
    benchmarkreturns=(dailyreturns*equalweights).sum(axis=1)
    return benchmarkreturns

def sharpe(returns, tradingdays=252): #same sharpe calc from the trading strategy lab
    return (returns.mean()/returns.std())*np.sqrt(tradingdays)

def maxdrawdown(returns): #same drawdown calc from the trading strategy lab
    cumulative=(1+returns).cumprod()
    runningmax=cumulative.cummax()
    drawdown=(cumulative-runningmax)/runningmax
    return drawdown.min()

if __name__ == '__main__':
    from data import getuniverse, cleanuniverse
    from factors import compositescore
    from selection import monthlyrebalanceweights

    tickers=["AAPL","MSFT","GOOGL","AMZN","NVDA","META","TSLA","JPM","BAC","WFC","GS","MS",
              "XOM","CVX","COP","JNJ","PFE","UNH","ABBV","KO","PG","WMT","COST","MCD",
              "DIS","NFLX","V","MA","HD","LOW","BA","CAT","GE","INTC","AMD","CRM","ADBE","ORCL","IBM","CSCO"]
    prices=getuniverse(tickers)
    prices=cleanuniverse(prices)

    scores=compositescore(prices)
    weights=monthlyrebalanceweights(scores, topn=10, method="equal")

    strategyreturns=backtestselection(prices, weights)
    benchmarkreturns=buyholdbenchmark(prices)

    strategyreturns=strategyreturns.dropna()
    benchmarkreturns=benchmarkreturns.loc[strategyreturns.index]

    print("=== Factor Strategy vs Equal-Weight Benchmark ===")
    print(f"Strategy total return: {(1+strategyreturns).prod()-1:.4f}")
    print(f"Benchmark total return: {(1+benchmarkreturns).prod()-1:.4f}")
    print(f"Strategy Sharpe: {sharpe(strategyreturns):.4f}")
    print(f"Benchmark Sharpe: {sharpe(benchmarkreturns):.4f}")
    print(f"Strategy Max Drawdown: {maxdrawdown(strategyreturns):.4f}")
    print(f"Benchmark Max Drawdown: {maxdrawdown(benchmarkreturns):.4f}")
