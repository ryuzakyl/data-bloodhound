#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, August 2016

import numpy as np


def manhattan(x, y):
    """Manhattan distance among two vectors.

    Args:
        x (list): The first vector.
        y (list): The second vector.

    Returns:
        float: The manhattan distance between vectors x and y.

    """

    # converting python lists to numpy arrays
    x_arr = np.array(x)
    y_arr = np.array(y)

    # computing manhattan distance
    return np.linalg.norm(x_arr - y_arr)
