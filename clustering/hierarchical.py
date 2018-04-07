#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, March 2017

from sklearn.cluster import AgglomerativeClustering

from scipy.spatial.distance import pdist, squareform

import measures

# ---------------------------------------------------------------

LINKAGE_LIST = ['ward', 'complete', 'average']

# ---------------------------------------------------------------


def agglomerative_clustering_in_some_space(X, k, linkage, affinity):
    """Agglomerative clustering in some space.

    Args:
        X (np.ndarray): The data array.

        k (int): The amount of clusters for the KMeans clustering algorithm.

        linkage: {"ward", "complete", "average"}.
            Which linkage criterion to use. The linkage criterion determines which
            distance to use between sets of observation. The algorithm will merge
            the pairs of cluster that minimize this criterion.

            - ward minimizes the variance of the clusters being merged.
            - average uses the average of the distances of each observation of
              the two sets.
            - complete or maximum linkage uses the maximum distances between
              all observations of the two sets.

        affinity: string or callable
        Metric used to compute the linkage.
        If linkage is "ward", only "euclidean" is accepted.

    Returns:
        The partition found by Agglomerative clustering.

    Notes:
        * The space is assumed to be Euclidean.

    References:
        . http://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html

    Examples:
        >>> import numpy as np
        >>> X = np.array(range(1, 10)).reshape((3, 3))
        >>> labels = [0, 0, 1]
        >>> partition = agglomerative_clustering_in_some_space(X, 2, 'average', 'euclidean').tolist()
        >>> partition == labels
        True
        >>> partition = agglomerative_clustering_in_some_space(X, 2, 'complete', 'euclidean').tolist()
        >>> partition == labels
        True
        >>> partition = agglomerative_clustering_in_some_space(X, 2, 'complete', 'cityblock').tolist()
        >>> partition == labels
        True

    """

    # validating the X data
    if X.ndim != 2 or X.shape[0] < 1 or X.shape[1] < 1:
        raise ValueError('Data must be a valid 2D matrix.')

    # validating the amount of clusters
    if k <= 0:
        raise ValueError('The amount of clusters must be positive.')

    # validating the linkage method
    if linkage not in LINKAGE_LIST:
        raise ValueError('Unknown linkage method.')

    # validating the affinity parameter
    if not isinstance(affinity, str) and not callable(affinity):
        raise ValueError('Affinity must be string or callable.')

    # creating an instance of AgglomerativeClustering clustering algorithm
    ag_clus = AgglomerativeClustering(n_clusters=k, linkage=linkage, affinity=affinity)

    # performing clustering
    ag_clus.fit(X)

    # returning computed partition
    return ag_clus.labels_


def agglomerative_clustering_in_euclidean_space(X, k, linkage):
    """Agglomerative clustering in an Euclidean space.

    Args:
        X (np.ndarray): The data array.

        k (int): The amount of clusters for the KMeans clustering algorithm.

        linkage: {"ward", "complete", "average"}.
            Which linkage criterion to use. The linkage criterion determines which
            distance to use between sets of observation. The algorithm will merge
            the pairs of cluster that minimize this criterion.

            - ward minimizes the variance of the clusters being merged.
            - average uses the average of the distances of each observation of
              the two sets.
            - complete or maximum linkage uses the maximum distances between
              all observations of the two sets.

    Returns:
        The partition found by Agglomerative clustering.

    References:
        . http://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html

    Examples:
        >>> import numpy as np
        >>> X = np.array(range(1, 10)).reshape((3, 3))
        >>> labels = [0, 0, 1]
        >>> partition = agglomerative_clustering_in_euclidean_space(X, 2, 'average').tolist()
        >>> partition == labels
        True
        >>> partition = agglomerative_clustering_in_euclidean_space(X, 2, 'complete').tolist()
        >>> partition == labels
        True

    """

    # validating the X data
    if X.ndim != 2 or X.shape[0] < 1 or X.shape[1] < 1:
        raise ValueError('Data must be a valid 2D matrix.')

    # validating the amount of clusters
    if k <= 0:
        raise ValueError('The amount of clusters must be positive.')

    # validating the linkage method
    if linkage not in LINKAGE_LIST:
        raise ValueError('Unknown linkage method.')

    # returning the partition obtained for agglomerative clustering in the built space
    return agglomerative_clustering_in_some_space(X, k, linkage=linkage, affinity='euclidean')


