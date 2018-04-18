#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, February 2017

import numpy as np
from sklearn import metrics
from scipy.spatial.distance import pdist, squareform

from measures import measure_to_function as d_to_f

# ---------------------------------------------------------------


def silhouette_score_from_data(X, labels, measure):
    """Computes the silhouette score.

    Note:
        Additional info can be found here:
        . http://scikit-learn.org/stable/modules/clustering.html#silhouette-coefficient
        . http://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html

    Args:
        X (ndarray): The data to be analyzed.
        labels (ndarray, list): The labels of X data.
        measure: The measure (metric or not) used as a metric for silhouette.

    Returns:
        The silhouette score for the given data and provided labels.

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
    if measure not in d_to_f:
        raise ValueError('Unknown dissimilarity measure.')

    # getting the metric function
    d = d_to_f[measure]

    # build distance/dissimilarity matrix
    dm = squareform(pdist(X, d))

    # compute silhouette from distance matrix
    return silhouette_score_from_dist_mat(dm, y)


def silhouette_score_from_dist_mat(X, labels):
    """Computes the silhouette score from a distance matrix.

    Note:
        Additional info can be found here:
        . http://scikit-learn.org/stable/modules/clustering.html#silhouette-coefficient
        . http://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html

    Args:
        X (ndarray): The distance matrix.
        labels (ndarray, list): The labels of the original X data.

    Returns:
        The silhouette score for the distance matrix and provided labels.

    """

    # validating 'data' and 'labels'
    if not isinstance(X, np.ndarray) or not (isinstance(labels, np.ndarray) or isinstance(labels, list)):
        raise ValueError('Distributions must be lists')

    # getting the values of labels as ndarray
    y = labels.copy() if isinstance(labels, np.ndarray) else np.array(labels)

    # computing the silhouette score
    return metrics.silhouette_score(X, y, metric='precomputed')
