#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, August 2016

import numpy as np
from scipy.spatial.distance import minkowski as scipy_minkowski


def minkowski(x, y, p=5):
    """Computes Minkowski distance.

    Args:
        x (list): The first vector.
        y (list): The second vector.
        p (int): Parameter p of Minkowski.

    Returns:
        float: The minkowski distance value between vectors x and y.

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

    # returning minkowski distance from scipy
    return scipy_minkowski(x_arr, y_arr, p)
