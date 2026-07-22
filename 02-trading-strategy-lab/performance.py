import numpy as np
import pandas as pd

#This is the sharpe ratio for risk adjusted return. higher --> better. annualized assuming daily returns
def sharpe(returns, riskfree=0.0, tradingdays=252):
    excessreturn = returns - (riskfree/tradingdays)
    return (excessreturn.mean() / excessreturn.std()) * np.sqrt(tradingdays)

#max drawdown is the worst peak to trough decline over the whole period
def maxdrawdown(returns):
    cumulative=(1+returns).cumprod()
    runningmax=cumulative.cummax()
    drawdown=(cumulative-runningmax)/runningmax
    return drawdown.min()

#total and annualized return, plus volatility and it is put all in one summary
def summary(returns, tradingdays=252):
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
    benchmarkreturns=df.pct_change()  #just buy and hold SPY

    print("Momentum:", summary(momentumreturns))
    print("RSI:", summary(rsireturns))
    print("Bollinger:", summary(bollingerreturns))
    print("Buy & Hold Benchmark:", summary(benchmarkreturns))
