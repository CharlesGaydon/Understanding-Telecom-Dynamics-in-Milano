import pandas as pd
from sklearn.ensemble import IsolationForest


def isolate(data):
    clf = IsolationForest(n_estimators=1000,
                          max_samples=500,
                          contamination=0.02,
                          max_features=1.01,
                          bootstrap=False,
                          verbose=0)
    clf.fit(data)
    return clf.predict(data)

