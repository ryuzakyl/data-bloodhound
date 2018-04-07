#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, August 2016

from math import acos
import numpy as np


def sam(x, y):
    """Computes the Spectral Angle Mapper (SAM) dissimilarity value.

    Args:
        x (list): The first vector.
        y (list): The second vector.

    Returns:
        float: The spectral angle mapper dissimilarity value between vectors x and y.

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

    # computing fractions values
    num = np.dot(x_arr, y_arr)
    den = np.sqrt(np.dot(x_arr, x_arr) * np.dot(y_arr, y_arr))

    # clipping value in domain
    coc = num / den
    coc = -1.0 if coc < -1.0 else 1.0 if coc > 1.0 else coc

    # returning acos (num / den)
    return acos(coc)
