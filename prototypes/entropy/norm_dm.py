#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, May 2017

import numpy as np

# ---------------------------------------------------------------


def norm_dm(dm):
    """Normalizes a similarity/dissimilarity matrix

    Args:
        dm (ndarray): The similarity/dissimilarity matrix of the gallery.

    Returns:
        The normalized matrix and the total sum.

    Examples:
        >>> dm = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
        >>> dm_norm, somma = norm_dm(dm)
        >>> somma
        11.0
        >>> np.isclose([dm_norm[0, 1], dm_norm[0, 2], dm_norm[1, 2]], [0.18181818, 0.27272727, 0.54545455]).all()
        True
        >>> dm = np.array([[1.0, 0.8, 0.7], [0.8, 1.0, 0.7], [0.7, 0.8, 1.0]])
        >>> dm_norm, somma = norm_dm(dm)
        >>> somma
        2.2000000000000002
        >>> np.isclose([dm_norm[0, 1], dm_norm[0, 2], dm_norm[1, 2]], [0.36363636, 0.31818182, 0.31818182]).all()
        True
    """

    # validating dm data
    rows, cols = dm.shape
    if rows != cols:
        raise ValueError("Matrix must be a squared matrix.")

    # making a copy
    dm_norm = dm.copy()

    # with parameter k=1 we are excluding the diagonal
    somma = np.sum(np.triu(dm_norm, 1))

    # normalizing by the sum
    dm_norm = np.triu(dm_norm, 1) / somma

    return dm_norm, somma
