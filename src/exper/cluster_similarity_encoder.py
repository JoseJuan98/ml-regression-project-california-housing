# -*- coding: utf-8 -*-
"""Cluster Similarity transformer using Scikit-learn Transformer API."""

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import rbf_kernel


class ClusterSimilarityEncoder(BaseEstimator, TransformerMixin):
    """Cluster Similarity Encoder.

    Desc:
        It uses KMeans to find the clusters in the data and then uses `rbf_kernel` (radius based function kernel) in
         the transform method to compute the similar samples based in the cluster centroids.
    """

    def __init__(self, n_clusters=10, gamma: float = 1.0, max_iters: int = 300, random_state: int | None = None):
        """Initilize Cluster Similarity Transformer.

        Args:
            n_clusters:
            gamma:
            random_state:
        """
        self.n_clusters = n_clusters
        self.gamma = gamma
        self.random_state = random_state
        self.max_iters = max_iters
        self._kmeans: KMeans | None = None

    def fit(self, X, y=None, sample_weight=None):
        self._kmeans = KMeans(n_clusters=self.n_clusters, max_iter=self.max_iters, random_state=self.random_state)
        self._kmeans.fit(X, sample_weight=sample_weight)
        return self

    def transform(self, X):
        return rbf_kernel(X=X, Y=self._kmeans.cluster_centers_, gamma=self.gamma)

    def get_feature_names_out(self, names=None):
        return [f"cluster_{cluster}_similirity" for cluster in range(self.n_clusters)]
