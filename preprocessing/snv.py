#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, February 2017

"""SNV normalization method (spectral pre-processing).

This module aims at giving a simple implementation of `SNV normalization` 
for spectral pre-processing.

For more information on this concept, please visit 
`Eigenvector documentation on SNV entry`_ or 
`This blog post on SNV`_.

Note:
    * Normalization method for spectral data. SNV method description was briefly taken from **Quimiometrix** help.

.. _Eigenvector documentation on SNV entry:
    http://wiki.eigenvector.com/index.php?title=Advanced_Preprocessing:_Sample_Normalization
   
.. _This blog post on SNV:
    http://nir-quimiometria.blogspot.com/2012/02/standard-normal-variate-snv.html

"""

import numpy as np

# ---------------------------------------------------------------


def snv_norm(X):
    """SNV normalization for spectral data.

    Args:
        X (np.ndarray): The data array.

    Returns:
        The X data normalized by SNV.

    Notes:
        * SNV is a pre-processing method used quite often in Near Infrared (NIR) data to remove the scatter.
        * SNV is applied to every spectrum individually.

    """

    # validating 'data'
    if not isinstance(X, np.ndarray):
        raise ValueError('Verify data.')

    # applying normalization for each row
    x_snv = np.apply_along_axis(lambda r: (r - r.mean()) / (r.std() + 1e-5), axis=1, arr=X)

    # returning data normalized via SNV
    return x_snv
