import numpy as np
from scipy.optimize import minimize
from optimization import portfolioreturn, portfoliovol, negativesharpe

def maxsharpeconstrained(expreturns, cov, maxweight=0.25, riskfree=0.0): #same as before but caps any single position at maxweight
    n=len(expreturns)
    args=(expreturns, cov, riskfree)
    constraints=({"type":"eq", "fun": lambda w: np.sum(w)-1})
    bounds=tuple((0,maxweight) for i in range(n)) #this is the actual constraint, real desks almost always cap concentration
    guess=n*[1/n]
    result=minimize(negativesharpe, guess, args=args, method="SLSQP", bounds=bounds, constraints=constraints)
    return result.x

def minvarconstrained(cov, maxweight=0.25): #min variance with the same cap
    n=len(cov)
    args=(cov,)
    constraints=({"type":"eq", "fun": lambda w: np.sum(w)-1})
    bounds=tuple((0,maxweight) for i in range(n))
    guess=n*[1/n]
    result=minimize(lambda w, cov: portfoliovol(w, cov), guess, args=args, method="SLSQP", bounds=bounds, constraints=constraints)
    return result.x

def dollarallocation(weights, tickers, portfoliovalue): #turns weights into actual dollars to put into each ticker, this is what makes it usable
    allocation={}
    for ticker, weight in zip(tickers, weights):
        if weight>0.0001: #skip basically zero positions, no point showing $0.02 allocations
            allocation[ticker]=round(weight*portfoliovalue, 2)
    return allocation

if __name__ == '__main__':
    from data import getdata, cleandata
    from optimization import dailyreturns, expectedreturns, covmatrix
    tickers=["AAPL","MSFT","GOOGL","AMZN","NVDA","META","JPM","BAC","XOM","CVX","JNJ","PFE","KO","PG","WMT","DIS","V","HD","SPY","QQQ"]
    prices=getdata(tickers)
    prices=cleandata(prices)
    returns=dailyreturns(prices)
    expreturns=expectedreturns(returns)
    cov=covmatrix(returns)

    print("=== Unconstrained Max Sharpe ===")
    unconstrained=maxsharpeconstrained(expreturns, cov, maxweight=1.0) #maxweight of 1.0 is basically no cap
    for ticker, weight in zip(tickers, unconstrained):
        if weight>0.0001:
            print(f"{ticker}: {weight:.4f}")
