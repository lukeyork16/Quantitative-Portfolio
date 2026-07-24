import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression

from data import getmultipleseasons
from features import addfeatures

def trainmodel(data, trainseasons, testseason, featurecols):
    train = data[data["season"].isin(trainseasons)]
    test = data[data["season"]==testseason]

    xtrain = train[featurecols]
    ytrain = train["homewin"]
    xtest = test[featurecols]
    ytest = test["homewin"]

    model = LogisticRegression()
    model.fit(xtrain, ytrain)

    return model, xtrain, ytrain, xtest, ytest

def savemodel(model, path="wnbamodel.pkl"):
    with open(path, "wb") as f:
        pickle.dump(model, f)

def loadmodel(path="wnbamodel.pkl"):
    with open(path, "rb") as f:
        return pickle.load(f)


if __name__ == '__main__':
    seasons = [2022, 2023, 2024, 2025]
    rawgames = getmultipleseasons(seasons)
    data = addfeatures(rawgames)

    fullfeatures = ["winpctdiff","margindiff","elodiff","restdiff"]

    #walk-forward cross validation: for each season, train only on seasons that came before it
    print("=== Walk-Forward Cross-Validation ===")
    results = []
    for testseason in [2023, 2024, 2025]:
        trainseasons = [s for s in seasons if s < testseason]

        model, xtrain, ytrain, xtest, ytest = trainmodel(data, trainseasons, testseason, fullfeatures)
        modelacc = model.score(xtest, ytest)

        #baseline 1: home team always wins
        homebaseline = ytest.mean()

        #baseline 2: elo alone, no other features
        eloonly, _, _, xtesteloonly, ytesteloonly = trainmodel(data, trainseasons, testseason, ["elodiff"])
        eloacc = eloonly.score(xtesteloonly, ytesteloonly)

        results.append({"testseason":testseason, "hometeamalwayswins":homebaseline, "eloonly":eloacc, "fullmodel":modelacc})
        print(f"{testseason} — Home-always-wins: {homebaseline:.4f} | Elo-only: {eloacc:.4f} | Full model: {modelacc:.4f}")

    resultsdf = pd.DataFrame(results)
    print("\nAverage across seasons:")
    print(resultsdf.mean(numeric_only=True))

    #train the final model on everything, save it for predicting future games
    finalmodel, xtrain, ytrain, _, _ = trainmodel(data, seasons, testseason=9999, featurecols=fullfeatures)
    finalmodel.fit(data[fullfeatures], data["homewin"])
    savemodel(finalmodel)
    print("\nFinal model (trained on all seasons) saved to wnbamodel.pkl")
