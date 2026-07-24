# Portfolio Optimization

## Overview
A Modern Portfolio Theory optimizer built in Python. Given a list of stocks, it solves for the portfolio weights that either maximize risk-adjusted return (Sharpe ratio) or minimize volatility, using 5 years of real daily price data. I added a position cap and a transaction cost model on top of the basic optimizer, because an unconstrained version will happily dump most of your money into 1-2 stocks, and that's not something anyone should actually do with their money.

## My Process

I started with just 5 tickers (AAPL, MSFT, GOOGL, AMZN, SPY) to get the math working — covariance matrix, expected returns, and the actual optimizer. The results came back looking broken: max Sharpe put 69% into AAPL and 31% into AMZN with everything else at zero, and min variance put 100% into SPY. At first that looked like a bug, but it wasn't — with only 5 tickers, the optimizer genuinely didn't have much room to diversify, and SPY being a bundle of 500 stocks meant it was always going to win on pure volatility.

I bumped the universe up to 20 tickers spanning tech, financials, energy, healthcare, consumer names, and two index funds, to give the optimizer an actual choice to make. These tickers were decided by Claude AI. That got more realistic results, max Sharpe spread across 5 names instead of 1-2, and min variance spread across 7. Still, even with 20 tickers to pick from, the unconstrained max Sharpe portfolio still concentrated almost 66% of the money into just two stocks (AAPL and KO). That's not a bug either, it's a well known real weakness of basic mean variance optimization, and it's exactly why I added a 25% position cap next, so no single stock could dominate the portfolio.

Once the optimizer was actually producing something usable, I wanted this to be more than a math exercise, so I added two more pieces: a function that turns the weights into real dollar amounts for any portfolio size, and a transaction cost model, since rebalancing a portfolio isn't free in real life and I wanted the numbers to reflect that honestly.

## Key Concepts
- Covariance matrix and expected returns from historical price data
- Efficient frontier logic via `scipy.optimize`
- Maximum Sharpe ratio portfolio (best risk-adjusted return)
- Minimum variance portfolio (lowest possible risk, ignores return)
- Position constraints (max weight per stock) to prevent unrealistic concentration
- Transaction cost modeling to show the real cost of rebalancing into a target portfolio
- Dollar allocation — converts weights into an actual, usable dollar breakdown for any investment amount

## Tools & Libraries
Python, pandas, NumPy, SciPy, yfinance

## Files
| File | Purpose |
|---|---|
| `data.py` | Downloads and cleans price data for a list of tickers |
| `optimization.py` | Covariance matrix, expected returns, unconstrained max Sharpe and min variance portfolios |
| `constraints.py` | Position-capped optimization, dollar allocation, and transaction cost modeling |

## Results
Using a 20 stock sample (2019-2024 data): the unconstrained max Sharpe portfolio scored a 1.39 Sharpe ratio but concentrated 66% of the weight into 2 stocks. Adding a 25% position cap spread it across 6 stocks and only cost 0.014 in Sharpe ratio (1.37) a small, quantifiable price for a much more reasonable looking portfolio. The minimum variance portfolio spread across 8 names and landed on SPY as its largest single position, since a pre-diversified index fund is hard to beat on volatility alone. Rebalancing $10,000 from equal-weight into the constrained target portfolio costs about $14.35 in transaction costs, dropping the net Sharpe slightly to 1.364.

## Status
✅ Complete — data pipeline, covariance/expected returns, unconstrained and constrained optimization, dollar allocation, and transaction cost modeling are all built and tested. Full results and a plain-English breakdown of what they mean are in `portfolio_optimization_report.pdf`.

## Notes & Limitations
- Expected returns are estimated from 5 years of trailing history which is a noisy, backwardlooking estimate of what a stock will actually return going forward.
- No shorting is allowed; every weight sits between 0% and the position cap.
- Transaction costs are modeled as a flat 0.1% per dollar traded, a simplification of real costs like bid-ask spread and market impact.
- Debugging, grammar fixing, and README supported by Claude AI
- Report made from uploading notes to Claude AI and compiled for tables and direct answers.
