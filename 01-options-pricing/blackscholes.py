import math
from scipy.stats import norm

#Making the actual core Black-Scholes pricing, takes the 5 standard inputs plus dividend yield q
def d1d2(S,K,T,r,sigma,q=0):
    d1=(math.log(S/K)+(r - q + 0.5*sigma**2)*T)/(sigma*math.sqrt(T))
    d2=d1-sigma*math.sqrt(T)
    return d1, d2

#actual pricing formula, plugs d1/d2 into the call or put version
def price(S,K,T,r,sigma,q=0,optiontype="call"):
    d1,d2=d1d2(S, K, T, r, sigma, q)
    if optiontype =="call":
        return S*math.exp(-q*T)*norm.cdf(d1)-K*math.exp(-r*T)*norm.cdf(d2)
    else:
        return K*math.exp(-r*T)*norm.cdf(-d2)-S*math.exp(-q*T)*norm.cdf(-d1)

#delta, how much the price moves per $1 move in the stock
def delta(S,K,T,r,sigma,q=0,optiontype="call"):
    d1,d2=d1d2(S,K,T,r,sigma,q)
    if optiontype =="call":
        return math.exp(-q*T)*norm.cdf(d1)
    else:
        return math.exp(-q*T)*(norm.cdf(d1) - 1)

#gamma, how fast delta itself changes, same formula for calls and puts
def gamma(S,K,T,r,sigma,q=0):
    d1,d2=d1d2(S,K,T,r,sigma,q)
    return (math.exp(-q*T)*norm.pdf(d1))/(S*sigma*math.sqrt(T))

#vega, sensitivity to a change in volatility, also same for calls and puts
def vega(S,K,T,r,sigma,q=0):
    d1,d2=d1d2(S,K,T,r,sigma,q)
    return S*math.exp(-q*T)*norm.pdf(d1)*math.sqrt(T)

#theta, time decay, how much value the option loses per year just from time passing
def theta(S,K,T,r,sigma,q=0,optiontype="call"):
    d1,d2=d1d2(S,K,T,r,sigma,q)
    term1=-(S*math.exp(-q*T)*norm.pdf(d1)*sigma)/(2*math.sqrt(T))
    if optiontype=="call":
        return term1-r*K*math.exp(-r*T)*norm.cdf(d2)+q*S*math.exp(-q*T)*norm.cdf(d1)
    else:
        return term1+r*K*math.exp(-r*T)*norm.cdf(-d2)-q*S*math.exp(-q*T)*norm.cdf(-d1)

#rho, sensitivity to interest rate changes, usually the smallest greek
def rho(S,K,T,r,sigma,q=0,optiontype="call"):
    d1,d2=d1d2(S,K,T,r,sigma,q)
    if optiontype=="call":
        return K*T*math.exp(-r*T)*norm.cdf(d2)
    else:
        return -K*T*math.exp(-r*T)*norm.cdf(-d2)

if __name__ == '__main__':
    # quick check against known textbook example, S=K=100, 1yr, 5% rate, 20% vol
    p = price(100, 100, 1.0, 0.05, 0.20, optiontype="call")
    print("Call price:", p)
