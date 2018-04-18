#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, February 2017

from collections import defaultdict

import numpy as np
from scipy.spatial.distance import cdist, pdist

import measures

# ---------------------------------------------------------------


def intra_inter_class_distances(X, labels, metric):
    """Computes the `intra` and `inter` class distances.

    Args:
        X (np.ndarray): The data array.
        labels (list, np.ndarray): The data labels.
        metric (string, func): The metric type. These are the metrics provided
        by Scipy. See https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html

    Returns:
        The lists of `intra` and `inter` class distances respectively.

    Examples:
        >>> X = np.array(range(1, 26)).reshape((5, 5))
        >>> labels = [0, 1, 0, 0, 1]
        >>> intra, inter = intra_inter_class_distances(X, labels, 'euclidean')
        >>> intra
        [22.360679774997898, 33.54101966249684, 11.180339887498949, 33.54101966249684]
        >>> inter
        [11.180339887498949, 44.721359549995796, 11.180339887498949, 22.360679774997898, 22.360679774997898, 11.180339887498949]

    """

    # validating 'data' and 'labels'
    if not isinstance(X, np.ndarray) or not (isinstance(labels, np.ndarray) or isinstance(labels, list)):
        raise ValueError('Verify data and labels.')

    # getting the values of labels as ndarray
    y = labels.copy() if isinstance(labels, np.ndarray) else np.array(labels)

    # validating consistency between samples and labels
    if X.shape[0] != y.shape[0]:
        raise ValueError('Amount of samples must be the same as the amount of labels.')

    # validating the metric parameter
    if metric is None or not (isinstance(metric, str) or callable(metric)):
        raise ValueError('Invalid metric type.')

    # returning the `intra` and `inter` class comparisons
    return intra_inter_class_comparisons(X, y, metric)


def intra_inter_class_dissimilarities(X, labels, measure):
    """Computes the `intra` and `inter` class dissimilarities.

    Args:
        X (np.ndarray): The data array.
        labels (list, np.ndarray): The data labels.
        measure (int): The type of dissimilarity to use as metric (see 'measures' module).

    Returns:
        The lists of `intra` and `inter` class distances respectively.

    Examples:
        >>> X = np.array(range(1, 26)).reshape((5, 5))
        >>> labels = [0, 1, 0, 0, 1]
        >>> intra, inter = intra_inter_class_dissimilarities(X, labels, measures.EUCLIDEAN)
        >>> intra
        [22.360679774997898, 33.54101966249684, 11.180339887498949, 33.54101966249684]
        >>> inter
        [11.180339887498949, 44.721359549995796, 11.180339887498949, 22.360679774997898, 22.360679774997898, 11.180339887498949]

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

    # getting the comparison function
    cmp_func = measures.measure_to_function[measure]

    # returning the `intra` and `inter` class comparisons
    return intra_inter_class_comparisons(X, y, cmp_func)


def intra_inter_class_comparisons(X, labels, cmp_func):
    """Computes the `intra` and `inter` class comparisons (distances, dissimilarities, similarities).

    Args:
        X (np.ndarray): The data array.
        labels (list, np.ndarray): The data labels.
        cmp_func (string, func): The comparison function for the objects.

    Returns:
        The lists of `intra` and `inter` class distances respectively.

    Examples:
        >>> X = np.array(range(1, 26)).reshape((5, 5))
        >>> labels = [0, 1, 0, 0, 1]
        >>> m = measures.measure_to_function[measures.EUCLIDEAN]
        >>> intra, inter = intra_inter_class_comparisons(X, labels, m)
        >>> intra
        [22.360679774997898, 33.54101966249684, 11.180339887498949, 33.54101966249684]
        >>> inter
        [11.180339887498949, 44.721359549995796, 11.180339887498949, 22.360679774997898, 22.360679774997898, 11.180339887498949]

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
    if cmp_func is None:
        raise ValueError('Invalid comparison function.')

    # validating the metric parameter
    if cmp_func is None or not (isinstance(cmp_func, str) or callable(cmp_func)):
        raise ValueError('Invalid comparison function.')

    # declaring the lists of intra and inter class distances
    intra_dists = []
    inter_dists = []

    # finding the unique labels and sorting them
    y_unique = np.sort(np.unique(y))
    y_unique_len = len(y_unique)

    # computing the range of unique labels (and using ids instead of original labels)
    labels_range = list(range(0, y_unique_len))

    # map of clusters with corresponding samples
    c_list = dict()

    # for each label k
    for k in labels_range:
        if k in c_list:
            ck = c_list[k]
        else:
            c_list[k] = X[np.where(y == y_unique[k])]
            ck = c_list[k]

        # appending all intra-class comparisons of cluster k
        intra_dists += pdist(ck, cmp_func).tolist()

        # for clusters other than k
        for l in labels_range[k + 1:]:
            if l in c_list:
                cl = c_list[l]
            else:
                c_list[l] = X[np.where(y == y_unique[l])]
                cl = c_list[l]

            # appending inter-class comparisons between cluster k and l (https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html)
            inter_dists += np.ravel(cdist(ck, cl, cmp_func)).tolist()

    # returning the intra and inter class distances
    return intra_dists, inter_dists


def cvt_distributions_list_to_dicts(d1, d2, precision=2):
    # validating distributions are lists
    if not isinstance(d1, list) or not isinstance(d2, list):
        raise ValueError('Distributions must be lists')

    # declaring distributions dictionaries
    d1_dict = defaultdict(int)
    d2_dict = defaultdict(int)

    # filling 'd1_dict'
    for p1 in d1:
        d1_dict[round(p1, precision)] += 1

    # filling 'd2_dict'
    for p2 in d2:
        d2_dict[round(p2, precision)] += 1

    # returning distributions dictionaries
    return dict(d1_dict), dict(d2_dict)
