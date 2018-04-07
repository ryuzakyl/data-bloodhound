#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, August 2016

from math import sqrt

from scipy.spatial.distance import correlation as scy_correlation


def correlation(x, y):
    """Computes the correlation coefficient.

    Args:
        x (list): The first vector.
        y (list): The second vector.

    Returns:
        float: The correlation coefficient between vectors x and y.

    """

    # getting the length of the vectors
    x_length = len(x)
    y_length = len(y)

    # validating parameters
    if x_length != y_length:
        raise Exception('Vectors with different sizes')

    # computing the means of both vectors
    mean_x = 0.0
    mean_y = 0.0
    for i in range(x_length):
        mean_x += x[i]
        mean_y += y[i]

    # dividing by the length of the vectors
    mean_x /= x_length
    mean_y /= y_length

    # computing the values k, f1 and f2
    k = 0.0
    f1 = 0.0
    f2 = 0.0
    for i in range(x_length):
        # computing the offsets
        offset_x = x[i] - mean_x
        offset_y = y[i] - mean_y

        # updating k, f1 and f2
        k += offset_x * offset_y
        f1 += offset_x * offset_x
        f2 += offset_y * offset_y

    # returning the computed correlation distance
    return k / (sqrt(f1) * sqrt(f2))


def probabilistic_correlation(x, y):
    """Computes the correlation coefficient as a probability value.

    Args:
        x (list): The first vector.
        y (list): The second vector.

    Returns:
        float: The correlation probability value between vectors x and y.

    """

    # computing the correlation value
    value = correlation(x, y)

    # moving value to interval [0, 2]
    value += 1.0

    # stretching value to the interval [0, 1]
    return 0.5 * value


def dis_correlation_manual(x, y):
    """Computes the correlation coefficient as a dissimilarity measure.

    Args:
        x (list): The first vector.
        y (list): The second vector.

    Returns:
        float: The dissimilarity value between vectors x and y.

    Examples:
        >>> dis_correlation_manual([1.0, 2.0, 3.0], [4.0, 5.0, 6.0])
        2.220446049250313e-16
        >>> dis_correlation_manual([1.0, 2.0, 3.0], [6.0, 5.0, 4.0])
        1.9999999999999998
        >>> dis_correlation_manual([1.0, 2.0, 3.0, 20.0, 150.0, 3.0], [6.0, 5.0, 4.0, 3.0, 2.0, 1.0])
        1.4245486433123256
        >>> dis_correlation_manual([1.0, 2.0, 3.0, 20.0, 150.0, 3.0], [1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        0.5754513566876744

    """

    # computing the correlation value
    value = correlation(x, y)

    # setting dissimilarity value to the interval [0, 2]
    return 1 - value


def dis_correlation_scipy(x, y):
        """Computes the correlation distance between `x` and `y`.

        Args:
            x (list): The first vector.
            y (list): The second vector.

        Returns:
            double: The correlation distance between vectors `x` and `y`.

        References:
            * https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.correlation.html

        Examples:
            >>> dis_correlation_scipy([1.0, 2.0, 3.0], [4.0, 5.0, 6.0])
            2.2204460492503131e-16
            >>> dis_correlation_scipy([1.0, 2.0, 3.0], [6.0, 5.0, 4.0])
            1.9999999999999998
            >>> dis_correlation_scipy([1.0, 2.0, 3.0, 20.0, 150.0, 3.0], [6.0, 5.0, 4.0, 3.0, 2.0, 1.0])
            1.4245486433123256
            >>> dis_correlation_scipy([1.0, 2.0, 3.0, 20.0, 150.0, 3.0], [1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
            0.57545135668767444

        """

        # returning the correlation distance
        return scy_correlation(x, y)
