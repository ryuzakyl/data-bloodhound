#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, February 2017

import numpy as np
from sklearn import manifold
from scipy.spatial.distance import pdist, squareform

import measures

# ---------------------------------------------------------------


def dr_mds_rayleigh(X, labels, measure, k=5):
    """Computes the Fisher score in an embedded Euclidean space from the dissimilarity matrix.

    Args:
        X (ndarray): The data to be analyzed.
        labels (ndarray, list): The labels of X data.
        measure: The measure (metric or not) used as a metric for the dissimilarity representation.
        k: Amount of times that MDS + Rayleigh will be performed (MDS implementation is non-deterministic)

    Returns:
        The average Rayleigh coefficient for the given data and provided labels.

    Note:
        Additional info can be found here:
        . http://scikit-learn.org/stable/modules/generated/sklearn.manifold.MDS.html

    """

    # validating 'data' and 'labels'
    if not isinstance(X, np.ndarray) or not (isinstance(labels, np.ndarray) or isinstance(labels, list)):
        raise ValueError('Verify data and labels.')

    # getting the values of labels as ndarray
    y = labels.copy() if isinstance(labels, np.ndarray) else np.array(labels)

    # validating consistency between samples and labels
    if X.shape[0] != y.shape[0]:
        raise ValueError('Amount of samples must be the same as the amount of labels.')

    # the specified metric must be one of the implemented measures
    if measure not in measures.measure_to_function:
        raise ValueError('Unknown dissimilarity measure.')

    # getting the metric function
    d = measures.measure_to_function[measure]

    # build distance/dissimilarity matrix
    dm = squareform(pdist(X, d))

    # size of the embedded euclidean feature space
    n_comps = dm.shape[0]

    # performing MDS + Rayleigh k times
    avg_rayleigh = 0.0
    for i in range(k):
        # performing MDS embedding
        mds = manifold.MDS(n_components=n_comps, dissimilarity='precomputed')
        mds_data = mds.fit_transform(dm)

        # computation of the rayleigh criterion
        avg_rayleigh += compute_rayleigh_coefficient(mds_data, labels)

    # computing average
    avg_rayleigh /= k

    # returning the average rayleigh coefficient
    return avg_rayleigh


def compute_rayleigh_coefficient(X, labels):
    """Rayleigh coefficient for a given clustering.

    Args:
        X (np.ndarray): The data array.
        labels (list, np.ndarray): The data labels.

    Returns:
        The Rayleigh coefficient for the 'given' space direction

    Note:
        . The higher the coefficient, the better clustering.
        . This coefficient/ratio underlies the optimization problem of LDA.

    References:
        . Dehak, N., Kenny, P. J., Dehak, R., Dumouchel, P., & Ouellet, P. (2011). Front-end
        factor analysis for speaker verification. IEEE Transactions on Audio, Speech, and
        Language Processing, 19(4), 788-798.

    Examples:
        >>> X = np.array(range(1, 26)).reshape((5, 5))
        >>> labels = [0, 1, 0, 0, 1]
        >>> compute_rayleigh_coefficient(X, labels)
        0.094890510948905091
        >>> labels = [0, 0, 1, 1, 1]
        >>> compute_rayleigh_coefficient(X, labels)
        3.5454545454545454

    """

    # validating 'data' and 'labels'
    if not isinstance(X, np.ndarray) or not (isinstance(labels, np.ndarray) or isinstance(labels, list)):
        raise ValueError('Verify data and labels.')

    # getting the values of labels as ndarray
    y = labels.copy() if isinstance(labels, np.ndarray) else np.array(labels)

    # validating consistency between samples and labels
    if X.shape[0] != y.shape[0]:
        raise ValueError('Amount of samples must be the same as the amount of labels.')

    # computing the 'inter-class' variance
    sb = 0.0

    # computing the 'intra-class' variance
    sw = 0.0

    # finding the unique labels and sorting them
    y_unique = np.sort(np.unique(y))
    y_unique_len = len(y_unique)

    # computing the range of unique labels (and using ids instead of original labels)
    labels_range = list(range(0, y_unique_len))

    # computing mean of all data (rows axis)
    w = np.mean(X, axis=0)

    # for each label k
    for k in labels_range:
        # getting cluster k samples data
        ck = X[np.where(y == y_unique[k])]

        # computing the mean of class 'si'
        wk = np.mean(ck, axis=0)

        # accounting for inter-class variance of class 'k'
        sb += np.dot(wk - w, wk - w)

        # getting class 'k' cardinality
        nk = ck.shape[0]

        # accounting for intra-class variance of class 'k'
        sw += (1.0 / nk) * sum(map(lambda v: np.dot(v - wk, v - wk), ck))

    # returning the rayleigh quotient
    return sb / sw
