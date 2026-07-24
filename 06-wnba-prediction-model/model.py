import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from data import getmultipleseasons
from features import addfeatures

#trains on earlier seasons, tests on the most recent one, genuine out of sample
def trainmodel(data, testseasons):
    train=data[~data["season"].isin(testseasons)]
    test=data[data["season"].isin(testseasons)]
    featurecols=["winpctdiff","margindiff"]
    xtrain=train[featurecols]
    ytrain=train["homewin"]
    xtest=test[featurecols]
    ytest=test["homewin"]
    model=LogisticRegression()
    model.fit(xtrain, ytrain)

    return model, xtrain, ytrain, xtest, ytest
#saves the trained model to disk so it can be reused for predicting future games without retraining
def savemodel(model, path="wnbamodel.pkl"):
    with open(path, "wb") as f:
        pickle.dump(model, f)
#loads a previously saved model
def loadmodel(path="wnbamodel.pkl"):
    with open(path, "rb") as f:
        return pickle.load(f)

if __name__ == '__main__':
    seasons=[2022, 2023, 2024, 2025]
    rawgames=getmultipleseasons(seasons)
    data=addfeatures(rawgames)

    #train on everything except 2025, test purely on 2025, never seen during training
    model, xtrain, ytrain, xtest, ytest=trainmodel(data, testseasons=[2025])
    trainacc=model.score(xtrain, ytrain)
    testacc=model.score(xtest, ytest)
    print(f"Train accuracy: {trainacc:.4f}")
    print(f"Test accuracy (out-of-sample, 2025 only): {testacc:.4f}")
    print(f"Model coefficients: winpctdiff={model.coef_[0][0]:.4f}, margindiff={model.coef_[0][1]:.4f}")
    print(f"Intercept (home court edge): {model.intercept_[0]:.4f}")
    savemodel(model)
    print("\nModel saved to wnbamodel.pkl")
