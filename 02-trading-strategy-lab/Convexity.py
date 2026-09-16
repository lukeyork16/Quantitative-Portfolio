import numpy as np
import pandas as pd

def convexity(strategyreturns, benchmarkreturns): 
    data=pd.DataFrame({"strategy": strategyreturns, "benchmark": benchmarkreturns}).dropna()
    x=data["benchmark"]
    y=data["strategy"]
    X=np.column_stack([np.ones(len(x)), x, x**2]) #this is the design matrix for the quadratic fit
    coeffs, residuals, rank, singularvals=np.linalg.lstsq(X, y, rcond=None) #solves for a,b,c by using least squares method
    a,b,c=coeffs
    return {"intercept": a, "linear_beta": b, "convexity_term": c}

if __name__ == '__main__':
    from data import getdata, cleandata
    from strategies import momentum
    from backtest import backtest
    df=getdata("SPY")
    df=cleandata(df)
    momentumreturns=backtest(df, momentum(df))
    benchmarkreturns=df.pct_change()
    result=convexity(momentumreturns, benchmarkreturns)
    print(result)
