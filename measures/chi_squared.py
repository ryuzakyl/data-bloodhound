#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, February 2017

import numpy as np


def X2(x, y, eps=1e-10):
    """Computes the Chi Squared (X2) distance value.

    Args:
        x (list): The first vector.
        y (list): The second vector.
        eps (float): Tolerance parameter to avoid zero division

    Returns:
        float: The chi squared distance between vectors x and y.

    References:
        . J. Puzicha, T. Hofmann, J. Buhmann, Non-parametric similarity measures for unsupervised
        texture segmentation and image retrieval, in: IEEE Computer Society Conference on Computer
        Vision and Pattern Recognition, CVPR ’97, 1997, pp. 267–272.

    Note:
        . Distance commonly used for histograms.

    Examples:
        >>> X2([1.0, 2.0, 3.0], [4.0, 5.0, 6.0])
        4.0857142210006714
        >>> X2([1.0, 2.0, 3.0], [6.0, 5.0, 4.0])
        4.9999999552965164
        >>> X2([1.0, 2.0, 3.0, 20.0, 150.0, 3.0], [6.0, 5.0, 4.0, 3.0, 2.0, 1.0])
        162.67048735916615
        >>> X2([1.0, 2.0, 3.0, 20.0, 150.0, 3.0], [1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        147.31182384490967

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

    # computing the squared differences
    num = (x_arr - y_arr) ** 2

    # computing the sum of both arrays
    den = eps + x_arr + y_arr

    # computing fractions
    fracs = num / den

    # returning the sum of all the fractions
    return sum(fracs)
