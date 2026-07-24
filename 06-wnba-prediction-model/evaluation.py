import numpy as np
import pandas as pd
from sklearn.metrics import log_loss, brier_score_loss
from data import getmultipleseasons
from features import addfeatures
from model import trainmodel

def getmetrics(model, x, y): #logloss punishes confident wrong picks harder than accuracy does, brier is avg squared error on the probabilities
    probs=model.predict_proba(x)[:,1]
    return {
        "accuracy": model.score(x,y),
        "logloss": log_loss(y, probs),
        "brierscore": brier_score_loss(y, probs),
    }

def calibrationtable(model, x, y, nbins=10): #checks if "70% confident" predictions actually win about 70% of the time
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
    trainseasons=[2022, 2023, 2024] #evaluate on 2025 as out-of-sample, same split as the walk-forward test
    model, xtrain, ytrain, xtest, ytest = trainmodel(data, trainseasons, 2025, fullfeatures)
    metrics=getmetrics(model, xtest, ytest)
    print("=== Out-of-Sample Metrics (2025) ===")
    for key, val in metrics.items():
        print(f"{key}: {val:.4f}")
    print("\n=== Calibration Table ===")
    calibration=calibrationtable(model, xtest, ytest)
    print(calibration)
