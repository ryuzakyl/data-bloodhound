#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, August 2016

import numpy as np


def dkolmogorov(x, y):
    """Computes Kolmogorov-Smirnov dissimilarity.

    Args:
        x (list): The first vector.
        y (list): The second vector.

    Returns:
        float: The kolmogorov-smirnov distance value between vectors x and y.

    """

    # getting the length of the vectors
    x_length = len(x)
    y_length = len(y)

    # validating parameters
    if x_length != y_length:
        raise Exception('Vectors with different sizes')

    # TODO: Here it is assumed that x and y are lists. Analyze the possibility for them to be tuples or numpy arrays

    # converting x and y to numpy arrays
    x_arr = np.array(x, np.float32)
    y_arr = np.array(y, np.float32)

    # converting x and y into probability distributions
    x_arr = x_arr if x_arr.min() >= 0 else x_arr + abs(x_arr.min())
    y_arr = y_arr if y_arr.min() >= 0 else y_arr + abs(y_arr.min())

    # computing cumsum of both vectors
    x_cum = np.cumsum(x_arr)
    y_cum = np.cumsum(y_arr)

    # normalizing to unit area
    x_norm = x_arr / x_cum[-1]
    y_norm = y_arr / y_cum[-1]

    return max(abs(x_norm - y_norm))
