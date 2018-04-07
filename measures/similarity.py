#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, August 2016

"""
Similarity measures utilities for data representation
"""

import measures


def to_similarity(d):
    """
    Builds a similarity measure from a dissimilarity.

    Args:
        d (int, callable): The dissimilarity to build the similarity from.

    Returns:
        The built similarity measure.

    """

    # validating the dissimilarity type
    if d not in measures.measure_to_function:
        raise ValueError('Unknown dissimilarity measure type.')

    # special case for correlation dissimilarity
    if d == measures.CORRELATION:
        return measures.prob_correlation

    # special case for pearson dissimilarity
    if d == measures.PEARSON:
        return measures.prob_pearson

    # special case for spearman dissimilarity
    if d == measures.SPEARMAN:
        return measures.prob_spearman

    # ---------------

    if callable(d):
        d_func = d

    elif d in measures.measures_list:
        d_func = measures.measure_to_function[d]

    else:
        raise ValueError('Unknown dissimilarity measure.')

    # returning a similarity function build on top of a dissimilarity function
    return lambda x, y: 1 / (1 + d_func(x, y))
