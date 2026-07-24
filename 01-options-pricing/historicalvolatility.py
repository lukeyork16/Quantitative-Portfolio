import numpy as np
import yfinance as yf

def historicalvolatility(ticker, period="1y", days=252): #realized volatility from actual price history, made yearly
    data=yf.download(ticker, period=period, progress=False)
    logreturns=np.log(data["Close"]/data["Close"].shift(1)).dropna()
    dailyvol=logreturns.std()
    return float(dailyvol*np.sqrt(days))

if __name__ == '__main__':
    vol=historicalvolatility("SPY")
    print("SPY historical vol:",round(vol,4))
