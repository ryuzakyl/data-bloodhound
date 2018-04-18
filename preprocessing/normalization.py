#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, March 2017

import numpy as np

from sklearn import preprocessing as skl_prep

# ---------------------------------------------------------------


def centering(X):
    """Mean subtraction normalization for spectral data.

    Args:
        X (np.ndarray): The data array.

    Returns:
        The X data normalized by mean subtraction.

    Notes:
        * The mean vector is subtracted from each vector in X.
        * The geometric interpretation is moving the cloud of points to the coordinate space origin.

    Examples:
        >>> import numpy as np
        >>> X = np.arange(1.0, 26.0).reshape((5, 5))
        >>> X_scaled = centering(X)
        >>> np.allclose(X - X.mean(axis=0), X_scaled)
        True
        >>> X_scaled.mean(axis=0)
        array([ 0.,  0.,  0.,  0.,  0.])

    """

    # validating 'data'
    if not isinstance(X, np.ndarray):
        raise ValueError('Verify data.')

    # returning the data with the mean subtracted
    return skl_prep.scale(X, with_mean=True, with_std=False)


def scaling(X, alpha):
    """Scaling normalization for spectral data.

    Args:
        X (np.ndarray): The data array.
        alpha (double): The scaling factor.

    Returns:
        The X data normalized by scaling.

    """

    # validating 'data'
    if not isinstance(X, np.ndarray):
        raise ValueError('Verify data.')

    # returning the data scaled by 'alpha' factor
    return X * alpha


def auto_scaling(X):
    """Mean subtraction normalization for spectral data.

    Args:
        X (np.ndarray): The data array.

    Returns:
        The X data normalized by auto-scaling.

    Examples:
        >>> import numpy as np
        >>> X = np.arange(1.0, 26.0).reshape((5, 5))
        >>> X_scaled = auto_scaling(X)
        >>> X_scaled.mean(axis=0)
        array([ 0.,  0.,  0.,  0.,  0.])
        >>> X_scaled.std(axis=0)
        array([ 1.,  1.,  1.,  1.,  1.])
    """

    # validating 'data'
    if not isinstance(X, np.ndarray):
        raise ValueError('Verify data.')

    # returning the data auto-scaled
    return skl_prep.scale(X, with_mean=True, with_std=True)
