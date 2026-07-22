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

if __name__ == '__main__':
    from data import getdata, cleandata
    df=getdata("SPY")
    df=cleandata(df)
    df_sma=sma(df, 20)
    df_rsi=rsi(df, 14)
    print(df_sma.tail())
    print(df_rsi.tail())
