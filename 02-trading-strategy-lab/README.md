# Quant Trading Strategy Lab

## Overview
A systematic trading strategy research tool built in Python — implements multiple technical indicators and trading strategies, backtests them against real historical data with no lookahead bias, benchmarks performance against buy-and-hold, and includes parameter optimization and a factor-based long/short portfolio approach. Wrapped in an interactive Streamlit dashboard.

## Key Concepts
- Technical indicators: SMA, EMA, RSI, MACD, Bollinger Bands
- Strategies: momentum (trend following), mean reversion (RSI-based and Bollinger-based), MACD crossover, pairs trading
- Backtesting engine with proper signal lag (avoids lookahead bias)
- Performance metrics: Sharpe ratio, max drawdown, annualized return/volatility, benchmarked vs. buy-and-hold
- Parameter optimization via grid search (Sharpe-maximizing window sizes)
- Factor investing: cross-sectional momentum ranking, long/short decile portfolio
- Convexity analysis: quadratic regression testing whether a strategy's returns respond nonlinearly to the market

## Tools & Libraries
Python, pandas, NumPy, yfinance, matplotlib, Streamlit

## Files
| File | Purpose |
|---|---|
| `data.py` | Downloads and cleans market data |
| `indicators.py` | SMA, EMA, RSI, MACD, Bollinger Bands |
| `strategies.py` | Momentum, mean reversion (RSI/Bollinger), MACD, pairs trading signals |
| `backtest.py` | Turns signals into realized returns (single-asset and pairs) |
| `performance.py` | Sharpe ratio, max drawdown, return/volatility summary |
| `optimization.py` | Grid search over strategy parameters, ranked by Sharpe |
| `factorinvesting.py` | Cross-sectional momentum factor, long/short decile portfolio |
| `convexity.py` | Tests whether a strategy's returns are convex relative to the benchmark |
| `dashboard.py` | Interactive Streamlit dashboard: pick a ticker/strategy, see live performance and an equity curve |

## Status
✅ Complete — all indicators, strategies, the backtesting engine, performance metrics, optimization, factor investing, convexity analysis, and the dashboard are built and tested.

## How to run the dashboard
pip install streamlit pandas numpy yfinance matplotlib
streamlit run dashboard.py

## Notes & Findings
- All backtests ended up with a shift signals forward one day before applying them to returns, avoiding lookahead bias.
- Pairs trading between two closely correlated ETFs (e.g. SPY/QQQ) showed limited edge, since the spread rarely drifts far from its mean — pairs trading tends to perform better on two individual stocks within the same narrow industry, where the relationship is tighter.
- Parameter optimization is run in-sample only; a natural next step would be out-of-sample testing (validating the best parameters on a separate, later time period) to check whether the edge holds up rather than reflecting overfitting to the historical window tested.

# Photos
<img width="1424" height="654" alt="image" src="https://github.com/user-attachments/assets/8734e725-5818-4a3e-99aa-1316a180d674" />
<img width="816" height="516" alt="image" src="https://github.com/user-attachments/assets/ea8b2080-bcc3-4816-a993-4229fb0febbe" />
