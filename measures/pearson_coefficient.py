#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, August 2016

from math import sqrt
import numpy as np
from scipy.stats.stats import pearsonr


def probabilistic_pearsonr(x, y):
    """Computes the pearson coefficient as a probability value.

    Args:
        x (list): The first vector.
        y (list): The second vector.

    Returns:
        float: The pearson probability value between vectors x and y.

    """

    # computing the correlation value
    value = pearsonr(x, y)[0]       # getting only the first value of the tuple

    # moving value to interval [0, 2]
    value += 1.0

    # stretching value to the interval [0, 1]
    return 0.5 * value


def dis_pearsonr(x, y):
    """Computes the pearson coefficient as a dissimilarity value.

    Args:
        x (list): The first vector.
        y (list): The second vector.

    Returns:
        float: The pearson dissimilarity value between vectors x and y.

    """

    # computing the correlation value
    value = pearsonr(x, y)[0]       # getting only the first value of the tuple

    # setting dissimilarity value to the interval [0, 2]
    return 1 - value


def dissimilarity_pcc(x, y):
    """Computes a dissimilarity value based on a Pearson Correlation Coefficient.

    Args:
        x (list): The first vector.
        y (list): The second vector.

    Returns:
        float: The pearson correlation coefficient-based dissimilarity value between vectors x and y.

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

    # computing vectors means and centered vectors
    x_mean = np.mean(x_arr)
    x_cent = x - x_mean
    y_mean = np.mean(y_arr)
    y_cent = y - y_mean

    num = np.dot(x_cent, y_cent)
    den = sqrt(np.dot(x_cent, x_cent) * np.dot(y_cent, y_cent))

    return 1 - num/den
