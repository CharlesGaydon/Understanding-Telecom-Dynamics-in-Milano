from sklearn.model_selection import train_test_split
from sklearn import svm
import pandas as pd
import numpy as np


def svm_prediction(df):
    dim = df[['SMSin', 'SMSout', 'Callin', 'Callout', 'Internet', 'overload']]
    X_train, X_test, y_train, y_test = train_test_split(dim[['SMSin', 'SMSout', 'Callin', 'Callout', 'Internet']], dim['overload'], test_size=.4, random_state=0)
    clf = svm.SVC()
    clf.fit(X_train, y_train)
    y_hat = clf.predict(X_test)
    print(np.array(y_test))
    print(y_hat)
    print(np.linalg.norm(np.array(list(map(int, y_test))) - np.array(list(map(int, y_hat)))))
    
