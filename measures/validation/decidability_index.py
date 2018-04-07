#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, February 2017

from math import sqrt

import numpy as np

from measures.validation.utils import intra_inter_class_distances, intra_inter_class_dissimilarities

# ---------------------------------------------------------------


def decidability_index(d1, d2):
    """Computes the decidability index for two distributions.

    Note:
        Definition of such index can be found here:
        `Daugman, J. (2004). How iris recognition works. IEEE
        Transactions on circuits and systems for video technology,
        14(1), 21-30`

    Args:
        d1 (list): The first distribution.
        d2 (list): The second distribution.

    Returns:
        The decidability index.

    Examples:
        >>> decidability_index([0.2, 0.3], [0.4, 0.5, 0.6])
        3.6927447293799833

    """

    # validating distributions are lists
    if not isinstance(d1, list) or not isinstance(d2, list):
        raise ValueError('Distributions must be lists')

    # validating distributions
    if not len(d1) or not len(d2):
        raise ValueError('')

    # building arrays from distribution lists
    arr_d1 = np.array(d1)
    arr_d2 = np.array(d2)

    # computing mean and std for d1 distribution
    miu1 = arr_d1.mean()
    std1 = arr_d1.std()

    # computing mean and std for d2 distribution
    miu2 = arr_d2.mean()
    std2 = arr_d2.std()

    # returning the decidability index
    return abs(miu1 - miu2) / sqrt((std1**2 + std2**2) / 2)


def decidability_index_in_euc_space(X, labels):
    # validating 'data' and 'labels'
    if not isinstance(X, np.ndarray) or not (isinstance(labels, np.ndarray) or isinstance(labels, list)):
        raise ValueError('Verify data and labels.')

    # getting the values of labels as ndarray
    y = labels.copy() if isinstance(labels, np.ndarray) else np.array(labels)

    # validating consistency between samples and labels
    if X.shape[0] != y.shape[0]:
        raise ValueError('Amount of samples must be the same as the amount of labels.')

    # computing intra and inter class distances for euclidean space
    d1, d2 = intra_inter_class_distances(X, y, metric='euclidean')

    # returning the decidability index
    return decidability_index(d1, d2)


def decidability_index_in_dis_space(X, labels, measure):
    # validating 'data' and 'labels'
    if not isinstance(X, np.ndarray) or not (isinstance(labels, np.ndarray) or isinstance(labels, list)):
        raise ValueError('Verify data and labels.')

    # getting the values of labels as ndarray
    y = labels.copy() if isinstance(labels, np.ndarray) else np.array(labels)

    # validating consistency between samples and labels
    if X.shape[0] != y.shape[0]:
        raise ValueError('Amount of samples must be the same as the amount of labels.')

    # computing intra and inter class dissimilarities
    d1, d2 = intra_inter_class_dissimilarities(X, labels, measure)

    # returning the decidability index
    return decidability_index(d1, d2)
