#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, May 2017

from math import log2

import numpy as np

# ---------------------------------------------------------------


def calc_ent(dm):
    """Computes the entropy of a gallery

    Args:
        dm (ndarray): The similarity matrix of the gallery.

    Returns:
        The entropy value.

    Examples:
        >>> dm = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> calc_ent(dm)
        -31.546487678572873
        >>> dm = np.array([[1.0, 0.8, 0.7], [0.8, 1.0, 0.7], [0.7, 0.8, 1.0]])
        >>> calc_ent(dm)
        0.58462931767437532

    """

    # validating the received matrix
    if not isinstance(dm, np.ndarray):
        raise ValueError('NumPy ndarray expected.')

    # making a copy of the data matrix
    dm_cpy = dm.copy()

    # computing the amount of positive (>0) values
    dm_pos_mask = (dm_cpy > 0.0).astype(int)
    n = np.sum(dm_pos_mask)

    # validating that the count of positive similarity values
    if n <= 1:
        return 0.0

    # log2 of matrix values (except zero values)
    dm_cpy[dm_cpy > 0] = np.log2(dm_cpy[dm_cpy > 0])

    # normalizing dm values by log2(n)
    log_dm = dm_cpy / log2(n)

    # multiplying each number by it's log2 value (excluding non-positive similarity values)
    t = dm_pos_mask * (-dm) * log_dm

    # returning the sum of all values
    return np.sum(t)
