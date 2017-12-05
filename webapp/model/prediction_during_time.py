import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_callin_during_time(filename):
    # take a file and return an dataframe with column1(time) and column2(callin)
    df = pd.read_csv(filename, sep = '\t', header=None)
    df.columns = ['Square','Time','Country','SMSin','SMSout','Callin','Callout','Internet']
    return df.fillna(0)[['Time', 'Callin']].groupby(['Time'], sort=True).mean()

def test():
    plt.plot(get_callin_during_time('data/sms.csv'))
    plt.show()
