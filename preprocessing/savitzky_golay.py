#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, March 2017

"""Savitsky-Golay smoothing method (spectral pre-processing).

This module aims at giving a simple implementation of `Savitsky-Golay smoothing` for spectral preprocessing.

For more information on this concept, please follow up in the following resources:
    * `Eigenvector link on advanced pre-processing`_.
    * `Savitzky–Golay filter Wikipedia entry`_.
    * `Savitzky–Golay function documentation in Eigenvector`_.
    * `Paper on the fusion of Savitzky–Golay and MSC`_.

Note:
    * Smoothing method for spectral data.

Todo:
    * Module TODOs here!!!
    * You have to also use ``sphinx.ext.todo`` extension

.. _Eigenvector link on advanced pre-processing:
    http://wiki.eigenvector.com/index.php?title=Advanced_Preprocessing:_Noise,_Offset,_and_Baseline_Filtering
.. _Savitzky–Golay filter Wikipedia entry:
    https://es.wikipedia.org/wiki/Filtro_de_Savitzky%E2%80%93Golay
.. _Savitzky–Golay function documentation in Eigenvector:
    http://wiki.eigenvector.com/index.php?title=Savgol
.. _Paper on the fusion of Savitzky–Golay and MSC:
    https://www.hindawi.com/journals/isrn/2013/642190/

"""

import numpy as np
from scipy.signal import savgol_filter

# ---------------------------------------------------------------


def savitsky_golay_smoothing(X, width, order, deriv=0):
    """Savitzky–Golay smoothing for spectral data.

    Args:
        X (np.ndarray): The data array.
        width (int): The width of the window.
        order (int): The polynomial order.
        deriv (int): The derivative order.

    Returns:
        The X data smoothed by Savitzky–Golay filter.

    """

    sg_mat = np.empty(X.shape)

    for i, x in enumerate(X):
        sg_mat[i, :] = savgol_filter(x, width, order, deriv=deriv)[:]

    return sg_mat
