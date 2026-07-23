import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from data import getdata, cleandata
from strategies import momentum, meanreversion_rsi, meanreversion_bollinger, macdstrategy, pairstrade
from backtest import backtest, backtestpairs
from performance import summary
from screener import screenstrategy

st.title("Trading Strategy Lab")

#maps the dropdown label to the actual function, so we only have to change this list in one place
strategyoptions = {
    "Momentum": momentum,
    "Mean Reversion (RSI)": meanreversion_rsi,
    "Mean Reversion (Bollinger)": meanreversion_bollinger,
    "MACD": macdstrategy,
}

strategyexplanations = {
    "Momentum": "Goes long when the short-term average is above the long-term average (an uptrend), short when it's below.",
    "Mean Reversion (RSI)": "Buys when RSI signals oversold (below 30), shorts when overbought (above 70), betting the price snaps back.",
    "Mean Reversion (Bollinger)": "Buys when price falls below its lower Bollinger Band, shorts when it pushes above the upper band.",
    "MACD": "Goes long when the MACD line crosses above its signal line, short when it crosses below.",
}

#a reasonably broad, liquid universe to screen across
defaultuniverse = ["AAPL","MSFT","GOOGL","AMZN","NVDA","META","TSLA","JPM","BAC","WMT",
                    "XOM","CVX","JNJ","PFE","KO","PEP","DIS","NFLX","INTC","AMD",
                    "V","MA","HD","PG","SPY","QQQ"]

mode = st.sidebar.radio("Mode", ["Analyze One Ticker", "Find Best Tickers for a Strategy"])

if mode == "Analyze One Ticker":
    ticker = st.sidebar.text_input("Ticker", "SPY")
    strategyname = st.sidebar.selectbox("Strategy", list(strategyoptions.keys()) + ["Pairs Trading"])

    if strategyname == "Pairs Trading":
        ticker2 = st.sidebar.text_input("Second Ticker (for the pair)", "QQQ")
        st.info("Bets that the spread between the two tickers reverts back toward its normal range.")

        df = getdata([ticker, ticker2])
        df = cleandata(df)

        signal, zscore = pairstrade(df[ticker], df[ticker2])
        strategyreturns = backtestpairs(df[ticker], df[ticker2], signal)
        benchmarkreturns = df[ticker].pct_change()

    else:
        st.info(strategyexplanations[strategyname])

        df = getdata(ticker)
        df = cleandata(df)

        signal = strategyoptions[strategyname](df)
        strategyreturns = backtest(df, signal)
        benchmarkreturns = df.pct_change()

    strategystats = summary(strategyreturns)
    benchmarkstats = summary(benchmarkreturns)

    statsdf = pd.DataFrame({strategyname: strategystats, "Buy & Hold": benchmarkstats})
    st.subheader("Performance Comparison")
    st.dataframe(statsdf.style.format("{:.4f}"))

    with st.expander("What do these numbers mean?"):
        st.write("""
        **Total Return**: how much $1 invested would have grown to, in total, over the whole period.

        **Annualized Return**: that same growth rate scaled to a yearly average, so different time periods are comparable.

        **Annualized Volatility**: how much the returns bounced around year to year. Higher means a bumpier ride.

        **Sharpe Ratio**: return per unit of risk taken. A strategy with a lower total return but a higher Sharpe
        is actually the more efficient bet, since it's earning more for the risk involved.

        **Max Drawdown**: the single worst decline from a peak to a low point over the whole period.
        This captures the worst pain you'd have felt actually holding the strategy, which average returns hide.
        """)

    st.subheader("Equity Curve")
    cumulativestrategy = (1+strategyreturns).cumprod()
    cumulativebenchmark = (1+benchmarkreturns).cumprod()

    fig, ax = plt.subplots(figsize=(9,5))
    ax.plot(cumulativestrategy.index, cumulativestrategy, label=strategyname)
    ax.plot(cumulativebenchmark.index, cumulativebenchmark, label="Buy & Hold", linestyle="--")
    ax.set_ylabel("Growth of $1")
    ax.legend()
    st.pyplot(fig)

    st.caption("If the solid line is above the dashed line, the strategy beat simply buying and holding the stock.")


else:
    st.write("Runs one strategy across a broad list of tickers and ranks them by Sharpe ratio, so you can see where a given strategy has actually worked best historically.")

    strategyname = st.sidebar.selectbox("Strategy to Screen", list(strategyoptions.keys()))
    tickerlist = st.sidebar.text_area("Tickers (comma separated)", ", ".join(defaultuniverse))
    tickers = [t.strip().upper() for t in tickerlist.split(",") if t.strip()]

    if st.sidebar.button("Run Screener"):
        with st.spinner(f"Running {strategyname} across {len(tickers)} tickers..."):
            resultsdf = screenstrategy(tickers, strategyoptions[strategyname])

        st.subheader(f"Best Tickers for {strategyname}")
        st.dataframe(resultsdf.style.format("{:.4f}"))

        if len(resultsdf) > 0:
            besttic = resultsdf.index[0]
            bestsharpe = resultsdf.iloc[0]["Sharpe Ratio"]
            st.success(f"{strategyname} has historically performed best on **{besttic}**, with a Sharpe ratio of {bestsharpe:.2f}.")

        st.caption("This is based entirely on historical data (2019-2024) and is not a guarantee of future performance. Past outperformance on a specific ticker can reflect randomness as much as a genuine, repeatable edge.")
