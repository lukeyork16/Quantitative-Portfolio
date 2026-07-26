import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data import getuniverse, cleanuniverse, getsp500tickers
from factors import compositescore
from selection import monthlyrebalanceweights, buildportfolioweights
from backtest import backtestselection, buyholdbenchmark, sharpe, maxdrawdown, spybenchmark

st.title("Stock Selection Algorithm")
st.write("Multi-factor model (momentum, low volatility, short-term reversal) ranking the full S&P 500, rebalanced monthly.")

@st.cache_data(ttl=86400) #caches for 24 hours so we're not redownloading the whole sp500 on every interaction
def loaduniverse():
    tickers=getsp500tickers()
    prices=getuniverse(tickers)
    prices=cleanuniverse(prices)
    return prices

@st.cache_data(ttl=86400)
def runbacktest(_prices, topn): #underscore on _prices tells streamlit not to try to hash the whole dataframe, just cache by topn
    scores=compositescore(_prices)
    weights=monthlyrebalanceweights(scores, topn=topn, method="score")
    strategyreturns=backtestselection(_prices, weights).dropna()
    benchmarkreturns=buyholdbenchmark(_prices).loc[strategyreturns.index]
    spyreturns=spybenchmark()
    spyreturns=spyreturns.loc[spyreturns.index.isin(strategyreturns.index)]
    return strategyreturns, benchmarkreturns, spyreturns, scores

topn=st.sidebar.slider("Number of stocks to hold", 5, 30, 10)
portfoliovalue=st.sidebar.number_input("Portfolio value ($)", min_value=1000, value=10000, step=1000)

with st.spinner("Loading S&P 500 universe (first run takes several minutes, cached after that)..."):
    prices=loaduniverse()

with st.spinner("Running backtest..."):
    strategyreturns, benchmarkreturns, spyreturns, scores=runbacktest(prices, topn)

st.header("Today's Buy List")
todaysscores=scores.iloc[-1].dropna()
todaysweights=buildportfolioweights(todaysscores, topn, method="equal")

buylist=pd.DataFrame({
    "Weight": todaysweights,
    "Dollar Amount": todaysweights*portfoliovalue,
}).sort_values("Weight", ascending=False)
st.dataframe(buylist.style.format({"Weight":"{:.1%}","Dollar Amount":"${:,.2f}"}))
st.caption(f"As of {prices.index[-1].strftime('%B %d, %Y')}. This is a point-in-time snapshot — rerun before your next monthly rebalance for a current list.")

st.header("Backtested Performance")
comparison=pd.DataFrame({
    "Strategy": [(1+strategyreturns).prod()-1, sharpe(strategyreturns), maxdrawdown(strategyreturns)],
    "Equal-Weight Universe": [(1+benchmarkreturns).prod()-1, sharpe(benchmarkreturns), maxdrawdown(benchmarkreturns)],
    "SPY": [(1+spyreturns).prod()-1, sharpe(spyreturns), maxdrawdown(spyreturns)],
}, index=["Total Return","Sharpe Ratio","Max Drawdown"])
st.dataframe(comparison.style.format("{:.4f}"))

with st.expander("What do these numbers mean?"):
    st.write("""
    **Total Return**: how much $1 invested would have grown to over the whole backtest period.

    **Sharpe Ratio**: return per unit of risk taken. Higher means a better risk-adjusted return, not just a bigger number.

    **Max Drawdown**: the worst peak-to-trough decline over the whole period, capturing the real pain of holding the strategy.
    """)

st.header("Growth of $1")
cumstrategy=(1+strategyreturns).cumprod()
cumbenchmark=(1+benchmarkreturns).cumprod()
cumspy=(1+spyreturns).cumprod()

fig,ax=plt.subplots(figsize=(9,5))
ax.plot(cumstrategy.index, cumstrategy, label="Strategy")
ax.plot(cumbenchmark.index, cumbenchmark, label="Equal-Weight Universe", linestyle="--")
ax.plot(cumspy.index, cumspy, label="SPY", linestyle=":")
ax.set_ylabel("Growth of $1")
ax.legend()
st.pyplot(fig)

st.caption("Backtested on historical data. Past performance doesn't guarantee future results — this reflects a specific historical period that included a strong bull market.")
