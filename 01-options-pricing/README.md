## Files
| File | Purpose |
|---|---|
| `blackscholes.py` | This establishes the core Black-Scholes pricing + Greeks for the dashboard and model |
| `impliedvolatility.py` | This is the actual implied volatility solver (Uses Newton-Raphson and bisection) |
| `historicalvolatility.py` | This is the actual realized volatility from price history |
| `volatilitysmile.py` | Here is what graphs the live volatility smile from a real options chain |
| `optionchain.py` | Pulls and cleans a live options chain using yfinance library |
| `payoffs.py` | Here are the payoff diagrams. Shows calls, puts, covered calls, straddles, iron condors, & butterflies |
| `dashboard.py` | This is the Interactive Streamlit dashboard with live pricing, Greeks, and plain English explanations that can be played around with. |

## Status
Complete —> pricing engine, Greeks, implied vol solver, historical volatility, live volatility smile, payoff diagrams, and an interactive dashboard are all built and tested.

## Notes
Coding was mainly tinkered with in google colab for debugging and Claude AI was the main help with decluttering code as well as debugging. Which was mainly used for historical volatity and dashboard creation.

## How to run the dashboard
```
pip install streamlit scipy numpy pandas matplotlib yfinance
streamlit run dashboard.py
```
