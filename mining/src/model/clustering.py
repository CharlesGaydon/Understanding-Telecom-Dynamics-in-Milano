from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import numpy as np


def apply_kmeans(df, nb_clusters):
    kmeansoutput = KMeans(n_clusters=nb_clusters, random_state=0).fit(df)
    return kmeansoutput.labels_


def apply_dbscan(X):
    db = DBSCAN(eps=1, min_samples=5).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    return db.labels_
