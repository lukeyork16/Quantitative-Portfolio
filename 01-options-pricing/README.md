## Files
| File | Purpose |
|---|---|
| `blackscholes.py` | Core Black-Scholes pricing + Greeks |
| `impliedvolatility.py` | Implied volatility solver (Newton-Raphson + bisection) |
| `historicalvolatility.py` | Realized volatility from price history |
| `volatilitysmile.py` | Live volatility smile from a real options chain |
| `optionchain.py` | Pulls and cleans a live options chain via yfinance |
| `payoffs.py` | Payoff diagrams: calls, puts, covered calls, straddles, iron condors, butterflies |
| `dashboard.py` | Interactive Streamlit dashboard with live pricing, Greeks, and plain-English explanations |

## Status
✅ Complete — pricing engine, Greeks, implied vol solver, historical vol, live volatility smile, payoff diagrams, and an interactive dashboard are all built and tested.

## How to run the dashboard
```
pip install streamlit scipy numpy pandas matplotlib yfinance
streamlit run dashboard.py
```
