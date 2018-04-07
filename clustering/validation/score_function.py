#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, March 2017

"""Score Function (clustering validation).

This module aims at giving a simple and fast implementation of ``Score Function`` for clustering validation.

Note:
    * Can be used to estimate the number of clusters in a data set.
    * Based on inter-cluster and intra-cluster distances.
    * Used for two purposes:
        * To estimate the number of clusters
        * To evaluate the quality of the clustering results
    * The score function is a function combining two terms: the distance between clusters and the distance inside a cluster.
    * The higher the value of the SF, the more suitable the number of clusters.

References:
    * Saitta, S., Raphael, B., & Smith, I. F. (2007, July). A bounded index for cluster validity. In International Workshop on Machine Learning and Data Mining in Pattern Recognition (pp. 174-187). Springer Berlin Heidelberg.

Todo:
    * Module TODOs here!!!
    * You have to also use ``sphinx.ext.todo`` extension

"""

from math import exp

import numpy as np
from scipy.spatial.distance import pdist, squareform

import measures

# ----------------------------------------


def score_function(X, labels, measure=None):
    """Score Function for clustering validation in an Dissimilarity space.

    Args:
        X (np.ndarray): The data array.
        labels (list, np.ndarray): The data labels.
        measure (int, string): The type of dissimilarity to use as metric (see 'measures' module).

    Returns:
        The Score Function for the given clustering.

    Notes:
        * The higher the value of the SF, the more suitable the number of clusters.

    Examples:
        >>> import measures
        >>> X = np.arange(1, 51).reshape((5, 10))

        # performing score function in the original euclidean space
        >>> labels = [0, 1, 0, 1, 0]
        >>> score_function(X, labels)
        0.3077993724446536
        >>> labels = [1, 1, 1, 0, 0]
        >>> score_function(X, labels)
        0.5159665227661613
        >>> labels = [1, 0, 0, 0, 1]
        >>> score_function(X, labels)
        0.3077993724446536

        # computing score function in a dissimilarity space
        >>> labels = [0, 1, 0, 1, 0]
        >>> score_function(X, labels, measures.KOLMOGOROV)
        0.36451454927650895
        >>> labels = [0, 0, 1, 1, 1]
        >>> score_function(X, labels, measures.COSINE)
        0.4363882069164694
        >>> labels = [0, 1, 1, 1, 1]
        >>> score_function(X, labels, measures.SAM)
        0.6992230437603538

    """

    # validating 'data' and 'labels'
    if not isinstance(X, np.ndarray) or not (isinstance(labels, np.ndarray) or isinstance(labels, list)):
        raise ValueError('Verify data and labels.')

    # getting the values of labels as ndarray
    y = labels.copy() if isinstance(labels, np.ndarray) else np.array(labels)

    # validating consistency between samples and labels
    if X.shape[0] != y.shape[0]:
        raise ValueError('Amount of samples must be the same as the amount of labels.')

    # performing SF on the original data
    if measure is None:
        D = X

    # taking X data as proximity values
    elif measure == 'precomputed':
        # checking for square matrix
        if X.shape[0] != X.shape[1]:
            raise ValueError('Proximity matrix must be a squared matrix.')

        # using X as proximity matrix
        D = X
    else:
        # validating provided measure
        if measure not in measures.measures_list:
            raise ValueError('Unknown measure')

        # building distance/dissimilarity matrix
        d = measures.measure_to_function[measure]
        D = squareform(pdist(X, d))

        # --------- index computation ---------

    # finding the unique labels and sorting them
    y_unique = np.sort(np.unique(y))
    y_unique_len = len(y_unique)

    # computing the range of unique labels (and using ids instead of original labels)
    labels_range = list(range(0, y_unique_len))

    # variables of interest in the paper's definition
    k = y_unique_len
    n = D.shape[0]
    bcd = 0.0
    wcd = 0.0

    # computing mean of all data (rows axis)
    z_tot = np.mean(D, axis=0)

    # for each label i
    for i in labels_range:
        # getting cluster i samples data
        ci = D[np.where(y == y_unique[i])]

        # number of items in cluster 'ci'
        ni = ci.shape[0]

        # computing the centroid of cluster 'i'
        zi = np.mean(ci, axis=0)

        # 2-norm of means difference vector x ni
        bcd += np.linalg.norm(zi - z_tot) * ni

        # cumulative normalized 2-norm of 'distance' of each item in the cluster to the centroid
        wcd += (1 / ni) * sum(map(lambda v: np.linalg.norm(v - zi), ci))

    # finally computing 'bcd'
    bcd /= n * k

    # computing the 'score function'
    x = (bcd - wcd) / (bcd + wcd)
    sf = 1 - (1 / exp(exp(x)))

    # returning the finally computed index
    return sf
