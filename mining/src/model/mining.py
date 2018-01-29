from mining.src.model.apriori import apriori
from mining.src.model.clustering import *
from collections import Counter
import pandas as pd
import glob
import re
import datetime
import numpy as np
import time as tt


def init_data(size):
    # merging multiple files into one pandaframe
    path = 'learning/data'  # use your path
    allFiles = glob.glob(path + "/sms-call-internet-mi-*.txt-sample.csv")
    frame = pd.DataFrame()
    list_ = []
    i = 0
    for file_ in allFiles:
        if i == size:
            break
        i += 1
        df = pd.read_csv(file_,delimiter=',',index_col=None, header=0)
        df['day'] = re.search(r'(\d+-\d+-\d+)',file_.split('/')[-1]).group(1)
        list_.append(df)
    frame = pd.concat(list_)
    frame.columns = ['Id', 'Square', 'Time', 'Country', 'SMSin', 'SMSout', 'Callin', 'Callout', 'Internet', 'day']
    # days = set(frame['day'])
    # squares = set(frame['Square'])
    #
    # for day in days:
    #     for square in squares:
    #         d = df[df['Square'] == square]
    #         dt = d[d['day'] == day]
    #
    #         smsin = np.std(dt['SMSin'])
    #         smsout = np.std(dt['SMSout'])
    #         callin = np.std(dt['Callin'])
    #         callout = np.std(dt['Callout'])
    #         internet = np.std(dt['Internet'])
    #
    #

    return frame.sample(frac=0.1)


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


class ClusteringResult:
    def __init__(self, size):
        self.init_data = init_data(size)
        self.mem = {}

    def sort_by_frequency(self, labels):
        freq = list(map(lambda x: x[0], sorted(list(Counter(labels).items()), key=lambda x: -x[1])))
        labels_ = []
        for label in labels:
            labels_.append(freq.index(label))
        return labels_

    def get_isolation_forest_result(self):
        if 'tree' in self.mem:
            return self.mem['tree']
        frame = self.init_data
        df = frame[frame['Square'].apply(lambda x: keep_a_square(x, 0, 100, 0, 100))]
        df = df.dropna()
        res = apply_isolation_forsest(df[['SMSin', 'SMSout', 'Callin', 'Callout', 'Internet']])
        res = self.sort_by_frequency(res)

        labels = dict(zip(list(map(str, df['Square'])), list(map(str, res))))
        self.mem['tree'] = {'labels': labels}
        return {'labels': labels}

    def get_hierarchical_result(self):

        if 'ward' in self.mem:
            return self.mem['ward']
        frame = self.init_data
        df = frame[frame['Square'].apply(lambda x: keep_a_square(x, 0, 100, 0, 100))]
        df = df.dropna()
        res = hierarchichal_ward(df[['SMSin', 'SMSout', 'Callin', 'Callout', 'Internet']])
        res = self.sort_by_frequency(res)
        labels = dict(zip(list(map(str, df['Square'])), list(map(str, res))))
        self.mem['ward'] = {'labels': labels}
        return {'labels': labels}

    def get_DBSCAN_result(self):
        if 'dbscan' in self.mem:
            return self.mem['dbscan']
        frame = self.init_data
        df = frame[frame['Square'].apply(lambda x: keep_a_square(x, 0, 100, 0, 100))]
        df = df.dropna()
        res = apply_dbscan(df[['SMSin', 'SMSout', 'Callin', 'Callout', 'Internet']])
        res = self.sort_by_frequency(res)
        labels = dict(zip(list(map(str, df['Square'])), list(map(str, res))))
        self.mem['dbscan'] = {'labels': labels}
        return {'labels': labels}

    def get_kmeans_result(self, nb_clusters):
        if 'kmean' in self.mem:
            return self.mem['kmean']
        frame = self.init_data
        df = frame[frame['Square'].apply(lambda x: keep_a_square(x, 0, 100, 0, 100))]
        df = df.dropna()
        res, anova = apply_kmeans(df[['SMSin', 'SMSout', 'Callin', 'Callout', 'Internet']], nb_clusters)
        res = self.sort_by_frequency(res)
        labels = dict(zip(list(map(str, df['Square'])), list(map(str, res))))
        self.mem['kmeans'] = {'labels': labels, 'anova': str(anova)}
        return {'labels': labels, 'anova': str(anova)}

    def get_apriori_result(self, x1=45, x2=50, x3=45, x4=50, support=60):
        if 'apriori' in self.mem:
            return self.mem['apriori']
        frame = self.init_data
        df = frame[frame['Square'].apply(lambda x: keep_a_square(x, x1, x2, x3, x4))]
        df['TIME'] = df['Time'].apply(unix_to_ints)
        df['TIME'] = df['TIME'].apply(lambda x: x[2])
        df = df.fillna(0)
        squares = set(df['Square'])
        times = set(df['TIME'])
        transation = []
        for square in squares:
            for time in times:
                d = df[df['Square'] == square]
                dt = set(d[d['TIME'] == time]['day'])
                if len(dt) != 0:
                    transation.append(dt)
        frequent_days = apriori(transation, len(transation)/support)







#
# for i in ['SMSin', 'SMSout', 'Callin', 'Callout', 'Internet']:
#     print('#'*30+" "+ i+" "+"#"*30)
#     print(apply_apriori(df, i))
#
#
# rares =isolate(df[['SMSin', 'SMSout', 'Callin', 'Callout', 'Internet']].dropna())
# print(len(df) - sum(rares))

