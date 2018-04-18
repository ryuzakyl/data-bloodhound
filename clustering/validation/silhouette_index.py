#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, February 2017

"""Silhouette index (clustering validation).

This module aims at giving implementations of `Silhouette-index` for clustering validation.

For more information on this concept, please visit `Silhouette-index Wikipedia entry`_.

Notes:
    * Silhouette analysis can be used to study the separation distance between the resulting clusters. The silhouette plot displays a measure of how close each point in one cluster is to points in the neighboring clusters and thus provides a way to assess parameters like number of clusters visually. This measure has a range of [-1, 1].
    * Silhouette coefficients (as these values are referred to as) near +1 indicate that the sample is far away from the neighboring clusters. A value of 0 indicates that the sample is on or very close to the decision boundary between two neighboring clusters and negative values indicate that those samples might have been assigned to the wrong cluster.

References:
    * Saitta, S., Raphael, B., & Smith, I. F. (2007, July). A bounded index for cluster validity. In International Workshop on Machine Learning and Data Mining in Pattern Recognition (pp. 174-187). Springer Berlin Heidelberg.

Todo:
    * Module TODOs here!!!
    * You have to also use ``sphinx.ext.todo`` extension

.. _Silhouette-index Wikipedia entry:
    https://en.wikipedia.org/wiki/Silhouette_(clustering)

"""

import numpy as np

import sklearn.metrics as skl_metrics

import measures

# ----------------------------------------


def silhouette(X, labels, measure):
    """Silhouette index for clustering validation in a dissimilarity space.

    Args:
        X (np.ndarray): The data array.
        labels (list, np.ndarray): The data labels.
        measure (int, string): The type of dissimilarity to use as metric (see 'measures' module).

    Returns:
        The Silhouette index for the given clustering.

    Notes:
        * Silhouette value near +1 indicate that the sample is far away from the neighboring clusters.
        * A value of 0 indicates that the sample is on or very close to the decision boundary between two neighboring clusters.
        * Negative values indicate that those samples might have been assigned to the wrong cluster.

    Examples:
        >>> import measures
        >>> from scipy.spatial.distance import pdist, squareform
        >>> X = np.array(range(1, 51)).reshape((5, 10))

        # testing 'silhouette' using euclidean distance as a comparison function
        >>> labels = [1, 0, 0, 0, 0]
        >>> silhouette(X, labels, measure=measures.EUCLIDEAN)
        0.17777777777777776
        >>> labels = [1, 0, 1, 0, 1]
        >>> silhouette(X, labels, measure=measures.EUCLIDEAN)
        -0.29999999999999999
        >>> labels = [0, 0, 1, 1, 1]
        >>> silhouette(X, labels, measure=measures.EUCLIDEAN)
        0.46761904761904755

        # testing 'silhouette' using a precomputed proximity/distance matrix
        >>> labels = [1, 0, 0, 0, 0]
        >>> d = measures.measure_to_function[measures.COSINE]
        >>> D = squareform(pdist(X, d))
        >>> silhouette(D, labels, measure='precomputed')
        0.76155606894147576

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

        # using X as proximity matrix and keeping precomputed metric
        m = measure
    else:
        # validating provided measure
        if measure not in measures.measures_list:
            raise ValueError('Unknown measure')

        # getting measure callable
        m = measures.measure_to_function[measure]

    # --------- index computation ---------

    # computing the silhouette scores for each sample
    sil_per_sample = skl_metrics.silhouette_samples(X, y, metric=m)

    # average of silhouette score of all samples
    sil_avg = sil_per_sample.mean()

    # returning the average silhouette index for all the samples
    return sil_avg
