#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, August 2016

from scipy.stats.stats import spearmanr


def probabilistic_spearmanr(x, y):
    """Computes the spearman coefficient as a probability value.

    Args:
        x (list): The first vector.
        y (list): The second vector.

    Returns:
        float: The spearman probability value between vectors x and y.

    """

    # computing the correlation value
    value = spearmanr(x, y)[0]       # getting only the first value of the tuple

    # moving value to interval [0, 2]
    value += 1.0

    # stretching value to the interval [0, 1]
    return 0.5 * value


def dis_spearmanr(x, y):
    """Computes the spearman coefficient as a dissimilarity value.

    Args:
        x (list): The first vector.
        y (list): The second vector.

    Returns:
        float: The spearman dissimilarity value between vectors x and y.

    """

    # computing the correlation value
    value = spearmanr(x, y)[0]       # getting only the first value of the tuple

    # setting dissimilarity value to the interval [0, 2]
    return 1 - value
