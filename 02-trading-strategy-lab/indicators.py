def sma(data, window=20): #simple average
    return data.rolling(window=window).mean()

def ema(data, span=20): #exponential moving average, weights recent prices more than a regular average
    return data.ewm(span=span, adjust=False).mean()

def rsi(data, window=14): #momentum measure scaled 0-100, above 70 overbought, below 30 oversold
    delta=data.diff()
    gain=delta.where(delta>0, 0)
    loss=-delta.where(delta<0, 0)
    avggain=gain.rolling(window=window).mean()
    avgloss=loss.rolling(window=window).mean()
    rs=avggain/avgloss
    rsi=100-(100/(1+rs))
    return rsi

def macd(data, fast=12, slow=26, signal=9): #gap between a fast and slow EMA, plus a signal line to catch crossovers
    emafast=ema(data, fast)
    emaslow=ema(data, slow)
    macdline=emafast-emaslow
    signalline=macdline.ewm(span=signal, adjust=False).mean()
    return macdline, signalline

def bollinger(data, window=20, numstd=2): #moving average with bands built from rolling volatility
    middle=sma(data, window)
    std=data.rolling(window=window).std()
    upper=middle+(std*numstd)
    lower=middle-(std*numstd)
    return upper, middle, lower

if __name__ == '__main__':
    from data import getdata, cleandata
    df=getdata("SPY")
    df=cleandata(df)
    df_sma=sma(df, 20)
    df_rsi=rsi(df, 14)
    macdline, signalline=macd(df)
    upper, middle, lower=bollinger(df)
    print(df_sma.tail())
    print(df_rsi.tail())
    print(macdline.tail())
    print(signalline.tail())
    print(upper.tail())
    print(lower.tail())
