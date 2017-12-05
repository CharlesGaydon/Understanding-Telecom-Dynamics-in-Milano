import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

def get_multiple_df(path="data/"):
    allFiles = glob.glob(os.getcwd() + "/" + path + "*.txt-sample.csv")
    frame = pd.DataFrame()
    list_ = []
    for file_ in allFiles:
        df = pd.read_csv(file_, sep=',', header=None)
        list_.append(df)
    return pd.concat(list_)

def get_callin_during_time(path="data/"):
    # take a file and return an dataframe with column1(time) and column2(callin)
    df = get_multiple_df()
    df.columns = ['Id','Square','Time','Country','SMSin','SMSout','Callin','Callout','Internet']
    return np.concatenate(df.fillna(0)[['Time', 'Callin']].groupby('Time', sort=True).mean().as_matrix())

def createstd(data):
    std = np.std(data)
    mean = np.mean(data)
    return ([mean-std]*len(data), [mean+std]*len(data))


