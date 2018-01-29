from mining.src.model.apriori import apriori
from mining.src.model.clustering import *
import pandas as pd
import glob
import re
import datetime
import numpy as np
import time as tt


def init_data():
    # merging multiple files into one pandaframe
    path = 'learning/data'  # use your path
    allFiles = glob.glob(path + "/sms-call-internet-mi-*.txt-sample.csv")
    frame = pd.DataFrame()
    list_ = []
    for file_ in allFiles:
        df = pd.read_csv(file_,delimiter=',',index_col=None, header=0)
        df['day'] = re.search(r'(\d+-\d+-\d+)',file_.split('/')[-1]).group(1)
        list_.append(df)
    frame = pd.concat(list_)
    frame.columns = ['Id', 'Square', 'Time', 'Country', 'SMSin', 'SMSout', 'Callin', 'Callout', 'Internet', 'day']
    return frame


def keep_a_square(x, xmin=20, xmax=60, ymin=15, ymax=60):
    j = x%100
    if j > xmax or j < xmin:
        return False
    i = (x-j)/100
    if i < ymin or i > ymax:
        return False
    return True


def unix_to_ints(unix_code):
     tstamp = datetime.datetime.utcfromtimestamp(unix_code/1000)
     mdH = tstamp.strftime('%m-%d-%H').split('-')
     mdH.append(tstamp.weekday())
     return list(map(int,mdH))


def apply_apriori(df, column, support=60):
    df['TIME'] = df['Time'].apply(unix_to_ints)
    df['TIME'] = df['TIME'].apply(lambda x: x[2])
    df = df.fillna(0)
    gb = df.groupby(['day', 'TIME']).apply(lambda x: (x["Square"], x[column]))
    k = gb.reset_index()

    transactions = []
    days = set(df['day'])
    times = set(df['TIME'])

    t = tt.time()

    for day in days:
        for time in times:
            timeday = list(k[k['TIME'] == time][k['day'] == day].as_matrix())
            square = timeday[0][2][0]
            smsin = timeday[0][2][1]
            std = np.std(smsin)
            data = list(zip(square, smsin))
            data = list(map(lambda x: x[0], filter(lambda x: x[1] > std, data)))
            transactions.append(set(data))

    t1 = tt.time()

    frequent_set = list(map(list, apriori(transactions, len(transactions)/support)))
    print("for=> " + str(t1 - t) + ", apriori=> " + str(tt.time() - t1))

    return frequent_set


# checking how often is in overload when the day is overloaded
def overload_frequence(square, dataset):
    res = 0
    for line in dataset:
        if square in line:
            res += 1
    return res/len(dataset)


def apply_apriori2(df, column, support=60):
    df['TIME'] = df['Time'].apply(unix_to_ints)
    df['TIME'] = df['TIME'].apply(lambda x: x[2])
    df.dropna()
    days = set(df['day'])
    times = set(df['TIME'])

    std = np.std(df[column])
    df = df[df['TIME'] == 12]
    df = df[['Square', column, 'TIME', 'day']]

    transactions = []
    for day in days:
        transaction = set()
        timeday = df[df['day'] == day]
        squares = list(timeday['Square'])
        for square in squares:
            if square > std:
                transaction.add(square)
        transactions.append(transaction)
    frequent_set = list(map(list, apriori(transactions, support)))
    return frequent_set


def get_isolation_forest_result():
    frame = init_data()
    df = frame[frame['Square'].apply(lambda x: keep_a_square(x, 0, 100, 0, 100))]
    df = df.dropna()
    res = apply_isolation_forsest(df[['SMSin', 'SMSout', 'Callin', 'Callout', 'Internet']])
    print(res)
    return dict(zip(list(map(str, df['Square'])), list(map(str, res))))


def get_DBSCAN_result():
    frame = init_data()
    df = frame[frame['Square'].apply(lambda x: keep_a_square(x, 0, 100, 0, 100))]
    df = df.dropna()
    res = apply_dbscan(df[['SMSin', 'SMSout', 'Callin', 'Callout', 'Internet']])
    print(res)
    return dict(zip(list(map(str, df['Square'])), list(map(str, res))))


def get_kmeans_result(nb_clusters):
    frame = init_data()
    df = frame[frame['Square'].apply(lambda x: keep_a_square(x, 0, 100, 0, 100))]
    df = df.dropna()
    res = apply_kmeans(df[['SMSin', 'SMSout', 'Callin', 'Callout', 'Internet']], nb_clusters)
    return dict(zip(list(map(str, df['Square'])), list(map(str, res))))

def get_apriori_result(x1=32, x2=50, x3=20, x4=40, support=60):
    frame = init_data()
    df = frame[frame['Square'].apply(lambda x: keep_a_square(x, x1, x2, x3, x4))]

    result = apply_apriori2(df, 'SMSin', support=support)
    size = 2
    layers = {}
    while True:
        data = list(filter(lambda x: len(x) == size, result))
        if len(data) == 0:
            break
        for lines in data:
            for line in lines:
                layers[str(line)] = size
        size += 1
    return layers




#
# for i in ['SMSin', 'SMSout', 'Callin', 'Callout', 'Internet']:
#     print('#'*30+" "+ i+" "+"#"*30)
#     print(apply_apriori(df, i))
#
#
# rares =isolate(df[['SMSin', 'SMSout', 'Callin', 'Callout', 'Internet']].dropna())
# print(len(df) - sum(rares))

