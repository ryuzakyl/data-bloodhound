#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, February 2017

"""Dunn index (clustering validation).

This module aims at giving a simple and fast implementation of
`Dunn-index` for clustering validation.

For more information on this concept, please visit `Dunn-index Wikipedia entry`_.

Note:
    * The Dunn index identifies clusters which are well separated and compact.
    * If Dunn index is large, it means that compact and well separated clusters exist.
    * Based on the implementation on: `Small module with Cluster Validity Indices (CVI) <https://github.com/jqmviegas/jqm_cvi>`_
    * It is computationally expensive and sensitive to noisy data (Halkidi, M., Batistakis, Y., Vazirgiannis, M.: On clustering validation techniques. Journal of Intelligent Information Systems 17(2-3) (2001) 107–145).

References:
    * J. Dunn. Well separated clusters and optimal fuzzy partitions. Journal of Cybernetics, 4:95-104, 1974.
    * Saitta, S., Raphael, B., & Smith, I. F. (2007, July). A bounded index for cluster validity. In International Workshop on Machine Learning and Data Mining in Pattern Recognition (pp. 174-187). Springer Berlin Heidelberg.

Todo:
    * Module TODOs here!!!
    * You have to also use ``sphinx.ext.todo`` extension

.. _Dunn-index Wikipedia entry:
   https://en.wikipedia.org/wiki/Dunn_index

"""

from math import inf as math_inf

import numpy as np
from scipy.spatial.distance import pdist, squareform

import measures

# ----------------------------------------


def min_delta_fast(ck, cl, distances):
    # getting a sub-matrix where 'ck' and 'cl' are 'True'
    values = distances[np.where(ck)][:, np.where(cl)]

    # getting only non-zero values
    values = values[np.nonzero(values)]

    # all values were non-zero. this strange behavior occurs when dissimilarities
    # between all pairs of samples of both clusters are zero. in this case i chose
    # to return 0.0 as a min value
    if values.size == 0:
        return 0.0

    # returning the minimum value
    return np.min(values)


def max_delta_fast(ci, distances):
    # getting a sub-matrix where rows and columns in 'ci' are 'True'
    values = distances[np.where(ci)][:, np.where(ci)]

    # returning the maximum value
    return np.max(values)


def dunn(X, labels, measure):
    """Dunn-index for clustering validation in a dissimilarity space.

    Args:
        X (np.ndarray): The data array.
        labels (list, np.ndarray): The data labels.
        measure (int, string): The type of dissimilarity to use as metric (see 'measures' module).

    Returns:
        The Dunn index for the given clustering

    Notes:
        . High values of Dunn-index indicate better clustering.
        . If the number of clusters `k` is not known a priori, the value `k` for which
        the index is the highest can be chosen as the number of clusters

    References:
        . J. Dunn. Well separated clusters and optimal fuzzy partitions. Journal of Cybernetics,
        4:95-104, 1974.

    Examples:
        >>> import measures
        >>> X = np.array(range(1, 51)).reshape((5, 10))

        # testing 'dunn' in the original space using Euclidean distance as comparison function
        >>> labels = [1, 0, 0, 0, 0]
        >>> dunn(X, labels, measure=measures.EUCLIDEAN)
        0.33333333333333337

        # using 'dunn' with precomputed proximities/comparisons
        >>> d = measures.measure_to_function[measures.EUCLIDEAN]
        >>> D = squareform(pdist(X, d))
        >>> dunn(D, labels, measure='precomputed')
        0.33333333333333337

        # testing 'dunn' in the original space using Cosine distance as comparison function
        >>> dunn(X, labels, measure=measures.COSINE)
        6.1116452342333893

        # using 'dunn' with precomputed proximities/comparisons
        >>> d = measures.measure_to_function[measures.COSINE]
        >>> D = squareform(pdist(X, d))
        >>> dunn(D, labels, measure='precomputed')
        6.1116452342333893

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

    # computing 'min' and 'max' deltas
    min_deltas = np.ones([y_unique_len, y_unique_len]) * math_inf
    max_deltas = np.zeros([y_unique_len, 1])

    # computing the range of unique labels (and using ids instead of original labels)
    labels_range = list(range(0, y_unique_len))

    # for each label k
    for k in labels_range:
        # for clusters other than k
        for l in (labels_range[0:k] + labels_range[k + 1:]):
            # computing the minimum distances of all clusters to cluster k
            min_deltas[k, l] = min_delta_fast((y == y_unique[k]), (y == y_unique[l]), D)

        # computing the maximum distance between pair of objects of cluster k
        max_deltas[k] = max_delta_fast((y == y_unique[k]), D)

    # computing the ratio (minimum inter-cluster distance / maximum intra-cluster distance)
    dunn_index = np.min(min_deltas) / np.max(max_deltas)

    # returning the computed dunn index
    return dunn_index
