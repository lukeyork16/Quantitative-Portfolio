import pandas as pd
import yfinance as yf
from impliedvolatility import findvol

def getchain(ticker, expiryindex=2): #bumped default to index 2 to skip 0DTE/weekly noise, land on a cleaner monthly-ish expiry
    stock=yf.Ticker(ticker)
    expiries=stock.options
    expiry=expiries[expiryindex]
    chain=stock.option_chain(expiry)
    calls=chain.calls
    puts=chain.puts
    spot=stock.history(period="1d")["Close"].iloc[-1]
    return calls, puts, expiry, spot

def cleanchain(chain): #when bid/ask are both 0 (stale, no quote), falls back to lastPrice instead
    chain=chain.copy()
    chain["mid"]=(chain["bid"]+chain["ask"])/2
    chain.loc[chain["mid"]==0, "mid"]=chain["lastPrice"]
    return chain[chain["mid"]>0] #drop anything still zero, truly no data

def addvols(chain, spot, expiry, r=0.04): #for every strike, solve what vol the market is implying
    chain=chain.copy()
    T=(pd.Timestamp(expiry)-pd.Timestamp.today()).days/365
    T=max(T, 1/365) #dont let T hit zero right on expiry day
    vols=[]
    for i, row in chain.iterrows():
        try:
            v=findvol(row["mid"],S=spot,K=row["strike"],T=T,r=r,optiontype="call")
        except Exception:
            v=None
        vols.append(v)
    chain["impliedvol"]=vols
    return chain.dropna(subset=["impliedvol"])

if __name__ == '__main__':
    calls, puts, expiry, spot = getchain("SPY")
    calls=cleanchain(calls)
    calls=addvols(calls, spot, expiry)
    print(calls[["strike", "mid", "impliedvol"]].head(15))
