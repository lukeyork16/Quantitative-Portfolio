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

def transactioncost(currentweights, targetweights, portfoliovalue, costpct=0.001): #cost to rebalance from current weights to target weights, costpct is per dollar traded
    weightchange=np.abs(np.array(targetweights)-np.array(currentweights))
    dollarstraded=weightchange*portfoliovalue
    totalcost=dollarstraded.sum()*costpct
    return totalcost, dollarstraded

def netsharpeaftercosts(expreturns, cov, currentweights, targetweights, portfoliovalue, costpct=0.001, riskfree=0.0): #the sharpe ratio actually achieved once you subtract the real cost of trading into it
    cost, dollarstraded=transactioncost(currentweights, targetweights, portfoliovalue, costpct)
    costasreturn=cost/portfoliovalue #turn the dollar cost into a return drag
    grossreturn=portfolioreturn(np.array(targetweights), expreturns)
    netreturn=grossreturn-costasreturn
    vol=portfoliovol(np.array(targetweights), cov)
    return (netreturn-riskfree)/vol

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
    print("\n=== Constrained Max Sharpe (25% cap per position) ===")
    constrained=maxsharpeconstrained(expreturns, cov, maxweight=0.25)
    for ticker, weight in zip(tickers, constrained):
        if weight>0.0001:
            print(f"{ticker}: {weight:.4f}")

    print(f"\nUnconstrained Sharpe: {-negativesharpe(unconstrained, expreturns, cov):.4f}")
    print(f"Constrained Sharpe: {-negativesharpe(constrained, expreturns, cov):.4f}")

    portfoliovalue=10000 #what would this actually look like if you had 10k to invest
    print(f"\n=== If investing ${portfoliovalue:,} (constrained portfolio) ===")
    dollars=dollarallocation(constrained, tickers, portfoliovalue)
    for ticker, amount in dollars.items():
        print(f"{ticker}: ${amount:,.2f}")
    print(f"\n=== Transaction Cost to Rebalance from Equal-Weight ===")
    currentweights=[1/len(tickers)]*len(tickers) #assume you're starting from an equal-weight portfolio, a common real starting point
    cost, dollarstraded=transactioncost(currentweights, constrained, portfoliovalue, costpct=0.001) #0.1% per dollar traded, a realistic retail-ish cost
    print(f"Total cost to rebalance ${portfoliovalue:,} into the constrained portfolio: ${cost:.2f}")

    netsharpe=netsharpeaftercosts(expreturns, cov, currentweights, constrained, portfoliovalue, costpct=0.001)
    print(f"Sharpe ratio after accounting for transaction costs: {netsharpe:.4f}")