def agglomerative_clustering_in_pretopological_space(X, k, linkage, measure):
    """Agglomerative clustering in a Pretopological space.

    Args:
        X (np.ndarray): The data array.

        k (int): The amount of clusters for the KMeans clustering algorithm.

        linkage: {"ward", "complete", "average"}.
            Which linkage criterion to use. The linkage criterion determines which
            distance to use between sets of observation. The algorithm will merge
            the pairs of cluster that minimize this criterion.

            - ward minimizes the variance of the clusters being merged.
            - average uses the average of the distances of each observation of
              the two sets.
            - complete or maximum linkage uses the maximum distances between
              all observations of the two sets.

        measure (int): The type of dissimilarity to use as metric (see 'measures' module).

    Notes:
        The dissimilarity measure is used as affinity between objects.

    Returns:
        The partition found by Agglomerative clustering.

    References:
        . http://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html

    Examples:
        >>> import numpy as np
        >>> X = np.array(range(1, 10)).reshape((3, 3))
        >>> labels = [0, 0, 1]
        >>> partition = agglomerative_clustering_in_pretopological_space(X, 2, 'average', measure=measures.EUCLIDEAN).tolist()
        >>> partition == labels
        True
        >>> partition = agglomerative_clustering_in_pretopological_space(X, 2, 'complete', measure=measures.MANHATTAN).tolist()
        >>> partition == labels
        True

    """

    # validating the X data
    if X.ndim != 2 or X.shape[0] < 1 or X.shape[1] < 1:
        raise ValueError('Data must be a valid 2D matrix.')

    # validating the amount of clusters
    if k <= 0:
        raise ValueError('The amount of clusters must be positive.')

    # validating the linkage method
    if linkage not in LINKAGE_LIST:
        raise ValueError('Unknown linkage method.')

    # the specified metric must be one of the implemented measures
    if measure not in measures.measure_to_function:
        raise ValueError('Unknown dissimilarity measure.')

    # getting the metric function
    d = measures.measure_to_function[measure]

    # build distance/dissimilarity matrix
    dm = squareform(pdist(X, d))

    # returning the partition obtained for agglomerative clustering in the built space
    return agglomerative_clustering_in_some_space(dm, k, linkage=linkage, affinity='precomputed')


def agglomerative_clustering_in_dissimilarity_space(X, k, linkage, measure):
    """Agglomerative clustering in a Dissimilarity space.

    Args:
        X (np.ndarray): The data array.

        k (int): The amount of clusters for the KMeans clustering algorithm.

        linkage: {"ward", "complete", "average"}.
            Which linkage criterion to use. The linkage criterion determines which
            distance to use between sets of observation. The algorithm will merge
            the pairs of cluster that minimize this criterion.

            - ward minimizes the variance of the clusters being merged.
            - average uses the average of the distances of each observation of
              the two sets.
            - complete or maximum linkage uses the maximum distances between
              all observations of the two sets.

        measure (int): The type of dissimilarity to use as metric (see 'measures' module).

    Returns:
        The partition found by Agglomerative clustering.

    References:
        . http://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html

    Examples:
        >>> import numpy as np
        >>> X = np.array(range(1, 10)).reshape((3, 3))
        >>> labels = [0, 0, 1]
        >>> partition = agglomerative_clustering_in_dissimilarity_space(X, 2, 'average', measure=measures.EUCLIDEAN).tolist()
        >>> partition == labels
        True
        >>> partition = agglomerative_clustering_in_dissimilarity_space(X, 2, 'complete', measure=measures.MANHATTAN).tolist()
        >>> partition == labels
        True

    """

    # validating the X data
    if X.ndim != 2 or X.shape[0] < 1 or X.shape[1] < 1:
        raise ValueError('Data must be a valid 2D matrix.')

    # validating the amount of clusters
    if k <= 0:
        raise ValueError('The amount of clusters must be positive.')

    # validating the linkage method
    if linkage not in LINKAGE_LIST:
        raise ValueError('Unknown linkage method.')

    # the specified metric must be one of the implemented measures
    if measure not in measures.measure_to_function:
        raise ValueError('Unknown dissimilarity measure.')

    # getting the metric function
    d = measures.measure_to_function[measure]

    # build distance/dissimilarity matrix
    dm = squareform(pdist(X, d))

    # returning the partition obtained for agglomerative clustering in the built space
    return agglomerative_clustering_in_some_space(dm, k, linkage=linkage, affinity='euclidean')
