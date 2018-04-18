#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, July 2017

import numpy as np

# ---------------------------------------------------------------


def select_ref(ref_type, X=None):
    if ref_type == 'mean':
        return np.nanmean(X, axis=0)

    elif ref_type == 'median':
        return np.nanmedian(X, axis=0)

    elif ref_type == 'bestcorr' and X is not None:
        # http://stackoverflow.com/questions/3425439/why-does-corrcoef-return-a-matrix
        norm_cov_mat = np.corrcoef(X)
        idx_max_corr = np.argmax(np.sum(norm_cov_mat, axis=1))
        return X[idx_max_corr, :]

    else:
        raise ValueError('Unsupported selection method for reference spectrum.')
