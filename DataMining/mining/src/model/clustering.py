from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
import numpy as np
from scipy.cluster.hierarchy import ward, fcluster


rng = np.random.RandomState(42)


def apply_kmeans(df, nb_clusters):
    kmeansoutput = KMeans(n_clusters=nb_clusters, random_state=0).fit(df)
    return kmeansoutput.labels_, kmeansoutput.inertia_


def apply_dbscan(X):
    db = DBSCAN(eps=1.7, min_samples=5).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    return db.labels_


def apply_isolation_forsest(X):
    clf = IsolationForest(random_state=rng, contamination=0.1)
    clf.fit(X)
    res = clf.predict(X)
    return res

def hierarchichal_ward(X):
   Z = ward(X)
   label=fcluster(Z, 3000, criterion='distance', depth=2, R=None, monocrit=None)
   return label
