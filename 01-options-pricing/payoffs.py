import numpy as np
import matplotlib.pyplot as plt

def callpayoff(Srange, K, premium=0):
    #payoff of a long call at expiration
    return np.maximum(Srange - K, 0)-premium

def putpayoff(Srange, K, premium=0):
    #payoff of a long put at expiration
    return np.maximum(K - Srange, 0)-premium

def coveredcall(Srange, S0, K, premium):
    #own the stock & sell a call against it, caps upside but you keep the premium
    stockpnl = Srange - S0
    shortcallpnl = -callpayoff(Srange, K, premium=0)+premium
    return stockpnl+shortcallpnl

def straddle(Srange, K, callprem, putprem):
    #long call & long put at the same strike, bets on a big move either direction
    return callpayoff(Srange, K, callprem)+putpayoff(Srange, K, putprem)

def ironcondor(Srange, Kputlong, Kputshort, Kcallshort, Kcalllong, netcredit):
    #sells a call spread and put spread together, profits if stock stays in a range
    longput=putpayoff(Srange, Kputlong, premium=0)
    shortput=-putpayoff(Srange, Kputshort, premium=0)
    shortcall=-callpayoff(Srange, Kcallshort, premium=0)
    longcall=callpayoff(Srange, Kcalllong, premium=0)
    return longput+shortput+shortcall+longcall+netcredit

def butterfly(Srange, Klow, Kmid, Khigh, netdebit):
    #bets the stock lands near Kmid, sell 2 in the middle, buy 1 on each side
    longlow=callpayoff(Srange, Klow, premium=0)
    shortmid=-2 * callpayoff(Srange, Kmid, premium=0)
    longhigh=callpayoff(Srange, Khigh, premium=0)
    return longlow+shortmid+longhigh-netdebit


if __name__ == '__main__':
    #test plot: just checking the basic long call payoff looks right
    Srange=np.linspace(50, 150, 200)
    payoff=callpayoff(Srange, K=100, premium=5)

    plt.figure(figsize=(8, 5))
    plt.plot(Srange, payoff)
    plt.axhline(0, color="black", linewidth=0.8)
    plt.axvline(100, color="gray", linestyle="--", label="Strike")
    plt.xlabel("Stock Price at Expiration")
    plt.ylabel("Profit/Loss")
    plt.title("Long Call Payoff (K=100, Premium=5)")
    plt.legend()
    plt.savefig("long_call_payoff.png")
    print("Saved long_call_payoff.png")
