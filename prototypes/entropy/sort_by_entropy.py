#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, May 2017

import sys

import numpy as np

from .find_pivot import find_pivot

# ---------------------------------------------------------------


def sort_by_entropy(dm, flag):
    """Orders a gallery of templates

    Args:
        dm (ndarray): The similarity matrix of the gallery.
        flag (int): 0 if normalization should be performed.


    Returns:
        The elements of the gallery ordered by entropy value

    Examples:
        >>> dm = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
        >>> sort_by_entropy(dm, 0)
        ([0, 1, 2], [-0.040987776989995339, 0.93086535907179324, 0.0])
        >>> dm = np.array([[1.0, 0.8, 0.7], [0.8, 1.0, 0.7], [0.7, 0.8, 1.0]])
        >>> sort_by_entropy(dm, 0)
        ([2, 0, 1], [0.15358447915447049, 0.83930340718725271, 0.0])
    """

    # validating dm data
    rows, cols = dm.shape
    if rows != cols:
        raise ValueError("Matrix must be a squared matrix.")

    # making a copy
    dm_norm = dm.copy()

    # performing normalization when flag = 0
    if flag == 0:
        # computing the sum of the meaningful comparisons
        somma = np.sum(np.triu(dm_norm))

        # normalizing by the sum
        dm_norm = np.triu(dm_norm) / somma

    # matrix used in the iterative process
    dm_tmp = dm_norm.copy()

    piv_cnt = 0
    PIVOTS = []
    MIN_ENT = []
    min_ent_df = 0.0
    while min_ent_df < sys.float_info.max:
        # finding the pivot for the current gallery
        pivot, min_ent_df = find_pivot(dm_tmp)

        # if no pivot could be found
        if pivot == -1:
            break

        # a pivot was found
        else:
            piv_cnt += 1
            PIVOTS.append(pivot)
            MIN_ENT.append(min_ent_df)

            # excluding pivot from gallery
            dm_tmp[:, pivot] = 0.0
            dm_tmp[pivot, :] = 0.0

    return PIVOTS, MIN_ENT
