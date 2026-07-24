import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data import getdata, cleandata
from strategies import momentum, meanreversion_rsi, meanreversion_bollinger, macdstrategy, pairstrade
from backtest import backtest, backtestpairs
from performance import summary
from screener import screenstrategy, screenall
from optimization import optimizemomentum

st.title("Trading Strategy Lab")

strategyoptions={
    "Momentum": momentum,
    "Mean Reversion (RSI)": meanreversion_rsi,
    "Mean Reversion (Bollinger)": meanreversion_bollinger,
    "MACD": macdstrategy,
}
strategyexplanations={
    "Momentum": "Goes long when the short-term average is above the long-term average (an uptrend), short when it's below.",
    "Mean Reversion (RSI)": "Buys when RSI signals oversold (below 30), shorts when overbought (above 70), betting the price snaps back.",
    "Mean Reversion (Bollinger)": "Buys when price falls below its lower Bollinger Band, shorts when it pushes above the upper band.",
    "MACD": "Goes long when the MACD line crosses above its signal line, short when it crosses below.",
}
defaultuniverse=["AAPL","MSFT","GOOGL","AMZN","NVDA","META","TSLA","JPM","BAC","WMT",
                  "XOM","CVX","JNJ","PFE","KO","PEP","DIS","NFLX","INTC","AMD",
                  "V","MA","HD","PG","SPY","QQQ"]

mode=st.sidebar.radio("Mode", ["Top Strategies", "Analyze One Ticker", "Optimize Parameters"])

if mode=="Top Strategies":
    st.write("Tests every strategy against every ticker and ranks every combination by Sharpe ratio, so you can see which strategy actually works best, and on what.")
    tickerlist=st.sidebar.text_area("Tickers (comma separated)", ", ".join(defaultuniverse))
    tickers=[t.strip().upper() for t in tickerlist.split(",") if t.strip()]
    if st.sidebar.button("Run Full Screen"):
        with st.spinner(f"Testing {len(strategyoptions)} strategies across {len(tickers)} tickers ({len(strategyoptions)*len(tickers)} backtests)..."):
            resultsdf=screenall(tickers, strategyoptions)
        st.subheader("Top 5 Strategy + Ticker Combinations")
        top5=resultsdf.head(5).reset_index(drop=True)
        st.dataframe(top5[["ticker","strategy","Sharpe Ratio","Total Return","Max Drawdown"]].style.format({
            "Sharpe Ratio": "{:.2f}", "Total Return": "{:.2%}", "Max Drawdown": "{:.2%}"
        }))
        if len(top5)>0: #callout for the winner, then list the rest
            best=top5.iloc[0]
            st.success(f"**Top pick:** {best['strategy']} on **{best['ticker']}** — Sharpe ratio of {best['Sharpe Ratio']:.2f}, total return of {best['Total Return']:.1%}, max drawdown of {best['Max Drawdown']:.1%}.")
            for i in range(1, min(5, len(top5))):
                row=top5.iloc[i]
                st.write(f"**#{i+1}:** {row['strategy']} on {row['ticker']} — Sharpe {row['Sharpe Ratio']:.2f}")
        with st.expander("Full results (all combinations tested)"):
            st.dataframe(resultsdf.style.format({
                "Sharpe Ratio": "{:.2f}", "Total Return": "{:.2%}", "Annualized Return": "{:.2%}",
                "Annualized Volatility": "{:.2%}", "Max Drawdown": "{:.2%}"
            }))
        st.caption("Ranked entirely on historical data (2019-2024). A top result here reflects what worked in the past, not a guarantee it keeps working — with this many combinations tested, some outperformance is expected from randomness alone, not necessarily a repeatable edge.")

elif mode=="Analyze One Ticker":
    ticker=st.sidebar.text_input("Ticker", "SPY")
    strategyname=st.sidebar.selectbox("Strategy", list(strategyoptions.keys())+["Pairs Trading"])
    if strategyname=="Pairs Trading":
        ticker2=st.sidebar.text_input("Second Ticker (for the pair)", "QQQ")
        st.info("Bets that the spread between the two tickers reverts back toward its normal range.")
        df=getdata([ticker, ticker2])
        df=cleandata(df)
        signal, zscore=pairstrade(df[ticker], df[ticker2])
        strategyreturns=backtestpairs(df[ticker], df[ticker2], signal)
        benchmarkreturns=df[ticker].pct_change()
    else:
        st.info(strategyexplanations[strategyname])
        df=getdata(ticker)
        df=cleandata(df)
        signal=strategyoptions[strategyname](df)
        strategyreturns=backtest(df, signal)
        benchmarkreturns=df.pct_change()

    strategystats=summary(strategyreturns)
    benchmarkstats=summary(benchmarkreturns)
    statsdf=pd.DataFrame({strategyname: strategystats, "Buy & Hold": benchmarkstats})
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
    cumulativestrategy=(1+strategyreturns).cumprod()
    cumulativebenchmark=(1+benchmarkreturns).cumprod()
    fig, ax=plt.subplots(figsize=(9,5))
    ax.plot(cumulativestrategy.index, cumulativestrategy, label=strategyname)
    ax.plot(cumulativebenchmark.index, cumulativebenchmark, label="Buy & Hold", linestyle="--")
    ax.set_ylabel("Growth of $1")
    ax.legend()
    st.pyplot(fig)
    st.caption("If the solid line is above the dashed line, the strategy beat simply buying and holding the stock.")

else:
    st.write("Finds the moving-average window sizes that historically maximized Sharpe ratio for the Momentum strategy, on one ticker.")
    ticker=st.sidebar.text_input("Ticker", "SPY")
    if st.sidebar.button("Run Optimization"):
        df=getdata(ticker)
        df=cleandata(df)
        with st.spinner("Testing window combinations..."):
            resultsdf, best=optimizemomentum(df, range(5,30,5), range(30,100,10))
        st.subheader(f"Best Momentum Windows for {ticker}")
        st.write(f"Short window: **{int(best['shortwindow'])}**, Long window: **{int(best['longwindow'])}**, Sharpe: **{best['sharpe']:.2f}**")
        st.dataframe(resultsdf.sort_values("sharpe", ascending=False).head(10).style.format({"sharpe":"{:.2f}"}))
        st.caption("Optimized in-sample on the same historical period being tested — a real risk of overfitting. Out-of-sample validation on a separate time period would be the natural next check.")
