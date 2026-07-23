# Quant Trading Strategy Lab

## Overview
A systematic trading strategy research tool built in Python — implements multiple technical indicators and trading strategies, backtests them against real historical data with no lookahead bias, and wraps everything in an interactive Streamlit dashboard that screens strategies across a broad universe of tickers to surface which strategy/ticker combinations have historically performed best.

## Key Concepts
- Technical indicators: SMA, EMA, RSI, MACD, Bollinger Bands
- Strategies: momentum (trend following), mean reversion (RSI-based and Bollinger-based), MACD crossover, pairs trading
- Backtesting engine with proper signal lag (avoids lookahead bias)
- Performance metrics: Sharpe ratio, max drawdown, annualized return/volatility, benchmarked vs. buy-and-hold
- Full strategy screener: every strategy tested against every ticker in a broad universe, ranked into one Sharpe-sorted leaderboard
- Parameter optimization via grid search (Sharpe-maximizing window sizes)
- Factor investing: cross-sectional momentum ranking, long/short decile portfolio
- Convexity analysis: quadratic regression testing whether a strategy's returns respond nonlinearly to the market

## Tools & Libraries
Python, pandas, NumPy, yfinance, matplotlib, Streamlit

## Files
| File | Purpose |
|---|---|
| `data.py` | This downloads and cleans market data |
| `indicators.py` | Indicators used are SMA, EMA, RSI, MACD, Bollinger Bands |
| `strategies.py` | Strategies used are Momentum, mean reversion (RSI/Bollinger), MACD, pairs trading signals |
| `backtest.py` | This code turns signals into realized returns (single-asset and pairs) |
| `performance.py` | Using Sharpe ratio, max drawdown, return/volatility summary |
| `screener.py` | This screens one strategy across many tickers, or every strategy against every ticker, ranked by Sharpe |
| `optimization.py` | It makes a grid search over strategy parameters, ranked by Sharpe |
| `factorinvesting.py` | Provides a crosssectioned momentum factor, with long or short portfolio |
| `convexity.py` | Tests whether a strategy's returns are convex relative to the benchmark |
| `dashboard.py` | Interactive Streamlit dashboard — see below |

## Dashboard
The dashboard has three modes, selectable from the sidebar:

- **Top Strategies** — the main view. Tests all four strategies against a broad, editable list of tickers (~26 by default) in one click, and surfaces a top-5 leaderboard ranked by Sharpe ratio, with a plain-English "top pick" summary of the best strategy/ticker combination found.
- **Analyze One Ticker** — pick a single ticker and strategy (including Pairs Trading, which takes a second ticker) and see a full performance comparison against buy-and-hold, plus an equity curve chart.
- **Optimize Parameters** — grid-searches moving-average window sizes for the Momentum strategy on a chosen ticker, ranked by Sharpe.

Every results table includes a disclaimer that historical outperformance across many tested combinations can reflect randomness (multiple comparisons bias) as much as a genuine, repeatable edge the dashboard surfaces the best historical result, not a guarantee.

## Status
Complete —> all indicators, strategies, the backtesting engine, performance metrics, the full strategy screener, parameter optimization, factor investing, convexity analysis, and the interactive dashboard are built and tested.

## How to run the dashboard
pip install streamlit pandas numpy yfinance matplotlib
streamlit run dashboard.py

## Notes & Findings
- All backtests shift signals forward one day before applying them to returns, avoiding lookahead bias (using information not actually available at the time of the trade).
- Pairs trading between two closely correlated ETFs (e.g. SPY/QQQ) showed limited edge, since the spread rarely drifts far from its mean — pairs trading tends to perform better on two individual stocks within the same narrow industry, where the relationship is tighter.
- Parameter optimization and the strategy screener are both run in-sample only; a natural next step would be out-of-sample testing (validating the best-performing combinations on a separate, later time period) to check whether the edge holds up rather than reflecting overfitting to the historical window tested.

- Used Claude code for bugging on dashboard, technical clarification on methods to select best strategy, pulling tickers, and grammar and formatting for code.

# Photos
<img width="1296" height="745" alt="image" src="https://github.com/user-attachments/assets/ad68ac0b-7090-431f-ab9e-93b6aec9159e" />
<img width="1324" height="601" alt="image" src="https://github.com/user-attachments/assets/1c99fac2-e1a2-41f4-a292-5765ffe3e4cd" />
<img width="849" height="509" alt="image" src="https://github.com/user-attachments/assets/33e5bf55-c962-411b-a040-9376497df41a" />
<img width="1290" height="743" alt="image" src="https://github.com/user-attachments/assets/7b00ae2a-8786-4599-9d8f-9c40fe282150" />




