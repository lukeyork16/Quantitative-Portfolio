#a simple average
def sma(data, window=20):
    return data.rolling(window=window).mean()
#this is the exponential moving average and it weights recent prices more than a regular average does
def ema(data, span=20):
    return data.ewm(span=span, adjust=False).mean()
