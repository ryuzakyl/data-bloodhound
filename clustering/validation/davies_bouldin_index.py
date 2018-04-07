#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, February 2017

"""Davies–Bouldin index (clustering validation).

This module aims at giving a simple and fast implementation of
`Davies–Bouldin-index` for clustering validation.

For more information on this concept, please visit `Davies–Bouldin-index Wikipedia entry`_.

Note:
    * Based on the implementation on: `Small module with Cluster Validity Indices (CVI) <https://github.com/jqmviegas/jqm_cvi>`_
    * This has a drawback that a good value reported by this method does not imply the best information retrieval.
    * Davies-Bouldin index (Davies, D., Bouldin, W.: A cluster separation measure. IEEE PAMI 1 (1979) 224–227) identifies clusters which are far from each other and compact.
    * The objective is to obtain clusters with minimum intra-cluster distances, small values for DB are interesting.
    * The index is defined to be `symmetric` and `non-negative`. Due to the way it is defined, as a function of the ratio of the within cluster scatter, to the between cluster separation, a lower value will mean that the clustering is better.

References:
    * D. L. Davies and D. W. Bouldin. A cluster separation measure. IEEE Transactions on Pattern Analysis and Machine Intelligence, 1(2):224-227, 1979.
    * Saitta, S., Raphael, B., & Smith, I. F. (2007, July). A bounded index for cluster validity. In International Workshop on Machine Learning and Data Mining in Pattern Recognition (pp. 174-187). Springer Berlin Heidelberg.

Todo:
    * Module TODOs here!!!
    * You have to also use ``sphinx.ext.todo`` extension

.. _Davies–Bouldin-index Wikipedia entry:
   https://en.wikipedia.org/wiki/Davies%E2%80%93Bouldin_index

"""

from math import inf as math_inf

import numpy as np
from scipy.spatial.distance import pdist, squareform

import measures

# ----------------------------------------


def davies_bouldin(X, labels, measure):
    """Davis-Bouldin index for clustering validation.

    Args:
        X (np.ndarray): The data array.
        labels (list, np.ndarray): The data labels.
        measure (int, string): The type of dissimilarity to use as metric (see 'measures' module).

    Returns:
        The Davis-Bouldin index for the given clustering.

    Notes:
        * Being a function of the ratio of the within cluster scatter, to the between cluster separation, a lower value will mean that the clustering is better.

    References:
        * D. L. Davies and D. W. Bouldin. A cluster separation measure. IEEE Transactions on Pattern Analysis and Machine Intelligence, 1(2):224-227, 1979.

    Examples:
        >>> import measures
        >>> X = np.array(range(1, 51)).reshape((5, 10))

        # testing 'davies_bouldin' using Euclidean distance as comparison function
        >>> labels = [1, 0, 0, 0, 0]
        >>> davies_bouldin(X, labels, measure=measures.EUCLIDEAN)
        0.5

        # using 'davies_bouldin' with precomputed proximities/comparisons
        >>> d = measures.measure_to_function[measures.EUCLIDEAN]
        >>> D = squareform(pdist(X, d))
        >>> davies_bouldin(D, labels, measure='precomputed')
        0.5

        # testing 'davies_bouldin' with different labels and Euclidean distance
        >>> labels = [0, 1, 0, 1, 0]
        >>> davies_bouldin(X, labels, measure=measures.EUCLIDEAN)
        2.3333333333333335

        # testing 'davies_bouldin' with different labels and Euclidean distance
        >>> labels = [0, 0, 1, 0, 0]
        >>> davies_bouldin(X, labels, measure=measures.EUCLIDEAN)
        1.5

        >>> labels = [0, 0, 1, 0, 0]
        >>> davies_bouldin(X, labels, measure=measures.COSINE)
        5.601177024374052

    """

    # validating 'data' and 'labels'
    if not isinstance(X, np.ndarray) or not (isinstance(labels, np.ndarray) or isinstance(labels, list)):
        raise ValueError('Verify data and labels.')

    # getting the values of labels as ndarray
    y = labels.copy() if isinstance(labels, np.ndarray) else np.array(labels)

    # validating consistency between samples and labels
    if X.shape[0] != y.shape[0]:
        raise ValueError('Amount of samples must be the same as the amount of labels.')

    # taking X data as proximity values
    if measure == 'precomputed':
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

    # creating the list holding the barycenters
    bary_idxs = np.zeros([y_unique_len], dtype=np.int)

    # average distance from samples of a cluster to their corresponding barycenter
    small_delta = np.zeros([y_unique_len])

    # computing the range of unique labels (and using ids instead of original labels)
    labels_range = list(range(0, y_unique_len))

    # actually computing the barycenters
    for k in labels_range:
        # getting euclidean distance matrix for cluster k (all rows but columns belonging only to cluster k)
        Dk = np.squeeze(D[:, np.where(y == y_unique[k])], axis=1)

        # adding distances of each sample of cluster k to all the objects
        Dk_dists = np.sum(Dk, axis=1)

        # setting to infinity values for samples not in cluster k (`analyzing` only distances for cluster k)
        Dk_dists[y != y_unique[k]] = math_inf

        # barycenter of cluster k is sample with min cumulative sum of distances
        ck_bary_index = np.argmin(Dk_dists)
        bary_idxs[k] = ck_bary_index

        # storing the average distance of samples to their barycenter
        small_delta[k] = Dk_dists[ck_bary_index] / Dk.shape[1]

    # computing pairwise distances between barycenters
    bary_idxs_index = np.array(bary_idxs)
    bary_euc = D[bary_idxs_index][:, bary_idxs_index]

    # the davies-bouldin index
    db_index = 0.0

    # for each label k
    for k in labels_range:
        # accumulate M value for cluster k
        db_index += np.max([
            (small_delta[k] + small_delta[l]) / bary_euc[k, l]
            for l in labels_range[0:k] + labels_range[k + 1:]
        ])

    # returning the average M value for all clusters
    return db_index / y_unique_len
