# Stock Selection Algorithm

## Overview
A multi-factor stock ranking and selection model built in Python. It scores every stock in the S&P 500 on momentum, low volatility, and short-term reversal, combines those into one composite score, and picks the top 10 to hold each month. Includes a live dashboard that shows today's actual buy list and compares the strategy's backtested performance against both an equal weight universe and SPY.

##My Process

I started this one small on purpose with 40 hand picked tickers across a few sectors, just to get the factor math and the ranking logic working. Once the selection and backtest pipeline was solid, I realized 40 tickers wasn't a real test, so I pulled the actual, current S&P 500 list straight from Wikipedia instead of hardcoding names, and ran the whole thing against all ~500 stocks. This took a while to pull correctly, but with AI I was able to get almost the whole S&P.

That jump caused real problems I had to debug, not just theoretical ones. Downloading 500 tickers in one shot got rate-limited by Yahoo Finance and started throwing `"unable to open database file"` errors which turned out yfinance uses a local SQLite cache internally, and downloading with multiple threads at once causes those threads to collide writing to that file. I fixed it by batching the downloads (50 tickers at a time) and turning threading off, which dropped my failure rate from about half the tickers failing down to only 27 out of 503 failing — a real, working universe of 476 stocks.

Once the data was solid, I built the actual ranking system: three factors (momentum, low-vol, short-term reversal), each converted to a z-score so they're actually comparable, blended into one composite score, then ranked and rebalanced monthly. I tested two ways to size the positions equal weight (every pick gets the same 10%) versus score weight (bigger positions in higher scoring picks), since I wanted a real answer for which one actually performs better, not just a guess.

##Key Concepts
- Momentum factor (trailing 6-month return, skipping the most recent month, since that tends to reverse rather than continue a real, documented finding)
- Low volatility factor (with calmer stocks historically carry better risk-adjusted returns than you'd expect)
- Short term reversal factor (bets against an unusually sharp move in the last week)
- Z-scoring to make three differently scaled factors directly comparable and combinable
- Monthly rebalancing instead of daily, to keep the strategy realistic and limit unnecessary trading
- Equal weight vs. score weight position sizing
- Benchmark design: comparing against an equal weight version of the same universe (isolates whether the ranking itself adds value) and against SPY (the real market comparison)

## Tools & Libraries
Python, pandas, NumPy, yfinance, Streamlit, matplotlib
Claude AI was extremely helpful with debugging code, pulling the S&P from wikipedia, and dashboard design

## Files
| File | Purpose |
|---|---|
| `data.py` | Pulls the live S&P 500 ticker list and price history, batched to avoid rate limits |
| `factors.py` | Momentum, low-vol, and reversal factor scores, combined into one composite score |
| `selection.py` | Ranks stocks and builds monthly-rebalanced portfolio weights (equal or score-weighted) |
| `backtest.py` | Walk-forward-style backtest against an equal-weight universe and SPY |
| `signals.py` | Generates today's real, live buy list |
| `dashboard.py` | Interactive Streamlit dashboard — live buy list, weighting toggle, and performance comparison |

## Results

Backtested on the full S&P 500 (476 tickers that survived cleaning), 2018 through today, rebalanced monthly, holding the top 10 stocks:

| | Total Return | Sharpe Ratio | Max Drawdown |
|---|---|---|---|
| **Strategy (equal-weight)** | 633.1% | 1.13 | -35.0% |
| **Strategy (score-weight)** | 638.7% | 0.91 | -39.6% |
| Equal-Weight Universe | 234.6% | 0.86 | -38.5% |
| SPY | 196.7% | 0.80 | -33.7% |

The strategy beat both benchmarks on total return and Sharpe ratio, under either weighting method. The more interesting finding is between the two weighting methods themselves: score-weighting produced a slightly higher raw return, but equal-weighting had a meaningfully better Sharpe ratio (1.13 vs. 0.91) and a smaller max drawdown (-35.0% vs. -39.6%). That means giving extra size to your "highest conviction" picks didn't actually pay off here — it just concentrated risk into a score that isn't precise enough to justify betting bigger on it. Equal weighting is the better choice of the two.

The one place SPY still wins is max drawdown (-33.7% vs. -35.0% for the equal-weight strategy) — a small, honest gap. The strategy takes on slightly more downside risk than the index itself, but gets paid for it with a much higher Sharpe and total return.

##What This Actually Means, and How I'd Use It

This tells me the multi-factor ranking is doing real work, not just riding the market up — both benchmarks (equal-weight universe and SPY) are measuring different things the model has to beat, and it beat both. The gap between equal and score weighting also taught me something concrete: a composite score built from noisy factors shouldn't be trusted down to the decimal point when it comes to position sizing. Ranking the stocks is reliable enough to act on; treating the exact score gap between #1 and #10 as meaningful enough to bet bigger money on isn't.

To actually use this: run the dashboard once a month, right before a rebalance date. It pulls live data, ranks the current S&P 500, and hands back the top 10 stocks with real dollar amounts for whatever portfolio size you enter. Buy that list, hold it, and run it again next month. That's the whole workflow — score, rank, rebalance, repeat.

##What I Learned

Building this taught me more about the mechanics of a real quant workflow than any of my other projects: how to actually pull and clean a broad universe of live data without it silently breaking (rate limits, threading bugs, delisted tickers), how to build a benchmark that isolates the actual question you're trying to answer instead of testing something else by accident, and how to read a result honestly when it's genuinely good instead of assuming something's wrong. It also taught me that "more sophisticated" (score-weighting) isn't automatically better, and sometimes the simpler method is the one that actually holds up.

##Status
✅ Complete — data pipeline (full live S&P 500, rate-limit safe), factor construction, monthly-rebalanced selection, walk-forward backtest against two benchmarks, live signal generation, and the interactive dashboard are all built and tested.

##How to Run
pip install streamlit pandas numpy yfinance matplotlib lxml requests
streamlit run dashboard.py --server.address=0.0.0.0
First run downloads the full S&P 500 (several minutes); results are cached for 24 hours after that.

##Limitations and other notes
- This backtest period of 2018 to 2026 includes an unusually strong bull market. Part of this result reflects a favorable period, not purely the strategy's skill — it hasn't been tested through a genuine multi-year downturn yet.
- Factor weights (40% momentum, 30% low-vol, 30% reversal) are a reasonable starting assumption, not something optimized or tuned. A natural next step would be testing whether different weightings perform meaningfully better or worse.
- No transaction costs are modeled in this backtest, unlike my Portfolio Optimization project monthly rebalancing across 10 positions would have some real cost that isn't reflected in these numbers.
- This ignores fundamentals entirely (earnings, valuation, balance sheet health) it's a purely price-based, technical model, which is a real and known limitation of this style of factor investing.
