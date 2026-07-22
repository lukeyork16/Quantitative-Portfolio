#a simple average
def sma(data, window=20):
    return data.rolling(window=window).mean()
#this is the exponential moving average and it weights recent prices more than a regular average does
def ema(data, span=20):
    return data.ewm(span=span, adjust=False).mean()
#RSI measures momentum, scaled 0-100. above 70 is usually called overbought, below 30 oversold
def rsi(data, window=14):
    delta=data.diff() # day over day price change
    gain=delta.where(delta>0, 0) #days we gained
    loss=-delta.where(delta<0, 0) # days we lost
    avggain=gain.rolling(window=window).mean()
    avgloss=loss.rolling(window=window).mean()
    rs=avggain/avgloss
    rsi=100-(100/(1+rs))
    return rsi

#MACD tracks the gap between a fast and slow EMA, plus a signal line to catch crossovers
def macd(data, fast=12, slow=26, signal=9):
    emafast=ema(data, fast)
    emaslow=ema(data, slow)
    macdline=emafast - emaslow
    signalline=macdline.ewm(span=signal, adjust=False).mean()
    return macdline, signalline

#bollinger bands: a moving average with bands above/below based on how volatile the price has been
def bollinger(data, window=20, numstd=2):
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
