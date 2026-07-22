import pandas as pd

#works for any strategy: just needs price data and a signal series (1, 0, -1)
def backtest(pricedata, signal):
    dailyreturn = pricedata.pct_change()
    strategyreturn = signal.shift(1) * dailyreturn  #shift so we trade on yesterday's signal, no lookahead
    return strategyreturn

if __name__ == '__main__':
    from data import getdata, cleandata
    from strategies import momentum, meanreversion_rsi, meanreversion_bollinger

    df = getdata("SPY")
    df = cleandata(df)

    momentumreturns = backtest(df, momentum(df))
    rsireturns = backtest(df, meanreversion_rsi(df))
    bollingerreturns = backtest(df, meanreversion_bollinger(df))

    print("Momentum total return:", (1+momentumreturns).prod()-1)
    print("RSI total return:", (1+rsireturns).prod()-1)
    print("Bollinger total return:", (1+bollingerreturns).prod()-1)
