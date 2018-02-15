from learning.model.LinearRegressionPrediction import linear_regression_prediction
from learning.model.SVMPrediction import svm_prediction
from sklearn.neural_network import MLPRegressor
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class PredictionResult:
    def __init__(self, df):
        self.df = df
        self.clusters = {}
    
    def dict2clusters(self, dict_):
        clusters = set(dict_.values())
        temp = {}
        for cluster in clusters:
            temp[cluster] = []
        for k,v in dict_.items():
            temp[v].append(k)
        return temp   

    def reset_clusters(self):
        self.clusters = {}

    def get_cluster(self, name, cluster):
        self.clusters[name] = self.df[self.df['Square'].isin(cluster)]
        
    def predict(self, cluster):
        data = self.clusters[cluster]
        return {'x':list(data['Time']), 'y':list(data['SMSin'])}

    def linear_predict(self, cluster):
        data = self.clusters[cluster]
        linear_regression_prediction(data)

    def svm_predict(self, cluster):
        data = self.clusters[cluster]
        svm_prediction(data)


