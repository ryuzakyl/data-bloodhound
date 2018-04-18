#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, May 2017

"""K-Medoids clustering algorithm

This module aims at giving a simple implementation of ``K-Medoids`` clustering algorithm.

For more information on this concept, please visit `K-Medoids Wikipedia entry`_.

Note:
    * Based on the implementation on: `K-Medoids implementation <https://github.com/letiantian/kmedoids>`_

References:
    * Bauckhage, C. (2015). Numpy/scipy Recipes for Data Science: k-Medoids Clustering. researchgate.net, Feb.

Todo:
    * Module TODOs here!!!
    * You have to also use ``sphinx.ext.todo`` extension

.. _K-Medoids Wikipedia entry:
   https://en.wikipedia.org/wiki/K-medoids

"""

import numpy as np
from scipy.spatial.distance import pdist, squareform

import measures

# ---------------------------------------------------------------


def kmedoids(X, k, measure, tmax=100):
    """K-Medoids clustering for proximity matrix.

    Args:
        X (np.ndarray): The data array.
        k (int): The amount of clusters for the KMedoids clustering algorithm.
        measure (int, string): The type of dissimilarity to use as metric (see 'measures' module).
        tmax (int): The amount of iterations

    Returns:
        The partition found by K-Medoids

    References:
        * https://github.com/letiantian/kmedoids
        * https://en.wikipedia.org/wiki/K-medoids

    """

    # validating the X data
    if X.ndim != 2 or X.shape[0] < 1 or X.shape[1] < 1:
        raise ValueError('Data must be a valid 2D matrix.')

    # validating the amount of clusters
    if k <= 0:
        raise ValueError('The amount of clusters must be positive.')

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

    # determine dimensions of distance matrix D
    m, n = D.shape

    if k > n:
        raise Exception('too many medoids')

    # randomly initialize an array of k medoid indices
    M = np.arange(n)
    np.random.shuffle(M)
    M = np.sort(M[:k])

    # create a copy of the array of medoid indices
    Mnew = np.copy(M)

    # initialize a dictionary to represent clusters
    C = {}
    for t in range(tmax):
        # determine clusters, i. e. arrays of data indices
        J = np.argmin(D[:, M], axis=1)
        for kappa in range(k):
            C[kappa] = np.where(J == kappa)[0]

        # update cluster medoids
        for kappa in range(k):
            J = np.mean(D[np.ix_(C[kappa], C[kappa])], axis=1)
            j = np.argmin(J)
            Mnew[kappa] = C[kappa][j]

        np.sort(Mnew)
        # check for convergence
        if np.array_equal(M, Mnew):
            break

        M = np.copy(Mnew)

    else:
        # final update of cluster memberships
        J = np.argmin(D[:, M], axis=1)
        for kappa in range(k):
            C[kappa] = np.where(J == kappa)[0]

    # setting samples labels
    labels = np.zeros((n,), int)
    for kappa in C:
        labels[C[kappa]] = kappa

    # return results
    return M, C, labels
