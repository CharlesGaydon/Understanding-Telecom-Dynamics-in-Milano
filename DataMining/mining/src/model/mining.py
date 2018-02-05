from mining.src.model.apriori import apriori
from mining.src.model.clustering import apply_isolation_forsest, apply_dbscan, apply_kmeans, hierarchichal_ward
from collections import Counter
import pandas as pd
import glob
import re
import datetime
import numpy as np
import time as tt
from sklearn import preprocessing


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


# checking how often is in overload when the day is overloadd
def overload_frequence(square, dataset):
    res = 0
    for line in dataset:
        if square in line:
            res += 1
    return res/len(dataset)

class ClusteringResult:
    def __init__(self, size, init_data):
        self.init_data = init_data
        self.mem = {}

    def get_most_frequent(self, df, labels):
        df['label'] = labels
        squares = set(df['Square'])
        res = []
        for square in squares:
            res.append((str(square), str(np.argmax(np.bincount(df[df['Square'] == square]['label'])))))
        return res

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
        labels = dict(self.get_most_frequent(df, res))
        self.mem['tree'] = {'labels': labels}
        return {'labels': labels}

    def get_hierarchical_result(self):
        if 'ward' in self.mem:
            return self.mem['ward']
        frame = self.init_data.sample(frac=.7)
        df = frame[frame['Square'].apply(lambda x: keep_a_square(x, 0, 100, 0, 100))]
        df = df.dropna()
        res = hierarchichal_ward(df[['SMSin', 'SMSout', 'Callin', 'Callout', 'Internet']])
        res = self.sort_by_frequency(res)
        labels = dict(self.get_most_frequent(df, res))
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
        labels = dict(self.get_most_frequent(df, res))
        self.mem['dbscan'] = {'labels': labels}
        return {'labels': labels}

    def get_kmeans_result(self, nb_clusters):
        if 'kmeans' + str(nb_clusters) in self.mem:
            return self.mem['kmeans' + str(nb_clusters)]
        frame = self.init_data
        df = frame[frame['Square'].apply(lambda x: keep_a_square(x, 0, 100, 0, 100))]
        df = df.dropna()
        res, anova = apply_kmeans(df[['SMSin', 'SMSout', 'Callin', 'Callout', 'Internet']], nb_clusters)
        res = self.sort_by_frequency(res)
        labels = dict(self.get_most_frequent(df, res))
        self.mem['kmeans' + str(nb_clusters)] = {'labels': labels, 'anova': str(anova)}
        return {'labels': labels, 'anova': str(anova)}

    @staticmethod
    def get_cluster(data, clusters, cluster_id):
        squares = []
        for square, cluster in clusters.items():
            if cluster == cluster_id:
                squares.append(square)
        return data[data['Square'].isin(squares)]

    def apriori_on_days(self, cluster):
        pass

    def apply_apriori(self, column, support=60):
        df = self.init_data
        df['TIME'] = df['Time'].apply(unix_to_ints)
        df['TIME'] = df['TIME'].apply(lambda x: x[2])
        df = df.fillna(0)

        transactions = []
        squares = set(df['Square'])
        t = tt.time()

        for square in squares:
            for time in [12]:
                timeday = df[df['TIME'] == time]
                timeday = timeday[timeday['Square'] == square]
                day = timeday['day']
                data = list(day)
                if len(data) > 0:
                    transactions.append(set(data))

        t1 = tt.time()
        print(transactions)
        frequent_set = list(map(list, apriori(transactions, support)))
        print("for=> " + str(t1 - t) + ", apriori=> " + str(tt.time() - t1))

        # frequent_set = list(filter(lambda x: len(x) > 2, frequent_set))
        return frequent_set







#
# for i in ['SMSin', 'SMSout', 'Callin', 'Callout', 'Internet']:
#     print('#'*30+" "+ i+" "+"#"*30)
#     print(apply_apriori(df, i))
#
#
# rares =isolate(df[['SMSin', 'SMSout', 'Callin', 'Callout', 'Internet']].dropna())
# print(len(df) - sum(rares))

