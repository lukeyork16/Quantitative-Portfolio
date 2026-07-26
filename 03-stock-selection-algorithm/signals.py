import pandas as pd

def generatetodayssignal(prices, topn=10, method="equal"): #uses the most recent date's data to generate a real, current buy list
    from factors import compositescore
    from selection import buildportfolioweights
    scores=compositescore(prices)
    todaysscores=scores.iloc[-1].dropna()
    weights=buildportfolioweights(todaysscores, topn, method)
    return weights

def printbuylist(weights, portfoliovalue=10000): #turns weights into an actual dollar buy list, same idea as the portfolio optimization project
    print(f"=== Buy List (${portfoliovalue:,} portfolio) ===")
    for ticker, weight in weights.sort_values(ascending=False).items():
        dollars=weight*portfoliovalue
        print(f"{ticker}: {weight:.1%} — ${dollars:,.2f}")

if __name__ == '__main__':
    from data import getuniverse, cleanuniverse, getsp500tickers
    tickers=getsp500tickers()
    prices=getuniverse(tickers)
    prices=cleanuniverse(prices)

    weights=generatetodayssignal(prices, topn=10, method="equal")
    printbuylist(weights, portfoliovalue=10000)
