import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date

def getuniverse(tickers, start="2018-01-01", end=None, batchsize=50): #pulls in smaller batches so yfinance doesnt get rate limited on big universes
    import time
    if end is None:
        end=date.today().strftime("%Y-%m-%d")

    alldata=[]
    for i in range(0, len(tickers), batchsize):
        batch=tickers[i:i+batchsize]
        print(f"Downloading batch {i//batchsize+1}: {len(batch)} tickers")
        batchdata=yf.download(batch, start=start, end=end, progress=False)["Close"]
        alldata.append(batchdata)
        time.sleep(2) #short pause between batches so we dont get rate limited

    data=pd.concat(alldata, axis=1)
    return data

def cleanuniverse(data): #keeps only tickers with enough history, drops rows with any gaps
    data=data.dropna(axis=1, thresh=int(len(data)*0.9)) #drop tickers missing more than 10% of their history
    data=data.dropna(axis=0, how="any")
    return data

def getsp500tickers(): #pulls the current sp500 list from wikipedia, needs a browser user agent or wikipedia blocks it
    import requests
    from io import StringIO
    headers={"User-Agent": "Mozilla/5.0"}
    response=requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies", headers=headers)
    table=pd.read_html(StringIO(response.text))[0]
    tickers=table["Symbol"].str.replace(".", "-", regex=False).tolist()
    return tickers

if __name__ == '__main__':
    tickers=getsp500tickers()
    print(f"Pulled {len(tickers)} sp500 tickers")
    data=getuniverse(tickers) #full universe now, batched
    data=cleanuniverse(data)
    print(data.tail())
    print(f"\nUniverse shape: {data.shape}")
