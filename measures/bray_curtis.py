#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, February 2017

from scipy.spatial.distance import braycurtis as scy_bray_curtis


def dis_bray_curtis(x, y):
    """Computes the Bray Curtis dissimilarity value.

    Args:
        x (list): The first vector.
        y (list): The second vector.

    Returns:
        float: The Bray-Curtis dissimilarity between vectors x and y.

    References:
        . Cha, S. H. (2007). Comprehensive survey on distance/similarity
        measures between probability density functions. City, 1(2), 1.

    Note:
        . Also known as Sørensen distance.
        . Widely used in ecology.
        . Used for comparing Probability Density Functions (FDFs)
        . Belongs to the L1 family.
        . (IMPORTANT) It seems that no matter the order of the vectors, the dissimilarity value is the same.

    Examples:
        >>> dis_bray_curtis([1.0, 2.0, 3.0], [4.0, 5.0, 6.0])
        0.42857142857142855
        >>> dis_bray_curtis([1.0, 2.0, 3.0], [6.0, 5.0, 4.0])
        0.42857142857142855
        >>> dis_bray_curtis([1.0, 2.0, 3.0, 20.0, 150.0, 3.0], [6.0, 5.0, 4.0, 3.0, 2.0, 1.0])
        0.88
        >>> dis_bray_curtis([1.0, 2.0, 3.0, 20.0, 150.0, 3.0], [1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        0.81999999999999995

    """

    # returning the bray curtis distance
    return scy_bray_curtis(x, y)
