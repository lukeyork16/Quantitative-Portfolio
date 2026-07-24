import numpy as np
import pandas as pd
from scipy.optimize import minimize

def dailyreturns(prices): #daily pct change for every ticker, this feeds everything else
    return prices.pct_change().dropna()

def expectedreturns(returns, tradingdays=252): #annualized average return per ticker
    return returns.mean()*tradingdays

def covmatrix(returns, tradingdays=252): #annualized covariance matrix, how tickers move together
    return returns.cov()*tradingdays

def portfolioreturn(weights, expreturns): #weighted average return of the whole portfolio
    return np.dot(weights, expreturns)

def portfoliovol(weights, cov): #portfolio volatility, this is where covariance actually matters not just individual vols
    return np.sqrt(np.dot(weights.T, np.dot(cov, weights)))

def negativesharpe(weights, expreturns, cov, riskfree=0.0): #scipy only minimizes, so we flip sharpe negative to "minimize" it into a max
    ret=portfolioreturn(weights, expreturns)
    vol=portfoliovol(weights, cov)
    return -(ret-riskfree)/vol

def maxsharpeportfolio(expreturns, cov, riskfree=0.0): #solves for the weights that maximize sharpe ratio
    n=len(expreturns)
    args=(expreturns, cov, riskfree)
    constraints=({"type":"eq", "fun": lambda w: np.sum(w)-1}) #weights have to add up to 1
    bounds=tuple((0,1) for i in range(n)) #no shorting, each weight between 0 and 1
    guess=n*[1/n] #start with equal weights
    result=minimize(negativesharpe, guess, args=args, method="SLSQP", bounds=bounds, constraints=constraints)
    return result.x

def minvarportfolio(expreturns, cov): #solves for the weights that minimize volatility, doesnt care about return at all
    n=len(cov)
    args=(cov,)
    constraints=({"type":"eq", "fun": lambda w: np.sum(w)-1})
    bounds=tuple((0,1) for i in range(n))
    guess=n*[1/n]
    result=minimize(lambda w, cov: portfoliovol(w, cov), guess, args=args, method="SLSQP", bounds=bounds, constraints=constraints)
    return result.x

if __name__ == '__main__':
    from data import getdata, cleandata
    tickers=["AAPL","MSFT","GOOGL","AMZN","NVDA","META","JPM","BAC","XOM","CVX","JNJ","PFE","KO","PG","WMT","DIS","V","HD","SPY","QQQ"]
    prices=getdata(tickers)
    prices=cleandata(prices)
    returns=dailyreturns(prices)
    expreturns=expectedreturns(returns)
    cov=covmatrix(returns)
    print("Expected annual returns:")
    print(expreturns)
    print("\nMax Sharpe weights:")
    maxsharpeweights=maxsharpeportfolio(expreturns, cov)
    for ticker, weight in zip(tickers, maxsharpeweights):
        print(f"{ticker}: {weight:.4f}")
    print(f"\nMax Sharpe portfolio return: {portfolioreturn(maxsharpeweights, expreturns):.4f}")
    print(f"Max Sharpe portfolio vol: {portfoliovol(maxsharpeweights, cov):.4f}")
    print("\nMin Variance weights:")
    minvarweights=minvarportfolio(expreturns, cov)
    for ticker, weight in zip(tickers, minvarweights):
        print(f"{ticker}: {weight:.4f}")
    print(f"\nMin Variance portfolio return: {portfolioreturn(minvarweights, expreturns):.4f}")
    print(f"Min Variance portfolio vol: {portfoliovol(minvarweights, cov):.4f}")
