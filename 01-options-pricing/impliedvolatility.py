from blackscholes import price, vega

def findvol(marketprice,S,K,T,r,optiontype="call",guess=0.20,tol=1e-6,maxiter=100): #newton's method, vega tells us how fast price changes with sigma
    sigma=guess
    for i in range(maxiter):
        modelprice=price(S,K,T,r,sigma,optiontype=optiontype)
        v=vega(S,K,T,r,sigma)
        diff=modelprice-marketprice
        if abs(diff)<tol:
            return sigma
        if v<1e-8:
            break #vega too small here, newton gets shaky, switch to bisection instead
        sigma=sigma-diff/v
        if sigma<=0:
            sigma=1e-4
    return findvolbackup(marketprice,S,K,T,r,optiontype)

def findvolbackup(marketprice,S,K,T,r,optiontype="call",low=1e-4,high=5.0,tol=1e-6,maxiter=200): #slower but never fails, keeps cutting the range in half
    for i in range(maxiter):
        mid=(low+high)/2
        modelprice=price(S,K,T,r,mid,optiontype=optiontype)
        if abs(modelprice-marketprice)<tol:
            return mid
        if modelprice>marketprice:
            high=mid
        else:
            low=mid
    return (low+high)/2

if __name__ == '__main__':
    truevol=0.25 #price something at a known vol, then solve backwards and see if we land on the same spot
    marketprice=price(100,105,0.5,0.04,truevol,optiontype="call")
    solved=findvol(marketprice,S=100,K=105,T=0.5,r=0.04,optiontype="call")
    print(f"True vol: {truevol:.4f} | Solved vol: {solved:.4f}")
