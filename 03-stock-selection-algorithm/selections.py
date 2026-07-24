import pandas as pd
import numpy as np

def selecttopstocks(scores, topn=10): #picks the top N stocks by composite score, for a single date's scores
    return scores.sort_values(ascending=False).head(topn)

def buildportfolioweights(scores, topn=10, method="equal"): #turns the top N picks into portfolio weights, equal weight or score weighted
    picks=selecttopstocks(scores, topn)
    if method=="equal":
        weights=pd.Series(1/topn, index=picks.index)
    else: #score weighted, better scores get bigger positions but never negative
        shiftedscores=picks-picks.min()+0.01 #shift so everything is positive, avoids negative weights
        weights=shiftedscores/shiftedscores.sum()
    return weights

def monthlyrebalanceweights(compositescores, topn=10, method="equal"): #builds a full history of portfolio weights, rebalanced at the start of every month
    rebalancedates=compositescores.resample("MS").first().index #MS = month start, one rebalance date per month
    alldates=compositescores.index

    weightshistory=pd.DataFrame(0.0, index=alldates, columns=compositescores.columns)
    currentweights=pd.Series(0.0, index=compositescores.columns)

    for date in alldates:
        if date in rebalancedates or date==alldates[0]: #only actually recompute weights on rebalance dates
            scorestoday=compositescores.loc[date].dropna()
            if len(scorestoday)>=topn:
                currentweights=pd.Series(0.0, index=compositescores.columns)
                picks=buildportfolioweights(scorestoday, topn, method)
                currentweights[picks.index]=picks.values
        weightshistory.loc[date]=currentweights

    return weightshistory

if __name__ == '__main__':
    from data import getuniverse, cleanuniverse
    from factors import compositescore
    tickers=["AAPL","MSFT","GOOGL","AMZN","NVDA","META","TSLA","JPM","BAC","WFC","GS","MS",
              "XOM","CVX","COP","JNJ","PFE","UNH","ABBV","KO","PG","WMT","COST","MCD",
              "DIS","NFLX","V","MA","HD","LOW","BA","CAT","GE","INTC","AMD","CRM","ADBE","ORCL","IBM","CSCO"]
    prices=getuniverse(tickers)
    prices=cleanuniverse(prices)

    scores=compositescore(prices)
    weights=monthlyrebalanceweights(scores, topn=10, method="equal")

    print("Portfolio weights, most recent date:")
    print(weights.iloc[-1][weights.iloc[-1]>0])
    print(f"\nWeights sum to: {weights.iloc[-1].sum():.4f}")
