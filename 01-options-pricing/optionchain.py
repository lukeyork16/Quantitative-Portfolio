import pandas as pd
import yfinance as yf

def getchain(ticker, expiryindex=2):
    #So I bumped default to index 2 to skip 0DTE or the weekly noise, land on a cleaner monthly-ish expiry
    stock=yf.Ticker(ticker)
    expiries=stock.options
    expiry=expiries[expiryindex]
    chain=stock.option_chain(expiry)
    calls=chain.calls
    puts=chain.puts
    spot=stock.history(period="1d")["Close"].iloc[-1]
    return calls, puts, expiry, spot


def cleanchain(chain):
    #For when bid or the ask are both 0 (stale or if there is no quote), it will fall back to lastPrice instead
    chain=chain.copy()
    chain["mid"]=(chain["bid"]+chain["ask"])/2
    chain.loc[chain["mid"]==0, "mid"]=chain["lastPrice"]
    return chain[chain["mid"]>0]  #drop anything still zero, truly no data

if __name__ == '__main__':
    calls, puts, expiry, spot = getchain("SPY")
    calls = cleanchain(calls)
    print("Spot price:", spot)
    print("Expiry:", expiry)
    print(calls[["strike", "bid", "ask", "lastPrice", "mid", "volume"]].head(10))
