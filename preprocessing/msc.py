#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, March 2017

from math import sqrt

import numpy as np

from utils import preprocessing as prep_utils
from preprocessing.normalization import centering

# ---------------------------------------------------------------


def mscorr_single_linreg(x, ref):
    """MSC base line correction for spectral data.

    Args:
        x (np.ndarray): The spectrum to correct.
        ref (np.ndarray): The reference spectrum.

    Returns:
        The spectrum corrected via MSC.

    Notes:
        * Both spectra were centered for better visual results.

    References:
        * http://wiki.eigenvector.com/index.php?title=Mscorr.
        * https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.lstsq.html
        * http://wiki.eigenvector.com/index.php?title=Advanced_Preprocessing:_Sample_Normalization

    """

    # centering `x` and `ref` (v - mean(v))
    x_c = centering(x)
    ref_c = centering(ref)

    # building matrix A
    A = np.vstack([x_c, np.ones(len(x_c))]).T

    # solving the linear regression problem using least squares
    beta, alpha = np.linalg.lstsq(A, ref_c)[0]

    # correcting xc by multiplicative factor 'beta', and 'alpha'
    x_msc = (x_c - alpha) / beta

    # returning the corrected spectrum
    return x_msc


def mscorr_linreg(X, ref):
    # 'ref' spectrum has to be determined
    if isinstance(ref, str):
        y = prep_utils.select_ref(ref, X)

    # 'ref' spectrum is provided, either as a 'list' or a 'np.ndarray'
    elif isinstance(ref, np.ndarray) or isinstance(ref, list):
        # converting 'ref' specrtum to ndarray
        y = ref.copy() if isinstance(ref, np.ndarray) else np.array(ref)

        # 'ref' spectrum must have the same size of data
        if y.shape[0] != X.shape[1]:
            raise ValueError('Reference spectrum must have the same dimensions.')

    # invalid 'ref' spectrum provided
    else:
        raise ValueError('Invalid reference spectrum.')

    # msc correction of each row of X via linear regression
    return np.apply_along_axis(
        lambda v: mscorr_single_linreg(v, y),
        arr=X, axis=1)


def mscorr(X, ref='mean'):
    """MSC base line correction for spectral data.

    Args:
        X (np.ndarray): The data set to correct.
        ref (list, np.ndarray): The reference spectrum.

    Returns:
        The data set corrected via MSC.

    Notes:
        * Implementation partially taken from: By Cleiton A. Nunes (UFLA, MG, Brazil).

    References:
        * http://wiki.eigenvector.com/index.php?title=Advanced_Preprocessing:_Sample_Normalization

    """

    # 'ref' spectrum has to be determined
    if isinstance(ref, str):
        y = prep_utils.select_ref(ref, X)

    # 'ref' spectrum is provided, either as a 'list' or a 'np.ndarray'
    elif isinstance(ref, np.ndarray) or isinstance(ref, list):
        # converting 'ref' specrtum to ndarray
        y = ref.copy() if isinstance(ref, np.ndarray) else np.array(ref)

        # 'ref' spectrum must have the same size of data
        if y.shape[0] != X.shape[1]:
            raise ValueError('Reference spectrum must have the same dimensions.')

    # invalid 'ref' spectrum provided
    else:
        raise ValueError('Invalid reference spectrum.')

    # getting column count of X data
    x_cols = X.shape[1]

    # 'x_cols' x 2 (1s in first column and 'ref' spectrum in second column)
    R1 = np.vstack([np.ones(x_cols), y]).T

    # z: r * r' ('ref' vector multiplied by its transpose-1 column of 1s was added-)
    # @: infix operator for matrix multiplication
    z = R1.T @ R1

    # applying SVD decomposition
    u, s, v = np.linalg.svd(z)

    # replacing singular values smaller that 'thres' with threshold value
    thres = s[0] / sqrt(10 ** 12)
    s[s < thres] = thres

    # reconstructing 'z' matrix
    z = u @ np.diag(s) @ v.T

    # computing inverse of matrix 'z'
    z_inv = np.linalg.inv(z)

    # computing 'alpha' and 'beta' coefficients
    ab = z_inv @ R1.T @ X.T

    # correcting by substracting 'alpha' values
    alphas = ab[0, :]
    X_msc = X - np.tile(alphas, (x_cols, 1)).T

    # correcting by normalizing using 'beta' values
    betas = ab[1, :]
    X_msc = X_msc / np.tile(betas, (x_cols, 1)).T

    # returning the corrected samples
    return X_msc
