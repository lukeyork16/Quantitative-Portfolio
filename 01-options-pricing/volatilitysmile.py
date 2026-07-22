import matplotlib.pyplot as plt
from optionchain import getchain, cleanchain, addvols

def plotsmile(ticker):
    calls, puts, expiry, spot = getchain(ticker)
    calls = cleanchain(calls)
    calls = addvols(calls, spot, expiry)
    calls["moneyness"]=calls["strike"]/spot
    plt.figure(figsize=(9,5))
    plt.plot(calls["moneyness"], calls["impliedvol"]*100, marker="o", linewidth=1)
    plt.axvline(1.0, color="gray", linestyle="--", label="ATM")
    plt.xlabel("Moneyness (Strike/Spot)")
    plt.ylabel("Implied Vol (%)")
    plt.title(f"{ticker} Volatility Smile - {expiry}")
    plt.legend()
    plt.savefig(f"{ticker}smile.png")
    print(f"Saved {ticker}smile.png")

if __name__ == '__main__':
    plotsmile("SPY")
