import numpy as np
import pandas as pd
from sklearn.metrics import log_loss, brier_score_loss

from data import getmultipleseasons
from features import addfeatures
from model import trainmodel

#log loss punishes confident wrong predictions much harder than accuracy does
#brier score is the average squared error between predicted probability and actual outcome (0 or 1), lower is better
def getmetrics(model, x, y):
    probs=model.predict_proba(x)[:,1]

    return {
        "accuracy": model.score(x,y),
        "logloss": log_loss(y, probs),
        "brierscore": brier_score_loss(y, probs),
    }

#checks calibration: when the model says 70% confident, does the team actually win about 70% of the time?
def calibrationtable(model, x, y, nbins=10):
    probs=model.predict_proba(x)[:,1]
    df=pd.DataFrame({"predicted":probs, "actual":y})
    df["bin"]=pd.cut(df["predicted"], bins=nbins)
    calibration=df.groupby("bin", observed=True).agg(
        avgpredicted=("predicted","mean"),
        avgactual=("actual","mean"),
        ngames=("actual","count")
    ).reset_index()
    return calibration

if __name__ == '__main__':
    seasons=[2022, 2023, 2024, 2025]
    rawgames=getmultipleseasons(seasons)
    data=addfeatures(rawgames)
    fullfeatures=["winpctdiff","margindiff","elodiff","restdiff"]

    #evaluate on 2025 as the out-of-sample test, same split used in the walk-forward test
    trainseasons=[2022, 2023, 2024]
    model, xtrain, ytrain, xtest, ytest = trainmodel(data, trainseasons, 2025, fullfeatures)

    metrics=getmetrics(model, xtest, ytest)
    print("=== Out-of-Sample Metrics (2025) ===")
    for key, val in metrics.items():
        print(f"{key}: {val:.4f}")

    print("\n=== Calibration Table ===")
    calibration=calibrationtable(model, xtest, ytest)
    print(calibration)
