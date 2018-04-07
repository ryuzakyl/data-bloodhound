#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, March 2017

from sklearn.cluster import KMeans

from scipy.spatial.distance import pdist, squareform

import measures

# ---------------------------------------------------------------

# http://stackoverflow.com/questions/25921762/changes-of-clustering-results-after-each-time-run-in-python-scikit-learn
RND_MAGIC_SALT = 513

# ---------------------------------------------------------------

def kmeans_from_data_in_some_space(X, k, n_init=3):
    """KMeans clustering in some vector space.

    Args:
        X (np.ndarray): The data array.
        k (int): The amount of clusters for the KMeans clustering algorithm.
        n_init (int): The amount of random initializations to try on

    Returns:
        The partition found by KMeans.

    Notes:
        * The space is assumed to be Euclidean.

    References:
        . https://en.wikipedia.org/wiki/K-means_clustering
        . http://scikit-learn.org/stable/modules/clustering.html#k-means
        . http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans

    Examples:
        >>> import numpy as np
        >>> X = np.arange(1, 10).reshape((3, 3))
        >>> true_labels = [0, 0, 1]
        >>> partition = kmeans_from_data_in_some_space(X, 2).tolist()
        >>> partition == true_labels
        True

    """

    # validating the X data
    if X.ndim != 2 or X.shape[0] < 1 or X.shape[1] < 1:
        raise ValueError('Data must be a valid 2D matrix.')

    # validating the amount of clusters
    if k <= 0:
        raise ValueError('The amount of clusters must be positive.')

    # creating an instance of KMeans clustering algorithm
    kmeans = KMeans(n_clusters=k, n_init=n_init, random_state=RND_MAGIC_SALT)

    # performing clustering
    kmeans.fit(X)

    # returning computed partition
    return kmeans.labels_


def kmeans_in_euclidean_space(X, k, n_init=3):
    """KMeans clustering over a Euclidean space.

    Args:
        X (np.ndarray): The data array.
        k (int): The amount of clusters for the KMeans clustering algorithm.
        n_init (int): The amount of random initializations to try on

    Returns:
        The partition found by KMeans.

    References:
        . https://en.wikipedia.org/wiki/K-means_clustering
        . http://scikit-learn.org/stable/modules/clustering.html#k-means
        . http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans

    Examples:
        >>> import numpy as np
        >>> X = np.arange(1, 10).reshape((3, 3))
        >>> true_labels = [0, 0, 1]
        >>> partition = kmeans_in_euclidean_space(X, 2).tolist()
        >>> partition == true_labels
        True

    """

    # validating the X data
    if X.ndim != 2 or X.shape[0] < 1 or X.shape[1] < 1:
        raise ValueError('Data must be a valid 2D matrix.')

    # validating the amount of clusters
    if k <= 0:
        raise ValueError('The amount of clusters must be positive.')

    # returning the partition obtained for kmeans in some space (which is assumed to be euclidean)
    return kmeans_from_data_in_some_space(X, k, n_init=n_init)


def kmeans_in_dissimilarity_space(X, k, measure, n_init=3):
    """KMeans clustering over a Dissimilarity space.

    Args:
        X (np.ndarray): The data array.
        k (int): The amount of clusters for the KMeans clustering algorithm.
        measure (int): The type of dissimilarity to use as metric (see 'measures' module).
        n_init (int): The amount of random initializations to try on

    Returns:
        The partition found by KMeans in the built dissimilarity space.

    References:
        . https://en.wikipedia.org/wiki/K-means_clustering
        . http://scikit-learn.org/stable/modules/clustering.html#k-means
        . http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans

    Examples:
        >>> import numpy as np
        >>> import measures
        >>> X = np.arange(1, 10).reshape((3, 3))
        >>> true_labels = [0, 0, 1]
        >>> partition = kmeans_in_dissimilarity_space(X, 2, measures.EUCLIDEAN).tolist()
        >>> partition == true_labels
        True

    """

    # validating the X data
    if X.ndim != 2 or X.shape[0] < 1 or X.shape[1] < 1:
        raise ValueError('Data must be a valid 2D matrix.')

    # validating the amount of clusters
    if k <= 0:
        raise ValueError('The amount of clusters must be positive.')

    # the specified metric must be one of the implemented measures
    if measure not in measures.measure_to_function:
        raise ValueError('Unknown dissimilarity measure.')

    # getting the metric function
    d = measures.measure_to_function[measure]

    # build distance/dissimilarity matrix
    dm = squareform(pdist(X, d))

    # returning the partition obtained for kmeans in the built space
    return kmeans_from_data_in_some_space(dm, k, n_init=n_init)
