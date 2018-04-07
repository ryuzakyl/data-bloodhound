#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, May 2017

import sys

import numpy as np

from .calc_ent import calc_ent

# ---------------------------------------------------------------


def find_pivot(dm_norm):
    """Finds a pivot in the gallery

    Args:
        dm_norm (ndarray): The similarity matrix of the gallery.

    Returns:
        The element with minimum entropy value as pivot.

    Examples:
        >>> dm = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> find_pivot(dm)
        (2, -21.546487678572873)
        >>> dm = np.array([[1.0, 0.8, 0.7], [0.8, 1.0, 0.7], [0.7, 0.8, 1.0]])
        >>> find_pivot(dm)
        (1, 0.22442809669354452)

    """

    # validating dm data
    rows, cols = dm_norm.shape
    if rows != cols:
        raise ValueError("Matrix must be a squared matrix.")

    # computing the entropy of the whole gallery
    ent_total = calc_ent(dm_norm)

    pivot = -1
    min_ent = sys.float_info.max
    for i in range(rows):
        # samples with zero sum are not fit for entropy computation
        if sum(dm_norm[i, :]) > 0:
            dm_tmp = dm_norm.copy()
            dm_tmp[i, :] = 0
            dm_tmp[:, i] = 0
            ent_val = ent_total - calc_ent(dm_tmp)
        else:
            ent_val = sys.float_info.max

        # updating the minimum entropy value found so far
        if ent_val < min_ent:
            min_ent = ent_val
            pivot = i

    # returning the 'pivot' index and entropy value
    return pivot, min_ent
