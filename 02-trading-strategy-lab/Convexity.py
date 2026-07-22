import numpy as np
import pandas as pd

#checks whether a strategy's returns are convex relative to the benchmark comparison
#fits strategy return = a + b*benchmarkreturn + c*benchmarkreturn^2
#a positive c means convexity: the strategy does better than a straight line would predict during big moves
def convexity(strategyreturns, benchmarkreturns):
    data=pd.DataFrame({"strategy": strategyreturns, "benchmark": benchmarkreturns}).dropna()

    x=data["benchmark"]
    y=data["strategy"]

    #builds the design matrix for a quadratic fit
    X=np.column_stack([np.ones(len(x)), x, x**2])

    #solves for a, b, c using least squares method
    coeffs, residuals, rank, singularvals=np.linalg.lstsq(X, y, rcond=None)
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
