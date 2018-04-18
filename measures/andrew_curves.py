#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, May 2017

"""
Andrew curves utilities for data representation and visualization.
"""

from math import ceil, sqrt, pi
import numpy as np
import measures

# -------------------------------------------------


def dis_andrews_curves(x, y, measure, m=100):
    """Computes Andrew's Curves for the given data

    Args:
        x (list): The first vector.
        y (list): The second vector.
        measure (int): The type of dissimilarity to use as metric (see 'measures' module).
        m (int): The range of values for the angles.

    Returns:
        The dissimilarity using the given measure of Andrew's Curves representations of data

    Notes:
        * Uses the Andrew's Curves representation of data for comparison

    """

    # getting the length of the vectors
    x_length = len(x)
    y_length = len(y)

    # validating parameters
    if x_length != y_length:
        raise Exception('Vectors with different sizes')

    # the specified metric must be one of the implemented measures
    if measure not in measures.measures_list:
        raise ValueError('Unknown dissimilarity measure.')

    # getting the metric function
    d = measures.measure_to_function[measure]

    # TODO: Here it is assumed that x and y are lists. Analyze the possibility for them to be tuples or numpy arrays

    # converting x and y to numpy arrays
    x_arr = np.array(x, np.float32)
    y_arr = np.array(y, np.float32)

    # building data matrix
    M = np.array([x_arr, y_arr])

    # computing andrew curves
    andrews = andrews_curves(M, m)

    # returning the dissimilarity m between both curves
    return d(andrews[0, :], andrews[0, :])


def andrews_curves(M, m=100):
    """Computes Andrew's Curves for the given data

    Args:
        M (np.ndarray): The data matrix (rows are samples).
        m (int): The range of values for the angles.

    Returns:
        The data `encoded` as Andrew's Curves

    Notes:
        Let :math:`x = (x_1, x_2, \cdots, x_n)` be a data vector
        
        Let :math:`t = (t1, t2, t3, \cdots, tm)` be an angular resolution
        
        Let
        
        .. math::
        
          A= \\left( 
                \\begin{array}{cccccc}
                    \\frac{1}{\sqrt{2}} & sin(t_1) & cos(t_1) & sin(2t_1) & cos(2t_1) & \cdots \\\\
                    \\frac{1}{\sqrt{2}} & sin(t_2) & cos(t_2) & sin(2t_2) & cos(2t_2) & \cdots \\\\
                    \\vdots             & \\vdots  & \\vdots  & \\vdots   & \\vdots   & \\vdots \\\\
                    \\frac{1}{\sqrt{2}} & sin(t_m) & cos(t_m) & sin(2t_m) & cos(2t_m) & \cdots
              \\end{array} 
              \\right),
        
        be a matrix where rows are associated to vector features and 
        columns with the angular resolution.
        
        The Andrew curve for vector x can be computed as:
            :math:`Ax`

    References:
        * http://glowingpython.blogspot.com/2014/10/andrews-curves.html
        * https://gist.github.com/ryuzakyl/12c221ff0e54d8b1ac171c69ea552c0a

    Examples:
        >>> M = np.array(range(1, 51)).reshape((5, 10))
        >>> curves = andrews_curves(M, m=5)
        >>> np.allclose([curves[0, 0], curves[0, 2], curves[0, 4]], [4.70710678, 24.70710678, 4.70710678])
        True
        >>> np.allclose([curves[4, 0], curves[4, 2], curves[4, 4]], [32.99137803, 212.99137803, 32.99137803])
        True

    """

    # validating samples data
    if not isinstance(M, np.ndarray):
        raise ValueError('Unsupported format for samples.')

    # validating data dimensions
    if not 1 <= len(M.shape) <= 2:
        raise ValueError("Only data vectors (1D) and collections of data vectors (2D) arrays supported")

    # getting data vectors
    X = np.reshape(M, (1, -1)) if len(M.shape) == 1 else M.copy()

    # getting the rows and the amount
    rows, n = X.shape

    # andrew curve dimension (a.k.a, amount theta angles)
    t = np.linspace(-pi, pi, m)

    # matrix Amxn:
    # m: range of values for angle 'theta'
    # n: amount of components for the Fourier function
    A = np.empty((m, n))

    # setting first column of A
    A[:, 0] = [1.0 / sqrt(2.0)] * m

    # filling columns of A
    for i in range(1, n):
        # computing the scaling coefficient for angle 'theta'
        c = ceil(i / 2)

        # computing i-th column of matrix A
        col = np.sin(c * t) if i % 2 == 1 else np.cos(c * t)

        # setting column in matrix A
        A[:, i] = col[:]

    # computing the values of Andrew curves for data M
    andrew_curves = np.dot(A, X.T).T

    # returning the Andrew's Curves (raveling if needed)
    return np.ravel(andrew_curves) if andrew_curves.shape[0] == 1 else andrew_curves
