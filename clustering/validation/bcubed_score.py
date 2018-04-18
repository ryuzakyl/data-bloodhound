#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, March 2017

"""BCubed metrics (clustering validation).

This module aims at giving a simple and fast implementation of `BCubed family metrics` for clustering validation.

Note:
    * Code taken from `BCubed Python implementation in Github`_. https://github.com/hhromic/python-bcubed#start-of-content
    * Although BCubed is defined in Bagga and Baldwin (1998) as an  algorithm, it can also be described in terms of a function.
    * BCubed precision of an item is the proportion of items in its cluster which have the item’s category (including itself).
    * The overall BCubed precision is the averaged precision of all items in the distribution.
    * Since the average is calculated over items, it is not necessary to apply any weighting according to the size of clusters or categories.
    * The BCubed recall is analogous, replacing ``cluster`` with ``category``.

References:
    * Amigó, E., Gonzalo, J., Artiles, J., & Verdejo, F. (2009). A comparison of extrinsic clustering evaluation metrics based on formal constraints. Information retrieval, 12(4), 461-486.

Todo:
    * Module TODOs here!!!
    * You have to also use ``sphinx.ext.todo`` extension

.. _BCubed Python implementation in Github:
   https://github.com/hhromic/python-bcubed#start-of-content

"""

import numpy as np

# ----------------------------------------


def mult_precision(el1, el2, cdict, ldict):
    """Computes the multiplicity precision for two elements."""
    return min(len(cdict[el1] & cdict[el2]), len(ldict[el1] & ldict[el2])) \
        / float(len(cdict[el1] & cdict[el2]))


def mult_recall(el1, el2, cdict, ldict):
    """Computes the multiplicity recall for two elements."""
    return min(len(cdict[el1] & cdict[el2]), len(ldict[el1] & ldict[el2])) \
        / float(len(ldict[el1] & ldict[el2]))


def precision(cdict, ldict):
    """Computes overall extended BCubed precision for the C and L dicts."""
    return np.mean([np.mean([mult_precision(el1, el2, cdict, ldict) \
        for el2 in cdict if cdict[el1] & cdict[el2]]) for el1 in cdict])


def recall(cdict, ldict):
    """Computes overall extended BCubed recall for the C and L dicts."""
    return np.mean([np.mean([mult_recall(el1, el2, cdict, ldict) \
        for el2 in cdict if ldict[el1] & ldict[el2]]) for el1 in cdict])


def __fscore(p_val, r_val, beta=1.0):
    """Computes the F_{beta}-score of given precision and recall values."""
    return (1.0 + beta**2) * (p_val * r_val / (beta**2 * p_val + r_val))


def f_measure(labels, true_labels):
    """F-measure external index for clustering validation.

    Args:
        labels (list, np.ndarray): The clustering labels.
        true_labels (list, np.ndarray): The ground truth labels.

    Returns:
        The F-measure score for the given clustering and provided ground-truth.

    Notes:
        * The higher the value of F-measure, the better the clustering.

    Examples:
        >>> labels = [0, 1, 0]
        >>> true_labels = [1, 1, 0]
        >>> f_measure(labels, true_labels)
        0.66666666666666663
        >>> labels = [0, 1, 0, 0, 1]
        >>> true_labels = [1, 1, 0, 0, 0]
        >>> f_measure(labels, true_labels)
        0.53333333333333333
    """

    # getting the values of labels as ndarrays
    y = labels.copy() if isinstance(labels, np.ndarray) else np.array(labels)
    y_true = true_labels.copy() if isinstance(true_labels, np.ndarray) else np.array(true_labels)

    # validating consistency between labels and ground-truth
    if y.shape[0] != y_true.shape[0]:
        raise ValueError('Amount of labels and ground-truth labels must be the same.')

    # building 'ldict' (ground-truth data -also called gold-standard data-)
    ldict = {str(idx): {y_true[idx]} for idx in range(y_true.shape[0])}

    # building 'cdict' (the clustering output)
    cdict = {str(idx): {y[idx]} for idx in range(y.shape[0])}

    # computing 'precision' metric score
    p_score = precision(cdict, ldict)

    # computing 'recall' metric score
    r_score = recall(cdict, ldict)

    # computing F-Score for a default beta=1.0
    f_measure_score = __fscore(p_score, r_score)

    # returning the computed F-Score value
    return f_measure_score
