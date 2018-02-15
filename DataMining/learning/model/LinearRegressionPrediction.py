import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import TimeSeriesSplit


def linear_regression_prediction(df):
    dim = df[['Time', 'SMSin']].dropna()
    Xs = np.array(dim.drop(['SMSin'], 1)) 
    Ys = np.array(dim.drop(['Time'], 1 ))
    tscv = TimeSeriesSplit(n_splits=3)
    for train_index, test_index in tscv.split(Xs):
        Xs_train, Xs_test = Xs[train_index], Xs[test_index]
        Ys_train, Ys_test = Ys[train_index], Ys[test_index]
    regr = linear_model.LinearRegression()
    regr.fit(Xs_train, Ys_train)
    # y_hat = regr.predict(Xs_test)
    print(regr.score(Xs_test, Ys_test))


