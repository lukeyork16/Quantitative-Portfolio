import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from data import getdata, cleandata
from strategies import momentum, meanreversion_rsi, meanreversion_bollinger, macdstrategy, pairstrade
from backtest import backtest, backtestpairs
from performance import summary

st.title("Trading Strategy Lab")
st.write("Pick a ticker and a strategy, and see how it would have performed historically.")

#sidebar inputs
ticker=st.sidebar.text_input("Ticker", "SPY")
strategyname=st.sidebar.selectbox("Strategy", ["Momentum", "Mean Reversion (RSI)", "Mean Reversion (Bollinger)", "MACD"])

#pull and clean the data for whatever ticker was typed in
df=getdata(ticker)
df=cleandata(df)

#run whichever strategy was picked, and stash a short explanation to show alongside it
if strategyname == "Momentum":
    signal=momentum(df)
    explanation="Goes long when the short-term average is above the long-term average (an uptrend), short when it's below."
elif strategyname == "Mean Reversion (RSI)":
    signal=meanreversion_rsi(df)
    explanation="Buys when RSI signals oversold (below 30), shorts when overbought (above 70), betting the price snaps back."
elif strategyname == "Mean Reversion (Bollinger)":
    signal=meanreversion_bollinger(df)
    explanation="Buys when price falls below its lower Bollinger Band, shorts when it pushes above the upper band."
else:
    signal=macdstrategy(df)
    explanation="Goes long when the MACD line crosses above its signal line, short when it crosses below."

st.info(explanation)

strategyreturns=backtest(df, signal)
benchmarkreturns=df.pct_change()

#compute performance for both the strategy and a plain buy-and-hold benchmark
strategystats=summary(strategyreturns)
benchmarkstats=summary(benchmarkreturns)

#side by side comparison table
statsdf=pd.DataFrame({strategyname: strategystats, "Buy & Hold": benchmarkstats})
st.subheader("Performance Comparison")
st.dataframe(statsdf.style.format("{:.4f}"))
with st.expander("What do these numbers mean?"):
    st.write("""
    **Total Return**: tells us how much $1 invested would have grown to, in total, over the whole period.
    **Annualized Return**: that same growth rate scaled to a yearly average, so different time periods are comparable.
    **Annualized Volatility**: is how much the returns bounced around year to year. Higher means a bumpier ride.
    **Sharpe Ratio**: return per unit of risk taken. A strategy with a lower total return but a higher Sharpe
    is actually the more efficient bet, since it's earning more for the risk involved.
    **Max Drawdown**: the single worst decline from a peak to a low point over the whole period.
    This captures the worst pain you'd have felt actually holding the strategy, which average returns hide.
    """)
#equity curve: cumulative growth of $1 for the strategy vs buy and hold
st.subheader("Equity Curve")
cumulativestrategy=(1+strategyreturns).cumprod()
cumulativebenchmark=(1+benchmarkreturns).cumprod()
fig, ax=plt.subplots(figsize=(9,5))
ax.plot(cumulativestrategy.index, cumulativestrategy, label=strategyname)
ax.plot(cumulativebenchmark.index, cumulativebenchmark, label="Buy & Hold", linestyle="--")
ax.set_ylabel("Growth of $1")
ax.legend()
st.pyplot(fig)
st.caption("If the solid line is above the dashed line, the strategy beat simply buying and holding the stock.")
