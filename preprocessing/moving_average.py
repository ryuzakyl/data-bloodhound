#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, March 2017

"""Moving Average (Running Average) smoothing method (spectral pre-processing).

This module aims at giving a simple implementation of `Moving Average
smoothing` for spectral pre-processing.

For more information on this concept, please follow up in the following resources:
    * `Scipy Cookbook on Signal Processing`_.
    * `Moving Average Wikipedia entry`_.

Note:
    * Smoothing method for spectral data.
    * Implementation partially taken from: `http://scipy-cookbook.readthedocs.io/items/SignalSmooth.html`.

Todo:
    * Module TODOs here!!!
    * You have to also use ``sphinx.ext.todo`` extension

.. _Scipy Cookbook on Signal Processing:
    http://scipy-cookbook.readthedocs.io/items/SignalSmooth.html
.. _Moving Average Wikipedia entry:
    https://en.wikipedia.org/wiki/Moving_average

"""

import numpy as np

# ---------------------------------------------------------------


def mov_avg_1d(x, window_len=11):
    """Moving Average smoothing for spectral data.

    Args:
        x (np.ndarray): The 1D data array.
        window_len (int): The convolution window size.

    Notes:
        * Based on the convolution of a scaled window with the 1D array
        * 1D array prepared by introducing reflected copies (with the window size) in both ends so that transient parts are minimized in the beginning and end part of the output array.

    Returns:
        The x 1D array smoothed by Moving Average filter.

    Examples:
        >>> import numpy as np
        >>> t = np.linspace(-2, 2, num=5)
        >>> x = np.sin(t)
        >>> mov_avg_1d(x, window_len=3)
        array([-0.8640798 , -0.58358947,  0.        ,  0.58358947,  0.88668861])

    """

    # validating that array is a 1D array
    if x.ndim != 1:
        raise ValueError("Only 1D arrays are valid.")

    # validating array and window sizes
    if x.size < window_len:
        raise ValueError("Input array must be bigger than window size.")

    # returning the same data if window is too small
    if window_len < 3:
        return x

    # For more information see :
    # '/site-packages/numpy/lib/index_tricks.py'
    s = np.r_[x[window_len - 1:0:-1], x, x[-1:-window_len:-1]]

    # defining a window to convolve the signal with
    w = np.ones(window_len, 'd')

    # convolving the signal
    y = np.convolve(w / w.sum(), s, mode='valid')

    # remark: added by me (correcting size of convolved 1D array)
    offset = (y.shape[0] - x.shape[0]) // 2
    y = y[offset:-offset]   # trimming extra data from 'start' and 'end'

    # returning the convolved signal
    return y


def mov_avg_2d(X, window_len=11, axis=1):
    """Moving Average smoothing for spectral data.

    Args:
        X (np.ndarray): The 2D data array.
        window_len (int): The convolution window size.
        axis (int): The axis to perform moving average on.

    Notes:
        * Applies `mov_avg_1d` over the selected axis.

    Returns:
        The X data smoothed by Moving Average filter.

    """

    # validating that X is a 2D array
    if X.ndim != 2:
        raise ValueError("Only 2D arrays are valid.")

    # applying `mov_avg_1d` over the selected axis
    return np.apply_along_axis(lambda x: mov_avg_1d(x, window_len), axis=axis, arr=X)
