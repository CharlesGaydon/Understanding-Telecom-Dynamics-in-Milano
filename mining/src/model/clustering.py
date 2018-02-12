from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.cluster import AffinityPropagation
import numpy as np

rng = np.random.RandomState(42)

def apply_kmeans(df, nb_clusters):
    kmeansoutput = KMeans(n_clusters=nb_clusters, random_state=0).fit(df)
    return kmeansoutput.labels_


def apply_dbscan(X):
    db = DBSCAN(eps=1, min_samples=5).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    return db.labels_


def apply_isolation_forsest(X):
    clf = IsolationForest(max_samples=100, random_state=rng)
    clf.fit(X)
    return clf.predict(X)

def affinity_propagation(X):
    af = AffinityPropagation(preference=-50).fit(X)
    cluster_centers_indices = af.cluster_centers_indices_
    return af.labels_