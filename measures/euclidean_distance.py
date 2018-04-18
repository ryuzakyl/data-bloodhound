#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, August 2016

"""Module containing the utilities to compute Euclidean distance."""

import numpy as np


def euclidean(x, y):
    """Euclidean distance among two vectors.

    Args:
        x (list): The first vector.
        y (list): The second vector.

    Returns:
        float: The euclidean distance between vectors x and y.

    """

    # converting python lists to numpy arrays
    x_arr = np.array(x)
    y_arr = np.array(y)

    # computing euclidean distance
    return np.linalg.norm(x_arr - y_arr)
