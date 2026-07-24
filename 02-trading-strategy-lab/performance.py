import numpy as np
import pandas as pd

def sharpe(returns, riskfree=0.0, tradingdays=252): #risk adjusted return, higher is better, annualized assuming daily returns
    excessreturn=returns-(riskfree/tradingdays)
    return (excessreturn.mean()/excessreturn.std())*np.sqrt(tradingdays)

def maxdrawdown(returns): #worst peak to trough decline over the whole period
    cumulative=(1+returns).cumprod()
    runningmax=cumulative.cummax()
    drawdown=(cumulative-runningmax)/runningmax
    return drawdown.min()

def summary(returns, tradingdays=252): #total and annualized return, plus volatility, all in one summary
    totalreturn=(1+returns).prod()-1
    annualizedreturn=returns.mean()*tradingdays
    annualizedvol=returns.std()*np.sqrt(tradingdays)
    return {
        "Total Return": totalreturn,
        "Annualized Return": annualizedreturn,
        "Annualized Volatility": annualizedvol,
        "Sharpe Ratio": sharpe(returns, tradingdays=tradingdays),
        "Max Drawdown": maxdrawdown(returns),
    }

if __name__ == '__main__':
    from data import getdata, cleandata
    from strategies import momentum, meanreversion_rsi, meanreversion_bollinger
    from backtest import backtest
    df=getdata("SPY")
    df=cleandata(df)
    momentumreturns=backtest(df, momentum(df))
    rsireturns=backtest(df, meanreversion_rsi(df))
    bollingerreturns=backtest(df, meanreversion_bollinger(df))
    benchmarkreturns=df.pct_change() #just buy and hold SPY
    print("Momentum:", summary(momentumreturns))
    print("RSI:", summary(rsireturns))
    print("Bollinger:", summary(bollingerreturns))
    print("Buy & Hold Benchmark:", summary(benchmarkreturns))
